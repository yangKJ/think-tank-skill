#!/usr/bin/env python3
"""检查 v2.2 Research OS starter kit。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "think-tank" / "templates" / "research-workspace"
REQUIRED = [
    "README.md",
    "inbox/README.md",
    "sources/ledger.example.jsonl",
    "artifacts/README.md",
    "decisions/decision-record-template.md",
    "experiments/experiment-template.md",
    "runbooks/runbook-template.md",
    "memory/memory-candidate-template.md",
    "runs/run-record-template.json",
    "provider-ledger/provider-ledger-template.json",
]


def fail(message: str) -> None:
    raise SystemExit(f"research workspace template 检查失败: {message}")


def main() -> None:
    for rel in REQUIRED:
        path = BASE / rel
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")
    for rel in ["runs/run-record-template.json", "provider-ledger/provider-ledger-template.json"]:
        try:
            json.loads((BASE / rel).read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"{rel} JSON 无效: {exc}")
    readme = (BASE / "README.md").read_text(encoding="utf-8")
    for term in [".think-tank/", "Real workspace data is user-owned", "Do not copy private data"]:
        if term not in readme:
            fail(f"README 缺少: {term}")
    print("research workspace template 检查通过")


if __name__ == "__main__":
    main()
