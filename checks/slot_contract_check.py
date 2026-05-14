#!/usr/bin/env python3
"""检查 v0.2 capability slot contract。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLOT_CONTRACT = ROOT / "think-tank" / "capabilities" / "slot-contract.md"


def fail(message: str) -> None:
    raise SystemExit(f"slot contract 检查失败: {message}")


def main() -> None:
    if not SLOT_CONTRACT.exists():
        fail(f"缺少文件: {SLOT_CONTRACT.relative_to(ROOT)}")
    content = SLOT_CONTRACT.read_text(encoding="utf-8")
    required = [
        "required: true | false",
        "Required Slot",
        "Optional Slot",
        "Resolution Flow",
        "installed tool does not equal verified capability",
        "direct tool invocation does not equal full adapter runtime",
        "failed invocation must not fabricate sources or evidence",
        "capability_resolution",
        "slot_contract_v0_2: specified",
    ]
    missing = [snippet for snippet in required if snippet not in content]
    if missing:
        fail("缺少内容: " + ", ".join(missing))
    print("slot contract 检查通过")


if __name__ == "__main__":
    main()
