"""Platform-neutral council state helpers migrated from legacy agent-council."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class CouncilPhase(str, Enum):
    INTAKE = "intake"
    COLLECT = "collect"
    DISCUSS = "discuss"
    CONCLUDE = "conclude"
    COMPLETE = "complete"


PHASE_TO_PROTOCOL_STAGE = {
    CouncilPhase.INTAKE: "intake",
    CouncilPhase.COLLECT: "collection",
    CouncilPhase.DISCUSS: "deliberation",
    CouncilPhase.CONCLUDE: "synthesis",
    CouncilPhase.COMPLETE: "quality_check",
}


@dataclass(frozen=True)
class CouncilState:
    topic: str
    phase: CouncilPhase = CouncilPhase.INTAKE
    round: int = 0
    agents: list[str] = field(default_factory=list)
    agents_completed: list[str] = field(default_factory=list)
    consensus_level: str = "none"
    consensus_support: float = 0.0
    final_decision: str | None = None
    high_risk_operation: bool = False
    boundaries: list[str] = field(default_factory=list)
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["phase"] = self.phase.value
        data["protocol_stage"] = PHASE_TO_PROTOCOL_STAGE[self.phase]
        return data


def create_council_state(topic: str, agents: list[str], high_risk: bool = False) -> CouncilState:
    if not topic.strip():
        raise ValueError("topic is required")
    if len(agents) < 2:
        raise ValueError("council mode requires at least two agents")
    return CouncilState(topic=topic, phase=CouncilPhase.COLLECT, agents=list(agents), high_risk_operation=high_risk)


def all_agents_completed(state: CouncilState) -> bool:
    return set(state.agents).issubset(set(state.agents_completed))


def next_phase(state: CouncilState) -> CouncilPhase:
    if state.phase == CouncilPhase.INTAKE:
        return CouncilPhase.COLLECT
    if state.phase == CouncilPhase.COLLECT:
        return CouncilPhase.DISCUSS if all_agents_completed(state) else CouncilPhase.COLLECT
    if state.phase == CouncilPhase.DISCUSS:
        if state.consensus_level in {"L1", "L3"}:
            return CouncilPhase.CONCLUDE
        return CouncilPhase.DISCUSS
    if state.phase == CouncilPhase.CONCLUDE:
        return CouncilPhase.COMPLETE
    return CouncilPhase.COMPLETE


def should_trigger_l3(state: CouncilState, max_rounds: int = 10) -> bool:
    if state.consensus_level == "L3":
        return True
    if state.round >= max_rounds and state.consensus_support < 0.6:
        return True
    if state.round >= 8 and state.consensus_support < 0.5:
        return True
    if state.high_risk_operation and state.round >= 3 and state.consensus_support < 0.6:
        return True
    return False


def classify_consensus(support: float, round_number: int, max_rounds: int = 10, has_blocking_objection: bool = False) -> str:
    if support >= 0.6 and not has_blocking_objection:
        return "L1"
    if round_number >= max_rounds or (round_number >= 8 and support < 0.5):
        return "L3"
    return "L2"


def build_synthesis_payload(
    consensus: list[str],
    disagreements: list[dict[str, str]],
    recommendations: list[str],
    final_decision: str | None = None,
) -> dict[str, Any]:
    return {
        "consensus": consensus,
        "disagreements": disagreements,
        "final_decision": final_decision,
        "recommendations": recommendations,
        "boundaries": [
            "synthesis payload is platform-neutral",
            "external state signatures are adapter responsibilities",
        ],
    }
