#!/usr/bin/env python3
"""检查 v1.1 规划范围是否完整落地。"""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DOCS = [
    ROOT / "think-tank" / "docs" / "provider-integration-patterns.md",
    ROOT / "think-tank" / "docs" / "codex-installation.md",
    ROOT / "think-tank" / "docs" / "v1.1-roadmap.md",
    ROOT / "think-tank" / "docs" / "v1.1-release-notes.md",
    ROOT / "think-tank" / "assets" / "README.md",
    ROOT / "think-tank" / "assets" / "brand" / "README.md",
    ROOT / "think-tank" / "assets" / "prompts" / "README.md",
]
SUBCHECKS = [
    ["python3", "checks/provider_integration_patterns_check.py"],
    ["python3", "checks/workflow_patterns_check.py"],
    ["python3", "checks/readme_language_sync_check.py"],
    ["python3", "checks/visual_assets_check.py"],
    ["python3", "checks/markdown_image_links_check.py"],
]


def fail(message: str) -> None:
    raise SystemExit(f"v1.1 release 检查失败: {message}")


def require_text(path: Path, terms: list[str]) -> None:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for term in terms:
        if term not in text:
            fail(f"{path.relative_to(ROOT)} 缺少: {term}")


def main() -> None:
    for path in REQUIRED_DOCS:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")

    require_text(
        ROOT / "README.md",
        [
            "Provider Integration Patterns",
            "Codex Installation",
            "v1.1 Roadmap",
            "v1.1 Release Notes",
        ],
    )
    require_text(
        ROOT / "README_CN.md",
        [
            "Provider 接入模式",
            "Codex 安装",
            "v1.1 路线图",
            "v1.1 发布说明",
        ],
    )
    require_text(
        ROOT / "think-tank" / "README.md",
        [
            "docs/provider-integration-patterns.md",
            "docs/codex-installation.md",
            "docs/v1.1-roadmap.md",
        ],
    )

    for command in SUBCHECKS:
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        if completed.returncode != 0:
            detail = completed.stdout.strip() or completed.stderr.strip() or f"exit={completed.returncode}"
            fail(f"{' '.join(command)} -> {detail}")

    print("v1.1 release 检查通过")


if __name__ == "__main__":
    main()
