"""Codex leader runtime 的专家注册表和派遣辅助函数。"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

LEADER_ID = "think_tank_global_leader"
RUNTIME_ROOT = Path(__file__).resolve().parents[1]
GLOBAL_REGISTRY_PATH = RUNTIME_ROOT / "registries" / "global-experts.yaml"
SCHEMA_CHECKS = [
    "schema_complete",
    "evidence_present",
    "boundary_declared",
    "claim_traceable",
    "no_over_authority",
]


@dataclass(frozen=True)
class ExpertEntry:
    expert_id: str
    label: str
    owner_layer: str
    mapped_roles: list[str]
    specialties: list[str]
    supported_modes: list[str]
    preferred_intents: list[str]
    capability_affinity: list[str]
    dispatch_style: str
    authority_scope: str
    availability_status: str
    project_tags: list[str] = field(default_factory=list)
    boundaries: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_registry_source(path: Path = GLOBAL_REGISTRY_PATH) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"registry must be a mapping: {path}")
    return data


def _expert_from_dict(data: dict[str, Any]) -> ExpertEntry:
    return ExpertEntry(
        expert_id=data["expert_id"],
        label=data["label"],
        owner_layer=data["owner_layer"],
        mapped_roles=list(data.get("mapped_roles", [])),
        specialties=list(data.get("specialties", [])),
        supported_modes=list(data.get("supported_modes", [])),
        preferred_intents=list(data.get("preferred_intents", [])),
        capability_affinity=list(data.get("capability_affinity", [])),
        dispatch_style=data["dispatch_style"],
        authority_scope=data["authority_scope"],
        availability_status=data["availability_status"],
        project_tags=list(data.get("project_tags", [])),
        boundaries=list(data.get("boundaries", [])),
    )


def load_expert_pool(path: Path = GLOBAL_REGISTRY_PATH) -> list[ExpertEntry]:
    registry = load_registry_source(path)
    experts = registry.get("experts", [])
    if not isinstance(experts, list) or not experts:
        raise ValueError(f"registry must contain a non-empty experts list: {path}")
    return [_expert_from_dict(item) for item in experts]


GLOBAL_REGISTRY_SOURCE = load_registry_source()
GLOBAL_EXPERT_POOL = load_expert_pool()


def registry_payload(scope: str = "global", inherits_from: str | None = None) -> dict[str, Any]:
    return {
        "registry_id": GLOBAL_REGISTRY_SOURCE["registry_id"] if scope == "global" else "project_registry",
        "owner": LEADER_ID,
        "scope": scope,
        "inherits_from": inherits_from,
        "constraints": list(GLOBAL_REGISTRY_SOURCE.get("constraints", [])),
        "experts": [entry.to_dict() for entry in GLOBAL_EXPERT_POOL],
    }


def summarize_registry(mode: str, intent: str | None, capabilities: list[str]) -> dict[str, Any]:
    candidates = []
    for entry in GLOBAL_EXPERT_POOL:
        if mode not in entry.supported_modes:
            continue
        if intent and entry.preferred_intents and intent not in entry.preferred_intents:
            if not any(cap in entry.capability_affinity for cap in capabilities):
                continue
        candidates.append(entry)
    selected = candidates or GLOBAL_EXPERT_POOL
    return {
        "registry_id": GLOBAL_REGISTRY_SOURCE["registry_id"],
        "leader_id": LEADER_ID,
        "scope": "global",
        "candidate_count": len(selected),
        "candidate_experts": [entry.expert_id for entry in selected],
        "role_coverage": sorted({role for entry in selected for role in entry.mapped_roles}),
        "availability_summary": {
            "verified_partial": sum(1 for entry in selected if entry.availability_status == "verified_partial"),
            "specified": sum(1 for entry in selected if entry.availability_status == "specified"),
            "planned": sum(1 for entry in selected if entry.availability_status == "planned"),
            "verified": sum(1 for entry in selected if entry.availability_status == "verified"),
        },
    }


def _task_shape_from_route(mode: str, capabilities: list[str], request: str) -> str:
    lowered = request.lower()
    if mode == "strategy":
        return "multi_domain"
    if mode == "review":
        return "adversarial"
    if "research_to_video" in lowered or "视频" in request:
        return "execution_heavy"
    if len(capabilities) >= 2:
        return "multi_domain"
    if len(request) <= 24:
        return "focused"
    return "simple"


def _selected_profiles(mode: str, task_shape: str) -> list[str]:
    profiles = {
        "research": ["source-collector", "trend-analyst", "skeptic"],
        "council": ["product-strategist", "skeptic", "facilitator"],
        "review": ["source-collector", "skeptic", "report-architect"],
        "strategy": ["product-strategist", "skeptic", "report-architect"],
    }.get(mode, ["facilitator", "skeptic"])
    if task_shape == "execution_heavy" and "report-architect" not in profiles:
        profiles.append("report-architect")
    return profiles


def _selected_experts(mode: str, capabilities: list[str], task_shape: str) -> list[ExpertEntry]:
    role_need = ["collector", "skeptic", "synthesizer"]
    if mode in {"council", "strategy"}:
        role_need.insert(1, "domain_expert")
        role_need.append("builder")
    if task_shape == "execution_heavy" and "builder" not in role_need:
        role_need.append("builder")
    chosen: list[ExpertEntry] = []
    for role in role_need:
        match = next((entry for entry in GLOBAL_EXPERT_POOL if role in entry.mapped_roles and mode in entry.supported_modes), None)
        if match and match not in chosen:
            chosen.append(match)
    if any(cap in {"social-listening", "media-production"} for cap in capabilities):
        strategy = next((entry for entry in GLOBAL_EXPERT_POOL if entry.expert_id == "strategy_lead"), None)
        if strategy and strategy not in chosen:
            chosen.append(strategy)
    return chosen


def build_dispatch_decision(
    request: str,
    mode: str,
    intent: str | None,
    capabilities: list[str],
    platform_supports_subagents: bool,
) -> dict[str, Any]:
    task_shape = _task_shape_from_route(mode, capabilities, request)
    experts = _selected_experts(mode, capabilities, task_shape)
    selected_profiles = _selected_profiles(mode, task_shape)
    if task_shape == "simple":
        selected_path = "leader_direct"
        delegation_needed = False
    elif platform_supports_subagents and task_shape in {"multi_domain", "adversarial", "execution_heavy"}:
        selected_path = "expert_dispatch"
        delegation_needed = True
    elif task_shape in {"multi_domain", "adversarial", "execution_heavy"}:
        selected_path = "single_agent_multi_profile_fallback"
        delegation_needed = True
    else:
        selected_path = "structured_council"
        delegation_needed = True
    return {
        "leader_id": LEADER_ID,
        "task_shape": task_shape,
        "delegation_needed": delegation_needed,
        "reason": (
            "Codex leader should organize multiple expert views for non-trivial task shapes."
            if delegation_needed
            else "Task is simple enough for direct leader execution."
        ),
        "selected_path": selected_path,
        "fallback_path": "single_agent_multi_profile_fallback" if delegation_needed else "leader_direct",
        "verification_status": "verified_partial" if platform_supports_subagents else "specified",
        "selected_experts": [entry.expert_id for entry in experts],
        "candidate_experts": summarize_registry(mode, intent, capabilities)["candidate_experts"],
        "selected_profiles": selected_profiles,
        "required_capabilities": capabilities,
        "boundaries": [
            "Dispatch decision does not prove expert invocation by itself.",
            "Selected experts remain under leader acceptance governance.",
        ],
    }


def _mapped_role(entry: ExpertEntry) -> str:
    return entry.mapped_roles[0] if entry.mapped_roles else "domain_expert"


def build_expert_task_packets(
    request: str,
    mode: str,
    capabilities: list[str],
    selected_experts: list[str],
) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    for index, expert_id in enumerate(selected_experts, start=1):
        entry = next((item for item in GLOBAL_EXPERT_POOL if item.expert_id == expert_id), None)
        if entry is None:
            continue
        packets.append(
            {
                "task_id": f"{mode}-expert-{index}",
                "leader_id": LEADER_ID,
                "expert_id": entry.expert_id,
                "mapped_role": _mapped_role(entry),
                "objective": request,
                "task_scope": f"Handle the {entry.label.lower()} slice of the request.",
                "required_capabilities": [cap for cap in capabilities if cap in entry.capability_affinity] or capabilities[:1],
                "input_context": [f"mode={mode}", f"request={request}"],
                "deliverables": [
                    "claim",
                    "evidence",
                    "risks",
                    "recommendations",
                    "boundaries",
                ],
                "acceptance_checks": list(SCHEMA_CHECKS),
                "independence_boundary": "Use an isolated expert context when Codex runtime supports it.",
                "fallback_rule": "Downgrade to single_agent_multi_profile_fallback when no verified independent expert runtime is available.",
            }
        )
    return packets


def build_acceptance_report(
    checked_results: list[str],
    passed_checks: list[str],
    failed_checks: list[str],
    delegation_needed: bool,
) -> dict[str, Any]:
    if failed_checks:
        status = "failed"
        next_action = "retry" if delegation_needed else "manual_arbitration"
    elif checked_results:
        status = "passed"
        next_action = "accept"
    else:
        status = "pending"
        next_action = "downgrade" if delegation_needed else "accept"
    return {
        "acceptance_id": "leader-acceptance-001",
        "leader_id": LEADER_ID,
        "status": status,
        "retry_count": 0,
        "checked_results": checked_results,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "next_action": next_action,
        "notes": [
            "Leader acceptance is schema-first in the current Codex implementation.",
        ],
        "boundaries": [
            "Acceptance report does not imply true expert independence unless runtime evidence exists.",
        ],
    }
