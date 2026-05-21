#!/usr/bin/env python3
"""检查旧 research agent 全仓迁移处置是否完整。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"

DOCS = [
    THINK_TANK / "docs" / "v0.3-research-agent-migration.md",
    THINK_TANK / "docs" / "research-agent-full-inventory.md",
    THINK_TANK / "docs" / "external-skill-interoperability.md",
    THINK_TANK / "templates" / "monitoring-brief.md",
    THINK_TANK / "templates" / "evidence-table.md",
]

OLD_AGENTS = [
    "Research Sub Researcher",
    "Research Sub Trend Researcher",
    "Research Sub Xiaohongshu Researcher",
    "Research Sub Feedback Synthesizer",
    "Research Sub Research Report Architect",
    "Research Sub Product Manager",
    "Critic",
]

OLD_SKILLS = [
    "36kr-hotlist",
    "apple-reminders",
    "google-ai-mode-skill",
    "juejin-search",
    "knowledge-graph-builder",
    "mcp-cli",
    "notebooklm",
    "obsidian",
    "omni-research",
    "openai-whisper",
    "pdf-extraction",
    "playwright-cli",
    "research-workflow",
    "social-media-analyzer",
    "stable-diffusion-image-generation",
    "summarize",
    "taskflow",
    "think-tank",
    "using-tmux-for-interactive-commands",
    "vision-analysis",
    "web-access",
    "xiaohongshu",
    "xiaoyuzhou-transcribe",
    "yt-dlp",
]

def fail(message: str) -> None:
    raise SystemExit(f"research agent 全量迁移检查失败: {message}")


def main() -> None:
    missing = [path for path in DOCS if not path.exists()]
    if missing:
        fail("缺少文件: " + ", ".join(str(path.relative_to(ROOT)) for path in missing))

    inventory = (THINK_TANK / "docs" / "research-agent-full-inventory.md").read_text(encoding="utf-8")
    interop = (THINK_TANK / "docs" / "external-skill-interoperability.md").read_text(encoding="utf-8")
    v03 = (THINK_TANK / "docs" / "v0.3-research-agent-migration.md").read_text(encoding="utf-8")

    for agent in OLD_AGENTS:
        if agent not in inventory:
            fail(f"旧 agent 未处置: {agent}")

    combined_skill_docs = inventory + "\n" + interop
    for skill in OLD_SKILLS:
        if skill not in combined_skill_docs:
            fail(f"旧 skill 未处置: {skill}")

    required_status = [
        "research_agent_migration: complete",
        "legacy_assets_without_disposition: 0",
        "external_skills_required_for_core: false",
        "private_domain_knowledge_in_core: false",
        "agents_disposed: 7",
        "skills_disposed: 24",
    ]
    combined = inventory + "\n" + interop + "\n" + v03
    for term in required_status:
        if term not in combined:
            fail(f"缺少完成状态: {term}")

    print("research agent 全量迁移检查通过")


if __name__ == "__main__":
    main()
