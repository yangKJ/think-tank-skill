#!/usr/bin/env python3
"""检查 Claude Code 平台验证产物的最低完整性。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"


REQUIRED_FILES = [
    THINK_TANK / "docs" / "claude-code-preflight.md",
    THINK_TANK / "docs" / "claude-code-validation-report.md",
    THINK_TANK / "platforms" / "claude-code" / "adapter.md",
    THINK_TANK / "platforms" / "claude-code" / "skill-mapping.md",
    THINK_TANK / "platforms" / "claude-code" / "dispatch-contract.md",
    THINK_TANK / "platforms" / "claude-code" / "dispatch-prompt.md",
    THINK_TANK / "platforms" / "claude-code" / "final-validation-prompt.md",
    THINK_TANK / "platforms" / "claude-code" / "minimal-runtime.md",
    THINK_TANK / "examples" / "claude-code-research-validation.md",
    THINK_TANK / "examples" / "claude-code-council-validation.md",
    THINK_TANK / "examples" / "claude-code-capability-discovery.md",
    THINK_TANK / "examples" / "claude-code-external-source-readonly.md",
    THINK_TANK / "examples" / "claude-code-adapter-dispatch-attempt.md",
    THINK_TANK / "examples" / "claude-code-dispatch-contract-sample.md",
    THINK_TANK / "examples" / "claude-code-dispatch-contract-validation.md",
    THINK_TANK / "examples" / "claude-code-dispatch-pre-invocation-validation.md",
    THINK_TANK / "examples" / "claude-dispatch-sample.json",
    THINK_TANK / "examples" / "claude-runtime-sample.json",
    THINK_TANK / "examples" / "claude-runtime-failure-sample.json",
    THINK_TANK / "schemas" / "claude-dispatch.schema.json",
    THINK_TANK / "schemas" / "claude-runtime.schema.json",
]

REPORT_REQUIRED_SNIPPETS = [
    "research_mode: verified_with_format_gap",
    "council_mode: verified_as_single_agent_council_preflight",
    "skill_discovery: verified",
    "capability_auto_mapping: verified_partial_pre_invocation_decision",
    "external_source_readonly: verified_partial",
    "adapter_dispatch_attempt: adapter_dispatch_not_executed_verified_partial",
    "dispatch_contract_validation: verified_partial_with_order_gap",
    "dispatch_pre_invocation_decision: verified_partial",
    "result_recovery_contract: partial_manual_mapping",
]

DISPATCH_CONTRACT_REQUIRED_SNIPPETS = [
    "dispatch_request",
    "dispatch_decision",
    "dispatch_log",
    "sources:",
    "evidence:",
    "不得把直接 WebFetch 调用称为完整 adapter dispatch",
]

DISPATCH_PROMPT_REQUIRED_SNIPPETS = [
    "dispatch_request:",
    "dispatch_decision:",
    "dispatch_log:",
    "sources:",
    "evidence:",
    "如果没有输出 dispatch_decision 和 dispatch_log",
]

MINIMAL_RUNTIME_REQUIRED_SNIPPETS = [
    "claude-code-minimal",
    "dispatch_request",
    "dispatch_decision",
    "invocation",
    "recovery",
    "runtime_verified",
]

FINAL_VALIDATION_PROMPT_REQUIRED_SNIPPETS = [
    "成功路径",
    "失败路径",
    "dispatch_decision_before_invocation",
    "No fallback was executed",
    "不得声明 adapter_dispatch_runtime: verified",
]

FORBIDDEN_SNIPPETS = [
    "capability_auto_mapping: verified\n",
    "adapter_dispatch: verified",
    "result_recovery_contract: verified",
    "subagent_dispatch: verified",
    "true_multi_agent_runtime: verified",
]


def fail(message: str) -> None:
    raise SystemExit(f"Claude Code 验证检查失败: {message}")


def read(path: Path) -> str:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def require_snippets(path: Path, snippets: list[str]) -> None:
    content = read(path)
    missing = [snippet for snippet in snippets if snippet not in content]
    if missing:
        fail(f"{path.relative_to(ROOT)} 缺少内容: {', '.join(missing)}")


def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not path.exists()]
    if missing:
        fail("缺少文件: " + ", ".join(str(path.relative_to(ROOT)) for path in missing))


def check_report() -> None:
    require_snippets(THINK_TANK / "docs" / "claude-code-validation-report.md", REPORT_REQUIRED_SNIPPETS)


def check_dispatch_contract() -> None:
    require_snippets(THINK_TANK / "platforms" / "claude-code" / "dispatch-contract.md", DISPATCH_CONTRACT_REQUIRED_SNIPPETS)


def check_dispatch_prompt() -> None:
    require_snippets(THINK_TANK / "platforms" / "claude-code" / "dispatch-prompt.md", DISPATCH_PROMPT_REQUIRED_SNIPPETS)


def check_minimal_runtime() -> None:
    require_snippets(THINK_TANK / "platforms" / "claude-code" / "minimal-runtime.md", MINIMAL_RUNTIME_REQUIRED_SNIPPETS)


def check_final_validation_prompt() -> None:
    require_snippets(THINK_TANK / "platforms" / "claude-code" / "final-validation-prompt.md", FINAL_VALIDATION_PROMPT_REQUIRED_SNIPPETS)


def check_forbidden_status() -> None:
    files = [
        THINK_TANK / "docs" / "claude-code-validation-report.md",
        THINK_TANK / "platforms" / "claude-code" / "adapter.md",
        THINK_TANK / "platforms" / "claude-code" / "skill-mapping.md",
        THINK_TANK / "docs" / "claude-code-preflight.md",
    ]
    for path in files:
        content = read(path)
        found = [snippet for snippet in FORBIDDEN_SNIPPETS if snippet in content]
        if found:
            fail(f"{path.relative_to(ROOT)} 出现禁止状态: {', '.join(found)}")


def main() -> None:
    check_required_files()
    check_report()
    check_dispatch_contract()
    check_dispatch_prompt()
    check_minimal_runtime()
    check_final_validation_prompt()
    check_forbidden_status()
    print("Claude Code 验证检查通过")


if __name__ == "__main__":
    main()
