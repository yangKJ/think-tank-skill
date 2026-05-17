#!/usr/bin/env python3
"""检查 promoted project candidate 的派遣计划契约。"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEADER_RUNTIME = ROOT / "leader-runtime"
RUNTIME_DIR = LEADER_RUNTIME / "runtime"
TEAM_ACTIVATION = RUNTIME_DIR / "project_team_activation.py"
CANDIDATE_DISPATCH = RUNTIME_DIR / "project_candidate_dispatch.py"
TEAM_PACK = LEADER_RUNTIME / "examples" / "promoted-project-team-pack.sample.yaml"


def fail(message: str) -> None:
    raise SystemExit(f"project candidate dispatch 检查失败: {message}")


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
    for path in [TEAM_ACTIVATION, CANDIDATE_DISPATCH, TEAM_PACK]:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")
    schema_path = LEADER_RUNTIME / "schemas" / "project-candidate-task-packet.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    for field in [
        "task_id",
        "leader_id",
        "candidate_agent_id",
        "source_path",
        "required_capabilities",
        "dispatch_status",
        "invocation_boundary",
    ]:
        if field not in schema["required"]:
            fail(f"project-candidate-task-packet.schema.json required 缺少: {field}")

    activation_module = load_module(TEAM_ACTIVATION, "leader_runtime_activation_for_candidate_dispatch")
    dispatch_module = load_module(CANDIDATE_DISPATCH, "leader_runtime_project_candidate_dispatch")
    activation = activation_module.run_activation(TEAM_PACK)
    packets = dispatch_module.build_project_candidate_task_packets(
        "制定产品策略",
        "strategy",
        ["source-acquisition", "knowledge-persistence"],
        activation,
    )
    if len(packets) != 1:
        fail("样例 team pack 应生成 1 个 project candidate packet")
    packet = packets[0]
    if packet["candidate_agent_id"] != "product_strategy_analyst":
        fail("candidate_agent_id 不正确")
    if packet["dispatch_status"] != "planned_uninvoked":
        fail("project candidate packet 必须保持 planned_uninvoked")
    if "has not been invoked" not in packet["invocation_boundary"]:
        fail("packet 必须声明未调用边界")
    summary = dispatch_module.summarize_project_candidate_dispatch(packets)
    if summary["planned_count"] != 1:
        fail("summary planned_count 不正确")
    if summary["dispatch_status"] != "planned_uninvoked":
        fail("summary dispatch_status 必须是 planned_uninvoked")

    empty = dispatch_module.build_project_candidate_task_packets("x", "research", [], None)
    if empty:
        fail("无 project team activation 时不应生成 candidate packets")

    print("project candidate dispatch 检查通过")


if __name__ == "__main__":
    main()
