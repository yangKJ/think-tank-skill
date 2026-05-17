#!/usr/bin/env python3
"""Operational helper for one-shot project leader pilot runs.

The script runs a pilot spec and writes one CSV row for production verification
tracking.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from project_leader_pilot import run_project_leader_pilot


FIELDNAMES = [
    "run_id",
    "timestamp",
    "project_id",
    "request",
    "selection_count",
    "selected_candidate_count",
    "promoted_count",
    "activated_candidate_count",
    "dispatch_status",
    "invocation_gate_status",
    "bundle_status",
    "host_provider",
    "host_result_path",
    "successful_invocations",
    "failed_invocations",
    "boundary_violations",
    "host_errors",
    "manual_fallback_count",
    "operator",
    "operator_notes",
]


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"invalid pilot spec mapping: {path}")
    return data


def _safe_result_count(invocation_result: dict[str, Any] | None) -> tuple[int, int]:
    if not invocation_result:
        return 0, 0
    result_count = int(invocation_result.get("result_count", 0))
    successful = int(invocation_result.get("successful_invocations", 0))
    failed = max(0, result_count - successful)
    return successful, failed


def _coerce_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ";".join(str(item) for item in value)
    return str(value)


def build_row(spec: Path, operator: str, notes: str, host_provider: str | None) -> dict[str, Any]:
    spec_data = _load_yaml(spec)
    result = run_project_leader_pilot(spec)
    orchestrator_result = result.get("orchestrator_result", {})
    gate = orchestrator_result.get("project_candidate_invocation_gate", {})
    bundle = orchestrator_result.get("project_candidate_host_dispatch_bundle", {})
    invocation_evidence = orchestrator_result.get("project_candidate_invocation_evidence")
    selection = result.get("selection_result", {})
    review = result.get("review_report", {})
    activation = result.get("project_team_activation")

    selection_count = int(selection.get("selected_count", 0))
    promoted_count = int(review.get("promoted_count", 0))
    activated_candidates = len(activation.get("candidate_agents", [])) if activation else 0
    dispatch_status = bundle.get("dispatch_status", "not_applicable")
    boundary_violations = 0
    if dispatch_status == "ready_for_host_dispatch" and not invocation_evidence and host_provider:
        boundary_violations += 1

    successful, failed = _safe_result_count(invocation_evidence)
    if not spec_data.get("candidate_host_results"):
        boundary_violations += 1

    return {
        "run_id": f"{spec_data['project_id']}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "project_id": spec_data["project_id"],
        "request": spec_data["request"],
        "selection_count": selection_count,
        "selected_candidate_count": int(selection.get("selected_count", 0)),
        "promoted_count": promoted_count,
        "activated_candidate_count": activated_candidates,
        "dispatch_status": dispatch_status,
        "invocation_gate_status": gate.get("decision_status", "not_applicable"),
        "bundle_status": bundle.get("dispatch_status", "not_applicable"),
        "host_provider": host_provider or "",
        "host_result_path": _coerce_str(spec_data.get("candidate_host_results")),
        "successful_invocations": successful,
        "failed_invocations": failed,
        "boundary_violations": boundary_violations,
        "host_errors": "none",
        "manual_fallback_count": 0,
        "operator": operator,
        "operator_notes": notes,
    }


def append_csv(log_path: Path, row: dict[str, Any]) -> None:
    exists = log_path.exists()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def run_once(spec: Path, log_path: Path, operator: str, notes: str, host_provider: str | None) -> dict[str, Any]:
    row = build_row(spec, operator=operator, notes=notes, host_provider=host_provider)
    append_csv(log_path, row)
    return row


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a project leader pilot and emit one verification row.")
    parser.add_argument("pilot", type=Path, help="Pilot spec path.")
    parser.add_argument(
        "--log-csv",
        required=True,
        type=Path,
        help="CSV file path to append one row of verification metrics.",
    )
    parser.add_argument("--operator", default="leader-runtime-operator", help="Operator name.")
    parser.add_argument("--notes", default="", help="Operator notes for this run.")
    parser.add_argument("--host-provider", default="", help="Host provider identifier for this run.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    row = run_once(args.pilot, args.log_csv, args.operator, args.notes, args.host_provider or None)
    print("run_id:", row["run_id"])
    print("log_csv:", args.log_csv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
