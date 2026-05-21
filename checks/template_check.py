#!/usr/bin/env python3
"""检查迁移模板是否符合当前 think-tank 输出契约。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "think-tank" / "templates"

REQUIRED_FILES = [
    TEMPLATES / "README.md",
    TEMPLATES / "deep-research.md",
    TEMPLATES / "expert-meeting.md",
    TEMPLATES / "task-kickoff.md",
    TEMPLATES / "monitoring-brief.md",
    TEMPLATES / "evidence-table.md",
    TEMPLATES / "council-state.md",
]

REQUIRED_TERMS = [
    "mode",
    "profiles",
    "capabilities",
    "Risks",
    "Boundaries",
    "Quality Check",
]


def fail(message: str) -> None:
    raise SystemExit(f"template 检查失败: {message}")


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not path.exists()]
    if missing:
        fail("缺少模板文件: " + ", ".join(str(path.relative_to(ROOT)) for path in missing))

    for path in REQUIRED_FILES:
        if path.name == "README.md":
            continue
        content = path.read_text(encoding="utf-8")
        missing_terms = [term for term in REQUIRED_TERMS if term not in content]
        if missing_terms:
            fail(f"{path.relative_to(ROOT)} 缺少字段: {', '.join(missing_terms)}")
        forbidden_terms = ["sub-researcher", "Think Tank v2.0 生成", ".think-tank/conclusions"]
        leaked = [term for term in forbidden_terms if term in content]
        if leaked:
            fail(f"{path.relative_to(ROOT)} 泄漏旧平台模板字段: {', '.join(leaked)}")

    print("template 检查通过")


if __name__ == "__main__":
    main()
