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
    THINK_TANK / "domain-packs" / "image-editing" / "legacy-knowledge-index.md",
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
    "competitor_analysis",
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

OLD_KNOWLEDGE_FILES = [
    "AI消除功能技术方案-20260511.md",
    "Final_Skills_Report.md",
    "agency-analysis-report.md",
    "ai_image_restoration_research.md",
    "ai_models_for_image_editing_latest.md",
    "awakening/Awakening项目全景综合报告.md",
    "awakening/Awakening项目完整概览.md",
    "awakening/README.md",
    "awakening/UI组件与交互深度报告.md",
    "awakening/前端面板架构深度报告.md",
    "awakening/多图编辑与导出系统深度报告.md",
    "awakening/技术架构深度报告.md",
    "awakening/数据模型深度报告.md",
    "awakening/未来功能扩张路线图.md",
    "awakening/测试安全与增长报告.md",
    "awakening/竞品宣传策略调研报告.md",
    "awakening/运维发布流程分析.md",
    "awakening/配置与扩展模块深度报告.md",
    "awakening_missing_ai_models.md",
    "competitor_analysis_method.md",
    "ios_automation_research_report_2026-05-04.md",
    "ios_automation_xcodebuildmcp_integration.md",
    "ios_memory_optimization_report.md",
    "ios_real_device_automation_technical_report.md",
    "metal3_mesh_shader_research.md",
    "metal_gpu_performance_resources.md",
    "permissive_license_image_enhancement.md",
    "research_tools.md",
    "tools_guide_summary.md",
    "ui_design_learning_resources.md",
    "xcodebuildmcp-ui-automation.md",
    "xingtu_pixelcake_ai_comparison.md",
    "xor_mask_blending_resources.md",
    "xor_mask_technology_research.md",
    "zero_dce_ios_feasibility_report.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"research agent 全量迁移检查失败: {message}")


def main() -> None:
    missing = [path for path in DOCS if not path.exists()]
    if missing:
        fail("缺少文件: " + ", ".join(str(path.relative_to(ROOT)) for path in missing))

    inventory = (THINK_TANK / "docs" / "research-agent-full-inventory.md").read_text(encoding="utf-8")
    interop = (THINK_TANK / "docs" / "external-skill-interoperability.md").read_text(encoding="utf-8")
    knowledge = (THINK_TANK / "domain-packs" / "image-editing" / "legacy-knowledge-index.md").read_text(encoding="utf-8")
    v03 = (THINK_TANK / "docs" / "v0.3-research-agent-migration.md").read_text(encoding="utf-8")

    for agent in OLD_AGENTS:
        if agent not in inventory:
            fail(f"旧 agent 未处置: {agent}")

    combined_skill_docs = inventory + "\n" + interop
    for skill in OLD_SKILLS:
        if skill not in combined_skill_docs:
            fail(f"旧 skill 未处置: {skill}")

    for filename in OLD_KNOWLEDGE_FILES:
        if filename not in knowledge:
            fail(f"旧 knowledge 文件未索引: {filename}")

    required_status = [
        "research_agent_migration: complete",
        "legacy_assets_without_disposition: 0",
        "external_skills_required_for_core: false",
        "knowledge_files: 35",
        "agents_disposed: 7",
        "skills_disposed: 25",
    ]
    combined = inventory + "\n" + interop + "\n" + knowledge + "\n" + v03
    for term in required_status:
        if term not in combined:
            fail(f"缺少完成状态: {term}")

    print("research agent 全量迁移检查通过")


if __name__ == "__main__":
    main()

