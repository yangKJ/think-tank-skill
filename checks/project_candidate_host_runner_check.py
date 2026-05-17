#!/usr/bin/env python3
"""检查项目候选 Host runner 的离线模拟行为。"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile


ROOT = Path(__file__).resolve().parents[1]
LEADER_RUNTIME = ROOT / "leader-runtime"
RUNTIME_DIR = LEADER_RUNTIME / "runtime"
HOST_ADAPTER = RUNTIME_DIR / "project_candidate_host_runner.py"
SCHEMA = LEADER_RUNTIME / "schemas" / "project-candidate-invocation-evidence.schema.json"
EXAMPLE_BUNDLE = {
    "bundle_id": "project-candidate-host-dispatch-bundle",
    "adapter": "codex-host-subagent",
    "adapter_version": "0.1.0",
    "dispatch_status": "ready_for_host_dispatch",
    "request_count": 2,
    "dispatch_requests": [
        {
            "task_id": "research-project-candidate-1",
            "candidate_agent_id": "product_strategy_analyst",
            "candidate_name": "Product Strategy Analyst",
            "dispatch_status": "ready_for_host_dispatch",
            "host_payload": {},
            "invoked": False,
        },
        {
            "task_id": "research-project-candidate-2",
            "candidate_agent_id": "go_to_market_specialist",
            "candidate_name": "Go To Market Specialist",
            "dispatch_status": "ready_for_host_dispatch",
            "host_payload": {},
            "invoked": False,
        },
    ],
}


def fail(message: str) -> None:
    raise SystemExit(f"project candidate host runner 检查失败: {message}")


def load_module(path: Path, name: str):
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"无法加载模块: {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    for path in [HOST_ADAPTER, SCHEMA]:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")

    host_schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    required = [
        "evidence_id",
        "bundle_id",
        "result_count",
        "successful_invocations",
        "results",
    ]
    for field in required:
        if field not in host_schema["required"]:
            fail(f"project-candidate-invocation-evidence.schema.json 缺少: {field}")

    module = load_module(HOST_ADAPTER, "leader_runtime_project_candidate_host_runner")
    results = module.build_simulated_host_results(
        EXAMPLE_BUNDLE,
        host_provider="test-host",
        run_id="runner-check",
    )
    result = module.build_simulated_host_evidence(EXAMPLE_BUNDLE, results)

    if result["result_count"] != 2:
        fail("示例 runner 应输出 2 条 result")
    if result["successful_invocations"] != 2:
        fail("示例 runner 在不指定失败任务时应全量成功")
    if result["results"][0]["invocation_status"] != "success":
        fail("结果必须带 success 状态")
    if result["results"][0]["invoked"] is not True:
        fail("成功结果必须 invoked=true")

    failed_results = module.build_simulated_host_results(
        EXAMPLE_BUNDLE,
        host_provider="test-host",
        run_id="runner-check",
        force_fail_task_ids={"research-project-candidate-2"},
    )
    fail_result = module.build_simulated_host_evidence(EXAMPLE_BUNDLE, failed_results)
    if fail_result["successful_invocations"] != 1:
        fail("指定 fail_task_ids 时成功数应减 1")
    if fail_result["results"][1]["invocation_status"] != "failed":
        fail("命中 fail_task_ids 的任务应是 failed")
    if fail_result["results"][1]["invoked"] is not False:
        fail("失败结果不应 invoked=true")

    with NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".json", delete=False) as temp:
        temp_path = Path(temp.name)
    temp_path.write_text(json.dumps(EXAMPLE_BUNDLE, ensure_ascii=False), encoding="utf-8")
    with NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".json", delete=False) as out:
        out_path = Path(out.name)

    payload = module.build_simulated_host_results(
        json.loads(temp_path.read_text(encoding="utf-8")),
        host_provider="test-host",
        run_id="runner-check",
    )
    module.write_json(out_path, payload)
    if not out_path.exists():
        fail("runner 应将结果写入 output-json")
    output_payload = json.loads(out_path.read_text(encoding="utf-8"))
    if len(output_payload) != 2:
        fail("runner output 结果应与 bundle 匹配")

    print("project candidate host runner 检查通过")


if __name__ == "__main__":
    main()
