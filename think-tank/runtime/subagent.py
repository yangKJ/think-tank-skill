"""Specialist subagent runtime primitives for think-tank v0.5."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


PROFILE_CAPABILITY_HINTS = {
    "source-collector": ["source-acquisition"],
    "trend-analyst": ["source-acquisition"],
    "social-listener": ["social-listening"],
    "feedback-synthesizer": [],
    "report-architect": [],
    "skeptic": [],
    "product-strategist": [],
    "facilitator": [],
}

PROFILE_MISSION = {
    "source-collector": "Collect evidence, sources, gaps, and reliability boundaries.",
    "trend-analyst": "Identify trends, weak signals, market or technical implications.",
    "social-listener": "Analyze user/community/social feedback samples and sentiment boundaries.",
    "feedback-synthesizer": "Synthesize multiple voices into themes, disagreements, and priorities.",
    "report-architect": "Structure findings into decision-ready reports and recommendations.",
    "skeptic": "Challenge assumptions, verify claims, identify risks and blocking objections.",
    "product-strategist": "Translate evidence into product, strategy, priority, and roadmap judgment.",
    "facilitator": "Keep the process neutral, make disagreements explicit, and preserve decision quality.",
}

VALID_EXECUTION_METHODS = {
    "specialist_subagent",
    "single_agent_multi_profile_fallback",
    "external_platform_adapter",
}


@dataclass(frozen=True)
class SubagentTask:
    task_id: str
    profile: str
    mode: str
    objective: str
    input_context: list[str] = field(default_factory=list)
    required_capabilities: list[str] = field(default_factory=list)
    expected_output_schema: str = "role-result"
    independence_boundary: str = "Run in an isolated profile context when platform supports it."

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RoleResult:
    profile: str
    execution_method: str
    claim: str
    evidence: list[str] = field(default_factory=list)
    sources: list[dict[str, Any]] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    objections: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    confidence: str = "medium"
    boundaries: list[str] = field(default_factory=list)
    status: str = "completed"

    def __post_init__(self) -> None:
        if self.execution_method not in VALID_EXECUTION_METHODS:
            raise ValueError(f"invalid execution_method: {self.execution_method}")
        if self.confidence not in {"low", "medium", "high"}:
            raise ValueError(f"invalid confidence: {self.confidence}")
        if self.status not in {"completed", "partial", "failed", "blocked"}:
            raise ValueError(f"invalid status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubagentRuntimePlan:
    mode: str
    objective: str
    selected_profiles: list[str]
    dispatch_strategy: str
    tasks: list[SubagentTask]
    fallback_allowed: bool
    authority_level: str
    boundaries: list[str]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["tasks"] = [task.to_dict() for task in self.tasks]
        return data


def build_profile_prompt(task: SubagentTask) -> str:
    mission = PROFILE_MISSION.get(task.profile, "Apply the assigned think-tank profile.")
    capabilities = ", ".join(task.required_capabilities) or "none"
    context = "\n".join(f"- {item}" for item in task.input_context) or "- No extra context provided."
    return f"""You are the think-tank specialist profile: {task.profile}.

Mission:
{mission}

Mode:
{task.mode}

Objective:
{task.objective}

Required capabilities:
{capabilities}

Input context:
{context}

Return only a role-result object with:
- profile
- claim
- evidence[]
- sources[]
- risks[]
- objections[]
- recommendations[]
- confidence
- boundaries[]
- status
"""


def plan_subagent_runtime(
    mode: str,
    objective: str,
    profiles: list[str],
    platform_supports_subagents: bool,
    input_context: list[str] | None = None,
) -> SubagentRuntimePlan:
    if not profiles:
        raise ValueError("at least one profile is required")
    strategy = "parallel_specialist_subagents" if platform_supports_subagents else "single_agent_multi_profile_fallback"
    authority = "specialist_independent" if platform_supports_subagents else "lower_fallback_single_context"
    method_boundary = (
        "Each profile should run in an independent subagent context."
        if platform_supports_subagents
        else "Platform lacks verified subagent runtime; execute as single-agent multi-profile fallback."
    )
    context = input_context or []
    tasks = [
        SubagentTask(
            task_id=f"{mode}-{index + 1}-{profile}",
            profile=profile,
            mode=mode,
            objective=objective,
            input_context=context,
            required_capabilities=PROFILE_CAPABILITY_HINTS.get(profile, []),
        )
        for index, profile in enumerate(profiles)
    ]
    return SubagentRuntimePlan(
        mode=mode,
        objective=objective,
        selected_profiles=profiles,
        dispatch_strategy=strategy,
        tasks=tasks,
        fallback_allowed=True,
        authority_level=authority,
        boundaries=[method_boundary],
    )


def aggregate_role_results(results: list[RoleResult]) -> dict[str, Any]:
    if not results:
        return {
            "role_views": [],
            "evidence": [],
            "risks": ["No role results were produced."],
            "recommendations": [],
            "boundaries": ["No specialist result available."],
            "status": "failed",
        }
    return {
        "role_views": [result.to_dict() for result in results],
        "evidence": [item for result in results for item in result.evidence],
        "sources": [source for result in results for source in result.sources],
        "risks": [risk for result in results for risk in result.risks],
        "objections": [objection for result in results for objection in result.objections],
        "recommendations": [rec for result in results for rec in result.recommendations],
        "boundaries": [boundary for result in results for boundary in result.boundaries],
        "status": "partial" if any(result.status != "completed" for result in results) else "completed",
    }
