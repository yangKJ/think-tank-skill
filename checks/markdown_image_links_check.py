#!/usr/bin/env python3
"""检查公开 Markdown 图片链接是否指向仓库内存在的文件。"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN_FILES = [
    ROOT / "README.md",
    ROOT / "think-tank" / "README.md",
]
IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def fail(message: str) -> None:
    raise SystemExit(f"Markdown 图片链接检查失败: {message}")


def main() -> None:
    missing: list[str] = []
    for file in SCAN_FILES:
        content = file.read_text(encoding="utf-8")
        for line_number, line in enumerate(content.splitlines(), start=1):
            for match in IMAGE_PATTERN.finditer(line):
                target = match.group(1)
                if "://" in target:
                    continue
                resolved = (file.parent / target).resolve()
                if not resolved.exists():
                    missing.append(f"{file.relative_to(ROOT)}:{line_number}: {target}")
    if missing:
        fail("; ".join(missing))
    print("Markdown 图片链接检查通过")


if __name__ == "__main__":
    main()
