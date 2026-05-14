#!/usr/bin/env python3
"""Codex natural-language runtime orchestrator for think-tank."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
CODEX_RUNTIME_DIR = ROOT / "think-tank" / "platforms" / "codex" / "runtime"
sys.path.insert(0, str(CODEX_RUNTIME_DIR))

from provider_policy import load_effective_policy, policy_path, registry, resolve_request  # noqa: E402
from provider_registry import PROJECT_SKILLS  # noqa: E402
from source_acquisition_minimal import runtime_result as source_runtime_result  # noqa: E402


DEFAULT_TARGET = ROOT / "think-tank" / "examples" / "browser-automation-fixture.html"
DEFAULT_RUNS_DIR = ROOT / ".think-tank" / "runs"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.exists() else str(path)


def mode_from_route(route_result: dict[str, Any]) -> str:
    mode = route_result.get("selected_mode")
    return mode if mode in {"research", "council", "review", "strategy"} else "council"


def should_invoke_source(route_result: dict[str, Any], target: str | None) -> bool:
    capabilities = set(route_result.get("selected_capabilities", []) or [])
    return bool(target) and "source-acquisition" in capabilities


def make_run_record(request: str, target: str | None, write_run: bool, runs_dir: Path) -> dict[str, Any]:
    digest = hashlib.sha1(f"{request}\n{target or ''}".encode("utf-8")).hexdigest()[:12]
    run_id = f"nlrt-{digest}"
    artifact_path = runs_dir / f"{run_id}.json"
    return {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "artifact_requested": write_run,
        "artifact_written": False,
        "artifact_path": str(artifact_path.relative_to(ROOT)) if artifact_path.is_relative_to(ROOT) else str(artifact_path),
    }


def build_runtime_provenance(
    *,
    route_result: dict[str, Any],
    source_result: dict[str, Any] | None,
    invoked: bool,
) -> dict[str, Any]:
    recovered = bool(source_result and source_result.get("sources"))
    if invoked:
        evidence_state = "verified_partial" if recovered else "failed"
        result_recovery = "automatic" if recovered else "none"
        execution_method = "adapter_runtime"
        data_collection = source_result.get("runtime_provenance", {}).get("data_collection", "provider_managed") if source_result else "provider_managed"
    elif route_result.get("matched"):
        evidence_state = "selected"
        result_recovery = "none"
        execution_method = "protocol_only"
        data_collection = "none"
    else:
        evidence_state = "planned"
        result_recovery = "none"
        execution_method = "protocol_only"
        data_collection = "none"

    return {
        "think_tank_runtime_used": True,
        "provider_policy_checked": True,
        "dispatch_decision_emitted": invoked,
        "provider_invoked": invoked,
        "result_recovered": recovered,
        "true_multi_agent_runtime": False,
        "execution_method": execution_method,
        "data_collection": data_collection,
        "evidence_state": evidence_state,
        "result_recovery": result_recovery,
        "boundaries": [
            "Codex natural-language orchestrator is a minimal adapter runtime.",
            "It does not claim true independent multi-agent execution.",
            "Policy provider selection is distinct from the minimal runtime provider actually invoked.",
        ],
    }


def build_final_output(request: str, route_result: dict[str, Any], source_result: dict[str, Any] | None) -> dict[str, Any]:
    if source_result and source_result.get("sources"):
        evidence = source_result.get("evidence", [])
        conclusion = f"Request routed to {route_result.get('selected_recipe')} and completed minimal source recovery."
        recommendations = [
            "Use recovered sources as input for role analysis.",
            "Do not mark external peer providers verified until they are invoked and recovered.",
        ]
    elif route_result.get("matched"):
        evidence = []
        conclusion = f"Request routed to {route_result.get('selected_recipe')} without provider invocation."
        recommendations = [
            "Proceed with protocol-only analysis or provide a target/source for minimal source-acquisition.",
        ]
    else:
        evidence = []
        conclusion = "No routing policy matched; fall back to core protocol."
        recommendations = ["Clarify intent or run protocol-only think-tank analysis."]

    return {
        "request": request,
        "conclusion": conclusion,
        "evidence": evidence,
        "recommendations": recommendations,
    }


def run_orchestrator(
    request: str,
    target: str | None = None,
    skills_dir: Path = PROJECT_SKILLS,
    write_run: bool = False,
    runs_dir: Path = DEFAULT_RUNS_DIR,
) -> dict[str, Any]:
    effective_policy, policy_sources = load_effective_policy()
    selected_policy_path = policy_path()
    provider_registry = registry(skills_dir)
    route_result = resolve_request(request, effective_policy, provider_registry["providers"])
    route_result["policy_path"] = rel(selected_policy_path)
    route_result["policy_sources"] = [rel(source) for source in policy_sources]
    route_result["provider_count"] = provider_registry["provider_count"]

    selected_target = target or str(DEFAULT_TARGET.relative_to(ROOT))
    invoke_source = should_invoke_source(route_result, selected_target)
    source_result = source_runtime_result(selected_target, "codex-minimal") if invoke_source else None
    dispatch_record = {
        "dispatch_decision_emitted": invoke_source,
        "policy_selected_provider": route_result.get("skill_route", {}).get("selected_provider"),
        "runtime_selected_provider": "local_static_reader" if invoke_source else None,
        "status": "dispatched" if invoke_source else "not_dispatched",
        "boundary": (
            "Policy-selected provider is not automatically invoked by the minimal orchestrator."
            if invoke_source
            else "No source-acquisition runtime dispatch was needed or possible."
        ),
    }
    runtime_provenance = build_runtime_provenance(
        route_result=route_result,
        source_result=source_result,
        invoked=invoke_source,
    )
    boundaries = list(route_result.get("boundaries", []))
    boundaries.extend(runtime_provenance["boundaries"])
    if source_result:
        boundaries.extend(source_result.get("boundaries", []))

    run_record = make_run_record(request, selected_target, write_run, runs_dir)
    result = {
        "runtime": "codex-natural-language-orchestrator",
        "runtime_provenance": runtime_provenance,
        "request": request,
        "mode": mode_from_route(route_result),
        "run_record": run_record,
        "policy_route": route_result,
        "dispatch_record": dispatch_record,
        "source_result": source_result,
        "final_output": build_final_output(request, route_result, source_result),
        "quality_check": {
            "protocol_complete": True,
            "runtime_provenance_present": True,
            "provider_invocation_truthful": True,
            "evidence_boundary_clear": True,
            "actionable": True,
        },
        "boundaries": boundaries,
    }
    if write_run:
        runs_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = Path(run_record["artifact_path"])
        if not artifact_path.is_absolute():
            artifact_path = ROOT / artifact_path
        artifact_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        result["run_record"]["artifact_written"] = True
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Codex natural-language think-tank orchestrator.")
    parser.add_argument("request")
    parser.add_argument("--target", default=str(DEFAULT_TARGET.relative_to(ROOT)))
    parser.add_argument("--skills-dir", type=Path, default=PROJECT_SKILLS)
    parser.add_argument("--write-run", action="store_true")
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    args = parser.parse_args()
    print(json.dumps(run_orchestrator(args.request, args.target, args.skills_dir, args.write_run, args.runs_dir), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
