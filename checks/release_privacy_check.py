#!/usr/bin/env python3
"""检查公开仓库内容不包含本地私有路径或私有领域素材。"""

from __future__ import annotations

import base64
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN_ROOTS = [
    ROOT / "README.md",
    ROOT / "CHANGELOG.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "checks",
    ROOT / "think-tank",
]

FORBIDDEN_TERMS = [
    base64.b64decode(value).decode("utf-8")
    for value in [
        "L1VzZXJzLw==",
        "aW1nLWNvbXBhbnk=",
        "aW9zLWF1dG9tYXRpb24tbWNw",
        "dGhpbmstdGFuay1za2lsbC8uY29kZXg=",
        "RGVza3RvcC90aGluay10YW5rLXNraWxs",
        "QXdha2VuaW5n",
        "VlNDTw==",
        "TGlnaHRyb29t",
        "6YaS5Zu+",
        "576O5Zu+",
        "aW1hZ2UtZWRpdGluZw==",
        "5Zu+5YOP57yW6L6R",
        "UGl4ZWxjYWtl",
        "5YOP57Sg6JuL57OV",
    ]
]

SKIP_PARTS = {".git", ".codex", "__pycache__"}
SKIP_SUFFIXES = {".pyc", ".DS_Store"}


def fail(message: str) -> None:
    raise SystemExit(f"release privacy 检查失败: {message}")


def iter_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_ROOTS:
        if root.is_file():
            files.append(root)
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if any(part in SKIP_PARTS for part in path.parts):
                continue
            if path.suffix in SKIP_SUFFIXES or path.name in SKIP_SUFFIXES:
                continue
            files.append(path)
    return files


def main() -> None:
    hits: list[str] = []
    for path in iter_files():
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(content.splitlines(), start=1):
            for term in FORBIDDEN_TERMS:
                if term in line:
                    hits.append(f"{path.relative_to(ROOT)}:{line_number}: {term}")
    if hits:
        fail("; ".join(hits[:20]))
    print("release privacy 检查通过")


if __name__ == "__main__":
    main()
