#!/usr/bin/env python3
"""检查 agent-council 迁移后的 council runtime helper。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COUNCIL_PATH = ROOT / "think-tank" / "runtime" / "council.py"


def fail(message: str) -> None:
    raise SystemExit(f"council runtime 检查失败: {message}")


def load_module():
    spec = importlib.util.spec_from_file_location("think_tank_runtime_council", COUNCIL_PATH)
    if spec is None or spec.loader is None:
        fail("无法加载 runtime/council.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if not COUNCIL_PATH.exists():
        fail("缺少 runtime/council.py")

    council = load_module()

    state = council.create_council_state("runtime migration", ["Code Reviewer", "Security Engineer"])
    if state.phase.value != "collect":
        fail("初始状态必须进入 collect")
    if council.next_phase(state).value != "collect":
        fail("未完成收集时不能进入 discuss")

    completed = council.CouncilState(
        topic=state.topic,
        phase=council.CouncilPhase.COLLECT,
        agents=state.agents,
        agents_completed=state.agents,
    )
    if not council.all_agents_completed(completed):
        fail("all_agents_completed 未识别完成状态")
    if council.next_phase(completed).value != "discuss":
        fail("收集完成后应进入 discuss")

    if council.classify_consensus(0.7, 1, has_blocking_objection=False) != "L1":
        fail("L1 共识判断失败")
    if council.classify_consensus(0.7, 1, has_blocking_objection=True) != "L2":
        fail("blocking objection 不得进入 L1")
    if council.classify_consensus(0.2, 10) != "L3":
        fail("L3 裁决判断失败")

    high_risk = council.CouncilState(
        topic="high risk",
        phase=council.CouncilPhase.DISCUSS,
        round=3,
        agents=["A", "B"],
        consensus_support=0.4,
        high_risk_operation=True,
    )
    if not council.should_trigger_l3(high_risk):
        fail("高风险低共识应触发 L3")

    payload = council.build_synthesis_payload(["A"], [{"risk": "B"}], ["Do X"], "裁决")
    if not payload["boundaries"] or payload["final_decision"] != "裁决":
        fail("synthesis payload 不完整")

    print("council runtime 检查通过")


if __name__ == "__main__":
    main()

