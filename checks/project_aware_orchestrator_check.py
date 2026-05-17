#!/usr/bin/env python3
"""检查 leader orchestrator 可选加载项目 team pack。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEADER_RUNTIME = ROOT / "leader-runtime"
ORCHESTRATOR = LEADER_RUNTIME / "runtime" / "orchestrator.py"
TEAM_PACK = LEADER_RUNTIME / "examples" / "promoted-project-team-pack.sample.yaml"
HOST_RESULTS = LEADER_RUNTIME / "examples" / "project-candidate-host-results.sample.json"
FIXTURE = "think-tank/examples/browser-automation-fixture.html"


def fail(message: str) -> None:
    raise SystemExit(f"project aware orchestrator 检查失败: {message}")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"无法加载模块: {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    for path in [ORCHESTRATOR, TEAM_PACK, HOST_RESULTS]:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")

    module = load_module(ORCHESTRATOR, "leader_runtime_project_aware_orchestrator")
    baseline = module.run_leader_orchestrator("竞品分析 Cursor 和 Codex", target=FIXTURE)
    if "project_team_activation" in baseline:
        fail("未传 team_pack 时不应出现 project_team_activation")
    if "project_team" in baseline["leader_context"]:
        fail("未传 team_pack 时 leader_context 不应包含 project_team")

    result = module.run_leader_orchestrator(
        "竞品分析 Cursor 和 Codex",
        target=FIXTURE,
        team_pack_path=TEAM_PACK,
    )
    activation = result.get("project_team_activation")
    if activation is None:
        fail("传入 team_pack 后必须输出 project_team_activation")
    if result["leader_context"]["project_team"]["project_id"] != "sample-product":
        fail("leader_context.project_team.project_id 不正确")
    if "product_strategy_analyst" not in activation["candidate_agents"]:
        fail("project_team_activation 必须包含 promoted candidate")
    candidate_rows = [item for item in activation["dispatch_roster"] if item["source"] == "project_candidate"]
    if not candidate_rows:
        fail("dispatch_roster 必须包含 project_candidate")
    if candidate_rows[0]["dispatch_status"] != "promoted_uninvoked":
        fail("project candidate 必须保持 promoted_uninvoked")
    candidate_packets = result.get("project_candidate_task_packets", [])
    if len(candidate_packets) != 1:
        fail("project-aware leader 必须为 promoted candidate 生成计划 packet")
    if candidate_packets[0]["candidate_agent_id"] != "product_strategy_analyst":
        fail("project candidate packet candidate_agent_id 不正确")
    if candidate_packets[0]["dispatch_status"] != "planned_uninvoked":
        fail("project candidate packet 必须保持 planned_uninvoked")
    if result["project_candidate_dispatch_summary"]["dispatch_status"] != "planned_uninvoked":
        fail("project candidate dispatch summary 必须保持 planned_uninvoked")
    gate = result.get("project_candidate_invocation_gate")
    if gate is None:
        fail("project-aware leader 必须输出 project_candidate_invocation_gate")
    if gate["decision_status"] != "blocked":
        fail("默认 project candidate invocation gate 必须 blocked")
    if any(item["invoked"] for item in gate["candidate_decisions"]):
        fail("默认 project candidate invocation gate 不得 invoked")
    host_bundle = result.get("project_candidate_host_dispatch_bundle")
    if host_bundle is None:
        fail("project-aware leader 必须输出 project_candidate_host_dispatch_bundle")
    if host_bundle["dispatch_status"] != "blocked":
        fail("默认 host dispatch bundle 必须 blocked")
    if host_bundle["request_count"] != 0:
        fail("默认 blocked host bundle 不应有 request")
    if result["think_tank_skill_result"]["runtime"] != "codex-natural-language-orchestrator":
        fail("project-aware leader 仍必须包装 think-tank Skill 结果")
    if "Project team activation loads roster entries only" not in " ".join(result["boundaries"]):
        fail("result boundaries 必须声明 activation 只加载 roster")

    ready = module.run_leader_orchestrator(
        "竞品分析 Cursor 和 Codex",
        target=FIXTURE,
        team_pack_path=TEAM_PACK,
        allow_candidate_invocation=True,
        candidate_runtime_support="verified_partial",
        candidate_host_results_path=HOST_RESULTS,
    )
    if ready["project_candidate_host_dispatch_bundle"]["dispatch_status"] != "ready_for_host_dispatch":
        fail("ready path 的 host dispatch bundle 应 ready_for_host_dispatch")
    if ready["project_candidate_host_dispatch_bundle"]["request_count"] != 1:
        fail("ready path 的 host dispatch bundle 应包含 1 条 request")
    evidence = ready.get("project_candidate_invocation_evidence")
    if evidence is None:
        fail("传入 host results 后应输出 invocation evidence")
    if evidence["successful_invocations"] != 1:
        fail("样例 host results 应回灌 1 次成功调用")
    if not evidence["results"][0]["invoked"]:
        fail("样例 evidence 应标记 invoked=true")

    print("project aware orchestrator 检查通过")


if __name__ == "__main__":
    main()
