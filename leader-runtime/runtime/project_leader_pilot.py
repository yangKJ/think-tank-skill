"""项目级 leader 试点闭环运行器。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from candidate_review import review_candidate_selection
from candidate_selection import run_selection
from orchestrator import run_leader_orchestrator
from project_team_activation import activate_project_team_pack


ROOT = Path(__file__).resolve().parents[2]


def load_pilot_spec(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"pilot spec must be a mapping: {path}")
    return data


def run_project_leader_pilot(spec_path: Path) -> dict[str, Any]:
    spec = load_pilot_spec(spec_path)
    policy_path = (ROOT / spec["selection_policy"]).resolve()
    selection_bundle = run_selection(policy_path)
    selection_result = selection_bundle["selection_result"]
    review_report = review_candidate_selection(
        selection_result,
        selection_bundle["project_team_pack_draft"],
        reviewer_id=spec.get("reviewer_id", "think_tank_global_leader"),
        approved_agent_ids=spec.get("approved_agent_ids"),
        rejected_agent_ids=spec.get("rejected_agent_ids"),
    )
    promoted_team_pack = review_report.get("promoted_team_pack")
    activation = activate_project_team_pack(promoted_team_pack) if promoted_team_pack else None
    orchestrator_result = run_leader_orchestrator(
        spec["request"],
        target=spec.get("target"),
        write_run=bool(spec.get("write_run", False)),
        team_pack_data=promoted_team_pack,
        allow_candidate_invocation=bool(spec.get("allow_candidate_invocation", False)),
        candidate_runtime_support=spec.get("candidate_runtime_support", "not_verified"),
        candidate_host_results_path=(ROOT / spec["candidate_host_results"]).resolve()
        if spec.get("candidate_host_results")
        else None,
    )
    return {
        "pilot_id": spec["pilot_id"],
        "project_id": spec["project_id"],
        "verification_status": "verified_partial",
        "selection_result": selection_result,
        "review_report": review_report,
        "project_team_activation": activation,
        "orchestrator_result": orchestrator_result,
        "boundaries": [
            "Project leader pilot runs a repo-local sample flow and does not prove every external host runtime.",
            "Selection, review, promotion, activation, dispatch planning, gate, and host evidence remain distinct states.",
            "Host evidence is only acknowledged when the spec provides a candidate_host_results file.",
        ],
    }


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run a project leader pilot flow.")
    parser.add_argument("pilot", type=Path)
    args = parser.parse_args()
    print(json.dumps(run_project_leader_pilot(args.pilot), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
