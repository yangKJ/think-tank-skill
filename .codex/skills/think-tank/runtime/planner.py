#!/usr/bin/env python3
"""Platform-neutral runtime planner for think-tank."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


MODE_TRIGGERS = {
    "research": ["深度调研", "协作调研", "团队调研", "研究", "research"],
    "council": ["开会", "讨论", "审议", "council"],
    "review": ["评审", "审核", "review"],
    "strategy": ["策略", "路线", "strategy"],
}


MODE_CAPABILITIES = {
    "research": {
        "required": ["source-acquisition"],
        "optional": ["browser-automation", "knowledge-persistence"],
    },
    "council": {
        "required": [],
        "optional": ["source-acquisition"],
    },
    "review": {
        "required": [],
        "optional": ["source-acquisition"],
    },
    "strategy": {
        "required": [],
        "optional": ["source-acquisition", "knowledge-persistence"],
    },
}


MODE_PROFILES = {
    "research": ["source-collector", "trend-analyst", "skeptic", "report-architect"],
    "council": ["facilitator", "product-strategist", "skeptic", "feedback-synthesizer"],
    "review": ["skeptic", "report-architect", "product-strategist"],
    "strategy": ["product-strategist", "trend-analyst", "skeptic", "report-architect"],
}


@dataclass(frozen=True)
class StagePlan:
    name: str
    max_rounds: int
    load_mode: str
    required_capabilities: list[str]
    optional_capabilities: list[str]
    expected_output: list[str]
    failure_behavior: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RuntimePlan:
    mode: str
    selected_profiles: list[str]
    priority: str
    complexity: str
    strict: bool
    fallback_behavior: str
    stages: list[StagePlan]
    boundaries: list[str]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["stages"] = [stage.to_dict() for stage in self.stages]
        return data


def resolve_mode(task: str, requested_mode: str | None = None, strict: bool = False) -> tuple[str, list[str]]:
    """Resolve mode from requested mode or trigger words."""
    boundaries: list[str] = []
    if requested_mode:
        if requested_mode not in MODE_TRIGGERS:
            if strict:
                raise ValueError(f"unknown mode: {requested_mode}")
            boundaries.append(f"Unknown requested mode '{requested_mode}', fallback to research.")
            return "research", boundaries
        return requested_mode, boundaries

    for mode, triggers in MODE_TRIGGERS.items():
        if any(trigger in task for trigger in triggers):
            return mode, boundaries

    if strict:
        raise ValueError("no mode trigger matched in strict mode")
    boundaries.append("No explicit mode trigger matched; fallback to research.")
    return "research", boundaries


def infer_complexity(task: str) -> str:
    deep_markers = ["深度", "长期", "战略", "多渠道", "竞品", "系统", "架构"]
    if any(marker in task for marker in deep_markers) or len(task) > 80:
        return "high"
    return "medium"


def plan_runtime(task: str, requested_mode: str | None = None, strict: bool = False) -> RuntimePlan:
    """Build a minimal runtime plan from a task."""
    mode, boundaries = resolve_mode(task, requested_mode=requested_mode, strict=strict)
    complexity = infer_complexity(task)
    priority = "high" if complexity == "high" else "medium"
    caps = MODE_CAPABILITIES[mode]
    stages = [
        StagePlan(
            name="collection",
            max_rounds=1,
            load_mode="standard",
            required_capabilities=caps["required"],
            optional_capabilities=caps["optional"],
            expected_output=["sources[]", "evidence[]", "boundaries[]"],
            failure_behavior="degrade_or_stop_for_missing_required",
        ),
        StagePlan(
            name="analysis",
            max_rounds=1,
            load_mode="standard",
            required_capabilities=[],
            optional_capabilities=[],
            expected_output=["role_views[]", "risks[]"],
            failure_behavior="synthesize_partial",
        ),
        StagePlan(
            name="synthesis",
            max_rounds=1,
            load_mode="standard",
            required_capabilities=[],
            optional_capabilities=[],
            expected_output=["conclusion", "recommendations[]", "quality_check"],
            failure_behavior="output_boundaries",
        ),
    ]
    return RuntimePlan(
        mode=mode,
        selected_profiles=MODE_PROFILES[mode],
        priority=priority,
        complexity=complexity,
        strict=strict,
        fallback_behavior="ask_for_clarification" if strict else "use_default_mode",
        stages=stages,
        boundaries=boundaries,
    )


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Plan a think-tank runtime.")
    parser.add_argument("task")
    parser.add_argument("--mode")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    print(json.dumps(plan_runtime(args.task, args.mode, args.strict).to_dict(), ensure_ascii=False, indent=2))
