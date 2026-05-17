#!/usr/bin/env python3
"""检查项目 team pack 激活为 dispatch roster 的契约。"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEADER_RUNTIME = ROOT / "leader-runtime"
RUNTIME_DIR = LEADER_RUNTIME / "runtime"
TEAM_ACTIVATION = RUNTIME_DIR / "project_team_activation.py"
CANDIDATE_REVIEW = RUNTIME_DIR / "candidate_review.py"
SAMPLE_POLICY = LEADER_RUNTIME / "examples" / "candidate-selection-policy.sample.yaml"


def fail(message: str) -> None:
    raise SystemExit(f"project team activation 检查失败: {message}")


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
    if not TEAM_ACTIVATION.exists():
        fail(f"缺少文件: {TEAM_ACTIVATION.relative_to(ROOT)}")
    require_schema(
        "project-team-activation.schema.json",
        ["activation_id", "project_id", "pack_id", "active_count", "dispatch_roster", "verification_status"],
    )

    review_module = load_module(CANDIDATE_REVIEW, "leader_runtime_candidate_review_for_activation")
    activation_module = load_module(TEAM_ACTIVATION, "leader_runtime_project_team_activation")

    passed_review = review_module.run_review(SAMPLE_POLICY, approved_agent_ids=["product_strategy_analyst"])
    promoted_pack = passed_review["review_report"]["promoted_team_pack"]
    activation = activation_module.activate_project_team_pack(promoted_pack)
    if activation["project_id"] != "sample-product":
        fail("activation project_id 不正确")
    if "evidence_collector" not in activation["global_experts"]:
        fail("activation 必须包含基础全局专家")
    if "product_strategy_analyst" not in activation["candidate_agents"]:
        fail("activation 必须包含 promoted candidate")
    if activation["active_count"] != len(activation["dispatch_roster"]):
        fail("active_count 必须等于 dispatch_roster 数量")
    candidate_rows = [item for item in activation["dispatch_roster"] if item["source"] == "project_candidate"]
    if not candidate_rows:
        fail("dispatch_roster 必须包含 project_candidate")
    if candidate_rows[0]["dispatch_status"] != "promoted_uninvoked":
        fail("promoted candidate dispatch_status 必须是 promoted_uninvoked")

    selection_bundle = review_module.run_selection(SAMPLE_POLICY)
    draft_activation = activation_module.activate_project_team_pack(selection_bundle["project_team_pack_draft"])
    if draft_activation["candidate_agents"]:
        fail("未 review 的 candidate 不应进入 active roster")
    if "evidence_collector" not in draft_activation["global_experts"]:
        fail("draft activation 仍应保留基础全局专家")

    print("project team activation 检查通过")


if __name__ == "__main__":
    main()
