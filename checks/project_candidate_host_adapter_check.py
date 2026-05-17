#!/usr/bin/env python3
"""检查项目候选 subagent 的 host dispatch bundle 与结果回灌。"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEADER_RUNTIME = ROOT / "leader-runtime"
RUNTIME_DIR = LEADER_RUNTIME / "runtime"
HOST_ADAPTER = RUNTIME_DIR / "project_candidate_host_adapter.py"
INVOCATION_GATE = RUNTIME_DIR / "project_candidate_invocation_gate.py"
TEAM_PACK = LEADER_RUNTIME / "examples" / "promoted-project-team-pack.sample.yaml"
HOST_RESULTS = LEADER_RUNTIME / "examples" / "project-candidate-host-results.sample.json"


def fail(message: str) -> None:
    raise SystemExit(f"project candidate host adapter 检查失败: {message}")


def load_module(path: Path, name: str):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"无法加载模块: {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    for path in [HOST_ADAPTER, INVOCATION_GATE, TEAM_PACK, HOST_RESULTS]:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")

    for schema_name, required in {
        "project-candidate-host-dispatch-bundle.schema.json": ["bundle_id", "dispatch_status", "request_count", "dispatch_requests"],
        "project-candidate-invocation-evidence.schema.json": ["evidence_id", "bundle_id", "result_count", "successful_invocations", "results"],
    }.items():
        schema = json.loads((LEADER_RUNTIME / "schemas" / schema_name).read_text(encoding="utf-8"))
        for field in required:
            if field not in schema["required"]:
                fail(f"{schema_name} required 缺少: {field}")

    host_module = load_module(HOST_ADAPTER, "leader_runtime_project_candidate_host_adapter")
    gate_module = load_module(INVOCATION_GATE, "leader_runtime_project_candidate_invocation_gate_for_host")
    packets = [
        {
            "task_id": "research-project-candidate-1",
            "candidate_agent_id": "product_strategy_analyst",
            "candidate_name": "Product Strategy Analyst",
            "objective": "竞品分析",
            "task_scope": "strategy slice",
            "input_context": ["mode=research"],
            "deliverables": ["claim"],
            "acceptance_checks": ["schema_complete"],
            "fallback_rule": "fallback",
        }
    ]
    blocked_gate = gate_module.evaluate_project_candidate_invocation_gate(packets)
    blocked_bundle = host_module.build_host_dispatch_bundle(packets, blocked_gate)
    if blocked_bundle["dispatch_status"] != "blocked":
        fail("blocked gate 应产出 blocked bundle")
    if blocked_bundle["request_count"] != 0:
        fail("blocked bundle 不应生成 host requests")

    ready_gate = gate_module.evaluate_project_candidate_invocation_gate(
        packets,
        allow_invocation=True,
        runtime_support="verified_partial",
    )
    ready_bundle = host_module.build_host_dispatch_bundle(packets, ready_gate)
    if ready_bundle["dispatch_status"] != "ready_for_host_dispatch":
        fail("ready gate 应产出 ready_for_host_dispatch bundle")
    if ready_bundle["request_count"] != 1:
        fail("ready bundle 应生成 1 条 host request")
    if ready_bundle["dispatch_requests"][0]["invoked"]:
        fail("host dispatch bundle 初始不得 invoked")

    evidence = host_module.ingest_host_results(
        ready_bundle,
        host_module.load_host_results(HOST_RESULTS),
    )
    if evidence["successful_invocations"] != 1:
        fail("样例 host results 应回灌 1 次成功调用")
    if not evidence["results"][0]["invoked"]:
        fail("evidence 结果应标记 invoked=true")

    print("project candidate host adapter 检查通过")


if __name__ == "__main__":
    main()
