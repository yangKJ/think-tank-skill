#!/usr/bin/env python3
"""检查公开发布包边界和默认发行档定义是否完整。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "open-source-packages.yaml"
README = ROOT / "README.md"
OPEN_SOURCE_RELEASE = ROOT / "think-tank" / "docs" / "open-source-release.md"
SUPPORT_MATRIX = ROOT / "think-tank" / "docs" / "support-matrix.md"
GITIGNORE = ROOT / ".gitignore"


def fail(message: str) -> None:
    raise SystemExit(f"public package boundary 检查失败: {message}")


def require_text(path: Path, terms: list[str]) -> str:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for term in terms:
        if term not in text:
            fail(f"{path.relative_to(ROOT)} 缺少: {term}")
    return text


def main() -> None:
    require_text(
        MANIFEST,
        [
            "current_default_release: skill_core_only_bundle",
            "skill_core_only_bundle:",
            "checks/*.py",
            ".think-tank/**",
            ".codex/**",
            "leader-runtime-project",
        ],
    )
    require_text(
        README,
        [
            "release_posture: public_beta",
            "standalone sibling project",
            "checks/open_source_release_suite.py",
        ],
    )
    require_text(
        OPEN_SOURCE_RELEASE,
        [
            "skill_core_only_bundle",
            "current default public release is `skill_core_only_bundle`",
        ],
    )
    require_text(
        SUPPORT_MATRIX,
        [
            "current_default_release: skill_core_only_bundle",
            "leader-runtime packaging: moved to standalone sibling project",
            "skill-only packaging: current default release",
        ],
    )
    require_text(
        GITIGNORE,
        [
            "AGENTS.md",
            ".think-tank/",
            ".codex/",
            ".claude/",
            "checks/*",
            "!checks/*.py",
        ],
    )

    print("public package boundary 检查通过")


if __name__ == "__main__":
    main()
