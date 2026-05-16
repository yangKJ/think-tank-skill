"""Project-derived leader helpers for leader-runtime."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from leader_registry import GLOBAL_EXPERT_POOL, LEADER_ID, SCHEMA_CHECKS, registry_payload


DEFAULT_ESCALATION_PATH = ["retry", "reroute", "downgrade", "manual_arbitration"]


def default_project_team_pack(project_id: str, project_tags: list[str] | None = None) -> dict[str, Any]:
    return {
        "pack_id": f"{project_id}-core-pack",
        "project_id": project_id,
        "inherits_from_registry": "think_tank_codex_global_registry",
        "include_experts": ["evidence_collector", "domain_analyst", "risk_skeptic"],
        "include_candidate_agents": [],
        "candidate_source_policy": None,
        "exclude_experts": [],
        "project_tags": project_tags or [project_id],
        "capability_overrides": {},
        "acceptance_overrides": {
            "required_checks": list(SCHEMA_CHECKS),
            "retry_limit": 2,
        },
        "boundaries": [
            "Project team pack may narrow the expert subset but must not rewrite global expert semantics.",
        ],
    }


def default_project_leader(project_id: str, project_label: str, team_pack_id: str) -> dict[str, Any]:
    return {
        "project_id": project_id,
        "project_label": project_label,
        "leader_id": f"{project_id.replace('-', '_')}_leader",
        "inherits_from": LEADER_ID,
        "team_pack_id": team_pack_id,
        "supported_modes": ["research", "review", "strategy"],
        "default_dispatch_path": "single_agent_multi_profile_fallback",
        "acceptance_profile": {
            "required_checks": list(SCHEMA_CHECKS),
            "retry_limit": 2,
            "escalation_path": list(DEFAULT_ESCALATION_PATH),
        },
        "enabled_capabilities": ["source-acquisition", "knowledge-persistence"],
        "disabled_capabilities": [],
        "boundaries": [
            "Project leader inherits leader-runtime governance and only narrows scope.",
        ],
    }


def derive_project_registry(team_pack: dict[str, Any]) -> dict[str, Any]:
    base = registry_payload(scope="project", inherits_from=team_pack["inherits_from_registry"])
    includes = set(team_pack.get("include_experts", []))
    excludes = set(team_pack.get("exclude_experts", []))
    tags = team_pack.get("project_tags", [])
    experts = []
    for entry in GLOBAL_EXPERT_POOL:
        if includes and entry.expert_id not in includes:
            continue
        if entry.expert_id in excludes:
            continue
        item = deepcopy(entry.to_dict())
        item["owner_layer"] = "project"
        item["project_tags"] = sorted(set(item.get("project_tags", []) + tags))
        overrides = team_pack.get("capability_overrides", {})
        if overrides:
            item["capability_affinity"] = sorted(
                set(item.get("capability_affinity", []))
                | {cap for cap in overrides.keys() if cap in item.get("capability_affinity", []) or cap in overrides}
            )
        experts.append(item)
    base["registry_id"] = f"{team_pack['project_id']}_project_registry"
    base["constraints"] = team_pack.get("boundaries", [])
    base["experts"] = experts
    return base


def derive_project_leader(project_id: str, project_label: str, team_pack: dict[str, Any]) -> dict[str, Any]:
    leader = default_project_leader(project_id, project_label, team_pack["pack_id"])
    overrides = team_pack.get("acceptance_overrides", {})
    if "required_checks" in overrides:
        leader["acceptance_profile"]["required_checks"] = list(overrides["required_checks"])
    if "retry_limit" in overrides:
        leader["acceptance_profile"]["retry_limit"] = overrides["retry_limit"]
    return leader
