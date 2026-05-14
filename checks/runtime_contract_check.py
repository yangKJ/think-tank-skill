#!/usr/bin/env python3
"""检查 v0.2 runtime/state contract。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"


def fail(message: str) -> None:
    raise SystemExit(f"runtime contract 检查失败: {message}")


def require(path: Path, snippets: list[str]) -> None:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    content = path.read_text(encoding="utf-8")
    missing = [snippet for snippet in snippets if snippet not in content]
    if missing:
        fail(f"{path.relative_to(ROOT)} 缺少内容: {', '.join(missing)}")


def main() -> None:
    require(
        THINK_TANK / "protocol" / "runtime-contract.md",
        [
            "trigger_resolution",
            "strict: true",
            "runtime_plan",
            "required_capabilities",
            "optional_capabilities",
            "missing_required_capability",
            "Platform Boundary",
            "full_adapter_runtime",
        ],
    )
    require(
        THINK_TANK / "protocol" / "state-result-contract.md",
        [
            "Run Identity",
            "run_id",
            "Heartbeat",
            "Result",
            "Recovery",
            "structured_manual",
            "automatic_recovery: not_verified",
        ],
    )
    print("runtime contract 检查通过")


if __name__ == "__main__":
    main()
