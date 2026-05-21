#!/usr/bin/env python3
"""检查公开发布文案、支持矩阵和 beta 边界是否完整。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
THINK_TANK_README = ROOT / "think-tank" / "README.md"
QUICKSTART = ROOT / "think-tank" / "docs" / "open-source-quickstart.md"
SUPPORT_MATRIX = ROOT / "think-tank" / "docs" / "support-matrix.md"
OPEN_SOURCE_RELEASE = ROOT / "think-tank" / "docs" / "open-source-release.md"
CAPABILITY_STATUS = ROOT / "think-tank" / "platforms" / "codex" / "capability-status.md"
RELEASE_SUITE = ROOT / "checks" / "open_source_release_suite.py"
WORKFLOW = ROOT / ".github" / "workflows" / "open-source-release.yml"
PACKAGE_MANIFEST = ROOT / "open-source-packages.yaml"


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
            "release_posture: public_beta",
            "think-tank/docs/open-source-quickstart.md",
            "think-tank/docs/support-matrix.md",
            "think-tank/docs/open-source-release.md",
            "open-source-packages.yaml",
            "python3 checks/open_source_release_suite.py",
            "python3 checks/open_source_release_check.py",
        ],
    )
    require_text(
        THINK_TANK_README,
        [
            "release_posture: public_beta",
            "docs/open-source-quickstart.md",
            "docs/support-matrix.md",
            "docs/open-source-release.md",
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
            "python3 checks/open_source_release_suite.py",
            "python3 checks/release_privacy_check.py",
            "python3 checks/open_source_release_check.py",
            "route selection 不等于 provider invocation",
        ],
    )
    require_text(
        SUPPORT_MATRIX,
        [
            "release_posture: public_beta",
            "multi_agent_runtime: verified_partial_for_readonly_council_only",
            "| Codex | verified_foundation |",
            "| Claude Code | deferred |",
            "| agent-reach | available_not_verified |",
            "Not Claimed",
        ],
    )
    require_text(
        OPEN_SOURCE_RELEASE,
        [
            "safe_to_publish: true",
            "safe_to_market_as_stable_product: false",
            "versioning_hint: 0.x",
            "full_repo_public_beta",
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
            "leader-runtime/**",
        ],
    )
    require_text(
        RELEASE_SUITE,
        [
            "checks/release_privacy_check.py",
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
