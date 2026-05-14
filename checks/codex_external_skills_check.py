#!/usr/bin/env python3
"""检查旧 research tools 是否作为项目内 Codex 同级 skills 安装。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT_CODEX_SKILLS = ROOT / ".codex" / "skills"
FORBIDDEN_DIR_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
}

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
    if not (PROJECT_CODEX_SKILLS / "think-tank" / "SKILL.md").exists():
        fail("think-tank 未安装到项目内 Codex skills")

    for name in EXPECTED_EXTERNAL:
        target = PROJECT_CODEX_SKILLS / name
        if not target.exists():
            fail(f"缺少同级 skill: {name}")
        if not (target / "SKILL.md").exists():
            fail(f"{name} 缺少 SKILL.md")
        if target.is_symlink():
            fail(f"{name} 必须是项目内复制目录，不允许软链接")
        skill_text = (target / "SKILL.md").read_text(encoding="utf-8")
        for forbidden in ["~/.claude/skills", "/Users/condy/Desktop/img-company/agents/research"]:
            if forbidden in skill_text:
                fail(f"{name}/SKILL.md 仍依赖旧平台路径: {forbidden}")

    forbidden_dirs = [
        path
        for path in PROJECT_CODEX_SKILLS.rglob("*")
        if path.is_dir() and path.name in FORBIDDEN_DIR_NAMES
    ]
    if forbidden_dirs:
        sample = ", ".join(str(path.relative_to(ROOT)) for path in forbidden_dirs[:5])
        fail(f"项目内 skills 不应包含运行时依赖或缓存目录: {sample}")

    global_symlinks = [
        path
        for path in (Path.home() / ".codex" / "skills").glob("*")
        if path.is_symlink()
        and path.name in [*EXPECTED_EXTERNAL, "think-tank"]
    ]
    if global_symlinks:
        sample = ", ".join(path.name for path in global_symlinks)
        fail(f"仍存在旧的全局软链接安装: {sample}")

    for name in ["README.md", "think-tank.zip"]:
        if (PROJECT_CODEX_SKILLS / name).exists() or (PROJECT_CODEX_SKILLS / name).is_symlink():
            fail(f"非 skill 文件不应安装: {name}")

    for capability, skills in CAPABILITY_GROUPS.items():
        missing = [name for name in skills if not (PROJECT_CODEX_SKILLS / name / "SKILL.md").exists()]
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
