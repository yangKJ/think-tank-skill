#!/usr/bin/env python3
"""检查公开示例是否覆盖核心宿主消费场景。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "think-tank" / "examples" / "public"

FILES_AND_TERMS = {
    PUBLIC / "research-request.md": [
        "selected_intent:",
        "selected_mode:",
        "boundaries:",
        "verification_status:",
    ],
    PUBLIC / "council-decision.md": [
        "selected_intent:",
        "selected_mode:",
        "boundaries:",
        "verification_status:",
    ],
    PUBLIC / "review-acceptance.md": [
        "selected_intent: review_acceptance",
        "selected_recipe: review-acceptance",
        "verification_status:",
    ],
    PUBLIC / "research-to-action.md": [
        "selected_intent: research_to_action",
        "selected_recipe: research-to-action",
        "observe_only",
        "verification_status:",
    ],
    PUBLIC / "strategy-backlog.md": [
        "selected_intent: strategy_planning",
        "selected_recipe: strategy-planning",
        "next_owner",
        "verification_status:",
    ],
}


def fail(message: str) -> None:
    raise SystemExit(f"public examples 检查失败: {message}")


def main() -> None:
    for path, terms in FILES_AND_TERMS.items():
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")
        content = path.read_text(encoding="utf-8")
        missing = [term for term in terms if term not in content]
        if missing:
            fail(f"{path.relative_to(ROOT)} 缺少字段: {', '.join(missing)}")

    print("public examples 检查通过")


if __name__ == "__main__":
    main()
