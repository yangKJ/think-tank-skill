"""Filesystem-based message bus for agent communication.

This module provides a Team API-free alternative for multi-agent coordination.
It uses atomic file writes for safe concurrent access and supports task
dispatch, result collection, shutdown signalling, and bus cleanup.

Usage:
    python -m think_tank.runtime.filesystem_bus --run-id test-001 --action create
    python -m think_tank.runtime.filesystem_bus --run-id test-001 --action send
"""

from __future__ import annotations

import json
import os
import tempfile
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
import shutil
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class BusMessage:
    """Standardised message envelope for filesystem bus communication."""

    message_id: str
    from_profile: str
    to_profile: str           # single profile name or "broadcast"
    msg_type: str             # task | result | shutdown_request | shutdown_approved | heartbeat | ack
    timestamp: str
    correlation_id: Optional[str]
    payload: dict = field(default_factory=dict)
    ttl_seconds: int = 300

    def to_dict(self) -> dict:
        d = {
            "message_id": self.message_id,
            "from": self.from_profile,
            "to": self.to_profile,
            "type": self.msg_type,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
            "payload": self.payload,
            "ttl_seconds": self.ttl_seconds,
        }
        return d


@dataclass
class BusConfig:
    """Configuration for a filesystem message bus instance."""

    root_dir: str
    profiles: list[str] = field(default_factory=list)
    run_id: str = ""
    timeout_graceful: int = 15
    timeout_force: int = 30

    @property
    def dispatch_dir(self) -> Path:
        return Path(self.root_dir) / "dispatch"

    @property
    def results_dir(self) -> Path:
        return Path(self.root_dir) / "results"

    @property
    def signals_dir(self) -> Path:
        return Path(self.root_dir) / "signals"

    @property
    def state_dir(self) -> Path:
        return Path(self.root_dir) / "state"


# ---------------------------------------------------------------------------
# Atomic file write
# ---------------------------------------------------------------------------


