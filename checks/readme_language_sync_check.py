#!/usr/bin/env python3
"""检查英文和中文 README 的公开入口保持同步。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
README_CN = ROOT / "README_CN.md"

SHARED_LINKS = [
    "think-tank/README.md",
    "think-tank/docs/open-source-quickstart.md",
    "think-tank/docs/provider-ecosystem-examples.md",
    "think-tank/docs/provider-integration-patterns.md",
    "think-tank/docs/codex-installation.md",
    "think-tank/protocol/skill-trigger-intelligence.md",
    "think-tank/protocol/skill-invocation-contract.md",
    "think-tank/protocol/progressive-disclosure.md",
    "think-tank/docs/agent-compatibility-matrix.md",
    "think-tank/docs/skill-composition-guide.md",
    "think-tank/docs/skill-quality-score.md",
    "think-tank/examples/v3/",
    "think-tank/self-tests/",
    "think-tank/docs/index.md",
    "think-tank/docs/faq.md",
    "think-tank/docs/troubleshooting.md",
    "think-tank/docs/provider-test-matrix.md",
    "CHANGELOG.md",
    "python3 checks/open_source_release_suite.py",
    "python3 checks/stable_release_check.py",
]


def fail(message: str) -> None:
    raise SystemExit(f"README language sync 检查失败: {message}")


def require(path: Path, term: str) -> None:
    text = path.read_text(encoding="utf-8")
    if term not in text:
        fail(f"{path.relative_to(ROOT)} 缺少: {term}")


def main() -> None:
    require(README, "[中文](README_CN.md)")
    require(README_CN, "[English](README.md)")
    require(README, "think-tank/assets/brand/think-tank-hero-image2.png")
    require(README_CN, "think-tank/assets/brand/think-tank-hero-cn-image2.png")
    require(README, "think-tank/assets/brand/research-os-memory-runtime-image2.png")
    require(README_CN, "think-tank/assets/brand/research-os-memory-runtime-image2.png")
    for link in SHARED_LINKS:
        require(README, link)
        require(README_CN, link)
    print("README language sync 检查通过")


if __name__ == "__main__":
    main()
