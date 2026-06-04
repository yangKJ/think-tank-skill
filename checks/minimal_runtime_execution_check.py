#!/usr/bin/env python3
"""检查 repo 内 minimal runtime 是否能跑通成功和失败路径。"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from example_paths import resolve_example_path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "think-tank" / "platforms" / "codex" / "runtime" / "source_acquisition_minimal.py"
FIXTURE = ROOT / "think-tank" / "examples" / "browser-automation-fixture.html"
CODEX_SUCCESS_SAMPLE = resolve_example_path(ROOT, ROOT / "think-tank" / "examples" / "codex-runtime-sample.json")
CODEX_FAILURE_SAMPLE = resolve_example_path(ROOT, ROOT / "think-tank" / "examples" / "codex-runtime-failure-sample.json")


def fail(message: str) -> None:
    raise SystemExit(f"minimal runtime 执行检查失败: {message}")


def run_runtime(target: str, runtime: str = "codex-minimal") -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(RUNTIME), target, "--runtime", runtime],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"runtime 命令失败: {completed.stderr.strip()}")
    try:
        data = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        fail(f"runtime 输出不是合法 JSON: {exc}")
    if not isinstance(data, dict):
        fail("runtime 输出必须是 object")
    return data


def load_sample(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)} 不是合法 JSON: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} 必须是 object")
    return data


def check_success() -> None:
    data = run_runtime(str(FIXTURE))
    provenance = data.get("runtime_provenance", {})
    if provenance.get("provider_invoked") is not True:
        fail("成功路径 runtime_provenance.provider_invoked 必须是 true")
    if provenance.get("true_multi_agent_runtime") is not False:
        fail("成功路径不得声称真实多 agent runtime")
    if data.get("runtime") != "codex-minimal":
        fail("成功路径 runtime 必须是 codex-minimal")
    if data.get("invocation", {}).get("result_status") != "success":
        fail("成功路径 invocation.result_status 必须是 success")
    if data.get("recovery", {}).get("result_recovered") is not True:
        fail("成功路径必须回收到结果")
    if not data.get("sources"):
        fail("成功路径 sources[] 不能为空")
    if not data.get("evidence"):
        fail("成功路径 evidence[] 不能为空")


def check_failure() -> None:
    data = run_runtime(str(ROOT / "think-tank" / "examples" / "missing-runtime-target.html"))
    provenance = data.get("runtime_provenance", {})
    if provenance.get("result_recovered") is not False:
        fail("失败路径 runtime_provenance.result_recovered 必须是 false")
    if provenance.get("evidence_state") != "failed":
        fail("失败路径 runtime_provenance.evidence_state 必须是 failed")
    if data.get("invocation", {}).get("result_status") != "failed":
        fail("失败路径 invocation.result_status 必须是 failed")
    if data.get("recovery", {}).get("result_recovered") is not False:
        fail("失败路径不得标记为已回收")
    if data.get("sources"):
        fail("失败路径不得伪造 sources[]")
    if data.get("evidence"):
        fail("失败路径不得伪造 evidence[]")
    boundaries = "\n".join(data.get("boundaries", []))
    if "No fallback was executed." not in boundaries:
        fail("失败路径必须声明未执行 fallback")
    if "fabricated" not in boundaries:
        fail("失败路径必须声明不伪造来源或证据")


def check_static_samples() -> None:
    success = load_sample(CODEX_SUCCESS_SAMPLE)
    failure = load_sample(CODEX_FAILURE_SAMPLE)
    if success.get("runtime") != "codex-minimal":
        fail("codex-runtime-sample.runtime 必须是 codex-minimal")
    if "runtime_provenance" not in success or "runtime_provenance" not in failure:
        fail("codex runtime samples 必须包含 runtime_provenance")
    if success.get("invocation", {}).get("result_status") != "success":
        fail("codex-runtime-sample 必须是成功路径")
    if not success.get("sources") or not success.get("evidence"):
        fail("codex-runtime-sample 必须包含 sources[] 和 evidence[]")
    if failure.get("invocation", {}).get("result_status") != "failed":
        fail("codex-runtime-failure-sample 必须是失败路径")
    if failure.get("sources") or failure.get("evidence"):
        fail("codex-runtime-failure-sample 不得包含 sources[] 或 evidence[]")


def main() -> None:
    if not RUNTIME.exists():
        fail(f"缺少 runtime: {RUNTIME.relative_to(ROOT)}")
    for sample in [CODEX_SUCCESS_SAMPLE, CODEX_FAILURE_SAMPLE]:
        if not sample.exists():
            fail(f"缺少样例: {sample.relative_to(ROOT)}")
    check_success()
    check_failure()
    check_static_samples()
    print("minimal runtime 执行检查通过")


if __name__ == "__main__":
    main()
