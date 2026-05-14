#!/usr/bin/env python3
"""检查 Codex 平台验证产物的最低完整性。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"


REQUIRED_VALIDATION_FILES = [
    THINK_TANK / "docs" / "codex-validation-report.md",
    THINK_TANK / "docs" / "capability-degradation-report.md",
    THINK_TANK / "docs" / "browser-automation-integration-report.md",
    THINK_TANK / "docs" / "minimal-install-behavior.md",
    THINK_TANK / "docs" / "codex-acceptance.md",
    THINK_TANK / "docs" / "codex-readiness-matrix.md",
    THINK_TANK / "platforms" / "codex" / "operating-guide.md",
    THINK_TANK / "platforms" / "codex" / "task-templates.md",
    THINK_TANK / "platforms" / "codex" / "capability-status.md",
    THINK_TANK / "examples" / "codex-smoke-research.md",
    THINK_TANK / "examples" / "codex-council-validation.md",
    THINK_TANK / "examples" / "codex-review-validation.md",
    THINK_TANK / "examples" / "codex-strategy-validation.md",
    THINK_TANK / "examples" / "codex-minimal-install-validation.md",
    THINK_TANK / "examples" / "browser-automation-integration.md",
    THINK_TANK / "examples" / "schema-sample-input.json",
    THINK_TANK / "examples" / "schema-sample-output.json",
    THINK_TANK / "examples" / "codex-operational-request.md",
    THINK_TANK / "examples" / "codex-operational-validation.md",
    THINK_TANK / "examples" / "codex-local-source-artifact.md",
    THINK_TANK / "examples" / "codex-local-source-validation.md",
    THINK_TANK / "examples" / "codex-external-source-validation.md",
    THINK_TANK / "examples" / "codex-browser-external-blocked.md",
]

CODEX_REPORT_REQUIRED_SNIPPETS = [
    "research_mode: verified",
    "council_mode: verified",
    "review_mode: verified",
    "strategy_mode: verified",
    "browser_automation_localhost: verified_optional",
    "local_source_markdown_artifact: verified",
    "external_source_readonly: verified",
    "browser_automation_external_web: blocked",
    "true_multi_agent_execution: planned",
]

MINIMAL_INSTALL_REQUIRED_SNIPPETS = [
    "最小安装只保证",
    "最小安装不保证",
    "capability 被选择",
    "capability 有可用实现",
    "capability 已真实执行",
    "capability 只走降级路径",
]

ACCEPTANCE_REQUIRED_SNIPPETS = [
    "Codex Acceptance",
    "必须通过",
    "不能声称",
    "验收命令",
    "通过标准",
]

READINESS_MATRIX_REQUIRED_SNIPPETS = [
    "Codex Readiness Matrix",
    "ready_before_claude_code_preflight",
    "external readonly source acquisition",
    "browser external readonly",
    "当前已经达到该状态",
]

OPERATING_GUIDE_REQUIRED_SNIPPETS = [
    "default_execution: single_agent_multi_profile",
    "最小安装默认行为",
    "能力状态规则",
    "验收命令",
]


def fail(message: str) -> None:
    raise SystemExit(f"Codex 验证检查失败: {message}")


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
    missing = [path for path in REQUIRED_VALIDATION_FILES if not path.exists()]
    if missing:
        fail("缺少文件: " + ", ".join(str(path.relative_to(ROOT)) for path in missing))


def check_codex_report() -> None:
    require_snippets(THINK_TANK / "docs" / "codex-validation-report.md", CODEX_REPORT_REQUIRED_SNIPPETS)


def check_minimal_install() -> None:
    require_snippets(THINK_TANK / "docs" / "minimal-install-behavior.md", MINIMAL_INSTALL_REQUIRED_SNIPPETS)


def check_acceptance_doc() -> None:
    require_snippets(THINK_TANK / "docs" / "codex-acceptance.md", ACCEPTANCE_REQUIRED_SNIPPETS)


def check_operating_guide() -> None:
    require_snippets(THINK_TANK / "platforms" / "codex" / "operating-guide.md", OPERATING_GUIDE_REQUIRED_SNIPPETS)


def check_readiness_matrix() -> None:
    require_snippets(THINK_TANK / "docs" / "codex-readiness-matrix.md", READINESS_MATRIX_REQUIRED_SNIPPETS)


def check_example_boundaries() -> None:
    for example in [
        THINK_TANK / "examples" / "codex-smoke-research.md",
        THINK_TANK / "examples" / "codex-council-validation.md",
        THINK_TANK / "examples" / "codex-review-validation.md",
        THINK_TANK / "examples" / "codex-strategy-validation.md",
        THINK_TANK / "examples" / "codex-minimal-install-validation.md",
        THINK_TANK / "examples" / "codex-operational-validation.md",
        THINK_TANK / "examples" / "codex-local-source-artifact.md",
        THINK_TANK / "examples" / "codex-local-source-validation.md",
        THINK_TANK / "examples" / "codex-external-source-validation.md",
        THINK_TANK / "examples" / "codex-browser-external-blocked.md",
    ]:
        content = read(example)
        if "## 边界" not in content:
            fail(f"{example.relative_to(ROOT)} 缺少 ## 边界")
        if "## Quality Check" not in content:
            fail(f"{example.relative_to(ROOT)} 缺少 ## Quality Check")


def main() -> None:
    check_required_files()
    check_codex_report()
    check_minimal_install()
    check_acceptance_doc()
    check_operating_guide()
    check_readiness_matrix()
    check_example_boundaries()
    print("Codex 验证检查通过")


if __name__ == "__main__":
    main()
