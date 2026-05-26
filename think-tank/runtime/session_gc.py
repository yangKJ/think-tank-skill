"""Session-level garbage collection for zombie team resources.

This module provides a platform-neutral GC engine that scans team directories,
classifies teams (clean/zombie/orphan/active/unknown), and safely cleans up
zombie resources that accumulated due to shutdown_deadlock bugs.

Usage:
    cd think-tank && python -m runtime.session_gc --mode report_only
    cd think-tank && python -m runtime.session_gc --mode auto_clean --confirm
"""

from __future__ import annotations

import json
import os
import shlex
import shutil
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class TeamStatus:
    """Single team directory status snapshot."""

    team_name: str
    team_path: str
    classification: str  # clean | zombie | orphan | active | unknown
    member_count: int
    tmux_pane_states: dict
    last_modified: str
    evidence: list[str] = field(default_factory=list)


@dataclass
class GCReport:
    """Result of a GC scan."""

    scan_time: str
    team_root: str
    total_teams: int
    teams: list[TeamStatus] = field(default_factory=list)
    summary: dict = field(default_factory=dict)
    actions_taken: list[str] = field(default_factory=list)
    manual_cleanup: list[str] = field(default_factory=list)

    def format_summary(self) -> str:
        lines = [
            f"GC Report @ {self.scan_time}",
            f"  Team root: {self.team_root}",
            f"  Total teams: {self.total_teams}",
            f"  Clean:   {self.summary.get('clean', 0)}",
            f"  Zombie:  {self.summary.get('zombie', 0)}",
            f"  Orphan:  {self.summary.get('orphan', 0)}",
            f"  Active:  {self.summary.get('active', 0)}",
            f"  Unknown: {self.summary.get('unknown', 0)}",
        ]
        if self.actions_taken:
            lines.append("  Actions:")
            for a in self.actions_taken:
                lines.append(f"    - {a}")
        if self.manual_cleanup:
            lines.append("  Manual cleanup required:")
            for c in self.manual_cleanup:
                lines.append(f"    - {c}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def _expand_team_root(team_root: Optional[str] = None) -> Path:
    """Resolve team root path, defaulting to ~/.claude/teams/."""
    if team_root is None:
        team_root = os.path.join(os.path.expanduser("~"), ".claude", "teams")
    return Path(team_root).expanduser().resolve()


def _load_config(team_path: Path) -> Optional[dict]:
    """Safely load a team's config.json. Returns None on failure."""
    config_path = team_path / "config.json"
    if not config_path.exists():
        return None
    try:
        content = config_path.read_text(encoding="utf-8")
        return json.loads(content)
    except (json.JSONDecodeError, OSError):
        return None


def _team_age_seconds(team_path: Path) -> float:
    """Age of the team directory in seconds (mtime)."""
    try:
        return time.time() - team_path.stat().st_mtime
    except OSError:
        return 0.0


def _check_inbox_activity(team_path: Path) -> dict[str, list[str]]:
    """Check inbox directories for recent activity."""
    activity: dict[str, list[str]] = {}
    inbox_dir = team_path / "inboxes"
    if not inbox_dir.is_dir():
        return activity

    cutoff = time.time() - 300  # 5 min
    for inbox_file in inbox_dir.glob("*.json"):
        try:
            mtime = inbox_file.stat().st_mtime
            if mtime > cutoff:
                agent_name = inbox_file.stem
                activity[agent_name] = activity.get(agent_name, [])
                activity[agent_name].append(str(inbox_file))
        except OSError:
            pass
    return activity


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


def classify_team(
    team_path: Path,
    min_age_seconds: int = 600,
) -> TeamStatus:
    """Read config.json and classify a single team directory.

    Args:
        team_path: Path to the team directory.
        min_age_seconds: Minimum age before marking as zombie.

    Returns:
        TeamStatus with classification and evidence.
    """
    team_name = team_path.name
    evidence: list[str] = []
    member_count = 0
    tmux_states: dict[str, str] = {}

    config = _load_config(team_path)

    # No config → orphan
    if config is None:
        return TeamStatus(
            team_name=team_name,
            team_path=str(team_path),
            classification="orphan",
            member_count=0,
            tmux_pane_states={},
            last_modified=datetime.fromtimestamp(
                team_path.stat().st_mtime, tz=timezone.utc
            ).isoformat(),
            evidence=["No config.json found"],
        )

    members = config.get("members", [])
    member_count = len(members)

    # Collect tmux pane states
    for m in members:
        pane_id = m.get("tmuxPaneId", "")
        agent_id = m.get("agentId", m.get("name", "unknown"))
        tmux_states[str(agent_id)] = str(pane_id)

    age = _team_age_seconds(team_path)
    activity = _check_inbox_activity(team_path)

    # Check for shutdown_approved signals (config inbox messages)
    inbox_path = team_path / "inboxes"
    shutdown_approved_count = 0
    if inbox_path.is_dir():
        for inbox_f in inbox_path.glob("*.json"):
            try:
                data = json.loads(inbox_f.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    for msg in data:
                        text = str(msg.get("text", ""))
                        if "shutdown_approved" in text:
                            shutdown_approved_count += 1
            except (json.JSONDecodeError, OSError):
                pass

    # Classification logic
    has_in_process = any(v == "in-process" for v in tmux_states.values())
    has_terminated = bool(tmux_states) and all(
        v in ("", "terminated") for v in tmux_states.values()
    )
    has_activity = bool(activity)

    if has_activity:
        classification = "active"
        evidence.append("Recent inbox activity detected (within 5 min)")
    elif has_in_process and age >= min_age_seconds:
        classification = "zombie"
        evidence.append(
            f"tmuxPaneId is 'in-process' and team age {age:.0f}s >= {min_age_seconds}s"
        )
        if shutdown_approved_count >= 3:
            evidence.append(
                f"Agent sent shutdown_approved {shutdown_approved_count} times but never terminated"
            )
    elif has_terminated:
        classification = "clean"
        evidence.append("All agents show terminated or empty tmuxPaneId")
    elif has_in_process and age < min_age_seconds:
        classification = "active"
        evidence.append(
            f"tmuxPaneId is 'in-process' but team age {age:.0f}s < {min_age_seconds}s (grace period)"
        )
    else:
        classification = "unknown"
        evidence.append("Could not determine team state from config.json")

    return TeamStatus(
        team_name=team_name,
        team_path=str(team_path),
        classification=classification,
        member_count=member_count,
        tmux_pane_states=tmux_states,
        last_modified=datetime.fromtimestamp(
            team_path.stat().st_mtime, tz=timezone.utc
        ).isoformat(),
        evidence=evidence,
    )


# ---------------------------------------------------------------------------
# Scan & GC
# ---------------------------------------------------------------------------


def scan_teams(
    team_root: Optional[str] = None,
    min_age_seconds: int = 600,
) -> list[TeamStatus]:
    """Scan all team directories and classify each.

    Args:
        team_root: Path to teams directory (default: ~/.claude/teams/).
        min_age_seconds: Passed to classify_team for zombie detection.

    Returns:
        List of TeamStatus objects, one per directory.
    """
    root = _expand_team_root(team_root)
    if not root.is_dir():
        return []

    statuses: list[TeamStatus] = []
    for entry in sorted(root.iterdir()):
        if entry.is_dir():
            statuses.append(classify_team(entry, min_age_seconds=min_age_seconds))
    return statuses


def run_gc(
    team_root: Optional[str] = None,
    mode: str = "report_only",
    min_age_seconds: int = 600,
    dry_run: bool = True,
) -> GCReport:
    """Run garbage collection on team directories.

    Args:
        team_root: Path to teams directory.
        mode: 'report_only' | 'auto_clean' | 'interactive'.
        min_age_seconds: Teams younger than this are never cleaned.
        dry_run: If True, auto_clean only reports, never deletes.

    Returns:
        GCReport with scan results and actions taken.
    """
    root = _expand_team_root(team_root)
    teams = scan_teams(str(root), min_age_seconds=min_age_seconds)

    summary = _build_summary(teams)
    actions: list[str] = []
    manual: list[str] = []

    # Only clean teams with valid config.json (clean + zombie).
    # orphan directories lack config.json and must be handled manually.
    cleanable = {"clean", "zombie"}
    safe = {"active", "unknown", "orphan"}

    if mode == "report_only":
        actions.append("report_only: no files deleted")

    elif mode in ("auto_clean", "interactive"):
        for team in teams:
            team_path = Path(team.team_path)
            if team.classification in safe:
                continue
            if team.classification in cleanable:
                if _team_age_seconds(team_path) < min_age_seconds:
                    actions.append(f"skipped {team.team_name} (too young)")
                    continue
                if dry_run:
                    actions.append(
                        f"[dry-run] would delete {team.team_name} ({team.classification})"
                    )
                else:
                    ok = clean_team(str(team_path))
                    if ok:
                        actions.append(
                            f"deleted {team.team_name} ({team.classification})"
                        )
                    else:
                        manual.append(str(team_path))
                        actions.append(
                            f"FAILED to delete {team.team_name}"
                        )

    report = GCReport(
        scan_time=datetime.now(timezone.utc).isoformat(),
        team_root=str(root),
        total_teams=len(teams),
        teams=teams,
        summary=summary,
        actions_taken=actions,
        manual_cleanup=manual,
    )
    return report


def _build_summary(teams: list[TeamStatus]) -> dict[str, int]:
    """Count teams by classification."""
    counts: dict[str, int] = {}
    for t in teams:
        counts[t.classification] = counts.get(t.classification, 0) + 1
    return counts


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------


def clean_team(team_path: str, backup: bool = False) -> bool:
    """Delete a team directory.

    Args:
        team_path: Absolute path to the team directory.
        backup: If True, move to trash instead of deleting (not implemented).

    Returns:
        True if deletion succeeded.
    """
    p = Path(team_path)
    if not p.is_dir():
        return False
    try:
        # Safety: only clean directories inside known team roots
        # Use path component matching to avoid substring bypass
        resolved = p.resolve()
        parts = resolved.parts
        if not (
            len(parts) >= 2
            and parts[-2] == "teams"
            and parts[-3] == ".claude"
        ):
            return False
        # Reject symlinks to prevent TOCTOU attacks
        if p.is_symlink():
            return False
        shutil.rmtree(str(resolved))
        return True
    except OSError:
        return False


def format_cleanup_command(team_path: str) -> str:
    """Generate the manual cleanup command for a zombie team."""
    return f"rm -rf {shlex.quote(team_path)}"


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="think-tank Session GC — scan and clean zombie teams"
    )
    parser.add_argument(
        "--team-root",
        default=None,
        help="Path to teams directory (default: ~/.claude/teams/)",
    )
    parser.add_argument(
        "--mode",
        choices=["report_only", "auto_clean", "interactive"],
        default="report_only",
        help="GC mode (default: report_only)",
    )
    parser.add_argument(
        "--min-age",
        type=int,
        default=600,
        help="Minimum team age in seconds before cleanup (default: 600)",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Required for auto_clean mode (without this, auto_clean is dry-run)",
    )
    args = parser.parse_args()

    dry = True
    if args.mode in ("auto_clean", "interactive"):
        if not args.confirm:
            print("⚠️  --confirm not set, running in dry-run mode\n")
        dry = not args.confirm

    report = run_gc(
        team_root=args.team_root,
        mode=args.mode,
        min_age_seconds=args.min_age,
        dry_run=dry,
    )
    print(report.format_summary())