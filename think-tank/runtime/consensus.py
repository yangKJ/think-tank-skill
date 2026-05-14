#!/usr/bin/env python3
"""Minimal consensus evaluator for think-tank."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


VALID_VOTES = {"agree", "disagree", "abstain"}


@dataclass(frozen=True)
class Position:
    profile: str
    proposal: str
    evidence: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    objections: list[str] = field(default_factory=list)
    vote: str = "abstain"
    confidence: str = "medium"

    def __post_init__(self) -> None:
        if self.vote not in VALID_VOTES:
            raise ValueError(f"invalid vote: {self.vote}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def has_blocking_objection(self) -> bool:
        return self.vote == "disagree" and bool(self.objections)


@dataclass(frozen=True)
class ConsensusResult:
    level: str
    agreement_rate: float
    votes: dict[str, int]
    blocking_objections: list[dict[str, Any]]
    should_continue: bool
    stop_reason: str
    minority_opinions: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_consensus(
    positions: list[Position],
    threshold: float = 0.67,
    current_round: int = 1,
    max_rounds: int = 3,
) -> ConsensusResult:
    if not positions:
        return ConsensusResult("L3", 0.0, {"agree": 0, "disagree": 0, "abstain": 0}, [], False, "no_positions", [])

    votes = {vote: 0 for vote in VALID_VOTES}
    for position in positions:
        votes[position.vote] += 1
    agreement_rate = votes["agree"] / len(positions)
    blocking = [p.to_dict() for p in positions if p.has_blocking_objection]
    minority = [p.to_dict() for p in positions if p.vote != "agree"]

    if agreement_rate >= threshold and not blocking:
        return ConsensusResult("L1", agreement_rate, votes, blocking, False, "L1_consensus", minority)
    if current_round < max_rounds:
        return ConsensusResult("L2", agreement_rate, votes, blocking, True, "continue_targeted_round", minority)
    return ConsensusResult("L3", agreement_rate, votes, blocking, False, "max_rounds_reached_or_low_consensus", minority)


if __name__ == "__main__":
    import json

    sample = [
        Position(profile="architect", proposal="Use slot contract", vote="agree"),
        Position(profile="skeptic", proposal="Needs boundary", objections=["No automatic recovery"], vote="disagree"),
    ]
    print(json.dumps(evaluate_consensus(sample).to_dict(), ensure_ascii=False, indent=2))
