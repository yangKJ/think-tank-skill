"""为项目 promoted candidate agents 生成可审计的派遣计划。"""

from __future__ import annotations

from typing import Any

from leader_registry import LEADER_ID, SCHEMA_CHECKS


def candidate_rows(project_team_activation: dict[str, Any] | None) -> list[dict[str, Any]]:
    if project_team_activation is None:
        return []
    return [
        item
        for item in project_team_activation.get("dispatch_roster", [])
        if item.get("source") == "project_candidate"
        and item.get("dispatch_status") == "promoted_uninvoked"
    ]


def build_project_candidate_task_packets(
    request: str,
    mode: str,
    capabilities: list[str],
    project_team_activation: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    for index, row in enumerate(candidate_rows(project_team_activation), start=1):
        packets.append(
            {
                "task_id": f"{mode}-project-candidate-{index}",
                "leader_id": LEADER_ID,
                "candidate_agent_id": row["roster_id"],
                "candidate_name": row["name"],
                "source_path": row["source_path"],
                "objective": request,
                "task_scope": f"Prepare the project-specific expert slice for {row['name']}.",
                "input_context": [
                    f"mode={mode}",
                    f"request={request}",
                    "source=project_team_activation",
                ],
                "deliverables": [
                    "project_specific_claim",
                    "evidence_or_assumption",
                    "risks",
                    "recommendations",
                    "boundaries",
                ],
                "acceptance_checks": list(SCHEMA_CHECKS),
                "required_capabilities": list(capabilities),
                "dispatch_status": "planned_uninvoked",
                "invocation_boundary": "This packet is a dispatch plan only; the project candidate subagent has not been invoked.",
                "fallback_rule": "Use global expert packets and single_agent_multi_profile_fallback if candidate invocation is unavailable.",
            }
        )
    return packets


def summarize_project_candidate_dispatch(packets: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "planned_count": len(packets),
        "planned_candidate_agents": [packet["candidate_agent_id"] for packet in packets],
        "dispatch_status": "planned_uninvoked" if packets else "not_applicable",
        "boundaries": [
            "Project candidate task packets are dispatch plans, not invocation evidence.",
            "A promoted candidate can be planned without being called.",
        ],
    }
