#!/usr/bin/env python3
"""检查 think-tank 协议文档的最低完整性。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"


REQUIRED_FILES = [
    THINK_TANK / "SKILL.md",
    THINK_TANK / "README.md",
    THINK_TANK / "protocol" / "think-tank-protocol.md",
    THINK_TANK / "protocol" / "roles.md",
    THINK_TANK / "protocol" / "agent-selection.md",
    THINK_TANK / "protocol" / "intent-routing.md",
    THINK_TANK / "protocol" / "mode-selection.md",
    THINK_TANK / "protocol" / "quality-gates.md",
    THINK_TANK / "protocol" / "artifact-quality-gates.md",
    THINK_TANK / "protocol" / "runtime-contract.md",
    THINK_TANK / "protocol" / "state-result-contract.md",
    THINK_TANK / "protocol" / "consensus-contract.md",
    THINK_TANK / "protocol" / "subagent-runtime-contract.md",
    THINK_TANK / "protocol" / "post-run-curation.md",
    THINK_TANK / "protocol" / "versioning.md",
    THINK_TANK / "capabilities" / "README.md",
    THINK_TANK / "capabilities" / "slot-contract.md",
    THINK_TANK / "capabilities" / "media-production.md",
    THINK_TANK / "recipes" / "research-to-video.md",
    THINK_TANK / "routing" / "README.md",
    THINK_TANK / "routing" / "policy-schema.md",
    THINK_TANK / "routing" / "skill-router.md",
    THINK_TANK / "routing" / "dispatch-policy.md",
    THINK_TANK / "routing" / "result-recovery.md",
    THINK_TANK / "profiles" / "README.md",
    THINK_TANK / "profiles" / "prompt-pack.md",
    THINK_TANK / "platforms" / "claude-code" / "adapter.md",
    THINK_TANK / "platforms" / "claude-code" / "dispatch-contract.md",
    THINK_TANK / "platforms" / "claude-code" / "dispatch-prompt.md",
    THINK_TANK / "platforms" / "claude-code" / "final-validation-prompt.md",
    THINK_TANK / "platforms" / "claude-code" / "minimal-runtime.md",
    THINK_TANK / "platforms" / "claude-code" / "runtime-contract.md",
    THINK_TANK / "platforms" / "claude-code" / "runtime-pipeline.md",
    THINK_TANK / "platforms" / "claude-code" / "specialist-subagent-runtime.md",
    THINK_TANK / "platforms" / "claude-code" / "skill-mapping.md",
    THINK_TANK / "platforms" / "claude-code" / "agent-mapping.md",
    THINK_TANK / "platforms" / "codex" / "adapter.md",
    THINK_TANK / "platforms" / "codex" / "capability-mapping.md",
    THINK_TANK / "platforms" / "codex" / "capability-status.md",
    THINK_TANK / "platforms" / "codex" / "minimal-runtime.md",
    THINK_TANK / "platforms" / "codex" / "provider-registry.md",
    THINK_TANK / "platforms" / "codex" / "provider-policy.example.yaml",
    THINK_TANK / "platforms" / "codex" / "specialist-subagent-runtime.md",
    THINK_TANK / "platforms" / "codex" / "operating-guide.md",
    THINK_TANK / "platforms" / "codex" / "runtime" / "source_acquisition_minimal.py",
    THINK_TANK / "platforms" / "codex" / "runtime" / "pipeline.py",
    THINK_TANK / "platforms" / "codex" / "runtime" / "provider_registry.py",
    THINK_TANK / "platforms" / "codex" / "runtime" / "provider_policy.py",
    THINK_TANK / "platforms" / "codex" / "smoke-test.md",
    THINK_TANK / "platforms" / "codex" / "task-templates.md",
    THINK_TANK / "runtime" / "README.md",
    THINK_TANK / "runtime" / "__init__.py",
    THINK_TANK / "runtime" / "planner.py",
    THINK_TANK / "runtime" / "slot_resolver.py",
    THINK_TANK / "runtime" / "state_model.py",
    THINK_TANK / "runtime" / "consensus.py",
    THINK_TANK / "runtime" / "safety.py",
    THINK_TANK / "runtime" / "council.py",
    THINK_TANK / "runtime" / "subagent.py",
    THINK_TANK / "templates" / "README.md",
    THINK_TANK / "templates" / "deep-research.md",
    THINK_TANK / "templates" / "expert-meeting.md",
    THINK_TANK / "templates" / "task-kickoff.md",
    THINK_TANK / "templates" / "monitoring-brief.md",
    THINK_TANK / "templates" / "evidence-table.md",
    THINK_TANK / "templates" / "council-state.md",
    THINK_TANK / "templates" / "research-to-video-brief.md",
    THINK_TANK / "templates" / "video-storyboard.md",
    THINK_TANK / "templates" / "media-run-record.md",
    THINK_TANK / "domain-packs" / "README.md",
    THINK_TANK / "examples" / "codex-smoke-research.md",
    THINK_TANK / "examples" / "codex-council-validation.md",
    THINK_TANK / "examples" / "codex-review-validation.md",
    THINK_TANK / "examples" / "codex-strategy-validation.md",
    THINK_TANK / "examples" / "codex-minimal-install-validation.md",
    THINK_TANK / "examples" / "codex-operational-request.md",
    THINK_TANK / "examples" / "codex-operational-validation.md",
    THINK_TANK / "examples" / "codex-local-source-artifact.md",
    THINK_TANK / "examples" / "codex-local-source-validation.md",
    THINK_TANK / "examples" / "codex-external-source-validation.md",
    THINK_TANK / "examples" / "codex-browser-external-readonly.md",
    THINK_TANK / "examples" / "codex-long-running-adapter-runtime.md",
    THINK_TANK / "examples" / "codex-long-running-adapter-runtime.json",
    THINK_TANK / "examples" / "codex-subagent-lifecycle-validation.md",
    THINK_TANK / "examples" / "codex-subagent-lifecycle-validation.json",
    THINK_TANK / "examples" / "codex-runtime-sample.json",
    THINK_TANK / "examples" / "codex-runtime-failure-sample.json",
    THINK_TANK / "examples" / "claude-code-research-validation.md",
    THINK_TANK / "examples" / "claude-code-council-validation.md",
    THINK_TANK / "examples" / "claude-code-capability-discovery.md",
    THINK_TANK / "examples" / "claude-code-external-source-readonly.md",
    THINK_TANK / "examples" / "claude-code-adapter-dispatch-attempt.md",
    THINK_TANK / "examples" / "claude-code-dispatch-contract-sample.md",
    THINK_TANK / "examples" / "claude-code-dispatch-contract-validation.md",
    THINK_TANK / "examples" / "claude-code-dispatch-pre-invocation-validation.md",
    THINK_TANK / "examples" / "claude-code-final-validation.md",
    THINK_TANK / "examples" / "capability-degradation-media.md",
    THINK_TANK / "examples" / "capability-degradation-social.md",
    THINK_TANK / "examples" / "capability-degradation-knowledge.md",
    THINK_TANK / "examples" / "capability-degradation-browser.md",
    THINK_TANK / "examples" / "browser-automation-fixture.html",
    THINK_TANK / "examples" / "browser-automation-integration.md",
    THINK_TANK / "examples" / "schema-sample-input.json",
    THINK_TANK / "examples" / "schema-sample-output.json",
    THINK_TANK / "examples" / "runtime-e2e-fixture.json",
    THINK_TANK / "examples" / "post-run-curation-example.json",
    THINK_TANK / "examples" / "media-production-run-record.json",
    THINK_TANK / "examples" / "specialist-runtime-fixture.json",
    THINK_TANK / "examples" / "claude-dispatch-sample.json",
    THINK_TANK / "examples" / "claude-runtime-sample.json",
    THINK_TANK / "examples" / "claude-runtime-failure-sample.json",
    THINK_TANK / "docs" / "v0.1-readiness.md",
    THINK_TANK / "docs" / "v0.1-foundation-final.md",
    THINK_TANK / "docs" / "codex-validation-report.md",
    THINK_TANK / "docs" / "codex-external-skills-installation.md",
    THINK_TANK / "docs" / "codex-research-agent-takeover-test-plan.md",
    THINK_TANK / "docs" / "codex-acceptance.md",
    THINK_TANK / "docs" / "codex-readiness-matrix.md",
    THINK_TANK / "docs" / "open-source-quickstart.md",
    THINK_TANK / "docs" / "support-matrix.md",
    THINK_TANK / "docs" / "open-source-release.md",
    THINK_TANK / "docs" / "stable-release-criteria.md",
    THINK_TANK / "docs" / "stable-readiness-matrix.md",
    THINK_TANK / "docs" / "stable-release-checklist.md",
    THINK_TANK / "docs" / "capability-degradation-report.md",
    THINK_TANK / "docs" / "browser-automation-integration-report.md",
    THINK_TANK / "docs" / "claude-code-preflight.md",
    THINK_TANK / "docs" / "claude-code-validation-report.md",
    THINK_TANK / "docs" / "minimal-install-behavior.md",
    THINK_TANK / "docs" / "external-capability-testing-strategy.md",
    THINK_TANK / "docs" / "capability-validation-roadmap.md",
    THINK_TANK / "docs" / "runtime-mirror-report.md",
    THINK_TANK / "docs" / "final-acceptance-plan.md",
    THINK_TANK / "docs" / "research-migration-audit.md",
    THINK_TANK / "docs" / "legacy-think-tank-full-migration.md",
    THINK_TANK / "docs" / "legacy-runtime-safety.md",
    THINK_TANK / "docs" / "v0.2-runtime-hardening.md",
    THINK_TANK / "docs" / "v0.3-research-agent-migration.md",
    THINK_TANK / "docs" / "research-agent-full-inventory.md",
    THINK_TANK / "docs" / "external-skill-interoperability.md",
    THINK_TANK / "docs" / "v0.4-agent-council-migration.md",
    THINK_TANK / "docs" / "agent-council-full-inventory.md",
    THINK_TANK / "docs" / "agent-council-runtime-migration.md",
    THINK_TANK / "docs" / "agent-council-history-index.md",
    THINK_TANK / "docs" / "v0.5-specialist-subagent-runtime.md",
    THINK_TANK / "platforms" / "claude-code" / "legacy-team-runtime.md",
    THINK_TANK / "schemas" / "input.schema.json",
    THINK_TANK / "schemas" / "output.schema.json",
    THINK_TANK / "schemas" / "claude-dispatch.schema.json",
    THINK_TANK / "schemas" / "claude-runtime.schema.json",
    THINK_TANK / "schemas" / "runtime-result.schema.json",
    THINK_TANK / "schemas" / "role-result.schema.json",
    THINK_TANK / "schemas" / "post-run-curation.schema.json",
    THINK_TANK / "schemas" / "research-to-video.schema.json",
]

MODE_REQUIRED_SECTIONS = [
    "## 定位",
    "## 适用场景",
    "## 默认角色",
    "## 流程重点",
    "## 输出重点",
]

PROFILE_REQUIRED_SECTIONS = [
    "## 使命",
    "## 适用场景",
    "## 输入",
    "## 输出",
]

CAPABILITY_REQUIRED_SECTIONS = [
    "## 目的",
    "## 适用场景",
    "## 输入",
    "## 输出",
    "## 候选 skills",
    "## 降级策略",
]


def fail(message: str) -> None:
    raise SystemExit(f"协议检查失败: {message}")


def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not path.exists()]
    if missing:
        fail("缺少文件: " + ", ".join(str(path.relative_to(ROOT)) for path in missing))


def check_modes() -> None:
    for mode_file in sorted((THINK_TANK / "modes").glob("*.md")):
        if mode_file.name == "README.md":
            continue
        content = mode_file.read_text(encoding="utf-8")
        missing = [section for section in MODE_REQUIRED_SECTIONS if section not in content]
        if missing:
            fail(f"{mode_file.relative_to(ROOT)} 缺少章节: {', '.join(missing)}")


def check_profiles() -> None:
    for profile_file in sorted((THINK_TANK / "profiles").glob("*.md")):
        if profile_file.name == "README.md":
            continue
        content = profile_file.read_text(encoding="utf-8")
        missing = [section for section in PROFILE_REQUIRED_SECTIONS if section not in content]
        if missing:
            fail(f"{profile_file.relative_to(ROOT)} 缺少章节: {', '.join(missing)}")


def check_capabilities() -> None:
    for capability_file in sorted((THINK_TANK / "capabilities").glob("*.md")):
        if capability_file.name in {"README.md", "slot-contract.md"}:
            continue
        content = capability_file.read_text(encoding="utf-8")
        missing = [section for section in CAPABILITY_REQUIRED_SECTIONS if section not in content]
        if missing:
            fail(f"{capability_file.relative_to(ROOT)} 缺少章节: {', '.join(missing)}")


def check_json_schemas() -> None:
    for schema_file in sorted((THINK_TANK / "schemas").glob("*.json")):
        try:
            data = json.loads(schema_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"{schema_file.relative_to(ROOT)} 不是合法 JSON: {exc}")
        for key in ["$schema", "title", "type"]:
            if key not in data:
                fail(f"{schema_file.relative_to(ROOT)} 缺少 {key}")


def main() -> None:
    check_required_files()
    check_modes()
    check_profiles()
    check_capabilities()
    check_json_schemas()
    print("协议检查通过")


if __name__ == "__main__":
    main()
