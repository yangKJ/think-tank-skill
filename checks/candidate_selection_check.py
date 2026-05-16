#!/usr/bin/env python3
"""检查项目级候选 subagent 筛选策略。"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
LEADER_RUNTIME = ROOT / "leader-runtime"
RUNTIME_DIR = LEADER_RUNTIME / "runtime"
CANDIDATE_SELECTION = RUNTIME_DIR / "candidate_selection.py"
SAMPLE_POLICY = LEADER_RUNTIME / "examples" / "candidate-selection-policy.sample.yaml"
TEMPLATE_POLICY = LEADER_RUNTIME / "project-templates" / "candidate-selection-policy.template.yaml"


def fail(message: str) -> None:
    raise SystemExit(f"candidate selection 检查失败: {message}")


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
    for path in [CANDIDATE_SELECTION, SAMPLE_POLICY, TEMPLATE_POLICY]:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")

    require_schema(
        "candidate-selection-policy.schema.json",
        ["policy_id", "project_id", "candidate_sources", "max_candidates", "promotion_target"],
    )
    require_schema(
        "candidate-selection-result.schema.json",
        ["selection_id", "policy_id", "project_id", "selected_candidates", "review_required"],
    )
    team_pack_schema = json.loads((LEADER_RUNTIME / "schemas" / "project-team-pack.schema.json").read_text(encoding="utf-8"))
    for field in ["include_candidate_agents", "candidate_source_policy"]:
        if field not in team_pack_schema["properties"]:
            fail(f"project-team-pack.schema.json 缺少 candidate 字段: {field}")

    template = yaml.safe_load(TEMPLATE_POLICY.read_text(encoding="utf-8")) or {}
    if template.get("promotion_target") != "project_team_pack":
        fail("candidate selection template promotion_target 应为 project_team_pack")
    if ".claude/agents" not in template.get("candidate_sources", []):
        fail("candidate selection template 应指向 .claude/agents 作为默认候选源")

    module = load_module(CANDIDATE_SELECTION, "leader_runtime_candidate_selection")
    result = module.run_selection(SAMPLE_POLICY)
    selection = result["selection_result"]
    team_pack = result["project_team_pack_draft"]
    if selection["selected_count"] < 1:
        fail("sample policy 应至少选出一个 candidate")
    if not selection["review_required"]:
        fail("selection_result 必须要求 leader review")
    if selection["promotion_target"] != "project_team_pack":
        fail("selection_result promotion_target 不正确")
    if not team_pack["include_candidate_agents"]:
        fail("team pack draft 必须包含 include_candidate_agents")
    if team_pack["candidate_source_policy"] != result["policy"]["policy_id"]:
        fail("team pack draft 必须记录 candidate_source_policy")
    if any(item["conversion_status"] != "candidate" for item in team_pack["include_candidate_agents"]):
        fail("未经 review 的 team pack draft 只能包含 candidate 状态")
    if "evidence_collector" not in team_pack["include_experts"]:
        fail("candidate team pack draft 应保留基础全局专家")

    print("candidate selection 检查通过")


if __name__ == "__main__":
    main()
