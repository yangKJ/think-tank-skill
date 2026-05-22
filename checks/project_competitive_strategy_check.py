#!/usr/bin/env python3
"""检查项目竞品策略闭环的 recipe、协议、schema 和 golden sample。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TT = ROOT / "think-tank"

RECIPE = TT / "recipes" / "project-competitive-strategy.md"
EVIDENCE_PROTOCOL = TT / "protocol" / "evidence-sources.md"
ARTIFACT_PROTOCOL = TT / "protocol" / "artifact-write-policy.md"
BACKLOG_PROTOCOL = TT / "protocol" / "strategy-to-backlog.md"
SCHEMA = TT / "schemas" / "project-competitive-strategy.schema.json"
EVIDENCE_SCHEMA = TT / "schemas" / "evidence-sources.schema.json"
ARTIFACT_SCHEMA = TT / "schemas" / "artifact-plan.schema.json"
BACKLOG_SCHEMA = TT / "schemas" / "strategy-backlog.schema.json"
SAMPLE = TT / "examples" / "project-competitive-strategy-local-image-editor.json"


def fail(message: str) -> None:
    raise SystemExit(f"project competitive strategy 检查失败: {message}")


def read(path: Path) -> str:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"缺少 JSON 文件: {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)} 不是合法 JSON: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} 必须是 object")
    return data


def require_terms(content: str, terms: list[str], context: str) -> None:
    for term in terms:
        if term not in content:
            fail(f"{context} 缺少: {term}")


def main() -> None:
    recipe = read(RECIPE)
    require_terms(
        recipe,
        [
            "intent: project_competitive_strategy",
            "default_mode: strategy",
            "optional_peer_skills_are_dependencies: false",
            "evidence_sources:",
            "artifact_plan:",
            "strategy_to_backlog",
            "protocol/evidence-sources.md",
            "protocol/artifact-write-policy.md",
            "protocol/strategy-to-backlog.md",
            "不把本地文档愿景当作当前实现事实",
        ],
        "project-competitive-strategy recipe",
    )

    require_terms(
        read(EVIDENCE_PROTOCOL),
        [
            "local_code",
            "local_docs",
            "web_sources",
            "user_provided",
            "inference",
            "unavailable_data",
            "project_docs_not_treated_as_runtime_truth_without_code_check",
        ],
        "evidence-sources protocol",
    )
    require_terms(
        read(ARTIFACT_PROTOCOL),
        [
            "artifact_plan:",
            "write_requested_by_user",
            "overwrite_existing",
            "git_impact",
            "private_data_check",
            ".think-tank/artifacts",
        ],
        "artifact-write-policy protocol",
    )
    require_terms(
        read(BACKLOG_PROTOCOL),
        [
            "strategy_to_backlog:",
            "backlog_candidates",
            "readiness",
            "acceptance_criteria",
            "non_goals",
            "next_owner",
            "validation_plan",
            "not_claimed_as_implemented",
        ],
        "strategy-to-backlog protocol",
    )

    for schema_path in [SCHEMA, EVIDENCE_SCHEMA, ARTIFACT_SCHEMA, BACKLOG_SCHEMA]:
        schema = load_json(schema_path)
        if schema.get("type") != "object":
            fail(f"{schema_path.relative_to(ROOT)} type 必须是 object")

    sample = load_json(SAMPLE)
    required = load_json(SCHEMA).get("required", [])
    missing = [key for key in required if key not in sample]
    if missing:
        fail("golden sample 缺少 required 字段: " + ", ".join(missing))

    provenance = sample.get("runtime_provenance", {})
    if provenance.get("true_multi_agent_runtime") is not False:
        fail("golden sample 不得声称真实多 agent runtime")
    if provenance.get("result_recovery") != "manual":
        fail("golden sample 必须声明 manual recovery")

    evidence = sample.get("evidence_sources", {})
    for key in ["local_code", "local_docs", "web_sources", "user_provided", "inference", "unavailable_data"]:
        if key not in evidence:
            fail(f"golden sample evidence_sources 缺少 {key}")

    backlog = sample.get("strategy_to_backlog", {})
    candidates = backlog.get("backlog_candidates", [])
    if not candidates:
        fail("golden sample 必须包含 backlog_candidates")
    for item in candidates:
        if item.get("readiness") not in {"ready", "needs_input", "observe_only", "blocked"}:
            fail("每个 backlog candidate 必须包含合法 readiness")
        if not item.get("acceptance_criteria"):
            fail("每个 backlog candidate 必须有 acceptance_criteria")
        if not item.get("non_goals"):
            fail("每个 backlog candidate 必须有 non_goals")
        if not item.get("next_owner"):
            fail("每个 backlog candidate 必须有 next_owner")

    artifact = sample.get("artifact_plan", {})
    if artifact.get("write_requested_by_user") is not True:
        fail("artifact_plan 必须声明用户请求写入")
    if artifact.get("overwrite_existing") is not False:
        fail("artifact_plan golden sample 不应覆盖已有文件")
    if artifact.get("private_data_check") is not True:
        fail("artifact_plan 必须包含隐私检查")

    print("project competitive strategy 检查通过")


if __name__ == "__main__":
    main()
