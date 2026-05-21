#!/usr/bin/env python3
"""检查 v2.3 eval pack starter。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "think-tank" / "evals"
CASES = [
    "research-output-shape.json",
    "provider-selected-not-invoked.json",
    "memory-promotion-decision.json",
    "handoff-guardrail.json",
    "open-source-readiness-review.json",
]
REQUIRED_KEYS = ["eval_id", "case_type", "fixture", "expected_contracts", "actual_contracts", "passed", "failures", "residual_risk"]


def fail(message: str) -> None:
    raise SystemExit(f"eval pack 检查失败: {message}")


def main() -> None:
    if not (BASE / "README.md").exists():
        fail("缺少 evals/README.md")
    for name in CASES:
        path = BASE / "cases" / name
        if not path.exists():
            fail(f"缺少 eval case: {name}")
        data = json.loads(path.read_text(encoding="utf-8"))
        for key in REQUIRED_KEYS:
            if key not in data:
                fail(f"{name} 缺少字段: {key}")
        fixture = ROOT / data["fixture"]
        if not fixture.exists():
            fail(f"{name} 指向不存在 fixture: {data['fixture']}")
        if data["passed"] is not True:
            fail(f"{name} passed 必须为 true")
    expected = BASE / "expected" / "eval-contracts.md"
    if not expected.exists():
        fail("缺少 expected/eval-contracts.md")
    print("eval pack 检查通过")


if __name__ == "__main__":
    main()
