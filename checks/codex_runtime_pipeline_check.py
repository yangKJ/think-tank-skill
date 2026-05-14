#!/usr/bin/env python3
"""检查 Codex runtime pipeline 可重复执行。"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "think-tank" / "platforms" / "codex" / "runtime" / "pipeline.py"
FIXTURE = ROOT / "think-tank" / "examples" / "browser-automation-fixture.html"


def fail(message: str) -> None:
    raise SystemExit(f"Codex runtime pipeline 检查失败: {message}")


def run_pipeline(target: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(PIPELINE), "深度调研 think-tank runtime pipeline", str(target)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"pipeline 命令失败: {completed.stderr.strip()}")
    try:
        data = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        fail(f"pipeline 输出不是合法 JSON: {exc}")
    if not isinstance(data, dict):
        fail("pipeline 输出必须是 object")
    return data


def main() -> None:
    data = run_pipeline(FIXTURE)
    if data.get("runtime") != "codex-runtime-pipeline":
        fail("runtime 必须是 codex-runtime-pipeline")
    if data.get("mode") != "research":
        fail("mode 必须是 research")
    if data.get("slot_resolution", {}).get("can_continue") is not True:
        fail("slot_resolution.can_continue 必须是 true")
    if data.get("source_result", {}).get("invocation", {}).get("result_status") != "success":
        fail("source_result 必须成功")
    if data.get("consensus_result", {}).get("level") != "L1":
        fail("成功 fixture 应达成 L1")
    if not data.get("final_output", {}).get("evidence"):
        fail("final_output.evidence 不能为空")
    print("Codex runtime pipeline 检查通过")


if __name__ == "__main__":
    main()
