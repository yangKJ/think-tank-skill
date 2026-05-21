#!/usr/bin/env python3
"""检查旧 agent-council 是否完成全量迁移处置。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"

DOCS = [
    THINK_TANK / "docs" / "v0.4-agent-council-migration.md",
    THINK_TANK / "docs" / "agent-council-full-inventory.md",
    THINK_TANK / "docs" / "agent-council-runtime-migration.md",
    THINK_TANK / "docs" / "agent-council-history-index.md",
    THINK_TANK / "runtime" / "council.py",
    THINK_TANK / "templates" / "council-state.md",
]

REFERENCE_FILES = [
    "references/agents.md",
    "references/scenes.md",
    "references/steps.md",
    "references/format.md",
    "references/state_contract.md",
]

SCRIPT_ITEMS = [
    "scripts/state_manager.py",
    "scripts/state/atomic_writer.py",
    "scripts/state/circuit_breaker.py",
    "scripts/coordinator/round_coordinator.py",
    "scripts/research/*.py",
    "scripts/registry/agent_registry.py",
    "scripts/observability/observer.py",
    "scripts/discussion.sh",
    "scripts/merge.sh",
    "scripts/monitor.sh",
]

HISTORY_ITEMS = [
    "agent_selection_review.md",
    "auto_execution_test/",
    "collab_review.md",
    "collab_skill_review.md",
    "collect-cr.md",
    "council_v2_issues_review",
    "council_v77_review.md",
    "council_v791_review.md",
    "council_workflow_optimization.md",
    "doc_location_review.md",
    "project-codex-sample/",
    "project-prompt-sample/",
    "multi_agent_research_design/",
    "self_healing_review/",
    "skill-review.md",
    "skill_naming_review.md",
    "v76_test/",
    "v78_test.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"agent-council 全量迁移检查失败: {message}")


def main() -> None:
    missing = [path for path in DOCS if not path.exists()]
    if missing:
        fail("缺少文件: " + ", ".join(str(path.relative_to(ROOT)) for path in missing))

    inventory = (THINK_TANK / "docs" / "agent-council-full-inventory.md").read_text(encoding="utf-8")
    runtime = (THINK_TANK / "docs" / "agent-council-runtime-migration.md").read_text(encoding="utf-8")
    history = (THINK_TANK / "docs" / "agent-council-history-index.md").read_text(encoding="utf-8")
    v04 = (THINK_TANK / "docs" / "v0.4-agent-council-migration.md").read_text(encoding="utf-8")

    for item in REFERENCE_FILES:
        if item not in inventory:
            fail(f"旧 reference 未处置: {item}")
    for item in SCRIPT_ITEMS:
        if item not in inventory:
            fail(f"旧 script 未处置: {item}")
    for item in HISTORY_ITEMS:
        if item not in history:
            fail(f"旧 history 未处置: {item}")

    combined = inventory + "\n" + runtime + "\n" + history + "\n" + v04
    required_status = [
        "agent_council_migration: complete",
        "agent_council_parallel_brand_status: removed",
        "legacy_assets_without_disposition: 0",
        "core_protocol_dependency_on_ios_automation_mcp: none",
        "references_disposed: 5",
        "scripts_disposed: true",
        "history_items_disposed: true",
        "full_claude_code_team_runtime_verified: false",
    ]
    for term in required_status:
        if term not in combined:
            fail(f"缺少完成状态: {term}")

    forbidden = [
        "full_claude_code_team_runtime_verified: true",
        "core_protocol_dependency_on_ios_automation_mcp: true",
    ]
    for term in forbidden:
        if term in combined:
            fail(f"出现禁止声明: {term}")

    print("agent-council 全量迁移检查通过")


if __name__ == "__main__":
    main()
