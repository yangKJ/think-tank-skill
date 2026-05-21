#!/usr/bin/env python3
"""检查 consensus evaluator 最小实现。"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "think-tank" / "runtime"
sys.path.insert(0, str(RUNTIME_DIR))

from consensus import Position, evaluate_consensus  # noqa: E402


def fail(message: str) -> None:
    raise SystemExit(f"consensus runtime 检查失败: {message}")


def main() -> None:
    l1 = evaluate_consensus(
        [
            Position(profile="a", proposal="ship", vote="agree"),
            Position(profile="b", proposal="ship", vote="agree"),
            Position(profile="c", proposal="ship", vote="abstain"),
        ],
        threshold=0.66,
    )
    if l1.level != "L1" or l1.should_continue:
        fail("达到阈值且无 blocking objection 时应为 L1")
    l2 = evaluate_consensus(
        [
            Position(profile="a", proposal="ship", vote="agree"),
            Position(profile="skeptic", proposal="wait", objections=["evidence gap"], vote="disagree"),
        ],
        current_round=1,
        max_rounds=3,
    )
    if l2.level != "L2" or not l2.should_continue:
        fail("存在 blocking objection 且未达 max_rounds 时应继续 L2")
    if not l2.blocking_objections:
        fail("blocking objection 必须被记录")
    l3 = evaluate_consensus(
        [
            Position(profile="a", proposal="ship", vote="agree"),
            Position(profile="skeptic", proposal="wait", objections=["evidence gap"], vote="disagree"),
        ],
        current_round=3,
        max_rounds=3,
    )
    if l3.level != "L3" or l3.should_continue:
        fail("达到 max_rounds 时应进入 L3")
    print("consensus runtime 检查通过")


if __name__ == "__main__":
    main()
