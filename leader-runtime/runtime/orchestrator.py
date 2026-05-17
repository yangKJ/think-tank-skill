#!/usr/bin/env python3
"""Codex leader-runtime orchestrator.

This module is intentionally above the think-tank Skill runtime: it calls the
think-tank Codex adapter, then adds leader context, expert selection, task
packets, and acceptance governance around that Skill result.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


LEADER_RUNTIME_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = LEADER_RUNTIME_ROOT.parent
THINK_TANK_ROOT = REPO_ROOT / "think-tank"
THINK_TANK_CODEX_RUNTIME = THINK_TANK_ROOT / "platforms" / "codex" / "runtime"
sys.path.insert(0, str(THINK_TANK_CODEX_RUNTIME))
sys.path.insert(0, str(LEADER_RUNTIME_ROOT / "runtime"))

from leader_registry import (  # noqa: E402
    LEADER_ID,
    SCHEMA_CHECKS,
    build_acceptance_report,
    build_dispatch_decision,
    build_expert_task_packets,
    summarize_registry,
)
from project_team_activation import run_activation  # noqa: E402


def _load_think_tank_orchestrator():
    path = THINK_TANK_CODEX_RUNTIME / "orchestrator.py"
    spec = importlib.util.spec_from_file_location("think_tank_codex_orchestrator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load think-tank orchestrator at {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _capabilities_from_skill_result(skill_result: dict[str, Any]) -> list[str]:
    route = skill_result.get("policy_route", {})
    capabilities = route.get("selected_capabilities", [])
    return capabilities if isinstance(capabilities, list) else []


def _load_project_team_activation(team_pack_path: str | Path | None) -> dict[str, Any] | None:
    if team_pack_path is None:
        return None
    return run_activation(Path(team_pack_path))


def _leader_context_from_dispatch(
    dispatch_decision: dict[str, Any],
    project_team_activation: dict[str, Any] | None,
) -> dict[str, Any]:
    context: dict[str, Any] = {
        "leader_id": LEADER_ID,
        "execution_decision": dispatch_decision["selected_path"],
        "selected_profiles": dispatch_decision["selected_profiles"],
    }
    if project_team_activation is not None:
        context["project_team"] = {
            "project_id": project_team_activation["project_id"],
            "pack_id": project_team_activation["pack_id"],
            "active_count": project_team_activation["active_count"],
            "global_experts": project_team_activation["global_experts"],
            "candidate_agents": project_team_activation["candidate_agents"],
            "verification_status": project_team_activation["verification_status"],
        }
    return context


def run_leader_orchestrator(
    request: str,
    target: str | None = None,
    write_run: bool = False,
    team_pack_path: str | Path | None = None,
) -> dict[str, Any]:
    think_tank_orchestrator = _load_think_tank_orchestrator()
    skill_result = think_tank_orchestrator.run_orchestrator(
        request,
        target=target,
        write_run=write_run,
    )
    mode = skill_result.get("mode", "council")
    route = skill_result.get("policy_route", {})
    capabilities = _capabilities_from_skill_result(skill_result)
    dispatch_decision = build_dispatch_decision(
        request,
        mode,
        route.get("selected_intent"),
        capabilities,
        platform_supports_subagents=False,
    )
    project_team_activation = _load_project_team_activation(team_pack_path)
    packets = build_expert_task_packets(
        request,
        mode,
        capabilities,
        dispatch_decision["selected_experts"],
    )
    acceptance_report = build_acceptance_report(
        checked_results=["think_tank_skill_result", "dispatch_decision"],
        passed_checks=list(SCHEMA_CHECKS),
        failed_checks=[],
        delegation_needed=dispatch_decision["delegation_needed"],
    )
    boundaries = [
        "leader-runtime is the caller; think-tank remains a Skill result provider.",
        "Current leader execution still uses fallback-style expert packets until verified subagent dispatch is added.",
    ]
    if project_team_activation is not None:
        boundaries.append("Project team activation loads roster entries only; candidate agents remain promoted_uninvoked.")
    result = {
        "runtime": "leader-runtime-codex-orchestrator",
        "leader_context": _leader_context_from_dispatch(dispatch_decision, project_team_activation),
        "expert_registry_summary": summarize_registry(mode, route.get("selected_intent"), capabilities),
        "dispatch_decision": dispatch_decision,
        "expert_task_packets": packets,
        "acceptance_report": acceptance_report,
        "think_tank_skill_result": skill_result,
        "boundaries": boundaries,
    }
    if project_team_activation is not None:
        result["project_team_activation"] = project_team_activation
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Codex leader-runtime orchestrator.")
    parser.add_argument("request")
    parser.add_argument("--target", default=None)
    parser.add_argument("--write-run", action="store_true")
    parser.add_argument("--team-pack", default=None, help="Optional promoted project team pack YAML.")
    args = parser.parse_args()
    print(
        json.dumps(
            run_leader_orchestrator(args.request, args.target, args.write_run, team_pack_path=args.team_pack),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
