#!/usr/bin/env python3
"""检查 v0.2 consensus contract 和 council hardening。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"


def fail(message: str) -> None:
    raise SystemExit(f"consensus contract 检查失败: {message}")


def require(path: Path, snippets: list[str]) -> None:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    content = path.read_text(encoding="utf-8")
    missing = [snippet for snippet in snippets if snippet not in content]
    if missing:
        fail(f"{path.relative_to(ROOT)} 缺少内容: {', '.join(missing)}")


def main() -> None:
    require(
        THINK_TANK / "protocol" / "consensus-contract.md",
        [
            "Position",
            "agree | disagree | abstain",
            "Blocking Objection",
            "cannot_mark_L1_consensus",
            "L1",
            "L2",
            "L3",
            "Continue / Stop Conditions",
            "why stop now",
        ],
    )
    require(
        THINK_TANK / "modes" / "council.md",
        [
            "v0.2 显式投票",
            "blocking objection",
            "不能标记 L1 共识",
            "记录少数意见",
        ],
    )
    require(
        THINK_TANK / "protocol" / "quality-gates.md",
        [
            "v0.2 共识门禁",
            "agree",
            "disagree",
            "abstain",
            "blocking objection",
            "为什么现在可以进入结论",
        ],
    )
    print("consensus contract 检查通过")


if __name__ == "__main__":
    main()
