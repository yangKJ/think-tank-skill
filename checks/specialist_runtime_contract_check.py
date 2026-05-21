#!/usr/bin/env python3
"""检查 v0.5 specialist subagent runtime 文档契约。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"

FILES = [
    THINK_TANK / "protocol" / "subagent-runtime-contract.md",
    THINK_TANK / "docs" / "v0.5-specialist-subagent-runtime.md",
    THINK_TANK / "profiles" / "prompt-pack.md",
    THINK_TANK / "platforms" / "codex" / "specialist-subagent-runtime.md",
    THINK_TANK / "platforms" / "claude-code" / "specialist-subagent-runtime.md",
]

REQUIRED_TERMS = [
    "specialist_subagent",
    "single_agent_multi_profile_fallback",
    "role-result",
    "authority_level",
    "true_parallel_runtime_verified: false",
    "lower_fallback_single_context",
]


def fail(message: str) -> None:
    raise SystemExit(f"specialist runtime contract 检查失败: {message}")


def main() -> None:
    missing = [path for path in FILES if not path.exists()]
    if missing:
        fail("缺少文件: " + ", ".join(str(path.relative_to(ROOT)) for path in missing))

    combined = "\n".join(path.read_text(encoding="utf-8") for path in FILES)
    for term in REQUIRED_TERMS:
        if term not in combined:
            fail(f"缺少关键契约: {term}")

    forbidden = [
        "true_parallel_runtime_verified: true",
        "agent_team_full_runtime: verified",
        "codex_specialist_subagent_runtime: verified\n",
    ]
    for term in forbidden:
        if term in combined:
            fail(f"出现过度声明: {term}")

    print("specialist runtime contract 检查通过")


if __name__ == "__main__":
    main()
