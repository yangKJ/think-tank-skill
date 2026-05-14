#!/usr/bin/env python3
"""检查 slot resolver 最小实现。"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "think-tank" / "runtime"
sys.path.insert(0, str(RUNTIME_DIR))

from slot_resolver import resolve_slots  # noqa: E402


def fail(message: str) -> None:
    raise SystemExit(f"slot resolver 检查失败: {message}")


def main() -> None:
    mapping = {
        "source-acquisition": ["local_static_reader", "web.run"],
        "browser-automation": ["browser", "playwright"],
    }
    ok = resolve_slots(["source-acquisition"], ["browser-automation"], mapping, {"local_static_reader"})
    if not ok["can_continue"]:
        fail("required capability 可用时应继续")
    if ok["missing_required"]:
        fail("required capability 可用时 missing_required 应为空")
    source = ok["resolutions"][0]
    if source["selected_implementation"] != "local_static_reader":
        fail("应选择第一个可用实现")
    missing = resolve_slots(["source-acquisition"], ["browser-automation"], mapping, set())
    if missing["can_continue"]:
        fail("required capability 缺失时不得继续完整执行")
    if missing["missing_required"] != ["source-acquisition"]:
        fail("required 缺失必须记录")
    optional = missing["resolutions"][1]
    if optional["required"]:
        fail("browser-automation 应保持 optional")
    print("slot resolver 检查通过")


if __name__ == "__main__":
    main()
