#!/usr/bin/env python3
"""检查 Codex 长生命周期 adapter runtime 样例是否完整。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_MD = ROOT / "think-tank" / "examples" / "codex-long-running-adapter-runtime.md"
EXAMPLE_JSON = ROOT / "think-tank" / "examples" / "codex-long-running-adapter-runtime.json"


def fail(message: str) -> None:
    raise SystemExit(f"Codex long-running adapter 检查失败: {message}")


def require_text(path: Path, snippets: list[str]) -> None:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    content = path.read_text(encoding="utf-8")
    missing = [snippet for snippet in snippets if snippet not in content]
    if missing:
        fail(f"{path.relative_to(ROOT)} 缺少内容: {', '.join(missing)}")


def main() -> None:
    require_text(
        EXAMPLE_MD,
        [
            "status: verified_partial",
            "provider: research-to-video-production",
            "render_research_video_layout",
            "delivery_status: publish_candidate",
            "true_multi_agent_runtime: false",
            "不能",
        ],
    )
    if not EXAMPLE_JSON.exists():
        fail("缺少 JSON 样例")
    data = json.loads(EXAMPLE_JSON.read_text(encoding="utf-8"))
    if data["runtime_provenance"]["true_multi_agent_runtime"]:
        fail("long-running adapter 样例不能声称 true_multi_agent_runtime")
    if data["provider_preflight"]["status"] != "ready":
        fail("provider_preflight 应为 ready")
    if data["auto_handoff_result"]["status"] != "success":
        fail("auto_handoff_result 应为 success")
    if "render_research_video_layout" not in data["auto_handoff_result"]["steps"]:
        fail("缺少 render_research_video_layout step")
    if "create_delivery_report" not in data["auto_handoff_result"]["steps"]:
        fail("缺少 create_delivery_report step")
    print("Codex long-running adapter 检查通过")


if __name__ == "__main__":
    main()
