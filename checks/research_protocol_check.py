#!/usr/bin/env python3
"""检查 v0.2 research protocol hardening。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"


def fail(message: str) -> None:
    raise SystemExit(f"research protocol 检查失败: {message}")


def require(path: Path, snippets: list[str]) -> None:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    content = path.read_text(encoding="utf-8")
    missing = [snippet for snippet in snippets if snippet not in content]
    if missing:
        fail(f"{path.relative_to(ROOT)} 缺少内容: {', '.join(missing)}")


def main() -> None:
    require(
        THINK_TANK / "modes" / "research.md",
        [
            "v0.2 Research Hardening",
            "quick_scan",
            "deep_research",
            "continuous_monitoring",
            "autonomous_research",
            "source_authority: A | B | C",
            "content_hash",
            "cross_validation",
            "evidence table",
            "why-stop-now",
        ],
    )
    require(
        THINK_TANK / "docs" / "v0.2-runtime-hardening.md",
        [
            "runtime_hardening",
            "protocol/runtime-contract.md",
            "capabilities/slot-contract.md",
            "protocol/state-result-contract.md",
            "protocol/consensus-contract.md",
            "references/research-protocol.md",
        ],
    )
    print("research protocol 检查通过")


if __name__ == "__main__":
    main()
