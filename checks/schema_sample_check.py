#!/usr/bin/env python3
"""检查 think-tank JSON schema 样例的最低契约。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from example_paths import resolve_example_path


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"

INPUT_SAMPLE = THINK_TANK / "examples" / "schema-sample-input.json"
OUTPUT_SAMPLE = THINK_TANK / "examples" / "schema-sample-output.json"

INPUT_MODES = {"research", "council", "review", "strategy", "auto"}
OUTPUT_MODES = {"research", "council", "review", "strategy"}
CONFIDENCE = {"low", "medium", "high"}


def fail(message: str) -> None:
    raise SystemExit(f"schema 样例检查失败: {message}")


def load_json(path: Path) -> dict[str, Any]:
    path = resolve_example_path(ROOT, path)
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)} 不是合法 JSON: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} 必须是 object")
    return data


def require_keys(data: dict[str, Any], keys: list[str], name: str) -> None:
    missing = [key for key in keys if key not in data]
    if missing:
        fail(f"{name} 缺少字段: {', '.join(missing)}")


def require_string(data: dict[str, Any], key: str, name: str) -> None:
    if not isinstance(data.get(key), str) or not data[key]:
        fail(f"{name}.{key} 必须是非空字符串")


def require_string_list(data: dict[str, Any], key: str, name: str, min_items: int = 0) -> None:
    value = data.get(key)
    if not isinstance(value, list) or len(value) < min_items or not all(isinstance(item, str) for item in value):
        fail(f"{name}.{key} 必须是字符串数组")


def check_input_sample() -> None:
    data = load_json(INPUT_SAMPLE)
    require_keys(data, ["task"], "input")
    require_string(data, "task", "input")
    if data.get("mode", "auto") not in INPUT_MODES:
        fail("input.mode 不在允许范围")
    for key in ["context", "constraints", "success_criteria"]:
        if key in data:
            require_string_list(data, key, "input")
    if "evidence_policy" in data and not isinstance(data["evidence_policy"], dict):
        fail("input.evidence_policy 必须是 object")


def check_output_sample() -> None:
    data = load_json(OUTPUT_SAMPLE)
    require_keys(data, ["mode", "roles", "conclusion", "recommendations", "quality_check"], "output")
    if data["mode"] not in OUTPUT_MODES:
        fail("output.mode 不在允许范围")
    require_string_list(data, "roles", "output", min_items=1)
    require_string(data, "conclusion", "output")
    require_string_list(data, "recommendations", "output", min_items=1)
    for key in ["evidence", "disagreements", "risks", "boundaries", "next_steps"]:
        if key in data:
            require_string_list(data, key, "output")
    for index, view in enumerate(data.get("role_views", []), start=1):
        if not isinstance(view, dict):
            fail(f"output.role_views[{index}] 必须是 object")
        require_keys(view, ["role", "claim"], f"output.role_views[{index}]")
        if "confidence" in view and view["confidence"] not in CONFIDENCE:
            fail(f"output.role_views[{index}].confidence 不在允许范围")
    quality_check = data["quality_check"]
    if not isinstance(quality_check, dict):
        fail("output.quality_check 必须是 object")
    require_keys(quality_check, ["protocol_complete", "evidence_boundary_clear", "actionable"], "output.quality_check")
    for key in ["protocol_complete", "evidence_boundary_clear", "actionable"]:
        if not isinstance(quality_check[key], bool):
            fail(f"output.quality_check.{key} 必须是 boolean")


def main() -> None:
    check_input_sample()
    check_output_sample()
    print("schema 样例检查通过")


if __name__ == "__main__":
    main()
