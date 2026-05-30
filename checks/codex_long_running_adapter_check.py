#!/usr/bin/env python3
"""检查 Codex 长生命周期 adapter runtime 样例是否完整。

验证 orchestrator 输出的通用结构（不验证 provider 特定 handoff，
因为那属于 .think-tank/ 本地配置层）。
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_MD = ROOT / "think-tank" / "examples" / "platforms" / "codex" / "codex-long-running-adapter-runtime.md"
EXAMPLE_JSON = ROOT / "think-tank" / "examples" / "platforms" / "codex" / "codex-long-running-adapter-runtime.json"


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
            "true_multi_agent_runtime: false",
            "不能",
            "dispatch",
            "orchestrator",
        ],
    )
    if not EXAMPLE_JSON.exists():
        fail("缺少 JSON 样例")
    data = json.loads(EXAMPLE_JSON.read_text(encoding="utf-8"))

    # 验证运行时基本结构
    if data["runtime"] != "codex-natural-language-orchestrator":
        fail("runtime 字段必须是 codex-natural-language-orchestrator")
    if data["runtime_provenance"]["true_multi_agent_runtime"]:
        fail("long-running adapter 样例不能声称 true_multi_agent_runtime")
    if "dispatch_record" not in data:
        fail("缺少 dispatch_record")
    if "dispatch_log" not in data:
        fail("缺少 dispatch_log")
    if "provider_preflight" not in data:
        fail("缺少 provider_preflight")

    # 验证 provider_preflight 结构
    preflight = data["provider_preflight"]
    if "provider" not in preflight:
        fail("provider_preflight 缺少 provider 字段")
    if "status" not in preflight:
        fail("provider_preflight 缺少 status 字段")
    if "can_invoke" not in preflight:
        fail("provider_preflight 缺少 can_invoke 字段")

    # 验证 final_output 结构
    final = data["final_output"]
    for field in ("request", "conclusion", "evidence", "recommendations"):
        if field not in final:
            fail(f"final_output 缺少 {field} 字段")

    # 验证 quality_check
    qc = data["quality_check"]
    for field in ("protocol_complete", "runtime_provenance_present",
                  "provider_invocation_truthful", "evidence_boundary_clear", "actionable"):
        if field not in qc:
            fail(f"quality_check 缺少 {field} 字段")
        if not qc[field]:
            fail(f"quality_check.{field} 必须为 true")

    # 验证不再有 auto_handoff_result（已迁移到 .think-tank/ 本地配置）
    if "auto_handoff_result" in data:
        fail("orchestrator 输出不应再包含 auto_handoff_result，"
             "provider 特定 handoff 已迁移到 .think-tank/ 配置")

    print("Codex long-running adapter 检查通过")


if __name__ == "__main__":
    main()
