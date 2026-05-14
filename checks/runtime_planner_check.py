#!/usr/bin/env python3
"""检查 runtime planner 最小实现。"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "think-tank" / "runtime"
sys.path.insert(0, str(RUNTIME_DIR))

from planner import plan_runtime, resolve_mode  # noqa: E402


def fail(message: str) -> None:
    raise SystemExit(f"runtime planner 检查失败: {message}")


def main() -> None:
    plan = plan_runtime("深度调研跨平台 Skill 的 runtime 设计")
    data = plan.to_dict()
    if data["mode"] != "research":
        fail("深度调研应解析为 research mode")
    if "source-collector" not in data["selected_profiles"]:
        fail("research plan 应包含 source-collector")
    if not data["stages"]:
        fail("runtime plan 必须包含 stages")
    first = data["stages"][0]
    if "source-acquisition" not in first["required_capabilities"]:
        fail("research collection stage 必须要求 source-acquisition")
    try:
        resolve_mode("普通问题", strict=True)
    except ValueError:
        pass
    else:
        fail("strict 模式无匹配时必须失败")
    fallback = plan_runtime("普通问题")
    if not fallback.boundaries:
        fail("非 strict fallback 必须记录 boundary")
    print("runtime planner 检查通过")


if __name__ == "__main__":
    main()
