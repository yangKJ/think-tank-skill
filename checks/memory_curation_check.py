#!/usr/bin/env python3
"""检查 project memory capture 协议、schema、recipe 和样例。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "think-tank" / "protocol" / "memory-curation.md"
RECIPE = ROOT / "think-tank" / "recipes" / "project-memory-capture.md"
ITEM_SCHEMA = ROOT / "think-tank" / "schemas" / "memory-item.schema.json"
CAPTURE_SCHEMA = ROOT / "think-tank" / "schemas" / "memory-capture.schema.json"
TEMPLATE = ROOT / "think-tank" / "templates" / "project-memory-candidate.md"
SAMPLE = ROOT / "think-tank" / "examples" / "project-memory-capture-sample.json"
REPORT = ROOT / "think-tank" / "examples" / "project-memory-capture-report.md"


def fail(message: str) -> None:
    raise SystemExit(f"memory curation 检查失败: {message}")


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
            "project_memory_capture",
            "default_behavior: propose_only",
            "write_requires_confirmation: true",
            "architecture",
            "workflow",
            "convention",
            "pitfall",
            "decision",
            "think-tank/",
            "Quality Gates",
        ],
    )
    require_text(
        RECIPE,
        [
            "Project Memory Capture",
            "write_requires_confirmation: true",
            ".think-tank/memory/",
            "forbidden_default_targets",
            "think-tank/",
        ],
    )
    require_text(
        TEMPLATE,
        [
            "Project Memory Candidate",
            "privacy",
            "staleness_risk",
            "quality_check",
            "no_unverified_claim_as_fact",
        ],
    )
    require_text(
        REPORT,
        [
            "selected_recipe: project-memory-capture",
            "default_behavior: propose_only",
            "No public `think-tank/` file is modified by default",
        ],
    )

    item_schema = json.loads(ITEM_SCHEMA.read_text(encoding="utf-8"))
    for field in [
        "id",
        "type",
        "title",
        "summary",
        "source",
        "verified_at",
        "scope",
        "privacy",
        "staleness_risk",
        "confidence",
        "target",
        "action",
        "quality_check",
    ]:
        if field not in item_schema["required"]:
            fail(f"memory-item schema 缺少 required 字段: {field}")
    if "project_local" not in item_schema["properties"]["privacy"]["enum"]:
        fail("memory-item schema privacy 必须支持 project_local")

    capture_schema = json.loads(CAPTURE_SCHEMA.read_text(encoding="utf-8"))
    if capture_schema["properties"]["selected_recipe"]["const"] != "project-memory-capture":
        fail("memory-capture schema selected_recipe const 不正确")

    sample = json.loads(SAMPLE.read_text(encoding="utf-8"))
    candidate = sample["memory_candidates"][0]
    if candidate["target"].startswith("think-tank/"):
        fail("memory capture sample 不应写入公开 think-tank/")
    if candidate["privacy"] != "project_local":
        fail("memory capture sample 应为 project_local")
    if candidate["action"] not in {"append", "merge", "skip", "propose_only"}:
        fail("memory capture sample action 不合法")

    print("memory curation 检查通过")


if __name__ == "__main__":
    main()

