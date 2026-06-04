#!/usr/bin/env python3
"""检查 think-tank 2.0 Research OS + Memory Runtime 范围是否完整。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROTOCOLS = {
    "run-record.md": [
        "feature: run_record",
        "provider_invocation_ledger",
        "memory_runtime",
        "post_run_curation",
        "selected_vs_invoked_clear",
    ],
    "project-memory-runtime.md": [
        "feature: project_memory_runtime",
        "episodic",
        "semantic",
        "procedural",
        "conflict_check",
        "write_requires_confirmation: true",
    ],
    "provider-invocation-ledger.md": [
        "feature: provider_invocation_ledger",
        "selected is not `invoked`",
        "preflight_checked",
        "verified_partial",
    ],
    "handoff-protocol.md": [
        "feature: handoff_protocol",
        "input_filter",
        "true_multi_agent_runtime: false",
        "execution_method: single_agent_multi_profile",
    ],
    "guardrails.md": [
        "feature: guardrails",
        "permission_gate",
        "privacy_gate",
        "security_gate",
        "needs_user_confirmation",
    ],
    "research-os.md": [
        "feature: research_os",
        ".think-tank/",
        "sources/ledger.jsonl",
        "provider-ledger/",
        "local_workspace_stores_project_data: true",
    ],
    "eval-pack.md": [
        "feature: eval_pack",
        "provider_fallback",
        "memory_promotion",
        "handoff_guardrail",
    ],
}
SCHEMAS = [
    "run-record.schema.json",
    "provider-invocation-ledger.schema.json",
    "memory-runtime.schema.json",
    "handoff.schema.json",
    "guardrail-result.schema.json",
    "research-workspace.schema.json",
    "eval-case.schema.json",
]
TEMPLATES = [
    "think-tank-run-record.md",
    "provider-invocation-ledger.md",
    "memory-runtime-result.md",
]
EXAMPLES = [
    ROOT / "think-tank" / "examples" / "formats" / "research-os-run-record.json",
    ROOT / "think-tank" / "examples" / "formats" / "provider-invocation-ledger.json",
    ROOT / "think-tank" / "examples" / "formats" / "handoff-guardrail-eval.json",
    ROOT / "think-tank" / "examples" / "formats" / "research-workspace-contract.json",
]


def fail(message: str) -> None:
    raise SystemExit(f"v2.0 release 检查失败: {message}")


def require_text(path: Path, terms: list[str]) -> str:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for term in terms:
        if term not in text:
            fail(f"{path.relative_to(ROOT)} 缺少: {term}")
    return text


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)} JSON 无效: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} 必须是 object")
    return data


def require_keys(data: dict[str, Any], keys: list[str], label: str) -> None:
    missing = [key for key in keys if key not in data]
    if missing:
        fail(f"{label} 缺少字段: {', '.join(missing)}")


def check_run_record() -> None:
    data = load_json(ROOT / "think-tank" / "examples" / "formats" / "research-os-run-record.json")
    require_keys(
        data,
        [
            "run_id",
            "runtime_provenance",
            "provider_invocation_ledger",
            "post_run_curation",
            "memory_runtime",
            "quality_check",
        ],
        "research-os-run-record",
    )
    provenance = data["runtime_provenance"]
    if provenance.get("provider_invoked") is not False:
        fail("fixture 必须明确 provider_invoked=false")
    ledger_entries = data["provider_invocation_ledger"].get("entries", [])
    if not ledger_entries:
        fail("fixture 缺少 provider ledger entries")
    for entry in ledger_entries:
        if entry["state"] == "selected" and entry["invocation"]["invoked"]:
            fail("selected provider 不能同时标记 invoked=true")
    quality = data["quality_check"]
    for key in [
        "has_runtime_provenance",
        "has_provider_invocation_ledger",
        "selected_vs_invoked_clear",
        "memory_boundary_clear",
        "post_run_curation_present",
    ]:
        if quality.get(key) is not True:
            fail(f"quality_check.{key} 必须为 true")


def check_provider_ledger() -> None:
    data = load_json(ROOT / "think-tank" / "examples" / "formats" / "provider-invocation-ledger.json")
    entries = data.get("entries", [])
    if not entries:
        fail("provider-invocation-ledger.json 缺少 entries")
    for entry in entries:
        require_keys(entry, ["state", "preflight", "dispatch", "invocation", "recovery", "verification"], "provider ledger entry")
        if entry["dispatch"]["permission_gate"] == "needs_user_confirmation" and entry["invocation"]["invoked"]:
            fail("needs_user_confirmation 时不能 invoked=true")


def check_handoff_guardrail_eval() -> None:
    data = load_json(ROOT / "think-tank" / "examples" / "formats" / "handoff-guardrail-eval.json")
    require_keys(data, ["handoff", "guardrail_result", "eval_result"], "handoff fixture")
    handoff = data["handoff"]
    if handoff["runtime_provenance"].get("true_multi_agent_runtime") is not False:
        fail("handoff fixture 必须诚实声明不是 true multi-agent runtime")
    guardrail = data["guardrail_result"]
    if guardrail["status"] not in {"pass", "fail", "blocked", "needs_user_confirmation"}:
        fail("guardrail_result.status 无效")
    if data["eval_result"].get("passed") is not True:
        fail("eval_result.passed 必须为 true")


def check_workspace_contract() -> None:
    data = load_json(ROOT / "think-tank" / "examples" / "formats" / "research-workspace-contract.json")
    required_dirs = {
        "inbox/",
        "sources/",
        "sources/ledger.jsonl",
        "artifacts/",
        "decisions/",
        "experiments/",
        "runbooks/",
        "memory/",
        "runs/",
        "provider-ledger/",
    }
    directories = set(data.get("directories", []))
    missing = sorted(required_dirs - directories)
    if missing:
        fail(f"Research OS workspace 缺少目录: {', '.join(missing)}")
    if data.get("public_core_defines_contract") is not True:
        fail("public_core_defines_contract 必须为 true")
    if data.get("local_workspace_stores_project_data") is not True:
        fail("local_workspace_stores_project_data 必须为 true")


def main() -> None:
    for filename, terms in PROTOCOLS.items():
        require_text(ROOT / "think-tank" / "protocol" / filename, terms)
    for filename in SCHEMAS:
        schema = load_json(ROOT / "think-tank" / "schemas" / filename)
        require_keys(schema, ["$schema", "$id", "title", "type"], filename)
    for filename in TEMPLATES:
        require_text(ROOT / "think-tank" / "templates" / filename, ["```yaml"])
    for path in EXAMPLES:
        load_json(path)

    check_run_record()
    check_provider_ledger()
    check_handoff_guardrail_eval()
    check_workspace_contract()

    require_text(
        ROOT / "think-tank" / "docs" / "v2.0-roadmap.md",
        ["Research OS + Memory Runtime", "run_record", "project_memory_runtime", "provider_invocation_ledger"],
    )
    require_text(
        ROOT / "think-tank" / "docs" / "v2.0-release-notes.md",
        ["Run Record", "Project Memory Runtime", "Provider Invocation Ledger", "Eval Pack"],
    )

    print("v2.0 release 检查通过")


if __name__ == "__main__":
    main()
