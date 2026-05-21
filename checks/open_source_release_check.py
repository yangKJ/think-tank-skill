#!/usr/bin/env python3
"""检查公开发布文案、支持矩阵和 stable 边界是否完整。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
README_CN = ROOT / "README_CN.md"
CHANGELOG = ROOT / "CHANGELOG.md"
THINK_TANK_README = ROOT / "think-tank" / "README.md"
QUICKSTART = ROOT / "think-tank" / "docs" / "open-source-quickstart.md"
SUPPORT_MATRIX = ROOT / "think-tank" / "docs" / "support-matrix.md"
VALIDATION_TIERS = ROOT / "think-tank" / "docs" / "validation-tiers.md"
HISTORY = ROOT / "think-tank" / "docs" / "history.md"
PROVIDER_ECOSYSTEM = ROOT / "think-tank" / "docs" / "provider-ecosystem-examples.md"
PROVIDER_PATTERNS = ROOT / "think-tank" / "docs" / "provider-integration-patterns.md"
CODEX_INSTALLATION = ROOT / "think-tank" / "docs" / "codex-installation.md"
V1_1_ROADMAP = ROOT / "think-tank" / "docs" / "v1.1-roadmap.md"
V1_1_RELEASE_NOTES = ROOT / "think-tank" / "docs" / "v1.1-release-notes.md"
V2_0_ROADMAP = ROOT / "think-tank" / "docs" / "v2.0-roadmap.md"
V2_0_RELEASE_NOTES = ROOT / "think-tank" / "docs" / "v2.0-release-notes.md"
V3_0_ROADMAP = ROOT / "think-tank" / "docs" / "v3.0-roadmap.md"
V3_0_RELEASE_NOTES = ROOT / "think-tank" / "docs" / "v3.0-release-notes.md"
OPEN_SOURCE_RELEASE = ROOT / "think-tank" / "docs" / "open-source-release.md"
CAPABILITY_STATUS = ROOT / "think-tank" / "platforms" / "codex" / "capability-status.md"
RELEASE_SUITE = ROOT / "checks" / "open_source_release_suite.py"
WORKFLOW = ROOT / ".github" / "workflows" / "open-source-release.yml"
PACKAGE_MANIFEST = ROOT / "public-release-manifest.yaml"
PUBLIC_RESEARCH = ROOT / "think-tank" / "examples" / "public" / "research-request.md"
PUBLIC_COUNCIL = ROOT / "think-tank" / "examples" / "public" / "council-decision.md"
PUBLIC_REVIEW = ROOT / "think-tank" / "examples" / "public" / "review-acceptance.md"
VISUALS = [
    ROOT / "think-tank" / "assets" / "brand" / "think-tank-hero-image2.png",
    ROOT / "think-tank" / "assets" / "brand" / "think-tank-hero-cn-image2.png",
    ROOT / "think-tank" / "assets" / "brand" / "think-tank-hero-v2-image2.png",
    ROOT / "think-tank" / "assets" / "brand" / "research-card-image2.png",
    ROOT / "think-tank" / "assets" / "brand" / "council-card-image2.png",
    ROOT / "think-tank" / "assets" / "brand" / "review-card-image2.png",
    ROOT / "think-tank" / "assets" / "brand" / "provider-ecosystem-image2.png",
    ROOT / "think-tank" / "assets" / "brand" / "research-os-memory-runtime-image2.png",
    ROOT / "think-tank" / "assets" / "brand" / "provider-ledger-image2.png",
    ROOT / "think-tank" / "assets" / "prompts" / "hero-image2-prompt.md",
    ROOT / "think-tank" / "assets" / "prompts" / "hero-v2-image2-prompt.md",
    ROOT / "think-tank" / "assets" / "prompts" / "hero-v2-cn-image2-prompt.md",
    ROOT / "think-tank" / "assets" / "prompts" / "provider-ecosystem-image2-prompt.md",
    ROOT / "think-tank" / "assets" / "prompts" / "research-os-memory-runtime-image2-prompt.md",
    ROOT / "think-tank" / "assets" / "prompts" / "provider-ledger-image2-prompt.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"open source release 检查失败: {message}")


def require_text(path: Path, terms: list[str]) -> str:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for term in terms:
        if term not in text:
            fail(f"{path.relative_to(ROOT)} 缺少: {term}")
    return text


def main() -> None:
    require_text(
        README,
        [
            "release_posture: stable_release",
            "[中文](README_CN.md)",
            "think-tank/docs/open-source-quickstart.md",
            "think-tank/docs/support-matrix.md",
            "think-tank/docs/validation-tiers.md",
            "think-tank/docs/provider-ecosystem-examples.md",
            "think-tank/docs/provider-integration-patterns.md",
            "think-tank/docs/codex-installation.md",
            "think-tank/protocol/skill-trigger-intelligence.md",
            "think-tank/protocol/skill-invocation-contract.md",
            "think-tank/protocol/progressive-disclosure.md",
            "think-tank/self-tests/",
            "think-tank/docs/open-source-release.md",
            "think-tank/examples/public/research-request.md",
            "think-tank/assets/brand/think-tank-hero-image2.png",
            "think-tank/assets/brand/provider-ecosystem-image2.png",
            "think-tank/assets/brand/research-os-memory-runtime-image2.png",
            "think-tank/assets/brand/provider-ledger-image2.png",
            "public-release-manifest.yaml",
            "python3 checks/open_source_release_suite.py",
            "python3 checks/open_source_release_check.py",
        ],
    )
    require_text(
        README_CN,
        [
            "[English](README.md)",
            "think-tank/assets/brand/think-tank-hero-cn-image2.png",
            "think-tank/assets/brand/research-os-memory-runtime-image2.png",
            "think-tank/assets/brand/provider-ledger-image2.png",
            "任务理解 + 角色组织 + 能力路由 + 证据汇总 + 边界声明",
            "python3 checks/open_source_release_suite.py",
            "python3 checks/stable_release_check.py",
            "think-tank/docs/provider-ecosystem-examples.md",
            "think-tank/docs/provider-integration-patterns.md",
            "think-tank/docs/codex-installation.md",
            "think-tank/protocol/skill-trigger-intelligence.md",
            "think-tank/protocol/skill-invocation-contract.md",
            "think-tank/protocol/progressive-disclosure.md",
            "CHANGELOG.md",
        ],
    )
    require_text(
        THINK_TANK_README,
        [
            "release_posture: stable_release",
            "docs/open-source-quickstart.md",
            "docs/support-matrix.md",
            "docs/validation-tiers.md",
            "docs/history.md",
            "docs/provider-ecosystem-examples.md",
            "docs/provider-integration-patterns.md",
            "docs/codex-installation.md",
            "docs/open-source-release.md",
            "examples/public/research-request.md",
            "examples/v3/",
            "../CHANGELOG.md",
            "skill_core_only_bundle",
            "python3 checks/open_source_release_suite.py",
            "python3 checks/open_source_release_check.py",
        ],
    )
    require_text(
        QUICKSTART,
        [
            "只安装 `think-tank` 时，默认保证",
            "只安装 `think-tank` 时，默认不保证",
            "think-tank/examples/public/research-request.md",
            "python3 checks/open_source_release_suite.py",
            "python3 checks/release_privacy_check.py",
            "python3 checks/open_source_release_check.py",
            "route selection 不等于 provider invocation",
        ],
    )
    require_text(
        SUPPORT_MATRIX,
        [
            "release_posture: stable_release",
            "multi_agent_runtime: verified_partial_with_scoped_write_lifecycle",
            "| Codex | verified_foundation |",
            "| Claude Code | deferred |",
            "| agent-reach | available_not_verified |",
            "default included?",
            "do not claim",
            "think-tank/docs/validation-tiers.md",
            "Not Claimed",
        ],
    )
    require_text(
        VALIDATION_TIERS,
        [
            "Tier 1: release gate",
            "Tier 2: core validation",
            "Tier 3: local provider validation",
            "provider_invoked",
        ],
    )
    require_text(
        HISTORY,
        [
            "维护者背景",
            "不是外部用户第一入口",
            "不能替代当前协议",
        ],
    )
    require_text(
        PROVIDER_ECOSYSTEM,
        [
            "optional_ecosystem_examples",
            "Representative Providers",
            "selected != dispatched != invoked != recovered != verified",
            "think-tank/assets/brand/provider-ecosystem-image2.png",
        ],
    )
    require_text(
        PROVIDER_PATTERNS,
        [
            "pattern_documented",
            "available_if_user_installs_provider",
            "requires_user_environment",
            "not_bundled",
            "selected != dispatched != invoked != recovered != verified",
        ],
    )
    require_text(
        CODEX_INSTALLATION,
        [
            "Copy The Skill Core",
            ".codex/",
            ".think-tank/",
            "provider being mentioned in docs means `pattern_documented`, not `invoked`",
        ],
    )
    require_text(
        V1_1_ROADMAP,
        [
            "Document provider integration patterns",
            "workflow pattern examples",
            "release_gate: v1_1_release_check",
        ],
    )
    require_text(
        V1_1_RELEASE_NOTES,
        [
            "Provider examples are patterns, not bundled capabilities",
            "python3 checks/v1_1_release_check.py",
        ],
    )
    require_text(
        V2_0_ROADMAP,
        [
            "Research OS + Memory Runtime",
            "protocol/run-record.md",
            "protocol/project-memory-runtime.md",
            "protocol/provider-invocation-ledger.md",
            "protocol/eval-pack.md",
        ],
    )
    require_text(
        V2_0_RELEASE_NOTES,
        [
            "Run Record",
            "Project Memory Runtime",
            "Provider Invocation Ledger",
            "python3 checks/v2_0_release_check.py",
        ],
    )
    require_text(
        V3_0_ROADMAP,
        [
            "Skill Experience Layer",
            "no built-in project-specific trigger words",
            "checks/skill_experience_check.py",
        ],
    )
    require_text(
        V3_0_RELEASE_NOTES,
        [
            "Skill Experience Layer",
            "user YAML policy owns actual trigger",
            "progressive disclosure",
        ],
    )
    require_text(
        CHANGELOG,
        [
            "## [3.0.0] - 2026-05-21",
            "Skill Experience Layer",
            "Research OS + Memory Runtime",
            "think-tank/assets/brand/think-tank-hero-v2-image2.png",
            "README Hero 图片回退为 v1 Image2 主视觉",
            "版本演进统一收敛到 `CHANGELOG.md`",
        ],
    )
    require_text(
        OPEN_SOURCE_RELEASE,
        [
            "safe_to_publish: true",
            "safe_to_market_as_stable_product: true",
            "versioning_hint: 1.0",
            "skill_core_only_bundle",
            "current default public release is `skill_core_only_bundle`",
            "python3 checks/open_source_release_suite.py",
            "python3 checks/open_source_release_check.py",
        ],
    )
    require_text(
        CAPABILITY_STATUS,
        [
            "external_research_skills_executable: per_provider_validation_required",
            "external_readonly_web_source: verified_partial",
            "codex_parallel_subagent_council: verified_partial",
            "current_default_release: skill_core_only_bundle",
        ],
    )
    require_text(
        PACKAGE_MANIFEST,
        [
            "current_default_release: skill_core_only_bundle",
            "skill_core_only_bundle:",
            "public_includes:",
            "public_excludes:",
            "skill_core",
            "skill_experience_docs",
            "skill_self_tests",
            "private_research_workspace",
            "closed_source_runtime_projects",
        ],
    )
    for path in [PUBLIC_RESEARCH, PUBLIC_COUNCIL, PUBLIC_REVIEW]:
        require_text(
            path,
            [
                "selected_intent:",
                "selected_mode:",
                "selected_profiles:",
                "invoked_providers:",
                "not_invoked_providers:",
                "boundaries:",
                "verification_status:",
            ],
        )
    for path in VISUALS:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")
        if path.suffix == ".md":
            require_text(path, ["Image2 Prompt"])
    require_text(
        RELEASE_SUITE,
        [
            "checks/release_privacy_check.py",
            "checks/markdown_image_links_check.py",
            "checks/v1_1_release_check.py",
            "checks/v2_0_release_check.py",
            "checks/skill_experience_check.py",
            "checks/public_package_boundary_check.py",
            "checks/open_source_release_check.py",
            "open source release suite 通过",
        ],
    )
    require_text(
        WORKFLOW,
        [
            "Open Source Release",
            "python3 checks/open_source_release_suite.py",
        ],
    )

    print("open source release 检查通过")


if __name__ == "__main__":
    main()
