#!/usr/bin/env python3
"""检查 memory promotion policy 协议、schema 和样例。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "think-tank" / "protocol" / "memory-promotion-policy.md"
SCHEMA = ROOT / "think-tank" / "schemas" / "memory-promotion.schema.json"
SAMPLE = ROOT / "think-tank" / "examples" / "memory-promotion-sample.json"
MEMORY_PROTOCOL = ROOT / "think-tank" / "protocol" / "memory-curation.md"


def fail(message: str) -> None:
    raise SystemExit(f"memory promotion policy 检查失败: {message}")


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
        PROTOCOL,
        [
            "keep_local_until_reviewed",
            ".think-tank/memory/",
            "AGENTS.md",
            "project_docs",
            "think-tank_public_protocol",
            "reject_public_promotion",
            "no_private_core_leak",
        ],
    )
    require_text(
        MEMORY_PROTOCOL,
        [
            "Memory Promotion",
            "memory-promotion-policy.md",
        ],
    )

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    targets = set(schema["properties"]["to"]["enum"])
    for target in [".think-tank/memory/", "AGENTS.md", "project_docs", "think-tank_public_protocol"]:
        if target not in targets:
            fail(f"schema 缺少 target: {target}")
    for decision in ["keep_local", "promote", "merge", "reject"]:
        if decision not in schema["properties"]["decision"]["enum"]:
            fail(f"schema 缺少 decision: {decision}")

    sample = json.loads(SAMPLE.read_text(encoding="utf-8"))
    if sample["to"] == "think-tank_public_protocol" and sample["privacy_review"]["public_safe"] is not True:
        fail("公开 promotion sample 必须 public_safe")
    if sample["quality_check"]["no_private_core_leak"] is not True:
        fail("promotion sample 必须声明 no_private_core_leak")
    if sample["staleness_review"]["has_expiry_rule"] is not True:
        fail("promotion sample 必须保留 expiry rule")

    print("memory promotion policy 检查通过")


if __name__ == "__main__":
    main()

