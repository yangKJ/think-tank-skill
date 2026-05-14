#!/usr/bin/env python3
"""检查旧 research tools 是否作为 Codex 同级 skills 安装。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEX_SKILLS = Path.home() / ".codex" / "skills"
OLD_SKILLS = Path("/Users/condy/Desktop/img-company/agents/research/.claude/skills")

EXPECTED_EXTERNAL = [
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
    "using-tmux-for-interactive-commands",
    "vision-analysis",
    "web-access",
    "xiaohongshu",
    "xiaoyuzhou-transcribe",
    "yt-dlp",
]

CAPABILITY_GROUPS = {
    "source-acquisition": ["web-access", "google-ai-mode-skill", "juejin-search", "36kr-hotlist", "pdf-extraction", "mcp-cli", "summarize"],
    "browser-automation": ["web-access", "playwright-cli"],
    "social-listening": ["xiaohongshu", "social-media-analyzer"],
    "media-processing": ["yt-dlp", "openai-whisper", "xiaoyuzhou-transcribe", "summarize", "vision-analysis"],
    "knowledge-persistence": ["obsidian", "notebooklm", "knowledge-graph-builder", "taskflow"],
}


def fail(message: str) -> None:
    raise SystemExit(f"Codex external skills 检查失败: {message}")


def main() -> None:
    if not (CODEX_SKILLS / "think-tank" / "SKILL.md").exists():
        fail("think-tank 未安装到 Codex skills")

    for name in EXPECTED_EXTERNAL:
        target = CODEX_SKILLS / name
        source = OLD_SKILLS / name
        if not target.exists():
            fail(f"缺少同级 skill: {name}")
        if not (target / "SKILL.md").exists():
            fail(f"{name} 缺少 SKILL.md")
        if target.resolve() != source.resolve():
            fail(f"{name} 未链接到旧 research skill 来源: {target.resolve()} != {source.resolve()}")

    for name in ["README.md", "think-tank.zip"]:
        if (CODEX_SKILLS / name).exists() or (CODEX_SKILLS / name).is_symlink():
            fail(f"非 skill 文件不应安装: {name}")

    for capability, skills in CAPABILITY_GROUPS.items():
        missing = [name for name in skills if not (CODEX_SKILLS / name / "SKILL.md").exists()]
        if missing:
            fail(f"{capability} 缺少候选 skills: {', '.join(missing)}")

    doc = ROOT / "think-tank" / "docs" / "codex-external-skills-installation.md"
    content = doc.read_text(encoding="utf-8")
    for term in ["external_skills_installed: verified", "external_skills_executable: not_verified", "old_research_agent_shell_required: false"]:
        if term not in content:
            fail(f"安装文档缺少边界声明: {term}")

    print("Codex external skills 检查通过")


if __name__ == "__main__":
    main()
