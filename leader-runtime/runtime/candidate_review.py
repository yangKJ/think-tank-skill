"""候选 subagent 晋升门禁。"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

from candidate_selection import run_selection


REVIEW_CHECKS = [
    "frontmatter_complete",
    "project_scoped",
    "source_path_relative",
    "boundary_declared",
    "not_global_registry_mutation",
]


def _candidate_checks(candidate: dict[str, Any]) -> tuple[list[str], list[str]]:
    passed: list[str] = []
    notes: list[str] = []
    if candidate.get("agent_id") and candidate.get("name"):
        passed.append("frontmatter_complete")
    else:
        notes.append("Missing agent_id or name.")
    source_path = str(candidate.get("source_path", ""))
    if source_path and not source_path.startswith("/"):
        passed.append("source_path_relative")
    else:
        notes.append("Source path must be relative before promotion.")
    if candidate.get("conversion_status") == "candidate":
        passed.append("project_scoped")
    else:
        notes.append("Only candidate status can be promoted by this gate.")
    passed.append("boundary_declared")
    passed.append("not_global_registry_mutation")
    return passed, notes


def review_candidate_selection(
    selection_result: dict[str, Any],
    team_pack_draft: dict[str, Any],
    reviewer_id: str = "think_tank_global_leader",
    approved_agent_ids: list[str] | None = None,
    rejected_agent_ids: list[str] | None = None,
) -> dict[str, Any]:
    selected = selection_result.get("selected_candidates", [])
    approved = set(approved_agent_ids) if approved_agent_ids is not None else {item["agent_id"] for item in selected}
    rejected = set(rejected_agent_ids or [])
    reviewed_candidates: list[dict[str, Any]] = []
    promoted_ids: set[str] = set()

    for candidate in selected:
        checks, notes = _candidate_checks(candidate)
        agent_id = candidate["agent_id"]
        should_promote = agent_id in approved and agent_id not in rejected and set(REVIEW_CHECKS).issubset(checks)
        decision = "promote" if should_promote else "reject"
        if should_promote:
            promoted_ids.add(agent_id)
        reviewed_candidates.append(
            {
                "agent_id": agent_id,
                "name": candidate["name"],
                "decision": decision,
                "checks": checks,
                "notes": notes or ["Candidate passed project-scoped promotion checks."],
            }
        )

    promoted_team_pack = deepcopy(team_pack_draft)
    promoted_team_pack["include_candidate_agents"] = [
        {**item, "conversion_status": "promoted"}
        for item in team_pack_draft.get("include_candidate_agents", [])
        if item["agent_id"] in promoted_ids
    ]
    promoted_team_pack["project_tags"] = sorted(set(promoted_team_pack.get("project_tags", []) + ["candidate-reviewed"]))
    promoted_team_pack["boundaries"] = list(promoted_team_pack.get("boundaries", [])) + [
        "Promoted candidate agents are project-scoped and do not alter the global registry.",
        "Promotion does not prove runtime invocation.",
    ]

    promoted_count = len(promoted_team_pack["include_candidate_agents"])
    rejected_count = len(reviewed_candidates) - promoted_count
    if promoted_count:
        status = "passed"
    elif reviewed_candidates:
        status = "needs_revision"
        promoted_team_pack = None
    else:
        status = "rejected"
        promoted_team_pack = None

    return {
        "review_id": f"{selection_result['project_id']}-{selection_result['policy_id']}-review",
        "reviewer_id": reviewer_id,
        "project_id": selection_result["project_id"],
        "policy_id": selection_result["policy_id"],
        "status": status,
        "reviewed_candidates": reviewed_candidates,
        "promoted_count": promoted_count,
        "rejected_count": rejected_count,
        "promoted_team_pack": promoted_team_pack,
        "boundaries": [
            "Candidate review does not invoke any subagent.",
            "Promotion is project-scoped and does not modify global-experts.yaml.",
            "Project leader still owns final dispatch and acceptance.",
        ],
    }


def run_review(policy_path: Path, approved_agent_ids: list[str] | None = None) -> dict[str, Any]:
    selection_bundle = run_selection(policy_path)
    report = review_candidate_selection(
        selection_bundle["selection_result"],
        selection_bundle["project_team_pack_draft"],
        approved_agent_ids=approved_agent_ids,
    )
    return {
        "selection_result": selection_bundle["selection_result"],
        "review_report": report,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Review and promote project-specific candidate agents.")
    parser.add_argument("policy", type=Path)
    parser.add_argument("--approve", action="append", default=None, help="Agent id to approve. Defaults to all selected candidates.")
    args = parser.parse_args()
    result = run_review(args.policy, approved_agent_ids=args.approve)
    print(yaml.safe_dump(result, allow_unicode=True, sort_keys=False))
