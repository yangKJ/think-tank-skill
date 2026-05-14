#!/usr/bin/env python3
"""检查 Claude Code dispatch 样例的最低契约。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"
SAMPLE = THINK_TANK / "examples" / "claude-dispatch-sample.json"
SCHEMA = THINK_TANK / "schemas" / "claude-dispatch.schema.json"


def fail(message: str) -> None:
    raise SystemExit(f"Claude dispatch 样例检查失败: {message}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)} 不是合法 JSON: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} 必须是 object")
    return data


def require_keys(data: dict[str, Any], keys: list[str], label: str) -> None:
    missing = [key for key in keys if key not in data]
    if missing:
        fail(f"{label} 缺少字段: {', '.join(missing)}")


def require_list(data: dict[str, Any], key: str, label: str, min_items: int = 1) -> None:
    value = data.get(key)
    if not isinstance(value, list) or len(value) < min_items:
        fail(f"{label}.{key} 必须是至少 {min_items} 项的数组")


def main() -> None:
    schema = load_json(SCHEMA)
    sample = load_json(SAMPLE)
    require_keys(schema, ["$schema", "title", "type"], "schema")
    require_keys(
        sample,
        ["dispatch_request", "dispatch_decision", "dispatch_log", "sources", "evidence", "boundaries", "quality_check"],
        "sample",
    )
    require_keys(
        sample["dispatch_decision"],
        ["selected_capability", "candidate_skills", "selected_skill", "invocation_method", "status"],
        "sample.dispatch_decision",
    )
    if sample["dispatch_decision"]["status"] != "dispatched":
        fail("sample.dispatch_decision.status 必须是 dispatched")
    require_keys(sample["dispatch_log"], ["invocation", "recovery"], "sample.dispatch_log")
    if sample["dispatch_log"]["invocation"].get("invoked") is not True:
        fail("sample.dispatch_log.invocation.invoked 必须是 true")
    if sample["dispatch_log"]["recovery"].get("result_recovered") is not True:
        fail("sample.dispatch_log.recovery.result_recovered 必须是 true")
    require_list(sample, "sources", "sample")
    require_list(sample, "evidence", "sample")
    require_list(sample, "boundaries", "sample")
    print("Claude dispatch 样例检查通过")


if __name__ == "__main__":
    main()
