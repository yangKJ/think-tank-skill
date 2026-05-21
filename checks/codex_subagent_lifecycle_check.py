#!/usr/bin/env python3
"""检查 Codex specialist subagent lifecycle 样例是否完整。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_MD = ROOT / "think-tank" / "examples" / "codex-subagent-lifecycle-validation.md"
EXAMPLE_JSON = ROOT / "think-tank" / "examples" / "codex-subagent-lifecycle-validation.json"


def fail(message: str) -> None:
    raise SystemExit(f"Codex subagent lifecycle 检查失败: {message}")


def require_text(path: Path, snippets: list[str]) -> str:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    content = path.read_text(encoding="utf-8")
    missing = [snippet for snippet in snippets if snippet not in content]
    if missing:
        fail(f"{path.relative_to(ROOT)} 缺少内容: {', '.join(missing)}")
    return content


def main() -> None:
    require_text(
        EXAMPLE_MD,
        [
            "status: verified_partial",
            "subagents_spawned: true",
            "subagent_count: 3",
            "peer_review_resumption: true",
            "multi-agent beyond readonly council",
            "long-running subagent lifecycle",
        ],
    )

    data = json.loads(require_text(EXAMPLE_JSON, ['"status": "verified_partial"']))
    if not data.get("subagents_spawned"):
        fail("subagents_spawned 应为 true")
    if data.get("subagent_count") != 3:
        fail("subagent_count 应为 3")
    profiles = data.get("profiles", [])
    if len(profiles) != 3:
        fail("profiles 数量应为 3")

    for item in profiles:
        if not item.get("phase_1_completed") or not item.get("phase_2_resumed"):
            fail("每个 subagent 都必须完成 phase_1 和 phase_2")
        role_file = ROOT / item["owned_file"]
        require_text(
            role_file,
            [
                "execution_method",
                "phase: initial",
                "## Lifecycle Update",
                "phase: resumed_after_peer_results",
                "peer_results_reviewed: 2",
            ],
        )

    print("Codex subagent lifecycle 检查通过")


if __name__ == "__main__":
    main()
