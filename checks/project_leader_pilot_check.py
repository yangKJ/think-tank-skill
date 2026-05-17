#!/usr/bin/env python3
"""检查项目 leader 试点闭环。"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEADER_RUNTIME = ROOT / "leader-runtime"
PILOT_RUNTIME = LEADER_RUNTIME / "runtime" / "project_leader_pilot.py"
PILOT_SPEC = LEADER_RUNTIME / "examples" / "project-leader-pilot.sample.yaml"


def fail(message: str) -> None:
    raise SystemExit(f"project leader pilot 检查失败: {message}")


def load_module(path: Path, name: str):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"无法加载模块: {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def require_schema(name: str, required: list[str]) -> None:
    path = LEADER_RUNTIME / "schemas" / name
    if not path.exists():
        fail(f"缺少 schema: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    for field in required:
        if field not in data["required"]:
            fail(f"{name} required 缺少: {field}")


def main() -> None:
    for path in [
        PILOT_RUNTIME,
        PILOT_SPEC,
        LEADER_RUNTIME / "project-templates" / "project-leader-pilot.template.yaml",
        LEADER_RUNTIME / "docs" / "project-derived-leader-model.md",
        LEADER_RUNTIME / "docs" / "project-leader-pilot-runbook.md",
        LEADER_RUNTIME / "README.md",
    ]:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")

    require_schema(
        "project-leader-pilot.schema.json",
        ["pilot_id", "project_id", "selection_policy", "request"],
    )

    module = load_module(PILOT_RUNTIME, "leader_runtime_project_leader_pilot")
    result = module.run_project_leader_pilot(PILOT_SPEC)
    if result["pilot_id"] != "sample-product-leader-pilot":
        fail("pilot_id 不正确")
    if result["selection_result"]["selected_count"] != 1:
        fail("样例 pilot 应筛出 1 个 candidate")
    if result["review_report"]["promoted_count"] != 1:
        fail("样例 pilot 应晋升 1 个 candidate")
    activation = result["project_team_activation"]
    if activation is None or "product_strategy_analyst" not in activation["candidate_agents"]:
        fail("样例 pilot 应激活 promoted candidate")
    orchestrator = result["orchestrator_result"]
    if orchestrator["project_candidate_host_dispatch_bundle"]["dispatch_status"] != "ready_for_host_dispatch":
        fail("样例 pilot 应进入 ready_for_host_dispatch")
    evidence = orchestrator["project_candidate_invocation_evidence"]
    if evidence is None or evidence["successful_invocations"] != 1:
        fail("样例 pilot 应回灌 1 次成功 host invocation")
    if not evidence["results"][0]["invoked"]:
        fail("样例 pilot evidence 应包含 invoked=true")

    print("project leader pilot 检查通过")


if __name__ == "__main__":
    main()
