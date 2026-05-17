#!/usr/bin/env python3
"""检查项目候选 subagent 真实调用前置门禁。"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEADER_RUNTIME = ROOT / "leader-runtime"
RUNTIME_DIR = LEADER_RUNTIME / "runtime"
INVOCATION_GATE = RUNTIME_DIR / "project_candidate_invocation_gate.py"
ORCHESTRATOR = RUNTIME_DIR / "orchestrator.py"
TEAM_PACK = LEADER_RUNTIME / "examples" / "promoted-project-team-pack.sample.yaml"
FIXTURE = "think-tank/examples/browser-automation-fixture.html"


def fail(message: str) -> None:
    raise SystemExit(f"project candidate invocation gate 检查失败: {message}")


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
    for path in [INVOCATION_GATE, ORCHESTRATOR, TEAM_PACK]:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")

    schema = json.loads((LEADER_RUNTIME / "schemas" / "project-candidate-invocation-gate.schema.json").read_text(encoding="utf-8"))
    for field in ["gate_id", "allow_invocation", "runtime_support", "decision_status", "candidate_decisions", "boundaries"]:
        if field not in schema["required"]:
            fail(f"project-candidate-invocation-gate.schema.json required 缺少: {field}")

    gate_module = load_module(INVOCATION_GATE, "leader_runtime_project_candidate_invocation_gate")
    packet = {
        "task_id": "strategy-project-candidate-1",
        "candidate_agent_id": "product_strategy_analyst",
    }
    blocked = gate_module.evaluate_project_candidate_invocation_gate([packet])
    if blocked["decision_status"] != "blocked":
        fail("默认 invocation gate 必须 blocked")
    if blocked["candidate_decisions"][0]["invoked"]:
        fail("默认 gate 不得 invoked")
    ready = gate_module.evaluate_project_candidate_invocation_gate(
        [packet],
        allow_invocation=True,
        runtime_support="verified_partial",
    )
    if ready["decision_status"] != "ready_uninvoked":
        fail("允许且 runtime verified_partial 时应为 ready_uninvoked")
    if ready["candidate_decisions"][0]["invoked"]:
        fail("ready_uninvoked 仍不得 invoked")

    orchestrator = load_module(ORCHESTRATOR, "leader_runtime_orchestrator_invocation_gate")
    result = orchestrator.run_leader_orchestrator(
        "竞品分析 Cursor 和 Codex",
        target=FIXTURE,
        team_pack_path=TEAM_PACK,
    )
    gate = result["project_candidate_invocation_gate"]
    if gate["decision_status"] != "blocked":
        fail("orchestrator 默认 candidate invocation gate 必须 blocked")
    if any(item["invoked"] for item in gate["candidate_decisions"]):
        fail("orchestrator 默认不得调用 candidate subagent")

    ready_result = orchestrator.run_leader_orchestrator(
        "竞品分析 Cursor 和 Codex",
        target=FIXTURE,
        team_pack_path=TEAM_PACK,
        allow_candidate_invocation=True,
        candidate_runtime_support="verified_partial",
    )
    ready_gate = ready_result["project_candidate_invocation_gate"]
    if ready_gate["decision_status"] != "ready_uninvoked":
        fail("orchestrator allow 后应为 ready_uninvoked")
    if any(item["invoked"] for item in ready_gate["candidate_decisions"]):
        fail("ready_uninvoked 不得被记录为 invoked")

    print("project candidate invocation gate 检查通过")


if __name__ == "__main__":
    main()
