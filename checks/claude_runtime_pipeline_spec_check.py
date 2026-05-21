#!/usr/bin/env python3
"""检查 Claude Code runtime pipeline spec。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "think-tank" / "platforms" / "claude-code" / "runtime-pipeline.md"


def fail(message: str) -> None:
    raise SystemExit(f"Claude runtime pipeline spec 检查失败: {message}")


def main() -> None:
    if not SPEC.exists():
        fail(f"缺少文件: {SPEC.relative_to(ROOT)}")
    content = SPEC.read_text(encoding="utf-8")
    required = [
        "planner.plan_runtime",
        "slot_resolver.resolve_slots",
        "WebFetch invocation",
        "state_model.StageResult",
        "consensus.evaluate_consensus",
        "runtime_result",
        "adapter_dispatch_runtime: not_full_verified",
        "automatic_recovery: not_verified",
        "不得把 WebFetch 单次调用称为完整 adapter runtime",
    ]
    missing = [snippet for snippet in required if snippet not in content]
    if missing:
        fail("缺少内容: " + ", ".join(missing))
    print("Claude runtime pipeline spec 检查通过")


if __name__ == "__main__":
    main()
