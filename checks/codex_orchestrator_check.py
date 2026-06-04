#!/usr/bin/env python3
"""检查 Codex 自然语言 orchestrator 的最小闭环。"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATOR = ROOT / "think-tank" / "platforms" / "codex" / "runtime" / "orchestrator.py"
PROTOCOL = ROOT / "think-tank" / "protocol" / "natural-language-runtime-orchestration.md"
SCHEMA = ROOT / "think-tank" / "schemas" / "codex-orchestrator-result.schema.json"
SAMPLE = ROOT / "think-tank" / "examples" / "runtime" / "codex-orchestrator-sample.json"
FIXTURE = "think-tank/examples/browser-automation-fixture.html"


def fail(message: str) -> None:
    raise SystemExit(f"Codex orchestrator 检查失败: {message}")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} 必须是 object")
    return data


def run_orchestrator(*args: str) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(ORCHESTRATOR), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        fail(f"orchestrator 命令失败: {completed.stderr.strip()}")
    return json.loads(completed.stdout)


def require_text(path: Path, terms: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for term in terms:
        if term not in text:
            fail(f"{path.relative_to(ROOT)} 缺少: {term}")


def main() -> None:
    for path in [ORCHESTRATOR, PROTOCOL, SCHEMA, SAMPLE]:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")
    require_text(
        PROTOCOL,
        [
            "user_request",
            "provider_policy route",
            "dispatch_record",
            "run_record",
            "provider_selection_is_invocation: false",
        ],
    )

    schema = load_json(SCHEMA)
    for field in [
        "runtime_provenance",
        "policy_route",
        "provider_preflight",
        "dispatch_record",
        "run_record",
        "final_output",
    ]:
        if field not in schema["required"]:
            fail(f"schema 缺少 required 字段: {field}")

    sample = load_json(SAMPLE)
    if sample["runtime"] != "codex-natural-language-orchestrator":
        fail("sample runtime 不正确")
    if sample["dispatch_record"]["policy_selected_provider"] == sample["dispatch_record"]["runtime_selected_provider"]:
        fail("sample 必须展示 policy provider 和 runtime provider 可分离")
    for leader_field in ["leader_context", "expert_registry_summary", "expert_task_packets", "acceptance_report"]:
        if leader_field in sample:
            fail(f"think-tank sample 不应包含 leader-runtime 字段: {leader_field}")

    data = run_orchestrator("竞品分析 Cursor 和 Codex", "--target", FIXTURE)
    if data["runtime"] != "codex-natural-language-orchestrator":
        fail("runtime 不正确")
    policy_route = data["policy_route"]
    if policy_route.get("selected_recipe") != "competitive-intelligence":
        fail("竞品分析必须命中 competitive-intelligence recipe")
    if policy_route.get("selected_intent") != "competitive_intelligence":
        fail("竞品分析必须命中 competitive_intelligence intent")
    provenance = data["runtime_provenance"]
    if provenance["provider_policy_checked"] is not True:
        fail("必须声明 provider_policy_checked")
    if provenance.get("authority_level") == "full_runtime":
        fail("minimal orchestrator 不得把 adapter runtime 标成 full_runtime authority")
    expects_source_recovery = "source-acquisition" in (
        policy_route.get("selected_capabilities", []) or []
    )
    if expects_source_recovery and provenance["result_recovered"] is not True:
        fail("source-acquisition 路径必须回收结果")
    if not expects_source_recovery and provenance["provider_invoked"] is not False:
        fail("无 source-acquisition capability 时不得声明 provider 已调用")
    if provenance["true_multi_agent_runtime"] is not False:
        fail("minimal orchestrator 不得声称真实多 agent")
    for leader_field in ["leader_context", "expert_registry_summary", "expert_task_packets", "acceptance_report"]:
        if leader_field in data:
            fail(f"think-tank runtime 不应包含 leader-runtime 字段: {leader_field}")
    preflight = data["provider_preflight"]
    if preflight["provider"] != data["policy_route"]["skill_route"]["selected_provider"]:
        fail("provider_preflight 必须检查 policy 选中的 provider")
    if preflight["can_invoke"] is True and preflight["missing"]:
        fail("preflight 有缺失项时不得 can_invoke=true")
    if "Preflight checks prerequisites only; it does not invoke the provider." not in preflight["boundaries"]:
        fail("preflight 必须声明不调用 provider")
    dispatch = data["dispatch_record"]
    if dispatch["policy_selected_provider"] == dispatch["runtime_selected_provider"]:
        fail("测试应证明 policy provider 不等于 minimal runtime provider")
    if data["run_record"]["artifact_written"] is not False:
        fail("默认不应写 run artifact")

    local_markdown = run_orchestrator("竞品分析 Cursor 和 Codex", "--target", "AGENTS.md")
    if "source-acquisition" in (local_markdown["policy_route"].get("selected_capabilities", []) or []):
        source_type = local_markdown["source_result"]["sources"][0]["source_type"]
        if source_type != "markdown":
            fail(f"Markdown 目标不应标成 HTML source_type: {source_type}")
    elif local_markdown["source_result"] is not None:
        fail("无 source-acquisition capability 时不应生成 source_result")

    run_dir = ROOT / ".think-tank" / "runs"
    written = run_orchestrator("竞品分析 Cursor 和 Codex", "--target", FIXTURE, "--write-run", "--runs-dir", str(run_dir))
    if written["run_record"]["artifact_written"] is not True:
        fail("--write-run 必须写入 artifact")
    artifact = ROOT / written["run_record"]["artifact_path"]
    if not artifact.exists():
        fail("run artifact 不存在")

    print("Codex orchestrator 检查通过")


if __name__ == "__main__":
    main()
