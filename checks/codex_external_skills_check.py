#!/usr/bin/env python3
"""检查项目内可选 Codex peer skills 是否保持解耦和干净。"""

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


def _installed_skill_roots() -> set[str]:
    """返回当前项目已存在的可安装 peer skill 根目录名（包含 think-tank）。"""
    roots = set(OPTIONAL_PEER_SKILLS)
    roots.add("think-tank")
    return roots


def _is_allowed_cache_dir(path: Path, installed_skill_roots: set[str]) -> bool:
    """允许在已安装 skill 根目录内部保留运行时缓存目录。

    这些目录常见于本地环境（例如 .venv、node_modules、__pycache__），
    不应阻断验证，只要它们不是直接位于 .codex/skills 根目录。
    """
    if not path.is_dir() or path.name not in FORBIDDEN_DIR_NAMES:
        return False

    rel_parts = path.relative_to(PROJECT_CODEX_SKILLS).parts
    return len(rel_parts) >= 2 and rel_parts[0] in installed_skill_roots

OPTIONAL_PEER_SKILLS = [
    "36kr-hotlist",
    "apple-reminders",
    "google-ai-mode-skill",
    "juejin-search",
    "knowledge-graph-builder",
    "mcp-cli",
    "notebooklm",
    "obsidian",
    "omni-research",
    "ollama-local-inference",
    "openai-whisper",
    "pdf-extraction",
    "playwright-cli",
    "research-workflow",
    "revieworg-audit-provider",
    "social-media-analyzer",
    "stable-diffusion-image-generation",
    "summarize",
    "taskflow",
    "using-tmux-for-interactive-commands",
    "vision-analysis",
    "web-access",
    "agent-reach",
    "xiaohongshu",
    "xiaoyuzhou-transcribe",
    "yt-dlp",
]

CAPABILITY_GROUPS = {
    "source-acquisition": ["agent-reach", "web-access", "google-ai-mode-skill", "juejin-search", "36kr-hotlist", "pdf-extraction", "mcp-cli", "summarize"],
    "browser-automation": ["web-access", "playwright-cli"],
    "social-listening": ["xiaohongshu", "social-media-analyzer"],
    "media-processing": ["yt-dlp", "openai-whisper", "xiaoyuzhou-transcribe", "summarize", "vision-analysis"],
    "knowledge-persistence": ["obsidian", "notebooklm", "knowledge-graph-builder", "taskflow"],
    "local-model-inference": ["ollama-local-inference"],
    "audit-governance": ["revieworg-audit-provider"],
}


def fail(message: str) -> None:
    raise SystemExit(f"Codex external skills 检查失败: {message}")


def main() -> None:
    if not PROJECT_CODEX_SKILLS.exists():
        print("Codex optional peer skills 检查跳过: .codex/ 是本地运行目录，未纳入 Git")
        return
    if not (PROJECT_CODEX_SKILLS / "think-tank" / "SKILL.md").exists():
        fail("think-tank 未安装到项目内 Codex skills")

    present_peer_skills: list[str] = []
    installed_skill_roots = _installed_skill_roots()
    private_home = str(Path.home())
    for name in OPTIONAL_PEER_SKILLS:
        target = PROJECT_CODEX_SKILLS / name
        if not target.exists():
            continue
        present_peer_skills.append(name)
        if not (target / "SKILL.md").exists():
            fail(f"{name} 缺少 SKILL.md")
        if target.is_symlink():
            fail(f"{name} 必须是项目内复制目录，不允许软链接")
        skill_text = (target / "SKILL.md").read_text(encoding="utf-8")
        for forbidden in ["~/.claude/skills", private_home, "legacy research workspace"]:
            if forbidden in skill_text:
                fail(f"{name}/SKILL.md 仍依赖旧平台路径: {forbidden}")

    forbidden_dirs = [
        path
        for path in PROJECT_CODEX_SKILLS.rglob("*")
        if path.is_dir()
        and path.name in FORBIDDEN_DIR_NAMES
        and not _is_allowed_cache_dir(path, installed_skill_roots)
    ]
    if forbidden_dirs:
        sample = ", ".join(str(path.relative_to(ROOT)) for path in forbidden_dirs[:5])
        fail(f"项目内 skills 不应包含运行时依赖或缓存目录: {sample}")

    global_symlinks = [
        path
        for path in (Path.home() / ".codex" / "skills").glob("*")
        if path.is_symlink()
        and path.name in [*OPTIONAL_PEER_SKILLS, "think-tank"]
    ]
    if global_symlinks:
        sample = ", ".join(path.name for path in global_symlinks)
        fail(f"仍存在旧的全局软链接安装: {sample}")

    for name in ["README.md", "think-tank.zip"]:
        if (PROJECT_CODEX_SKILLS / name).exists() or (PROJECT_CODEX_SKILLS / name).is_symlink():
            fail(f"非 skill 文件不应安装: {name}")

    for capability, skills in CAPABILITY_GROUPS.items():
        available = [name for name in skills if (PROJECT_CODEX_SKILLS / name / "SKILL.md").exists()]
        if not available:
            continue

    doc = ROOT / "think-tank" / "docs" / "codex-external-skills-installation.md"
    content = doc.read_text(encoding="utf-8")
    for term in [
        "external_peer_skills_are_optional: true",
        "external_skills_executable: not_verified",
        "old_research_agent_shell_required: false",
        "think_tank_core_depends_on_peer_skills: false",
    ]:
        if term not in content:
            fail(f"安装文档缺少边界声明: {term}")

    print(f"Codex optional peer skills 检查通过: present={len(present_peer_skills)}")


if __name__ == "__main__":
    main()
