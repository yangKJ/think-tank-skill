#!/usr/bin/env python3
"""检查 v3.0 Skill Experience Layer 是否完整。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "think-tank/protocol/skill-trigger-intelligence.md",
    "think-tank/protocol/skill-invocation-contract.md",
    "think-tank/protocol/progressive-disclosure.md",
    "think-tank/docs/agent-compatibility-matrix.md",
    "think-tank/docs/skill-composition-guide.md",
    "think-tank/docs/skill-quality-score.md",
    "think-tank/docs/v3.0-roadmap.md",
    "think-tank/docs/v3.0-release-notes.md",
    "think-tank/examples/v3/skill-route-decision.json",
    "think-tank/examples/v3/skill-invocation-contract.json",
    "think-tank/examples/v3/progressive-disclosure-plan.json",
    "think-tank/examples/v3/skill-self-test-result.json",
    "think-tank/examples/v3/skill-quality-score.json",
    "self-tests/README.md",
    "self-tests/research-trigger.json",
    "self-tests/anti-trigger-simple-command.json",
    "self-tests/provider-boundary.json",
    "self-tests/run-record-memory.json",
    "self-tests/composition-guide.json",
]


REQUIRED_TEXT = {
    "think-tank/protocol/skill-trigger-intelligence.md": [
        "not a built-in trigger-word table",
        "user-owned routing policy",
        "skill_route_decision",
        "trigger_status: example_only",
    ],
    "think-tank/protocol/skill-invocation-contract.md": [
        "think_tank_invocation",
        "provider_permissions",
        "progressive_disclosure_refs",
        "route_selected:",
        "policy_source: protocol_default",
    ],
    "think-tank/protocol/progressive-disclosure.md": [
        "Load only the smallest reference set",
        "SKILL.md",
        "progressive_disclosure_plan",
        "treating example trigger phrases as installed triggers",
    ],
    "think-tank/docs/agent-compatibility-matrix.md": [
        "Codex",
        "Claude Code",
        "Generic Agent",
        "intent inference != trigger policy",
    ],
    "think-tank/docs/skill-composition-guide.md": [
        "think-tank is the coordinating skill",
        "peer skills",
        "selection is not invocation",
    ],
    "think-tank/docs/skill-quality-score.md": [
        "Trigger clarity",
        "no hard-coded public trigger words",
        "stable skill experience",
    ],
    "think-tank/docs/v3.0-roadmap.md": [
        "Skill Experience Layer",
        "no built-in project-specific trigger words",
        "checks/skill_experience_check.py",
    ],
    "think-tank/docs/v3.0-release-notes.md": [
        "Skill Experience Layer",
        "user YAML policy owns actual trigger",
        "progressive disclosure",
    ],
}


REQUIRED_LINK_TARGETS = [
    "think-tank/protocol/skill-trigger-intelligence.md",
    "think-tank/protocol/skill-invocation-contract.md",
    "think-tank/protocol/progressive-disclosure.md",
    "think-tank/docs/agent-compatibility-matrix.md",
    "think-tank/docs/skill-composition-guide.md",
    "think-tank/docs/skill-quality-score.md",
    "think-tank/docs/v3.0-roadmap.md",
    "think-tank/docs/v3.0-release-notes.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"skill experience check 失败: {message}")


def read_text(path: str) -> str:
    full_path = ROOT / path
    if not full_path.exists():
        fail(f"缺少文件: {path}")
    return full_path.read_text(encoding="utf-8")


def check_files() -> None:
    for path in REQUIRED_FILES:
        full_path = ROOT / path
        if not full_path.exists():
            fail(f"缺少文件: {path}")


def check_required_text() -> None:
    for path, snippets in REQUIRED_TEXT.items():
        content = read_text(path)
        for snippet in snippets:
            if snippet not in content:
                fail(f"{path} 缺少关键文本: {snippet}")


def check_json_examples() -> None:
    for path in REQUIRED_FILES:
        if not path.endswith(".json"):
            continue
        full_path = ROOT / path
        try:
            json.loads(full_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"{path} 不是合法 JSON: {exc}")

    route = json.loads((ROOT / "think-tank/examples/v3/skill-route-decision.json").read_text(encoding="utf-8"))
    decision = route.get("skill_route_decision", {})
    if decision.get("trigger_status") != "inferred_intent_only":
        fail("skill-route-decision.json 必须声明 trigger_status=inferred_intent_only")
    if decision.get("policy_source") == "built_in":
        fail("skill-route-decision.json 不能声明 built_in policy")

    provider_case = json.loads((ROOT / "self-tests/provider-boundary.json").read_text(encoding="utf-8"))
    provider_state = provider_case.get("expected_provider_state", {})
    if provider_state.get("invoked_providers") != []:
        fail("provider-boundary.json 必须保持 invoked_providers 为空")


def check_navigation_links() -> None:
    combined = "\n".join(
        [
            read_text("README.md"),
            read_text("README_CN.md"),
            read_text("CHANGELOG.md"),
            read_text("think-tank/SKILL.md"),
            read_text("think-tank/protocol/README.md"),
            read_text("think-tank/docs/index.md"),
            read_text("think-tank/examples/README.md"),
            read_text("public-release-manifest.yaml"),
        ]
    )
    for target in REQUIRED_LINK_TARGETS:
        if target not in combined:
            fail(f"导航未引用: {target}")
    if "skill_self_tests" not in combined:
        fail("public-release-manifest.yaml 需要包含 skill_self_tests")


def main() -> None:
    check_files()
    check_required_text()
    check_json_examples()
    check_navigation_links()
    print("skill experience check 通过")


if __name__ == "__main__":
    main()
