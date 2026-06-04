#!/usr/bin/env python3
"""检查 Runtime Provenance Gate 协议、schema、样例、模板和 runtime result。"""

from __future__ import annotations

import json
from pathlib import Path

from example_paths import resolve_example_path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "think-tank" / "protocol" / "runtime-provenance.md"
SCHEMA = ROOT / "think-tank" / "schemas" / "runtime-provenance.schema.json"
RUNTIME_RESULT_SCHEMA = ROOT / "think-tank" / "schemas" / "runtime-result.schema.json"
SKILL = ROOT / "think-tank" / "SKILL.md"
QUALITY_GATES = ROOT / "think-tank" / "protocol" / "quality-gates.md"
SAMPLES = [
    ROOT / "think-tank" / "examples" / "runtime-provenance-direct-tool.json",
    ROOT / "think-tank" / "examples" / "runtime-provenance-full-runtime.json",
    ROOT / "think-tank" / "examples" / "runtime-provenance-single-agent.json",
]
RECIPE_FILES = [
    ROOT / "think-tank" / "recipes" / name
    for name in [
        "competitive-intelligence.md",
        "decision-council.md",
        "evidence-synthesis.md",
        "market-research.md",
        "media-research.md",
        "monitoring-plan.md",
        "project-memory-capture.md",
        "review-acceptance.md",
        "strategy-planning.md",
        "technical-research.md",
        "user-feedback-analysis.md",
    ]
]
TEMPLATE_FILES = [
    ROOT / "think-tank" / "templates" / name
    for name in [
        "council-state.md",
        "deep-research.md",
        "evidence-table.md",
        "expert-meeting.md",
        "monitoring-brief.md",
        "project-memory-candidate.md",
        "task-kickoff.md",
    ]
]


def fail(message: str) -> None:
    raise SystemExit(f"runtime provenance 检查失败: {message}")


def require_text(path: Path, terms: list[str]) -> str:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for term in terms:
        if term not in text:
            fail(f"{path.relative_to(ROOT)} 缺少: {term}")
    return text


def load_json(path: Path) -> dict:
    path = resolve_example_path(ROOT, path)
    if not path.exists():
        fail(f"缺少 JSON: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} 必须是 object")
    return data


def main() -> None:
    require_text(
        PROTOCOL,
        [
            "runtime_provenance",
            "direct_assistant_tool",
            "single_agent_multi_profile",
            "provider_invoked: false",
            "true_multi_agent_runtime: false",
            "direct_web_search_implies_source_acquisition_provider: false",
        ],
    )
    require_text(
        SKILL,
        [
            "runtime_provenance",
            "think_tank_runtime_used",
            "data_collection",
            "true_multi_agent_runtime",
        ],
    )
    require_text(
        QUALITY_GATES,
        [
            "Runtime Provenance",
            "runtime_provenance_present",
            "direct_assistant_tool",
        ],
    )

    schema = load_json(SCHEMA)
    for field in [
        "think_tank_runtime_used",
        "provider_policy_checked",
        "dispatch_decision_emitted",
        "provider_invoked",
        "result_recovered",
        "true_multi_agent_runtime",
        "execution_method",
        "data_collection",
        "evidence_state",
        "result_recovery",
        "boundaries",
    ]:
        if field not in schema["required"]:
            fail(f"runtime provenance schema 缺少 required 字段: {field}")
    if "direct_tool_call" not in schema["properties"]["execution_method"]["enum"]:
        fail("schema 必须支持 direct_tool_call")
    if "direct_assistant_tool" not in schema["properties"]["data_collection"]["enum"]:
        fail("schema 必须支持 direct_assistant_tool")

    runtime_result_schema = load_json(RUNTIME_RESULT_SCHEMA)
    if "runtime_provenance" not in runtime_result_schema["required"]:
        fail("runtime-result schema 必须要求 runtime_provenance")

    seen_methods = set()
    for sample_path in SAMPLES:
        sample = load_json(sample_path)
        missing = [field for field in schema["required"] if field not in sample]
        if missing:
            fail(f"{sample_path.relative_to(ROOT)} 缺少字段: {missing}")
        seen_methods.add(sample["execution_method"])
        if sample["execution_method"] == "direct_tool_call" and sample["data_collection"] != "direct_assistant_tool":
            fail("direct_tool_call 样例必须声明 direct_assistant_tool")
        if sample["execution_method"] == "single_agent_multi_profile" and sample["true_multi_agent_runtime"] is not False:
            fail("single_agent_multi_profile 样例不得声称真实多 agent")
    for method in ["direct_tool_call", "adapter_runtime", "single_agent_multi_profile"]:
        if method not in seen_methods:
            fail(f"缺少 runtime provenance 样例: {method}")

    for path in RECIPE_FILES + TEMPLATE_FILES:
        text = require_text(path, ["runtime_provenance"])
        if "true_multi_agent_runtime" not in text:
            fail(f"{path.relative_to(ROOT)} 缺少 true_multi_agent_runtime")

    print("runtime provenance 检查通过")


if __name__ == "__main__":
    main()
