#!/usr/bin/env python3
"""检查旧 research agent 触发词是否迁移到 Codex trigger routing。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTING = ROOT / "think-tank" / "platforms" / "codex" / "trigger-routing.md"
MIGRATION = ROOT / "think-tank" / "docs" / "research-trigger-migration.md"

REQUIRED_TRIGGERS = [
    "快速了解一下",
    "研究一下",
    "深度研究",
    "竞品分析",
    "小红书用户评价",
    "舆情分析",
    "持续监控",
    "开会讨论",
    "审查",
]

REQUIRED_SKILLS = [
    "research-workflow",
    "competitor_analysis",
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
    if not MIGRATION.exists():
        fail(f"缺少迁移文档: {MIGRATION}")

    routing = ROUTING.read_text(encoding="utf-8")
    migration = MIGRATION.read_text(encoding="utf-8")
    combined = routing + "\n" + migration

    for trigger in REQUIRED_TRIGGERS:
        if trigger not in combined:
            fail(f"缺少旧触发词迁移: {trigger}")

    for skill in REQUIRED_SKILLS:
        if skill not in combined:
            fail(f"缺少组合 skill 映射: {skill}")

    for boundary in REQUIRED_BOUNDARIES:
        if boundary not in routing:
            fail(f"缺少边界声明: {boundary}")

    if "router_owner: think-tank" not in routing:
        fail("trigger routing 必须声明 think-tank 是路由主语")
    if "research_agent_identity: replaced_by_think_tank_research_mode" not in migration:
        fail("迁移文档必须声明旧 research agent 身份被 research mode 接管")

    print("Codex trigger routing 检查通过")


if __name__ == "__main__":
    main()
