#!/usr/bin/env python3
"""Load Codex think-tank routing policy and apply provider preferences."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml

from provider_registry import PROJECT_SKILLS, registry


ROOT = Path(__file__).resolve().parents[4]
DEFAULT_POLICY = ROOT / "think-tank" / "platforms" / "codex" / "provider-policy.example.yaml"
LOCAL_WORKSPACE_POLICY = ROOT / ".think-tank" / "provider-policy.yaml"


def load_policy(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Policy must be a mapping: {path}")
    return data


def policy_path(explicit: Path | None = None) -> Path:
    if explicit is not None:
        return explicit
    if LOCAL_WORKSPACE_POLICY.exists():
        return LOCAL_WORKSPACE_POLICY
    return DEFAULT_POLICY


def match_pattern(text: str, pattern: str, match_mode: str) -> bool:
    if match_mode == "exact":
        return text == pattern
    if match_mode == "contains":
        return pattern in text
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def match_routes(text: str, policy: dict[str, Any]) -> list[dict[str, Any]]:
    routes = policy.get("routes", [])
    matched: list[tuple[int, int, dict[str, Any]]] = []
    for index, route in enumerate(routes):
        if not route.get("enabled", True):
            continue
        triggers = route.get("triggers", {})
        patterns = triggers.get("patterns", [])
        match_mode = triggers.get("match", "regex")
        if any(match_pattern(text, str(pattern), match_mode) for pattern in patterns):
            matched.append((int(route.get("priority", 0)), -index, route))
    return [route for _, _, route in sorted(matched, reverse=True)]


def select_providers(route: dict[str, Any], available_providers: list[dict[str, Any]]) -> dict[str, Any]:
    provider_policy = route.get("providers", {}) or {}
    prefer = list(provider_policy.get("prefer", []) or [])
    allow = set(provider_policy.get("allow", []) or [])
    deny = set(provider_policy.get("deny", []) or [])
    auto_select = bool(provider_policy.get("auto_select", True))
    capabilities = set(route.get("capabilities", []) or [])

    if not auto_select:
        return {
            "candidate_providers": [],
            "selected_provider": None,
            "provider_policy": {
                "prefer": prefer,
                "allow": sorted(allow),
                "deny": sorted(deny),
                "auto_select": auto_select,
            },
            "selection_reason": "Provider auto-selection is disabled for this route.",
        }

    if not capabilities and not prefer and not allow:
        return {
            "candidate_providers": [],
            "selected_provider": None,
            "provider_policy": {
                "prefer": prefer,
                "allow": sorted(allow),
                "deny": sorted(deny),
                "auto_select": auto_select,
            },
            "selection_reason": "No capability or explicit provider preference requires provider selection.",
        }

    candidates = []
    for provider in available_providers:
        provider_id = provider.get("id", "")
        provider_capabilities = set(provider.get("capabilities", []) or [])
        if provider_id in deny:
            continue
        if allow and provider_id not in allow:
            continue
        if capabilities and not (provider_capabilities & capabilities):
            continue
        candidates.append(provider)

    def score(provider: dict[str, Any]) -> tuple[int, str]:
        provider_id = provider.get("id", "")
        if provider_id in prefer:
            return (1000 - prefer.index(provider_id), provider_id)
        if not provider.get("requires_permission", True):
            return (100, provider_id)
        return (10, provider_id)

    ranked = sorted(candidates, key=score, reverse=True)
    selected = ranked[0] if ranked else None
    return {
        "candidate_providers": [provider["id"] for provider in ranked],
        "selected_provider": selected["id"] if selected else None,
        "provider_policy": {
            "prefer": prefer,
            "allow": sorted(allow),
            "deny": sorted(deny),
            "auto_select": auto_select,
        },
        "selection_reason": (
            "Selected by routing policy preference and capability match."
            if selected
            else "No available provider matched policy and capability constraints."
        ),
    }


def resolve_request(text: str, policy: dict[str, Any], available_providers: list[dict[str, Any]]) -> dict[str, Any]:
    matches = match_routes(text, policy)
    selected_route = matches[0] if matches else None
    if not selected_route:
        return {
            "policy_status": "loaded" if policy else "missing",
            "matched": False,
            "fallback": policy.get("defaults", {}).get("fallback", "core_protocol") if policy else "core_protocol",
            "boundaries": ["No routing policy route matched the request."],
        }

    provider_selection = select_providers(selected_route, available_providers)
    return {
        "policy_status": "loaded",
        "matched": True,
        "route_id": selected_route.get("id"),
        "selected_intent": selected_route.get("intent"),
        "selected_mode": selected_route.get("mode"),
        "selected_recipe": selected_route.get("recipe"),
        "selected_profiles": selected_route.get("profiles", []),
        "selected_capabilities": selected_route.get("capabilities", []),
        "skill_route": provider_selection,
        "fallback": selected_route.get("fallback", policy.get("defaults", {}).get("fallback", "core_protocol")),
        "boundaries": [
            "Policy route selection does not invoke any provider.",
            "Selected provider must still pass dispatch-policy and result-recovery before it can be verified.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve a request through Codex think-tank provider policy.")
    parser.add_argument("request")
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--skills-dir", type=Path, default=PROJECT_SKILLS)
    args = parser.parse_args()

    selected_policy_path = policy_path(args.policy)
    policy = load_policy(selected_policy_path)
    provider_registry = registry(args.skills_dir)
    result = resolve_request(args.request, policy, provider_registry["providers"])
    result["policy_path"] = str(selected_policy_path.relative_to(ROOT)) if selected_policy_path.exists() else str(selected_policy_path)
    result["provider_count"] = provider_registry["provider_count"]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
