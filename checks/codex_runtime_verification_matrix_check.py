#!/usr/bin/env python3
"""检查 Codex runtime 验证矩阵是否记录真实 subagent 和 provider 边界。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX_DOC = ROOT / "think-tank" / "docs" / "codex-runtime-verification-matrix.md"
MULTI_AGENT_DOC = ROOT / "think-tank" / "docs" / "codex-true-multi-agent-validation.md"
COUNCIL_EXAMPLE = ROOT / "think-tank" / "examples" / "codex-true-council-runtime.md"
PROVIDER_MATRIX = ROOT / "think-tank" / "examples" / "codex-provider-invocation-matrix.json"
POLICY_RUNTIME = ROOT / "think-tank" / "platforms" / "codex" / "runtime" / "provider_policy.py"
POLICY_CHECK = ROOT / "checks" / "codex_provider_policy_check.py"


def fail(message: str) -> None:
    raise SystemExit(f"Codex runtime verification matrix 检查失败: {message}")


def require_text(path: Path, terms: list[str]) -> str:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for term in terms:
        if term not in text:
            fail(f"{path.relative_to(ROOT)} 缺少: {term}")
    return text


def main() -> None:
    require_text(
        MATRIX_DOC,
        [
            "true_multi_agent_council: verified_partial",
            "codex_parallel_subagents | verified_partial",
            "public_http_static_reader",
            "playwright-cli",
            "available_not_verified",
            "无 capability 且无显式 provider 偏好时，不选择 provider",
            "cannot_claim",
        ],
    )
    require_text(
        MULTI_AGENT_DOC,
        [
            "status: verified_partial",
            "codex_spawn_agent_parallel_explorers",
            "role_results_recovered: true",
            "它不是 `full_verified`",
        ],
    )
    require_text(
        COUNCIL_EXAMPLE,
        [
            "subagents_spawned: true",
            "subagent_count: 3",
            "architect",
            "skeptic",
            "product-strategist",
            "verified_partial",
            "不验证外部工具调用",
        ],
    )
    require_text(
        POLICY_RUNTIME,
        [
            "No capability or explicit provider preference requires provider selection.",
        ],
    )
    require_text(
        POLICY_CHECK,
        [
            "无 capability 的 council route 不应默认选择 provider",
            "制定策略 未命中 strategy policy route",
        ],
    )

    if not PROVIDER_MATRIX.exists():
        fail("缺少 codex-provider-invocation-matrix.json")
    data = json.loads(PROVIDER_MATRIX.read_text(encoding="utf-8"))
    providers = {item["provider"]: item for item in data.get("providers", [])}
    for provider in ["local_static_reader", "public_http_static_reader", "playwright-cli", "web-access", "taskflow"]:
        if provider not in providers:
            fail(f"provider matrix 缺少 provider: {provider}")
    if providers["web-access"]["invoked"]:
        fail("web-access 只能记录为 policy selection，不应标记 invoked")
    if providers["taskflow"]["invoked"]:
        fail("taskflow 只能记录为 policy selection，不应标记 invoked")
    if providers["playwright-cli"]["status"] != "verified_partial":
        fail("playwright-cli 应为 verified_partial")
    samples = {item["trigger"]: item for item in data.get("policy_loop_samples", [])}
    for trigger in ["研究一下", "竞品分析", "开会讨论", "审查", "制定策略", "持续关注"]:
        if trigger not in samples:
            fail(f"policy loop samples 缺少 trigger: {trigger}")
    if samples["开会讨论"]["selected_provider"] is not None:
        fail("开会讨论 不应选择 provider")
    if samples["制定策略"]["selected_provider"] is not None:
        fail("制定策略 不应选择 provider")

    print("Codex runtime verification matrix 检查通过")


if __name__ == "__main__":
    main()

