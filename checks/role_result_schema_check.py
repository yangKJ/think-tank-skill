#!/usr/bin/env python3
"""检查 role-result schema 和 fixture。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "think-tank" / "schemas" / "role-result.schema.json"
FIXTURE = ROOT / "think-tank" / "examples" / "specialist-runtime-fixture.json"


def fail(message: str) -> None:
    raise SystemExit(f"role-result schema 检查失败: {message}")


def main() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    required = set(schema.get("required", []))
    expected = {
        "profile",
        "execution_method",
        "claim",
        "evidence",
        "sources",
        "risks",
        "objections",
        "recommendations",
        "confidence",
        "boundaries",
        "status",
    }
    if required != expected:
        fail("schema required 字段不完整")

    methods = set(schema["properties"]["execution_method"]["enum"])
    if "single_agent_multi_profile_fallback" not in methods or "specialist_subagent" not in methods:
        fail("execution_method enum 缺少关键状态")

    for result in fixture["role_results"]:
        missing = expected - set(result)
        if missing:
            fail(f"fixture role_result 缺少字段: {', '.join(sorted(missing))}")
        if result["execution_method"] not in methods:
            fail("fixture execution_method 非法")

    aggregated = fixture["aggregated_result"]
    if aggregated["specialist_independence"] == "verified":
        fail("fixture 不得声称 live specialist independence verified")

    print("role-result schema 检查通过")


if __name__ == "__main__":
    main()

