#!/usr/bin/env python3
"""检查 Claude Code minimal runtime 样例的最低契约。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"
SUCCESS_SAMPLE = THINK_TANK / "examples" / "claude-runtime-sample.json"
FAILURE_SAMPLE = THINK_TANK / "examples" / "claude-runtime-failure-sample.json"
SCHEMA = THINK_TANK / "schemas" / "claude-runtime.schema.json"


def fail(message: str) -> None:
    raise SystemExit(f"Claude runtime 样例检查失败: {message}")


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


def check_common_sample(sample: dict[str, Any], label: str) -> None:
    require_keys(
        sample,
        ["runtime", "mode", "profile", "capability", "dispatch_request", "dispatch_decision", "invocation", "recovery", "sources", "evidence", "boundaries", "quality_check"],
        label,
    )
    if sample["runtime"] != "claude-code-minimal":
        fail(f"{label}.runtime 必须是 claude-code-minimal")
    if sample["invocation"].get("invoked") is not True:
        fail(f"{label}.invocation.invoked 必须是 true")
    if not sample["boundaries"]:
        fail(f"{label}.boundaries 不能为空")


def check_success_sample(sample: dict[str, Any]) -> None:
    check_common_sample(sample, "success_sample")
    if sample["invocation"].get("result_status") != "success":
        fail("success_sample.invocation.result_status 必须是 success")
    if sample["recovery"].get("result_recovered") is not True:
        fail("success_sample.recovery.result_recovered 必须是 true")
    if not sample["sources"]:
        fail("success_sample.sources 不能为空")
    if not sample["evidence"]:
        fail("success_sample.evidence 不能为空")


def check_failure_sample(sample: dict[str, Any]) -> None:
    check_common_sample(sample, "failure_sample")
    if sample["invocation"].get("result_status") not in {"failed", "skipped"}:
        fail("failure_sample.invocation.result_status 必须是 failed 或 skipped")
    if sample["recovery"].get("result_recovered") is not False:
        fail("failure_sample.recovery.result_recovered 必须是 false")
    if sample["sources"]:
        fail("failure_sample.sources 必须为空，不能伪造来源")
    if sample["evidence"]:
        fail("failure_sample.evidence 必须为空，不能伪造证据")
    boundaries = "\n".join(str(item) for item in sample["boundaries"])
    if "No fallback was executed" not in boundaries:
        fail("failure_sample.boundaries 必须声明未执行 fallback")
    if "fabricated" not in boundaries:
        fail("failure_sample.boundaries 必须声明不伪造 evidence/source")


def main() -> None:
    schema = load_json(SCHEMA)
    success_sample = load_json(SUCCESS_SAMPLE)
    failure_sample = load_json(FAILURE_SAMPLE)
    require_keys(schema, ["$schema", "title", "type"], "schema")
    check_success_sample(success_sample)
    check_failure_sample(failure_sample)
    print("Claude runtime 样例检查通过")


if __name__ == "__main__":
    main()
