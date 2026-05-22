#!/usr/bin/env python3
"""检查 v2.5 docs site ready 文档结构。"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "think-tank" / "docs"
REQUIRED = [
    "index.md",
    "getting-started.md",
    "first-run-guide.md",
    "operator-manual.md",
    "cookbook.md",
    "progression-guide.md",
    "faq.md",
    "troubleshooting.md",
    "quickstart-codex.md",
    "concepts/protocol-overview.md",
    "concepts/research-os.md",
    "concepts/provider-evidence.md",
    "concepts/memory-runtime.md",
    "guides/install-skill-core.md",
    "guides/use-research-os-starter.md",
    "guides/add-provider-pattern.md",
    "guides/run-release-checks.md",
    "reference/protocol.md",
    "reference/schemas.md",
    "reference/templates.md",
    "reference/checks.md",
    "release/index.md",
    "v2.1-v2.5-release-notes.md",
]
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)#][^)]+)\)")


def fail(message: str) -> None:
    raise SystemExit(f"docs site 检查失败: {message}")


def main() -> None:
    for rel in REQUIRED:
        path = DOCS / rel
        if not path.exists():
            fail(f"缺少 docs site 文件: {rel}")
    index = (DOCS / "index.md").read_text(encoding="utf-8")
    for section in ["Start Here", "Concepts", "Guides", "Reference", "Release"]:
        if section not in index:
            fail(f"index.md 缺少 section: {section}")
    missing_links: list[str] = []
    for rel in REQUIRED:
        path = DOCS / rel
        text = path.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(text):
            target = match.group(1)
            if "://" in target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                missing_links.append(f"{path.relative_to(ROOT)} -> {target}")
    if missing_links:
        fail("; ".join(missing_links[:20]))
    print("docs site 检查通过")


if __name__ == "__main__":
    main()
