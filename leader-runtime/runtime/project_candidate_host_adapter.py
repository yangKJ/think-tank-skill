"""把 ready_uninvoked 的项目候选任务转成 host dispatch bundle，并接收结果证据。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ADAPTER_NAME = "codex-host-subagent"
ADAPTER_VERSION = "0.1.0"


def build_host_dispatch_bundle(
    candidate_packets: list[dict[str, Any]],
    invocation_gate: dict[str, Any],
) -> dict[str, Any]:
    decisions_by_task = {
        item["task_id"]: item
        for item in invocation_gate.get("candidate_decisions", [])
    }
    requests: list[dict[str, Any]] = []
    for packet in candidate_packets:
        decision = decisions_by_task.get(packet["task_id"])
        if decision is None or decision["decision"] != "ready_uninvoked":
            continue
        requests.append(
            {
                "task_id": packet["task_id"],
                "candidate_agent_id": packet["candidate_agent_id"],
                "candidate_name": packet["candidate_name"],
                "dispatch_status": "ready_for_host_dispatch",
                "host_payload": {
                    "objective": packet["objective"],
                    "task_scope": packet["task_scope"],
                    "input_context": packet["input_context"],
                    "deliverables": packet["deliverables"],
                    "acceptance_checks": packet["acceptance_checks"],
                    "fallback_rule": packet["fallback_rule"],
                },
                "invoked": False,
            }
        )

    if requests:
        dispatch_status = "ready_for_host_dispatch"
    elif invocation_gate.get("decision_status") == "blocked":
        dispatch_status = "blocked"
    else:
        dispatch_status = "not_applicable"

    return {
        "bundle_id": "project-candidate-host-dispatch-bundle",
        "adapter": ADAPTER_NAME,
        "adapter_version": ADAPTER_VERSION,
        "dispatch_status": dispatch_status,
        "request_count": len(requests),
        "dispatch_requests": requests,
        "boundaries": [
            "This bundle is host-ready but does not execute any subagent by itself.",
            "A host adapter must return explicit invoked=true evidence before the system can claim real invocation.",
        ],
    }


def load_host_results(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"host results must be a list: {path}")
    return data


def ingest_host_results(
    bundle: dict[str, Any],
    host_results: list[dict[str, Any]],
) -> dict[str, Any]:
    bundle_tasks = {
        item["task_id"]: item["candidate_agent_id"]
        for item in bundle.get("dispatch_requests", [])
    }
    results: list[dict[str, Any]] = []
    successful_invocations = 0
    for item in host_results:
        task_id = item["task_id"]
        candidate_agent_id = item["candidate_agent_id"]
        if bundle_tasks.get(task_id) != candidate_agent_id:
            continue
        if item.get("invoked") and item.get("invocation_status") == "success":
            successful_invocations += 1
        results.append(
            {
                "task_id": task_id,
                "candidate_agent_id": candidate_agent_id,
                "invocation_status": item["invocation_status"],
                "invoked": bool(item.get("invoked")),
                "result_ref": item["result_ref"],
                "summary": item.get("summary"),
            }
        )
    return {
        "evidence_id": "project-candidate-invocation-evidence",
        "bundle_id": bundle["bundle_id"],
        "result_count": len(results),
        "successful_invocations": successful_invocations,
        "results": results,
        "boundaries": [
            "Invocation evidence is only as trustworthy as the host adapter result source.",
            "Only host-returned invoked=true records can upgrade the claim from ready_uninvoked to real invocation evidence.",
        ],
    }


if __name__ == "__main__":
    import argparse
    import yaml

    parser = argparse.ArgumentParser(description="Build and ingest host dispatch bundles for project candidates.")
    parser.add_argument("--bundle-json", type=Path, default=None)
    parser.add_argument("--results-json", type=Path, default=None)
    args = parser.parse_args()
    if args.bundle_json and args.results_json:
        bundle = json.loads(args.bundle_json.read_text(encoding="utf-8"))
        evidence = ingest_host_results(bundle, load_host_results(args.results_json))
        print(yaml.safe_dump(evidence, allow_unicode=True, sort_keys=False))
