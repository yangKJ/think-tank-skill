"""项目候选 subagent 的真实调用前置门禁。"""

from __future__ import annotations

from typing import Any


READY_SUPPORT = {"verified_partial", "verified"}


def evaluate_project_candidate_invocation_gate(
    candidate_packets: list[dict[str, Any]],
    allow_invocation: bool = False,
    runtime_support: str = "not_verified",
) -> dict[str, Any]:
    if not candidate_packets:
        return {
            "gate_id": "project-candidate-invocation-gate",
            "allow_invocation": allow_invocation,
            "runtime_support": runtime_support,
            "decision_status": "not_applicable",
            "candidate_decisions": [],
            "boundaries": [
                "No project candidate task packets were present.",
                "No subagent invocation was attempted.",
            ],
        }

    candidate_decisions: list[dict[str, Any]] = []
    ready = allow_invocation and runtime_support in READY_SUPPORT
    for packet in candidate_packets:
        if ready:
            decision = "ready_uninvoked"
            reason = "Invocation permission and runtime support are present, but this gate does not execute the subagent."
        elif not allow_invocation:
            decision = "blocked"
            reason = "Invocation permission is false."
        else:
            decision = "blocked"
            reason = f"Runtime support is {runtime_support}; verified_partial or verified is required."
        candidate_decisions.append(
            {
                "candidate_agent_id": packet["candidate_agent_id"],
                "task_id": packet["task_id"],
                "decision": decision,
                "reason": reason,
                "invoked": False,
            }
        )

    return {
        "gate_id": "project-candidate-invocation-gate",
        "allow_invocation": allow_invocation,
        "runtime_support": runtime_support,
        "decision_status": "ready_uninvoked" if ready else "blocked",
        "candidate_decisions": candidate_decisions,
        "boundaries": [
            "This gate never invokes subagents; it only decides whether invocation would be allowed.",
            "ready_uninvoked is not invocation evidence.",
            "A later platform-specific invocation adapter must produce invoked=true evidence.",
        ],
    }
