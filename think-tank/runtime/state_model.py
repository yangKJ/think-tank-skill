#!/usr/bin/env python3
"""State and result model helpers for think-tank runtime."""

from __future__ import annotations

import re
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


RUN_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def validate_run_id(run_id: str) -> str:
    if not RUN_ID_RE.match(run_id) or ".." in run_id or "/" in run_id or "\\" in run_id:
        raise ValueError(f"invalid run_id: {run_id}")
    return run_id


def new_run_id(prefix: str = "run") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


@dataclass
class RunState:
    run_id: str
    protocol_version: str
    mode: str
    status: str = "pending"
    current_stage: str = "intake"
    current_round: int = 0
    selected_profiles: list[str] = field(default_factory=list)
    selected_capabilities: list[str] = field(default_factory=list)
    completed_stages: list[str] = field(default_factory=list)
    pending_stages: list[str] = field(default_factory=list)
    boundaries: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=now_iso)
    started_at: str | None = None
    completed_at: str | None = None

    def __post_init__(self) -> None:
        self.run_id = validate_run_id(self.run_id)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class StageResult:
    actor: str
    stage: str
    claim: str
    evidence: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    disagreements: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    confidence: str = "medium"
    boundaries: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RecoveryResult:
    result_recovered: bool
    recovered_as: list[str]
    recovery_method: str
    recovery_boundary: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def make_run(mode: str, profiles: list[str], capabilities: list[str], stages: list[str]) -> RunState:
    return RunState(
        run_id=new_run_id(),
        protocol_version="0.2",
        mode=mode,
        selected_profiles=profiles,
        selected_capabilities=capabilities,
        pending_stages=stages,
    )


if __name__ == "__main__":
    import json

    run = make_run("research", ["source-collector"], ["source-acquisition"], ["collection", "analysis"])
    print(json.dumps(run.to_dict(), ensure_ascii=False, indent=2))
