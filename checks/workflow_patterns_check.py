#!/usr/bin/env python3
"""检查 v1.1 workflow pattern 示例边界。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / "think-tank" / "examples" / "workflow-patterns"
FILES = [
    WORKFLOW_DIR / "research-provider-assisted.md",
    WORKFLOW_DIR / "council-release-decision.md",
    WORKFLOW_DIR / "review-open-source-readiness.md",
]
REQUIRED_TERMS = [
    "pattern_documented",
    "selected_intent:",
    "selected_mode:",
    "selected_profiles:",
    "selected_capabilities:",
    "skill_route:",
    "execution_method:",
    "invoked_providers:",
    "not_invoked_providers:",
    "boundaries:",
    "verification_status:",
]


def fail(message: str) -> None:
    raise SystemExit(f"workflow patterns 检查失败: {message}")


def main() -> None:
    for path in FILES:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        for term in REQUIRED_TERMS:
            if term not in text:
                fail(f"{path.relative_to(ROOT)} 缺少: {term}")
        if "not an implementation" not in text and "not a claim" not in text and "not a guarantee" not in text:
            fail(f"{path.relative_to(ROOT)} 缺少非能力承诺说明")
    print("workflow patterns 检查通过")


if __name__ == "__main__":
    main()
