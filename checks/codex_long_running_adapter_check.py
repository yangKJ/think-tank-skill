#!/usr/bin/env python3
"""检查 Codex 长生命周期 adapter runtime 样例是否完整且自洽。

验证 orchestrator 输出的通用结构（不验证 provider 特定 handoff，
因为那属于 .think-tank/ 本地配置层），并强制以下不变式，防止
样例把"未发生的 source recovery"伪造为 `verified_partial` 证据：

- dispatch_request.target、source_result、dispatch_log.invocation、
  dispatch_log.recovery 必须互相一致；
- evidence_state=verified_partial 必须有真实的 invocation+recovery 证据；
- verified_partial + execution_method=adapter_runtime 必须和
  sources_recovered=true 同时成立。
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


def _require_field(data: dict, path: list[str], label: str) -> None:
    cursor = data
    for key in path:
        if not isinstance(cursor, dict) or key not in cursor:
            fail(f"{label} 缺少字段: {'.'.join(path)}")
        cursor = cursor[key]


def _evidence_state(data: dict) -> str:
    return data.get("runtime_provenance", {}).get("evidence_state", "unknown")


def _execution_method(data: dict) -> str:
    return data.get("runtime_provenance", {}).get("execution_method", "unknown")


def main() -> None:
    require_text(
        EXAMPLE_MD,
        [
            "true_multi_agent_runtime: false",
            "不能",
            "dispatch",
            "orchestrator",
            "provider_invocation_truthful",
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

    # -------------------------------------------------------------------------
    # 不变式 1: dispatch_request.target / source_result / invocation / recovery
    # 必须互相一致。local_static_reader 这种 source-acquisition runtime 必须
    # 有非空 target + 非空 source_result.sources 才能声明 sources_recovered。
    # -------------------------------------------------------------------------
    _require_field(data, ["dispatch_log", "dispatch_request", "target"], "dispatch_log")
    _require_field(data, ["dispatch_log", "invocation", "provider_invoked"], "dispatch_log.invocation")
    _require_field(data, ["dispatch_log", "invocation", "status"], "dispatch_log.invocation")
    _require_field(data, ["dispatch_log", "recovery", "sources_recovered"], "dispatch_log.recovery")
    _require_field(data, ["dispatch_log", "recovery", "result_recovered"], "dispatch_log.recovery")

    target = data["dispatch_log"]["dispatch_request"]["target"]
    invocation = data["dispatch_log"]["invocation"]
    recovery = data["dispatch_log"]["recovery"]
    source_result = data.get("source_result")
    runtime_provider = invocation.get("provider")
    post_dispatch_result = data.get("post_dispatch_result")
    runtime_selected_provider = data.get("dispatch_record", {}).get("runtime_selected_provider")

    # source-acquisition 风格（local_static_reader / WebFetch）要求 target 非空
    if (
        runtime_provider in ("local_static_reader", "WebFetch")
        and invocation.get("provider_invoked")
        and invocation.get("status") == "success"
        and not target
    ):
        fail(
            "invocation 声明 local_static_reader 成功但 dispatch_request.target 为 null；"
            "source-acquisition 不可能在 null target 上跑出 source。请补 target 或把"
            "invocation 改成 not_invoked。"
        )

    # sources_recovered=true 必须能追溯到 source_result.sources 非空
    if recovery.get("sources_recovered"):
        if not source_result or not isinstance(source_result, dict):
            fail("recovery.sources_recovered=true 但 source_result 缺失")
        if not source_result.get("sources"):
            fail("recovery.sources_recovered=true 但 source_result.sources 为空")
        urls = [s.get("url") for s in source_result.get("sources", []) if isinstance(s, dict)]
        if not any(u for u in urls):
            fail("source_result.sources 全部缺 url，无法证明 source 真的被 read")

    # provider_invoked=true 但 sources_recovered=false 时，invocation_method
    # 必须是 post_dispatch_hook 或其他能解释"无 source 但有 invocation"的方式
    if invocation.get("provider_invoked") and not recovery.get("sources_recovered"):
        method = data.get("dispatch_log", {}).get("dispatch_decision", {}).get("invocation_method")
        if method not in {"post_dispatch_hook"}:
            fail(
                "provider_invoked=true 但 sources_recovered=false，且 "
                f"invocation_method={method!r}；这种情况应当是 post_dispatch_hook，"
                "否则就是 source recovery 证据缺失。"
            )

    # -------------------------------------------------------------------------
    # 不变式 2: evidence_state 跟 execution_method / recovery 状态必须一致。
    # 禁止把"未发生 provider invocation"的 run 标成 verified_partial。
    # -------------------------------------------------------------------------
    state = _evidence_state(data)
    method = _execution_method(data)
    if state == "verified_partial":
        if not invocation.get("provider_invoked"):
            fail("evidence_state=verified_partial 但 invocation.provider_invoked=false")
        if not recovery.get("result_recovered"):
            fail("evidence_state=verified_partial 但 recovery.result_recovered=false")
        if method != "adapter_runtime":
            fail(
                "evidence_state=verified_partial 但 execution_method="
                f"{method!r}（必须是 adapter_runtime）"
            )
        # post_dispatch 标 success 时必须 returncode==0 + 有 evidence
        if isinstance(post_dispatch_result, dict):
            if post_dispatch_result.get("status") != "success":
                fail(
                    "evidence_state=verified_partial 但 post_dispatch_result.status="
                    f"{post_dispatch_result.get('status')!r}"
                )
            if post_dispatch_result.get("returncode") not in (0, None):
                fail(
                    "evidence_state=verified_partial 但 post_dispatch_result.returncode="
                    f"{post_dispatch_result.get('returncode')!r}（必须为 0）"
                )

    if state == "selected" and method == "adapter_runtime":
        fail(
            "evidence_state=selected 不应同时 execution_method=adapter_runtime；"
            "adapter_runtime 应当产生 verified_partial 或 failed。"
        )

    # -------------------------------------------------------------------------
    # 不变式 3: runtime_selected_provider 必须跟 invocation.provider 一致；
    # 防止"policy 选了一个 provider / runtime 实际跑了另一个"却被 claim 成
    # 真实 invocation 的情况。
    # -------------------------------------------------------------------------
    if runtime_selected_provider != runtime_provider:
        fail(
            "dispatch_record.runtime_selected_provider="
            f"{runtime_selected_provider!r} 与 dispatch_log.invocation.provider="
            f"{runtime_provider!r} 不一致。"
        )

    print("Codex long-running adapter 检查通过")


if __name__ == "__main__":
    main()
