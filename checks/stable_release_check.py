#!/usr/bin/env python3
"""检查 stable release 是否已经达到可声明标准。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CRITERIA = ROOT / "think-tank" / "docs" / "stable-release-criteria.md"
MATRIX = ROOT / "think-tank" / "docs" / "stable-readiness-matrix.md"
CHECKLIST = ROOT / "think-tank" / "docs" / "stable-release-checklist.md"
READINESS = ROOT / "think-tank" / "examples" / "stable-release-readiness.yaml"
OPEN_SOURCE_RELEASE = ROOT / "think-tank" / "docs" / "open-source-release.md"


def fail(message: str) -> None:
    raise SystemExit(f"stable release 检查失败: {message}")


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
        CRITERIA,
        [
            "stable_release_requirements",
            "min_verified_or_verified_partial_invoked_providers: 3",
            "external_browser_readonly: verified_partial_or_verified",
            "long_running_lifecycle: not_not_verified",
        ],
    )
    require_text(
        MATRIX,
        [
            "stable_release_ready: true",
            "| provider invocation evidence |",
            "| browser external readonly |",
            "| multi-agent beyond readonly council |",
        ],
    )
    require_text(
        CHECKLIST,
        [
            "python3 checks/open_source_release_suite.py",
            "python3 checks/stable_release_check.py",
            "三条 optional provider invocation 样例存在且带 `dispatch_decision`",
        ],
    )
    readiness = require_text(
        READINESS,
        [
            "stable_release_ready: true",
            "current_public_proofs: 4",
            "browser_external_readonly:",
            "multi_agent_beyond_readonly_council:",
            "long_running_subagent_lifecycle:",
        ],
    )
    require_text(
        OPEN_SOURCE_RELEASE,
        [
            "safe_to_market_as_stable_product: true",
            "stable_release",
        ],
    )

    print("stable release 检查通过")


if __name__ == "__main__":
    main()
