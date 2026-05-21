#!/usr/bin/env python3
"""检查 capability evidence state machine 协议、schema 和样例。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "think-tank" / "protocol" / "capability-evidence-state-machine.md"
SCHEMA = ROOT / "think-tank" / "schemas" / "capability-evidence.schema.json"
SAMPLE = ROOT / "think-tank" / "examples" / "capability-evidence-sample.json"
QUALITY_GATES = ROOT / "think-tank" / "protocol" / "quality-gates.md"


def fail(message: str) -> None:
    raise SystemExit(f"capability evidence state 检查失败: {message}")


def require_text(path: Path, terms: list[str]) -> str:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for term in terms:
        if term not in text:
            fail(f"{path.relative_to(ROOT)} 缺少: {term}")
    return text


def main() -> None:
    require_text(
        PROTOCOL,
        [
            "installed",
            "discovered",
            "selected",
            "dispatched",
            "invoked",
            "recovered",
            "verified_partial",
            "verified",
            "selected_means_invoked: false",
            "no_state_inflation",
        ],
    )
    require_text(
        QUALITY_GATES,
        [
            "installed",
            "discovered",
            "selected",
            "invoked",
            "recovered",
            "verified_partial",
        ],
    )

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    states = set(schema["properties"]["state"]["enum"])
    required_states = {
        "planned",
        "mock",
        "installed",
        "discovered",
        "selected",
        "dispatched",
        "invoked",
        "recovered",
        "verified_partial",
        "verified",
        "blocked",
        "failed",
        "tracking",
    }
    if not required_states.issubset(states):
        fail(f"schema 缺少状态: {sorted(required_states - states)}")
    for field in ["capability", "provider", "state", "evidence", "boundaries", "quality_check"]:
        if field not in schema["required"]:
            fail(f"schema 缺少 required 字段: {field}")

    sample = json.loads(SAMPLE.read_text(encoding="utf-8"))
    if sample["state"] != "selected":
        fail("sample 应展示 selected 不等于 invoked")
    if sample["quality_check"].get("no_state_inflation") is not True:
        fail("sample 必须声明 no_state_inflation")
    if "invocation" in " ".join(sample["boundaries"]).lower() and sample["state"] == "verified":
        fail("sample 不应把未调用路径写成 verified")

    print("capability evidence state 检查通过")


if __name__ == "__main__":
    main()

