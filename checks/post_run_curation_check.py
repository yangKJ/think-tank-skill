#!/usr/bin/env python3
"""检查 post-run curation 是否作为 think-tank core 能力存在。"""

from __future__ import annotations

import json
import base64
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"

PROTOCOL = THINK_TANK / "protocol" / "post-run-curation.md"
SCHEMA = THINK_TANK / "schemas" / "post-run-curation.schema.json"
EXAMPLE = THINK_TANK / "examples" / "post-run-curation-example.json"
SKILL = THINK_TANK / "SKILL.md"
PROTOCOL_README = THINK_TANK / "protocol" / "README.md"
SCHEMA_README = THINK_TANK / "schemas" / "README.md"
EXAMPLES_README = THINK_TANK / "examples" / "README.md"

MODE_FILES = [
    THINK_TANK / "modes" / "research.md",
    THINK_TANK / "modes" / "strategy.md",
    THINK_TANK / "modes" / "review.md",
    THINK_TANK / "modes" / "council.md",
]

REQUIRED_TOP_LEVEL_KEYS = {
    "required",
    "should_persist",
    "source_candidates",
    "trend_candidates",
    "action_candidates",
    "generated_artifacts",
    "artifact_plan",
    "persistence_decision",
    "boundaries",
}

PROTOCOL_TERMS = [
    "Post-run Curation",
    "Required For",
    "source_candidates",
    "trend_candidates",
    "action_candidates",
    "generated_artifacts",
    "artifact_plan",
    "persistence_decision",
    "Project-local files",
]

PRIVATE_TERMS = [
    base64.b64decode(value).decode("utf-8")
    for value in [
        "QXdha2VuaW5n",
        "SGFyYmV0aA==",
        "aW1hZ2UtZWRpdGluZw==",
        "aW1nLWNvbXBhbnk=",
        "aW9zLWF1dG9tYXRpb24tbWNw",
    ]
]


def fail(message: str) -> None:
    raise SystemExit(f"post-run curation 检查失败: {message}")


def read(path: Path) -> str:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def check_protocol() -> None:
    content = read(PROTOCOL)
    missing = [term for term in PROTOCOL_TERMS if term not in content]
    if missing:
        fail(f"{PROTOCOL.relative_to(ROOT)} 缺少关键术语: {', '.join(missing)}")
    if ".think-tank/" not in content:
        fail("协议必须说明本地工作区只是落点，不是能力来源")


def check_core_entrypoints() -> None:
    skill = read(SKILL)
    required_terms = [
        "protocol/post-run-curation.md",
        "post_run_curation",
        "think-tank core",
        "可能的落点，不是这项能力的来源",
    ]
    missing = [term for term in required_terms if term not in skill]
    if missing:
        fail(f"{SKILL.relative_to(ROOT)} 未接入 post-run curation: {', '.join(missing)}")

    if "post-run-curation.md" not in read(PROTOCOL_README):
        fail("protocol/README.md 未列出 post-run-curation.md")
    if "post-run-curation.schema.json" not in read(SCHEMA_README):
        fail("schemas/README.md 未列出 post-run-curation.schema.json")
    if "post-run-curation-example.json" not in read(EXAMPLES_README):
        fail("examples/README.md 未列出 post-run-curation-example.json")


def check_modes() -> None:
    for mode_file in MODE_FILES:
        content = read(mode_file)
        if "## Post-run Curation" not in content:
            fail(f"{mode_file.relative_to(ROOT)} 缺少 Post-run Curation 章节")
        if "post_run_curation" not in content:
            fail(f"{mode_file.relative_to(ROOT)} 未显式要求 post_run_curation")


def check_schema_and_example() -> None:
    schema = json.loads(read(SCHEMA))
    example = json.loads(read(EXAMPLE))

    if schema.get("type") != "object":
        fail("post-run curation schema 顶层必须是 object")
    required = set(schema.get("required", []))
    if required != REQUIRED_TOP_LEVEL_KEYS:
        fail(f"schema required keys 不匹配: {sorted(required)}")

    missing = REQUIRED_TOP_LEVEL_KEYS - set(example)
    extra = set(example) - REQUIRED_TOP_LEVEL_KEYS
    if missing or extra:
        fail(f"example 顶层字段不匹配 missing={sorted(missing)} extra={sorted(extra)}")

    if example["persistence_decision"]["wrote_files"] is not False:
        fail("示例必须证明候选输出不等于实际写入")
    if not example["generated_artifacts"]:
        fail("示例必须包含 generated_artifacts")
    if not example["boundaries"]:
        fail("示例必须包含 boundaries")


def check_public_safety() -> None:
    for path in [PROTOCOL, SCHEMA, EXAMPLE, SKILL, *MODE_FILES]:
        content = read(path)
        hits = [term for term in PRIVATE_TERMS if term in content]
        if hits:
            fail(f"{path.relative_to(ROOT)} 包含不应进入公开 core 的私有术语: {', '.join(hits)}")


def main() -> None:
    check_protocol()
    check_core_entrypoints()
    check_modes()
    check_schema_and_example()
    check_public_safety()
    print("post-run curation 检查通过")


if __name__ == "__main__":
    main()
