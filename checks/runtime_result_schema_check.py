#!/usr/bin/env python3
"""检查平台无关 runtime-result schema。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "think-tank" / "schemas" / "runtime-result.schema.json"
FIXTURE = ROOT / "think-tank" / "examples" / "runtime-e2e-fixture.json"


def fail(message: str) -> None:
    raise SystemExit(f"runtime result schema 检查失败: {message}")


def load(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)} 不是合法 JSON: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} 必须是 object")
    return data


def main() -> None:
    schema = load(SCHEMA)
    fixture = load(FIXTURE)
    required = schema.get("required", [])
    missing = [key for key in required if key not in fixture]
    if missing:
        fail("fixture 缺少 schema required 字段: " + ", ".join(missing))
    for key in ["runtime_plan", "slot_resolution", "run_state", "source_result", "consensus_result", "final_output"]:
        if not isinstance(fixture.get(key), dict):
            fail(f"fixture.{key} 必须是 object")
    if fixture["slot_resolution"].get("can_continue") is not True:
        fail("fixture slot_resolution.can_continue 必须是 true")
    print("runtime result schema 检查通过")


if __name__ == "__main__":
    main()
