#!/usr/bin/env python3
"""检查 think-tank 是否安装到当前项目的 Codex skills 目录。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "think-tank"
TARGET = ROOT / ".codex" / "skills" / "think-tank"


def fail(message: str) -> None:
    raise SystemExit(f"Codex installed skill 检查失败: {message}")


def main() -> None:
    if not TARGET.exists():
        fail(f"安装目标不存在: {TARGET}")
    if not (TARGET / "SKILL.md").exists():
        fail("安装目标缺少 SKILL.md")
    if not TARGET.is_symlink():
        fail("项目内 .codex/skills/think-tank 必须是仓库内软链接，指向主仓 think-tank/")
    if TARGET.resolve() != SOURCE.resolve():
        fail(f"think-tank 软链接目标错误: {TARGET.resolve()} != {SOURCE.resolve()}")

    required = [
        TARGET / "protocol" / "subagent-runtime-contract.md",
        TARGET / "runtime" / "subagent.py",
        TARGET / "schemas" / "role-result.schema.json",
        TARGET / "platforms" / "codex" / "specialist-subagent-runtime.md",
        TARGET / "docs" / "codex-installed-skill-validation.md",
    ]
    missing = [path for path in required if not path.exists()]
    if missing:
        fail("安装目标缺少 v0.5 文件: " + ", ".join(str(path) for path in missing))

    skill = (TARGET / "SKILL.md").read_text(encoding="utf-8")
    for term in ["think-tank", "single_agent_multi_profile_fallback", "schemas/role-result.schema.json"]:
        if term not in skill:
            fail(f"SKILL.md 缺少关键入口规则: {term}")

    source_skill = (SOURCE / "SKILL.md").read_text(encoding="utf-8")
    if skill != source_skill:
        fail("项目内 .codex/skills/think-tank/SKILL.md 与主仓 think-tank/SKILL.md 不一致")

    print("Codex installed skill 软链接检查通过")


if __name__ == "__main__":
    main()
