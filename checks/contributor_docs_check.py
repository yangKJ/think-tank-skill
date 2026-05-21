#!/usr/bin/env python3
"""检查 v2.1 社区治理和贡献文档。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(f"contributor docs 检查失败: {message}")


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
        ROOT / "CONTRIBUTING.md",
        [
            "Project Scope",
            "Evidence And Claim Rules",
            "Adding 2.0 Runtime Features",
            "Visual Assets",
            "Pull Request Checklist",
        ],
    )
    require_text(ROOT / "SECURITY.md", ["Security Policy", "High-risk operations", "Reporting A Vulnerability"])
    require_text(ROOT / "CODE_OF_CONDUCT.md", ["Code of Conduct", "Expected Behavior", "Unacceptable Behavior"])
    require_text(ROOT / "SUPPORT.md", ["Support", "Best-Effort Support", "Not Included"])
    require_text(ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md", ["Boundary Review", "Validation"])
    for name in ["bug_report.yml", "protocol_change.yml", "provider_pattern.yml", "config.yml"]:
        if not (ROOT / ".github" / "ISSUE_TEMPLATE" / name).exists():
            fail(f"缺少 issue template: {name}")
    require_text(ROOT / "think-tank" / "docs" / "faq.md", ["selected != invoked != recovered != verified"])
    require_text(ROOT / "think-tank" / "docs" / "troubleshooting.md", ["Provider claims look too strong"])
    require_text(ROOT / "think-tank" / "docs" / "quickstart-codex.md", ["Codex Quickstart"])
    print("contributor docs 检查通过")


if __name__ == "__main__":
    main()
