#!/usr/bin/env python3
"""检查 Codex 领导者编排第一批契约。"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"
LEADER_RUNTIME = ROOT / "leader-runtime"
LEADER_REGISTRY = LEADER_RUNTIME / "runtime" / "leader_registry.py"


def fail(message: str) -> None:
    raise SystemExit(f"leader orchestration 检查失败: {message}")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"无法加载模块: {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def require_json(path: Path, required: list[str]) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} 必须是 object")
    for field in required:
        if field not in data:
            fail(f"{path.relative_to(ROOT)} 缺少字段: {field}")
    return data


def main() -> None:
    required_files = [
        LEADER_RUNTIME / "docs" / "codex-leader-orchestration-blueprint.md",
        LEADER_RUNTIME / "schemas" / "expert-role-registry.schema.json",
        LEADER_RUNTIME / "schemas" / "dispatch-decision.schema.json",
        LEADER_RUNTIME / "schemas" / "expert-task-packet.schema.json",
        LEADER_RUNTIME / "schemas" / "acceptance-report.schema.json",
        LEADER_RUNTIME / "templates" / "expert-task-packet.md",
        LEADER_RUNTIME / "templates" / "acceptance-report.md",
        LEADER_REGISTRY,
    ]
    for path in required_files:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")

    schema_required = {
        "expert-role-registry.schema.json": ["registry_id", "owner", "scope", "experts"],
        "dispatch-decision.schema.json": ["leader_id", "task_shape", "delegation_needed", "selected_path"],
        "expert-task-packet.schema.json": ["task_id", "leader_id", "expert_id", "mapped_role"],
        "acceptance-report.schema.json": ["acceptance_id", "leader_id", "status", "next_action"],
    }
    for name, fields in schema_required.items():
        data = require_json(LEADER_RUNTIME / "schemas" / name, ["required"])
        for field in fields:
            if field not in data["required"]:
                fail(f"{name} required 缺少: {field}")

    module = load_module(LEADER_REGISTRY, "think_tank_codex_leader_registry")
    registry = module.registry_payload()
    if registry["scope"] != "global":
        fail("registry_payload().scope 必须是 global")
    summary = module.summarize_registry("research", "competitive_intelligence", ["source-acquisition"])
    if not summary["candidate_experts"]:
        fail("summarize_registry 必须返回 candidate_experts")
    decision = module.build_dispatch_decision(
        "竞品分析 Cursor 和 Codex",
        "research",
        "competitive_intelligence",
        ["source-acquisition", "social-listening"],
        platform_supports_subagents=False,
    )
    if decision["selected_path"] != "single_agent_multi_profile_fallback":
        fail("当前 Codex fallback 路径必须是 single_agent_multi_profile_fallback")
    packets = module.build_expert_task_packets(
        "竞品分析 Cursor 和 Codex",
        "research",
        ["source-acquisition"],
        decision["selected_experts"],
    )
    if not packets:
        fail("build_expert_task_packets 必须返回至少一个 packet")
    report = module.build_acceptance_report(["dispatch_decision"], ["schema_complete"], [], delegation_needed=True)
    if report["status"] != "passed":
        fail("有 passed_checks 且无 failed_checks 时 acceptance status 必须是 passed")

    print("leader orchestration 检查通过")


if __name__ == "__main__":
    main()
