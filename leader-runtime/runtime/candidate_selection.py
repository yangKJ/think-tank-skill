"""按项目 policy 从 frontmatter candidates 中筛选专家候选队伍。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from agent_frontmatter import ROOT, iter_frontmatter_candidates
from leader_registry import SCHEMA_CHECKS


def load_selection_policy(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"selection policy must be a mapping: {path}")
    return data


def _resolve_source(path_value: str, policy_path: Path) -> Path:
    raw = Path(path_value)
    if raw.is_absolute():
        return raw
    policy_relative = (policy_path.parent / raw).resolve()
    if policy_relative.exists():
        return policy_relative
    return (ROOT / raw).resolve()


def load_candidates_for_policy(policy: dict[str, Any], policy_path: Path) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for source in policy.get("candidate_sources", []):
        source_path = _resolve_source(str(source), policy_path)
        candidates.extend(iter_frontmatter_candidates(source_path))
    return candidates


def _text_blob(candidate: dict[str, Any]) -> str:
    parts = [
        candidate.get("agent_id", ""),
        candidate.get("name", ""),
        candidate.get("description", ""),
        candidate.get("vibe", ""),
        candidate.get("source_domain", ""),
    ]
    return " ".join(str(part).lower() for part in parts if part)


def _matches_any_keyword(blob: str, keywords: list[str]) -> bool:
    if not keywords:
        return True
    return any(str(keyword).lower() in blob for keyword in keywords)


def _matches_tools(candidate_tools: list[str], required_tools_any: list[str]) -> bool:
    if not required_tools_any:
        return True
    normalized = {tool.lower() for tool in candidate_tools}
    return any(str(tool).lower() in normalized for tool in required_tools_any)


def _selection_reasons(candidate: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    reasons = [
        f"domain={candidate['source_domain']}",
        f"authority_scope={candidate['authority_scope_hint']}",
    ]
    if candidate.get("tools"):
        reasons.append("tools=" + ",".join(candidate["tools"]))
    keywords = [keyword for keyword in policy.get("keyword_any", []) if str(keyword).lower() in _text_blob(candidate)]
    if keywords:
        reasons.append("keyword_match=" + ",".join(str(keyword) for keyword in keywords))
    return reasons


def select_candidates(policy: dict[str, Any], candidates: list[dict[str, Any]]) -> dict[str, Any]:
    include_domains = set(policy.get("include_domains", []))
    exclude_domains = set(policy.get("exclude_domains", []))
    include_scopes = set(policy.get("include_authority_scopes", []))
    required_tools_any = list(policy.get("required_tools_any", []))
    keyword_any = list(policy.get("keyword_any", []))
    exclude_keywords = list(policy.get("exclude_keywords", []))
    max_candidates = int(policy.get("max_candidates", 10))

    selected: list[dict[str, Any]] = []
    rejected_count = 0
    seen: set[str] = set()
    for candidate in candidates:
        blob = _text_blob(candidate)
        if candidate["agent_id"] in seen:
            rejected_count += 1
            continue
        if include_domains and candidate["source_domain"] not in include_domains:
            rejected_count += 1
            continue
        if candidate["source_domain"] in exclude_domains:
            rejected_count += 1
            continue
        if include_scopes and candidate["authority_scope_hint"] not in include_scopes:
            rejected_count += 1
            continue
        if not _matches_tools(candidate.get("tools", []), required_tools_any):
            rejected_count += 1
            continue
        if not _matches_any_keyword(blob, keyword_any):
            rejected_count += 1
            continue
        if any(str(keyword).lower() in blob for keyword in exclude_keywords):
            rejected_count += 1
            continue
        selected.append(
            {
                "agent_id": candidate["agent_id"],
                "name": candidate["name"],
                "source_path": candidate["source_path"],
                "source_domain": candidate["source_domain"],
                "authority_scope_hint": candidate["authority_scope_hint"],
                "tools": list(candidate.get("tools", [])),
                "selection_reasons": _selection_reasons(candidate, policy),
                "conversion_status": "candidate",
            }
        )
        seen.add(candidate["agent_id"])
        if len(selected) >= max_candidates:
            rejected_count += max(0, len(candidates) - len(seen) - rejected_count)
            break

    return {
        "selection_id": f"{policy['project_id']}-{policy['policy_id']}",
        "policy_id": policy["policy_id"],
        "project_id": policy["project_id"],
        "selected_count": len(selected),
        "rejected_count": rejected_count,
        "selected_candidates": selected,
        "promotion_target": policy.get("promotion_target", "manual_review"),
        "review_required": True,
        "boundaries": [
            "Candidate selection does not invoke any source agent.",
            "Selected candidates are project-scoped and must be reviewed before promotion.",
            "A candidate team pack is not a global expert registry.",
        ],
    }


def build_project_team_pack_from_selection(
    policy: dict[str, Any],
    selection_result: dict[str, Any],
    base_experts: list[str] | None = None,
) -> dict[str, Any]:
    candidate_agents = [
        {
            "agent_id": item["agent_id"],
            "name": item["name"],
            "source_platform": "claude-code",
            "source_path": item["source_path"],
            "conversion_status": item["conversion_status"],
        }
        for item in selection_result.get("selected_candidates", [])
    ]
    return {
        "pack_id": f"{policy['project_id']}-candidate-pack",
        "project_id": policy["project_id"],
        "inherits_from_registry": "think_tank_codex_global_registry",
        "include_experts": base_experts or ["evidence_collector", "risk_skeptic"],
        "include_candidate_agents": candidate_agents,
        "candidate_source_policy": policy["policy_id"],
        "exclude_experts": [],
        "project_tags": [policy["project_id"], "candidate-selected"],
        "capability_overrides": {},
        "acceptance_overrides": {
            "required_checks": list(SCHEMA_CHECKS),
            "retry_limit": 2,
        },
        "boundaries": [
            "Candidate agents are project-scoped references, not global registry entries.",
            "Candidate agents require leader review before invocation or promotion.",
        ],
    }


def run_selection(policy_path: Path) -> dict[str, Any]:
    policy = load_selection_policy(policy_path)
    candidates = load_candidates_for_policy(policy, policy_path)
    selection = select_candidates(policy, candidates)
    return {
        "policy": policy,
        "selection_result": selection,
        "project_team_pack_draft": build_project_team_pack_from_selection(policy, selection),
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Select project-specific leader candidates.")
    parser.add_argument("policy", type=Path)
    args = parser.parse_args()
    result = run_selection(args.policy)
    print(yaml.safe_dump(result, allow_unicode=True, sort_keys=False))
