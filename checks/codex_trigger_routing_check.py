#!/usr/bin/env python3
"""检查旧 research agent 触发词是否迁移到 Codex provider policy。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTING = ROOT / "think-tank" / "platforms" / "codex" / "trigger-routing.md"
POLICY = ROOT / "think-tank" / "platforms" / "codex" / "provider-policy.example.yaml"
MIGRATION = ROOT / "think-tank" / "docs" / "research-trigger-migration.md"

REQUIRED_TRIGGERS = [
    "快速了解一下",
    "研究一下",
    "深度研究",
    "竞品分析",
    "竞争分析",
    "市场调研",
    "技术调研",
    "小红书用户评价",
    "舆情分析",
    "持续监控",
    "开会讨论",
    "审查",
    "制定策略",
    "用 think-tank 生成项目记忆候选",
    "think-tank memory candidate",
]

REQUIRED_SKILLS = [
    "research-workflow",
    "omni-research",
    "web-access",
    "summarize",
    "juejin-search",
    "xiaohongshu",
    "social-media-analyzer",
    "yt-dlp",
    "openai-whisper",
    "pdf-extraction",
    "obsidian",
    "taskflow",
]

REQUIRED_BOUNDARIES = [
    "old_research_agent_shell_required: false",
    "external_peer_skills_are_optional: true",
    "think_tank_core_depends_on_peer_skills: false",
    "external_skill_execution: must_be_verified_per_run",
    "true_parallel_subagents: requires_runtime_evidence",
    "不能因为 `.codex/skills/` 里有某个 skill，就声称它已经完成真实执行",
]


def fail(message: str) -> None:
    raise SystemExit(f"Codex trigger routing 检查失败: {message}")


def main() -> None:
    if not ROUTING.exists():
        fail(f"缺少路由文档: {ROUTING}")
    if not POLICY.exists():
        fail(f"缺少 provider policy 示例: {POLICY}")
    if not MIGRATION.exists():
        fail(f"缺少迁移文档: {MIGRATION}")

    routing = ROUTING.read_text(encoding="utf-8")
    policy = POLICY.read_text(encoding="utf-8")
    migration = MIGRATION.read_text(encoding="utf-8")
    combined = policy + "\n" + migration

    for trigger in REQUIRED_TRIGGERS:
        if trigger not in combined:
            fail(f"缺少旧触发词 policy 迁移: {trigger}")

    for skill in REQUIRED_SKILLS:
        if skill not in (policy + "\n" + migration + "\n" + routing):
            fail(f"缺少组合 skill 映射或 policy 示例: {skill}")

    if "legacy_competitive_orchestrator: replaced_by_yaml_provider_policy" not in migration:
        fail("迁移文档必须声明旧竞品编排能力已被 policy route 替代")

    for boundary in REQUIRED_BOUNDARIES:
        if boundary not in routing:
            fail(f"缺少边界声明: {boundary}")

    if "router_owner: think-tank" not in routing:
        fail("trigger routing 必须声明 think-tank 是路由主语")
    if "provider-policy.example.yaml" not in routing or ".think-tank/provider-policy.yaml" not in routing:
        fail("Codex trigger routing 必须指向 provider policy YAML")
    if "protocol/intent-routing.md" not in routing or "recipes/" not in routing:
        fail("Codex trigger routing 必须引用平台无关 intent/recipe 真相源")
    for term in ["intent:", "recipe:", "providers:", "triggers:"]:
        if term not in policy:
            fail(f"provider policy 示例缺少字段: {term}")
    if "research_agent_identity: replaced_by_think_tank_research_mode" not in migration:
        fail("迁移文档必须声明旧 research agent 身份被 research mode 接管")

    print("Codex trigger routing 检查通过")


if __name__ == "__main__":
    main()
