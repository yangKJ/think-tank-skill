#!/usr/bin/env python3
"""检查 state/result model 最小实现。"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "think-tank" / "runtime"
sys.path.insert(0, str(RUNTIME_DIR))

from state_model import RecoveryResult, StageResult, make_run, validate_run_id  # noqa: E402


def fail(message: str) -> None:
    raise SystemExit(f"state model 检查失败: {message}")


def main() -> None:
    run = make_run("research", ["source-collector"], ["source-acquisition"], ["collection"])
    data = run.to_dict()
    if data["mode"] != "research":
        fail("run.mode 必须保留")
    if data["status"] != "pending":
        fail("初始 status 应为 pending")
    if data["pending_stages"] != ["collection"]:
        fail("pending stages 未保留")
    try:
        validate_run_id("../bad")
    except ValueError:
        pass
    else:
        fail("run_id 必须拒绝路径穿越")
    result = StageResult(actor="source-collector", stage="collection", claim="found source", evidence=["e1"])
    if result.to_dict()["confidence"] != "medium":
        fail("StageResult 默认 confidence 应为 medium")
    recovery = RecoveryResult(True, ["sources[]"], "structured_manual", "partial recovery")
    if recovery.to_dict()["recovery_method"] != "structured_manual":
        fail("RecoveryResult 应支持 structured_manual")
    print("state model 检查通过")


if __name__ == "__main__":
    main()
