#!/usr/bin/env python3
"""检查旧 Claude Code think-tank 是否完成迁移处置。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"

FILES = [
    THINK_TANK / "docs" / "legacy-think-tank-full-migration.md",
    THINK_TANK / "docs" / "legacy-runtime-safety.md",
    THINK_TANK / "platforms" / "claude-code" / "legacy-team-runtime.md",
    THINK_TANK / "runtime" / "safety.py",
    THINK_TANK / "templates" / "deep-research.md",
    THINK_TANK / "templates" / "expert-meeting.md",
    THINK_TANK / "templates" / "task-kickoff.md",
]

MIGRATION_TERMS = [
    "legacy_think_tank_migration: complete",
    "abstracted_not_copied",
    "core_protocol_dependency_on_legacy: none",
    "full_team_runtime_status: not_verified",
    "不得声明",
    "adapter_dispatch_runtime",
    "automatic_recovery",
    "true_multi_agent_runtime",
]


def fail(message: str) -> None:
    raise SystemExit(f"legacy think-tank 迁移检查失败: {message}")


def main() -> None:
    missing = [path for path in FILES if not path.exists()]
    if missing:
        fail("缺少迁移文件: " + ", ".join(str(path.relative_to(ROOT)) for path in missing))

    full_migration = (THINK_TANK / "docs" / "legacy-think-tank-full-migration.md").read_text(encoding="utf-8")
    legacy_runtime = (THINK_TANK / "platforms" / "claude-code" / "legacy-team-runtime.md").read_text(encoding="utf-8")
    combined = full_migration + "\n" + legacy_runtime

    for term in MIGRATION_TERMS:
        if term not in combined:
            fail(f"迁移文档缺少关键声明: {term}")

    forbidden_claims = [
        "adapter_dispatch_runtime: full_verified",
        "automatic_recovery: full_verified",
        "true_multi_agent_runtime: full_verified",
    ]
    for claim in forbidden_claims:
        if claim in combined:
            fail(f"不得声明完整验证: {claim}")

    print("legacy think-tank 迁移检查通过")


if __name__ == "__main__":
    main()
