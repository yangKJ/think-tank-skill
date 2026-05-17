#!/usr/bin/env python3
"""Local host adapter simulator for project candidate dispatch bundles."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def build_simulated_host_results(
    bundle: dict[str, Any],
    host_provider: str,
    run_id: str | None = None,
    force_fail_task_ids: set[str] | None = None,
) -> list[dict[str, Any]]:
    if not isinstance(bundle, dict):
        raise TypeError("dispatch bundle must be a mapping")
    requests = bundle.get("dispatch_requests")
    if not isinstance(requests, list):
        raise ValueError("dispatch bundle must include dispatch_requests")
    run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    forced_fail = force_fail_task_ids or set()

    results: list[dict[str, Any]] = []
    for request in requests:
        task_id = request.get("task_id")
        candidate_agent_id = request.get("candidate_agent_id")
        if not task_id or not candidate_agent_id:
            results.append(
                {
                    "task_id": str(task_id or ""),
                    "candidate_agent_id": str(candidate_agent_id or ""),
                    "invocation_status": "failed",
                    "invoked": False,
                    "result_ref": f"{host_provider}://simulated/{run_id}/invalid-payload",
                    "summary": "Missing task_id or candidate_agent_id in dispatch request.",
                }
            )
            continue

        if task_id in forced_fail:
            results.append(
                {
                    "task_id": task_id,
                    "candidate_agent_id": candidate_agent_id,
                    "invocation_status": "failed",
                    "invoked": False,
                    "result_ref": f"{host_provider}://simulated/{run_id}/{task_id}/{candidate_agent_id}/failed",
                    "summary": "Simulated host execution failure by configuration.",
                }
            )
            continue

        result_ref = f"{host_provider}://simulated/{run_id}/{task_id}/{candidate_agent_id}/result"
        results.append(
            {
                "task_id": task_id,
                "candidate_agent_id": candidate_agent_id,
                "invocation_status": "success",
                "invoked": True,
                "result_ref": result_ref,
                "summary": f"Simulated host execution for {candidate_agent_id} on task {task_id}.",
            }
        )
    return results


def build_simulated_host_evidence(
    bundle: dict[str, Any],
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "evidence_id": "project-candidate-simulated-host-results",
        "bundle_id": bundle.get("bundle_id", "project-candidate-host-dispatch-bundle"),
        "result_count": len(results),
        "successful_invocations": sum(
            1 for item in results if item.get("invoked") and item.get("invocation_status") == "success"
        ),
        "results": results,
        "boundaries": [
            "This runner is a local simulator for development and test.",
            "It must not be treated as real external host invocation.",
            "Only external host-adapter results should be used for verified production evidence.",
        ],
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulate host execution for project candidate dispatch bundles.")
    parser.add_argument("--bundle-json", type=Path, required=True, help="Host dispatch bundle path.")
    parser.add_argument("--output-json", type=Path, required=True, help="Host results output path.")
    parser.add_argument("--host-provider", default="codex-host-simulator", help="Host adapter id label.")
    parser.add_argument(
        "--force-fail-task-ids",
        default="",
        help="Comma-separated task IDs that should be simulated as failed.",
    )
    parser.add_argument("--run-id", default=None, help="Optional run id to stabilize result_ref.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    bundle = json.loads(args.bundle_json.read_text(encoding="utf-8"))
    force_fail = set(
        filter(None, map(str.strip, args.force_fail_task_ids.split(",")))
    )
    results = build_simulated_host_results(
        bundle,
        host_provider=args.host_provider,
        run_id=args.run_id,
        force_fail_task_ids=force_fail,
    )
    write_json(args.output_json, results)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
