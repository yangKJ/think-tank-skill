#!/usr/bin/env python3
"""检查宿主增强反哺资产是否成套存在并保持关键契约。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TT = ROOT / "think-tank"

FILES_AND_TERMS = {
    TT / "docs" / "host-enhancement-backfeed.md": [
        "project_specific_facts_stay_local: true",
        "cross_project_methods_promote_to_think_tank: true",
        "研究结论转行动",
        "blocker 与 handoff 治理骨架",
        "strategy_to_backlog 的宿主消费体验",
    ],
    TT / "recipes" / "research-to-action.md": [
        "intent: research_to_action",
        "default_mode: strategy",
        "backlog 候选",
        "如果证据只够支持继续观察",
    ],
    TT / "templates" / "research-action-brief.md": [
        "建议动作",
        "暂不行动",
        "非目标",
    ],
    TT / "templates" / "blocker-handoff-brief.md": [
        "阻塞分类",
        "下一 owner",
        "升级判断",
    ],
    TT / "templates" / "strategy-backlog-brief.md": [
        "Readiness Values",
        "observe_only",
        "next_owner",
        "验证计划",
    ],
}


def fail(message: str) -> None:
    raise SystemExit(f"host enhancement backfeed 检查失败: {message}")


def main() -> None:
    for path, terms in FILES_AND_TERMS.items():
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")
        content = path.read_text(encoding="utf-8")
        missing = [term for term in terms if term not in content]
        if missing:
            fail(f"{path.relative_to(ROOT)} 缺少字段: {', '.join(missing)}")

    print("host enhancement backfeed 检查通过")


if __name__ == "__main__":
    main()
