#!/usr/bin/env python3
"""检查 intent routing 和 recipes 是否保持平台无关、工具解耦。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "think-tank" / "protocol" / "intent-routing.md"
RECIPES = ROOT / "think-tank" / "recipes"
SKILL = ROOT / "think-tank" / "SKILL.md"
CODEX_ROUTING = ROOT / "think-tank" / "platforms" / "codex" / "trigger-routing.md"
POLICY_SCHEMA = ROOT / "think-tank" / "routing" / "policy-schema.md"

RECIPE_FILES = [
    "competitive-intelligence.md",
    "market-research.md",
    "technical-research.md",
    "user-feedback-analysis.md",
    "media-research.md",
    "research-to-video.md",
    "research-to-action.md",
    "decision-council.md",
    "review-acceptance.md",
    "strategy-planning.md",
    "monitoring-plan.md",
    "evidence-synthesis.md",
    "project-competitive-strategy.md",
]

REQUIRED_INTENTS = [
    "general_research",
    "deep_research",
    "competitive_intelligence",
    "market_research",
    "technical_research",
    "user_feedback_analysis",
    "media_research",
    "research_to_video",
    "research_to_action",
    "decision_council",
    "review_acceptance",
    "strategy_planning",
    "monitoring_plan",
    "synthesis",
    "project_competitive_strategy",
]


def fail(message: str) -> None:
    raise SystemExit(f"intent/recipe 检查失败: {message}")


def require_terms(content: str, terms: list[str], context: str) -> None:
    for term in terms:
        if term not in content:
            fail(f"{context} 缺少: {term}")


def main() -> None:
    if not PROTOCOL.exists():
        fail(f"缺少 intent routing 协议: {PROTOCOL}")
    if not RECIPES.exists():
        fail(f"缺少 recipes 目录: {RECIPES}")

    protocol = PROTOCOL.read_text(encoding="utf-8")
    require_terms(protocol, REQUIRED_INTENTS, "protocol/intent-routing.md")
    require_terms(
        protocol,
        [
            "think-tank core 不内置固定触发词",
            "触发词属于 routing policy",
            "routing/policy-schema.md",
            "## Intent Catalog",
        ],
        "protocol/intent-routing.md",
    )
    require_terms(
        protocol,
        [
            "optional_peer_skills_are_dependencies: false",
            "missing_peer_skill_behavior: degrade_to_core_protocol",
            "execution_claim: only_verified_per_run",
        ],
        "protocol/intent-routing.md",
    )

    for filename in RECIPE_FILES:
        path = RECIPES / filename
        if not path.exists():
            fail(f"缺少 recipe: {filename}")
        content = path.read_text(encoding="utf-8")
        require_terms(
            content,
            [
                "intent:",
                "default_mode:",
                "core_question:",
                "optional_peer_skills_are_dependencies: false",
                "profiles:",
                "capabilities:",
                "optional_peer_skills:",
                "## Output",
            ],
            filename,
        )

    readme = (RECIPES / "README.md").read_text(encoding="utf-8")
    require_terms(
        readme,
        [
            "recipes_are_protocol_assets: true",
            "recipes_are_tool_implementations: false",
            "optional_peer_skills_are_dependencies: false",
        ],
        "recipes/README.md",
    )

    skill = SKILL.read_text(encoding="utf-8")
    require_terms(skill, ["protocol/intent-routing.md", "recipes/", "routing/policy-schema.md", "optional_peer_skills_are_dependencies: false"], "SKILL.md")

    policy_schema = POLICY_SCHEMA.read_text(encoding="utf-8")
    require_terms(
        policy_schema,
        [
            "purpose: configure_triggers_intents_recipes_capabilities_and_provider_preferences",
            "user_explicit_instruction",
            "project_local_policy",
            "routes:",
            "providers:",
            "missing_policy_behavior: use_adapter_defaults_or_core_protocol",
        ],
        "routing/policy-schema.md",
    )

    codex = CODEX_ROUTING.read_text(encoding="utf-8")
    require_terms(
        codex,
        [
            "protocol/intent-routing.md",
            "provider-policy.example.yaml",
            "recipes/",
            "routing/skill-router.md",
            "routing/result-recovery.md",
            "selected_intent:",
            "selected_recipe:",
            "think_tank_core_depends_on_peer_skills: false",
        ],
        "platforms/codex/trigger-routing.md",
    )

    print("intent/recipe 检查通过")


if __name__ == "__main__":
    main()
