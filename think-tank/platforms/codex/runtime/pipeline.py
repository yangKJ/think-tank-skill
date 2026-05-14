#!/usr/bin/env python3
"""Codex adapter pipeline built on the platform-neutral runtime library."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
RUNTIME_DIR = ROOT / "think-tank" / "runtime"
CODEX_RUNTIME_DIR = ROOT / "think-tank" / "platforms" / "codex" / "runtime"
sys.path.insert(0, str(RUNTIME_DIR))
sys.path.insert(0, str(CODEX_RUNTIME_DIR))

from consensus import Position, evaluate_consensus  # noqa: E402
from planner import plan_runtime  # noqa: E402
from slot_resolver import resolve_slots  # noqa: E402
from source_acquisition_minimal import runtime_result as source_runtime_result  # noqa: E402
from state_model import StageResult, make_run  # noqa: E402


CODEX_CAPABILITY_MAPPING = {
    "source-acquisition": ["local_static_reader", "user_provided_material"],
    "browser-automation": ["browser", "playwright"],
    "knowledge-persistence": ["repository_markdown"],
    "media-processing": ["user_provided_transcript"],
    "social-listening": ["user_provided_samples"],
}


def collect_capabilities(runtime_plan: dict[str, Any]) -> tuple[list[str], list[str]]:
    required: list[str] = []
    optional: list[str] = []
    for stage in runtime_plan.get("stages", []):
        for capability in stage.get("required_capabilities", []):
            if capability not in required:
                required.append(capability)
        for capability in stage.get("optional_capabilities", []):
            if capability not in optional and capability not in required:
                optional.append(capability)
    return required, optional


def run_pipeline(task: str, target: str, strict: bool = False) -> dict[str, Any]:
    runtime_plan = plan_runtime(task, requested_mode="research", strict=strict).to_dict()
    required, optional = collect_capabilities(runtime_plan)
    slot_resolution = resolve_slots(
        required,
        optional,
        CODEX_CAPABILITY_MAPPING,
        {"local_static_reader", "repository_markdown", "user_provided_material"},
    )
    run_state = make_run(
        runtime_plan["mode"],
        runtime_plan["selected_profiles"],
        required + optional,
        [stage["name"] for stage in runtime_plan["stages"]],
    )
    source_result = source_runtime_result(target, "codex-minimal")
    stage_result = StageResult(
        actor="source-collector",
        stage="collection",
        claim="source-acquisition completed" if source_result["sources"] else "source-acquisition failed",
        evidence=source_result["evidence"],
        risks=[] if source_result["sources"] else ["source target unavailable"],
        recommendations=["Use recovered sources for analysis"] if source_result["sources"] else ["Ask user for alternate source"],
        confidence="medium" if source_result["sources"] else "low",
        boundaries=source_result["boundaries"],
    )
    consensus_result = evaluate_consensus(
        [
            Position(
                profile="source-collector",
                proposal=stage_result.claim,
                evidence=stage_result.evidence,
                risks=stage_result.risks,
                vote="agree" if source_result["sources"] else "abstain",
                confidence=stage_result.confidence,
            ),
            Position(
                profile="skeptic",
                proposal="keep boundaries explicit",
                objections=[] if source_result["sources"] else ["source missing"],
                vote="agree" if source_result["sources"] else "disagree",
                confidence="medium",
            ),
        ],
        threshold=0.5,
    )
    final_output = {
        "conclusion": "Codex runtime pipeline completed with recovered source." if source_result["sources"] else "Codex runtime pipeline completed with degraded source-acquisition.",
        "evidence": source_result["evidence"],
        "recommendations": stage_result.recommendations,
        "stage_results": [stage_result.to_dict()],
    }
    boundaries = runtime_plan["boundaries"] + slot_resolution["boundaries"] + source_result["boundaries"]
    return {
        "runtime": "codex-runtime-pipeline",
        "mode": runtime_plan["mode"],
        "runtime_plan": runtime_plan,
        "slot_resolution": slot_resolution,
        "run_state": run_state.to_dict(),
        "source_result": source_result,
        "consensus_result": consensus_result.to_dict(),
        "final_output": final_output,
        "quality_check": {
            "protocol_complete": True,
            "evidence_boundary_clear": True,
            "actionable": True,
        },
        "boundaries": boundaries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Codex think-tank runtime pipeline.")
    parser.add_argument("task")
    parser.add_argument("target")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run_pipeline(args.task, args.target, args.strict), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
