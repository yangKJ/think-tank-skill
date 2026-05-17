"""把项目 team pack 激活成 leader 可见的项目专家队伍。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from leader_registry import GLOBAL_EXPERT_POOL


GLOBAL_EXPERTS_BY_ID = {entry.expert_id: entry for entry in GLOBAL_EXPERT_POOL}


def load_team_pack(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"team pack must be a mapping: {path}")
    return data


def _global_roster_entries(team_pack: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    excludes = set(team_pack.get("exclude_experts", []))
    for expert_id in team_pack.get("include_experts", []):
        if expert_id in excludes:
            continue
        expert = GLOBAL_EXPERTS_BY_ID.get(expert_id)
        if expert is None:
            continue
        entries.append(
            {
                "roster_id": expert.expert_id,
                "name": expert.label,
                "source": "global_registry",
                "authority_scope": expert.authority_scope,
                "dispatch_status": "available",
                "source_path": None,
            }
        )
    return entries


def _candidate_roster_entries(team_pack: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for candidate in team_pack.get("include_candidate_agents", []):
        if candidate.get("conversion_status") != "promoted":
            continue
        entries.append(
            {
                "roster_id": candidate["agent_id"],
                "name": candidate["name"],
                "source": "project_candidate",
                "authority_scope": "project_scoped",
                "dispatch_status": "promoted_uninvoked",
                "source_path": candidate["source_path"],
            }
        )
    return entries


def activate_project_team_pack(team_pack: dict[str, Any]) -> dict[str, Any]:
    global_entries = _global_roster_entries(team_pack)
    candidate_entries = _candidate_roster_entries(team_pack)
    roster = global_entries + candidate_entries
    return {
        "activation_id": f"{team_pack['project_id']}-{team_pack['pack_id']}-activation",
        "project_id": team_pack["project_id"],
        "pack_id": team_pack["pack_id"],
        "active_count": len(roster),
        "global_experts": [entry["roster_id"] for entry in global_entries],
        "candidate_agents": [entry["roster_id"] for entry in candidate_entries],
        "dispatch_roster": roster,
        "verification_status": "verified_partial" if roster else "specified",
        "boundaries": [
            "Project team activation loads roster entries only; it does not invoke any subagent.",
            "Promoted project candidates remain project-scoped and do not alter the global registry.",
            "Candidate dispatch requires a later runtime-specific invocation gate.",
        ],
    }


def run_activation(team_pack_path: Path) -> dict[str, Any]:
    return activate_project_team_pack(load_team_pack(team_pack_path))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Activate a project team pack into a dispatch roster.")
    parser.add_argument("team_pack", type=Path)
    args = parser.parse_args()
    print(yaml.safe_dump(run_activation(args.team_pack), allow_unicode=True, sort_keys=False))