def atomic_write_json(filepath: str, data: dict) -> bool:
    """Write JSON data atomically (temp file + rename).

    Args:
        filepath: Target file path (must end in .json).
        data: Dictionary to serialise.

    Returns:
        True on success.
    """
    target = Path(filepath)
    target.parent.mkdir(parents=True, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(
        suffix=".tmp", prefix=target.stem + "-", dir=str(target.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)
        os.rename(tmp_path, str(target))
        return True
    except (OSError, TypeError, ValueError) as e:
        # Clean up temp on failure (OSError: I/O error; TypeError/ValueError: bad JSON)
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        return False


# ---------------------------------------------------------------------------
# Bus lifecycle
# ---------------------------------------------------------------------------


def create_bus(
    run_id: str,
    profiles: list[str],
    base_dir: str = ".think-tank/runs",
) -> BusConfig:
    """Create message bus directory structure.

    Args:
        run_id: Unique run identifier.
        profiles: List of participating profile names.
        base_dir: Parent directory for run storage.

    Returns:
        Configured BusConfig pointing to the new bus.
    """
    root = Path(base_dir) / run_id / "bus"
    root.mkdir(parents=True, exist_ok=True)

    for sub in ("dispatch", "results", "signals", "state"):
        (root / sub).mkdir(exist_ok=True)

    # Initial state
    state = {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "profiles": profiles,
        "phase": "active",
        "message_count": 0,
    }
    atomic_write_json(str(root / "state" / "state.json"), state)

    return BusConfig(
        root_dir=str(root),
        profiles=list(profiles),
        run_id=run_id,
    )


# ---------------------------------------------------------------------------
# Messages
# ---------------------------------------------------------------------------


def _make_message_id() -> str:
    return uuid.uuid4().hex[:12]


def _make_filename(msg: BusMessage) -> str:
    """Build a sortable filename: {timestamp}-{to}-{from}-{type}-{msg_id}.json

    Uses to_profile first so receivers can discover messages by their profile name.
    For tasks: subagent searches dispatch/*collector*.json
    For results: facilitator searches results/*facilitator*.json
    """
    ts = int(time.time() * 1000)
    return f"{ts}-{msg.to_profile}-{msg.from_profile}-{msg.msg_type}-{msg.message_id}.json"


def send_message(config: BusConfig, msg: BusMessage) -> str:
    """Atomically write a message to the bus.

    Determines target directory from message type:
        task → dispatch/
        result → results/
        shutdown_* / heartbeat / ack → signals/

    Returns the file path where the message was written.
    """
    if msg.msg_type == "task":
        target_dir = config.dispatch_dir
    elif msg.msg_type == "result":
        target_dir = config.results_dir
    else:
        target_dir = config.signals_dir

    filename = _make_filename(msg)
    filepath = target_dir / filename
    atomic_write_json(str(filepath), msg.to_dict())
    return str(filepath)


def receive_messages(
    config: BusConfig,
    profile: str,
    msg_type: Optional[str] = None,
) -> list[BusMessage]:
    """Read all messages addressed to a profile from the bus.

    Args:
        config: Bus configuration.
        profile: Recipient profile name. "broadcast" matches all.
        msg_type: Filter by message type, or None for all.

    Returns:
        List of BusMessage sorted by timestamp.
    """
    msg_types = [msg_type] if msg_type else None
    return _read_messages_from_config(config, profile, msg_types)


def wait_for_messages(
    config: BusConfig,
    profile: str,
    msg_type: str,
    expected_count: int = 1,
    timeout_seconds: int = 30,
    poll_interval: float = 1.0,
) -> list[BusMessage]:
    """Block until expected_count messages arrive, or timeout.

    Args:
        config: Bus configuration.
        profile: Recipient profile.
        msg_type: Expected message type.
        expected_count: Minimum number of messages to wait for.
        timeout_seconds: Maximum wait time.
        poll_interval: Seconds between polls.

    Returns:
        List of received BusMessage (may be fewer than expected on timeout).
    """
    deadline = time.time() + timeout_seconds
    collected: list[BusMessage] = []

    while time.time() < deadline:
        msgs = receive_messages(config, profile, msg_type)
        # Deduplicate by message_id
        existing_ids = {m.message_id for m in collected}
        new_msgs = [m for m in msgs if m.message_id not in existing_ids]
        collected.extend(new_msgs)

        if len(collected) >= expected_count:
            return collected

        time.sleep(poll_interval)

    return collected


def _read_messages_from_config(
    config: BusConfig,
    profile: str,
    msg_types: Optional[list[str]] = None,
) -> list[BusMessage]:
    """Internal: scan all bus subdirectories for matching messages."""
    messages: list[BusMessage] = []

    for subdir in (
        config.dispatch_dir,
        config.results_dir,
        config.signals_dir,
    ):
        if not subdir.is_dir():
            continue
        for fpath in sorted(subdir.glob("*.json")):
            msg = _parse_message_file(fpath)
            if msg is None:
                continue
            # Match recipient
            if msg.to_profile not in (profile, "broadcast"):
                continue
            # Match type
            if msg_types and msg.msg_type not in msg_types:
                continue
            messages.append(msg)

    messages.sort(key=lambda m: m.timestamp)
    return messages


def _parse_message_file(fpath: Path) -> Optional[BusMessage]:
    """Parse a single message file. Returns None on failure."""
    try:
        data = json.loads(fpath.read_text(encoding="utf-8"))
        return BusMessage(
            message_id=data["message_id"],
            from_profile=data["from"],
            to_profile=data["to"],
            msg_type=data["type"],
            timestamp=data["timestamp"],
            correlation_id=data.get("correlation_id"),
            payload=data.get("payload", {}),
            ttl_seconds=data.get("ttl_seconds", 300),
        )
    except (json.JSONDecodeError, KeyError, OSError):
        return None


# ---------------------------------------------------------------------------
# High-level operations
# ---------------------------------------------------------------------------


def dispatch_tasks(config: BusConfig, tasks: list[dict]) -> list[str]:
    """Batch-dispatch task messages to the bus.

    Args:
        config: Bus configuration.
        tasks: List of task dicts, each must contain:
            profile, objective, (optional: mode, input_context, capabilities)

    Returns:
        List of message IDs that were dispatched.
    """
    ids: list[str] = []
    for task in tasks:
        profile = task["profile"]
        msg = BusMessage(
            message_id=_make_message_id(),
            from_profile="facilitator",
            to_profile=profile,
            msg_type="task",
            timestamp=datetime.now(timezone.utc).isoformat(),
            correlation_id=None,
            payload={
                "task_id": task.get("task_id", _make_message_id()),
                "profile": profile,
                "mode": task.get("mode", "research"),
                "objective": task["objective"],
                "input_context": task.get("input_context", []),
                "required_capabilities": task.get("required_capabilities", []),
                "expected_output_schema": "role-result",
            },
        )
        send_message(config, msg)
        ids.append(msg.message_id)
    return ids


def collect_results(
    config: BusConfig,
    timeout_seconds: int = 60,
) -> dict[str, dict]:
    """Wait for and collect results from all profiles.

    Args:
        config: Bus configuration.
        timeout_seconds: Maximum wait time.

    Returns:
        Dict mapping profile name to its role_result payload (or None on timeout).
    """
    results: dict[str, dict] = {}
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        for profile in config.profiles:
            if profile in results:
                continue
            msgs = receive_messages(config, "facilitator", "result")
            for m in msgs:
                from_p = m.from_profile
                # Only accept results from registered profiles
                if from_p not in config.profiles:
                    continue
                if from_p not in results:
                    results[from_p] = m.payload.get("role_result", {})

        if len(results) >= len(config.profiles):
            return results

        time.sleep(1.0)

    return results


def send_shutdown(config: BusConfig) -> dict[str, bool]:
    """Send shutdown_request and wait for all profiles to acknowledge.

    Args:
        config: Bus configuration.

    Returns:
        Dict mapping profile name to True (shutdown_approved received) or False (timeout).
    """
    deadline = config.timeout_graceful
    request_id = _make_message_id()

    if not config.profiles:
        return {}

    future_deadline = datetime.now(timezone.utc).timestamp() + deadline

    # Broadcast shutdown_request
    shutdown_msg = BusMessage(
        message_id=request_id,
        from_profile="facilitator",
        to_profile="broadcast",
        msg_type="shutdown_request",
        timestamp=datetime.now(timezone.utc).isoformat(),
        correlation_id=None,
        payload={
            "reason": "task complete",
            "deadline": datetime.fromtimestamp(
                future_deadline, tz=timezone.utc
            ).isoformat(),
        },
    )
    send_message(config, shutdown_msg)

    # Wait for approvals
    approved: dict[str, bool] = {p: False for p in config.profiles}
    start = time.time()

    while time.time() - start < deadline:
        msgs = receive_messages(config, "facilitator", "shutdown_approved")
        for m in msgs:
            from_p = m.from_profile
            if from_p in approved:
                approved[from_p] = True

        if all(approved.values()):
            return approved

        time.sleep(1.0)

    return approved


def cleanup_bus(config: BusConfig) -> bool:
    """Remove the entire bus directory tree.

    Returns:
        True on success.
    """
    root = Path(config.root_dir).resolve()
    if not root.is_dir():
        return True
    # Safety gate: only clean directories that look like bus directories
    # (must be named "bus" and contain dispatch/results/signals subdirs)
    if not (
        root.name == "bus"
        and (root / "dispatch").is_dir()
        and (root / "results").is_dir()
    ):
        return False
    try:
        shutil.rmtree(str(root))
        return True
    except OSError:
        return False


def check_bus_health(config: BusConfig) -> dict:
    """Inspect bus state for orphaned messages, timeouts, etc.

    Returns:
        Health check dict with counts and warnings.
    """
    root = Path(config.root_dir)
    total = 0
    orphaned = 0
    now = time.time()

    for sub in (config.dispatch_dir, config.results_dir, config.signals_dir):
        if not sub.is_dir():
            continue
        for fpath in sub.glob("*.json"):
            total += 1
            try:
                data = json.loads(fpath.read_text(encoding="utf-8"))
                ttl = data.get("ttl_seconds", 300)
                ts = data.get("timestamp", "")
                if ts:
                    age = now - datetime.fromisoformat(ts).timestamp()
                    if age > ttl:
                        orphaned += 1
            except (json.JSONDecodeError, KeyError, ValueError, OSError):

                orphaned += 1

    return {
        "total_messages": total,
        "orphaned_messages": orphaned,
        "healthy": total == 0 or orphaned < total * 0.5,
        "root_dir": str(root),
        "exists": root.is_dir(),
    }



# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="think-tank Filesystem Message Bus"
    )
    parser.add_argument(
        "--run-id",
        required=True,
        help="Run identifier for bus isolation",
    )
    parser.add_argument(
        "--action",
        choices=[
            "create", "send", "receive", "shutdown", "cleanup", "health",
        ],
        required=True,
    )
    parser.add_argument(
        "--profiles",
        nargs="+",
        default=["collector", "skeptic", "synthesizer"],
    )
    parser.add_argument(
        "--base-dir",
        default=".think-tank/runs",
    )
    args = parser.parse_args()

    # Validate run_id to prevent path traversal
    from .safety import validate_safe_name

    ok, reason = validate_safe_name(args.run_id)
    if not ok:
        print(f"❌ Invalid --run-id: {reason}")
        exit(1)

    if args.action == "create":
        bus = create_bus(args.run_id, args.profiles, args.base_dir)
        print(f"Bus created at {bus.root_dir} with profiles {bus.profiles}")

    elif args.action in ("receive", "health", "shutdown", "cleanup"):
        bus = BusConfig(
            root_dir=str(
                Path(args.base_dir) / args.run_id / "bus"
            ),
            profiles=args.profiles,
            run_id=args.run_id,
        )

        if args.action == "receive":
            for p in args.profiles:
                msgs = receive_messages(bus, p)
                print(f"Messages for {p}: {len(msgs)}")

        elif args.action == "shutdown":
            status = send_shutdown(bus)
            print(f"Shutdown status: {status}")

        elif args.action == "cleanup":
            ok = cleanup_bus(bus)
            print(f"Cleanup: {'OK' if ok else 'FAILED'}")

        elif args.action == "health":
            h = check_bus_health(bus)
            print(json.dumps(h, indent=2))