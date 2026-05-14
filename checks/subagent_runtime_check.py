#!/usr/bin/env python3
"""检查 v0.5 专业 subagent runtime helper。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUBAGENT_PATH = ROOT / "think-tank" / "runtime" / "subagent.py"


def fail(message: str) -> None:
    raise SystemExit(f"subagent runtime 检查失败: {message}")


def load_module():
    spec = importlib.util.spec_from_file_location("think_tank_runtime_subagent", SUBAGENT_PATH)
    if spec is None or spec.loader is None:
        fail("无法加载 runtime/subagent.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if not SUBAGENT_PATH.exists():
        fail("缺少 runtime/subagent.py")

    subagent = load_module()
    plan = subagent.plan_subagent_runtime(
        mode="research",
        objective="test specialist runtime",
        profiles=["source-collector", "skeptic"],
        platform_supports_subagents=True,
        input_context=["context A"],
    )
    if plan.dispatch_strategy != "parallel_specialist_subagents":
        fail("支持 subagent 时应使用 parallel_specialist_subagents")
    if plan.authority_level != "specialist_independent":
        fail("专业 runtime authority level 错误")
    if len(plan.tasks) != 2:
        fail("未按 profile 生成 task")
    if "source-acquisition" not in plan.tasks[0].required_capabilities:
        fail("source-collector capability hint 缺失")

    prompt = subagent.build_profile_prompt(plan.tasks[0])
    for term in ["role-result", "source-collector", "Required capabilities"]:
        if term not in prompt:
            fail(f"profile prompt 缺少 {term}")

    fallback = subagent.plan_subagent_runtime(
        mode="council",
        objective="fallback test",
        profiles=["skeptic"],
        platform_supports_subagents=False,
    )
    if fallback.dispatch_strategy != "single_agent_multi_profile_fallback":
        fail("无 subagent 能力时必须显式 fallback")
    if fallback.authority_level != "lower_fallback_single_context":
        fail("fallback authority level 错误")

    result = subagent.RoleResult(
        profile="skeptic",
        execution_method="specialist_subagent",
        claim="Do not overclaim.",
        evidence=["schema exists"],
        risks=["mislabeling"],
        objections=["fallback is not independent"],
        recommendations=["label execution method"],
        confidence="high",
        boundaries=["fixture only"],
    )
    aggregate = subagent.aggregate_role_results([result])
    if aggregate["status"] != "completed" or not aggregate["objections"]:
        fail("role result 聚合失败")

    print("subagent runtime 检查通过")


if __name__ == "__main__":
    main()

