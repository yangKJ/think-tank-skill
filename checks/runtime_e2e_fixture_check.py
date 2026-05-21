#!/usr/bin/env python3
"""检查 runtime E2E fixture。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "think-tank" / "examples" / "runtime-e2e-fixture.json"


def fail(message: str) -> None:
    raise SystemExit(f"runtime E2E fixture 检查失败: {message}")


def load_fixture() -> dict[str, Any]:
    if not FIXTURE.exists():
        fail(f"缺少文件: {FIXTURE.relative_to(ROOT)}")
    try:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"fixture 不是合法 JSON: {exc}")
    if not isinstance(data, dict):
        fail("fixture 必须是 object")
    return data


def main() -> None:
    data = load_fixture()
    if data.get("runtime") != "codex-runtime-pipeline":
        fail("fixture.runtime 必须是 codex-runtime-pipeline")
    if data.get("runtime_plan", {}).get("mode") != "research":
        fail("fixture.runtime_plan.mode 必须是 research")
    if data.get("slot_resolution", {}).get("missing_required"):
        fail("fixture 不应有 missing_required")
    if not data.get("source_result", {}).get("sources"):
        fail("fixture source_result.sources 不能为空")
    if data.get("consensus_result", {}).get("level") != "L1":
        fail("fixture consensus_result.level 必须是 L1")
    if not data.get("final_output", {}).get("recommendations"):
        fail("fixture final_output.recommendations 不能为空")
    print("runtime E2E fixture 检查通过")


if __name__ == "__main__":
    main()
