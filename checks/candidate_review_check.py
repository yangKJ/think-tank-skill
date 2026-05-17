#!/usr/bin/env python3
"""检查候选 subagent 晋升门禁。"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEADER_RUNTIME = ROOT / "leader-runtime"
RUNTIME_DIR = LEADER_RUNTIME / "runtime"
CANDIDATE_REVIEW = RUNTIME_DIR / "candidate_review.py"
SAMPLE_POLICY = LEADER_RUNTIME / "examples" / "candidate-selection-policy.sample.yaml"


def fail(message: str) -> None:
    raise SystemExit(f"candidate review 检查失败: {message}")


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
        CANDIDATE_REVIEW,
        LEADER_RUNTIME / "templates" / "candidate-review-report.md",
        SAMPLE_POLICY,
    ]:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")

    require_schema(
        "candidate-review-report.schema.json",
        ["review_id", "reviewer_id", "project_id", "policy_id", "status", "reviewed_candidates", "promoted_team_pack"],
    )

    module = load_module(CANDIDATE_REVIEW, "leader_runtime_candidate_review")
    result = module.run_review(SAMPLE_POLICY, approved_agent_ids=["product_strategy_analyst"])
    report = result["review_report"]
    if report["status"] != "passed":
        fail("样例候选晋升应通过")
    if report["promoted_count"] != 1:
        fail("样例应晋升 1 个 candidate")
    if report["rejected_count"] != 0:
        fail("样例不应产生 rejected candidate")
    promoted_pack = report["promoted_team_pack"]
    if promoted_pack is None:
        fail("通过 review 后必须生成 promoted_team_pack")
    promoted_agents = promoted_pack["include_candidate_agents"]
    if len(promoted_agents) != 1:
        fail("promoted_team_pack 应包含 1 个 candidate agent")
    if promoted_agents[0]["conversion_status"] != "promoted":
        fail("promoted candidate conversion_status 必须是 promoted")
    if "candidate-reviewed" not in promoted_pack["project_tags"]:
        fail("promoted team pack 必须标记 candidate-reviewed")
    if any("global-experts.yaml" in boundary for boundary in report["boundaries"]):
        pass
    else:
        fail("review report 必须声明不修改 global-experts.yaml")

    rejection = module.run_review(SAMPLE_POLICY, approved_agent_ids=[])
    if rejection["review_report"]["status"] != "needs_revision":
        fail("未批准任何 candidate 时应返回 needs_revision")
    if rejection["review_report"]["promoted_team_pack"] is not None:
        fail("needs_revision 不应生成 promoted_team_pack")

    print("candidate review 检查通过")


if __name__ == "__main__":
    main()
