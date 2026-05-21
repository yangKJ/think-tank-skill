#!/usr/bin/env python3
"""检查 v1.1 provider 接入模式文档没有写成能力承诺。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "think-tank" / "docs" / "provider-integration-patterns.md"
PATTERN_DIR = ROOT / "think-tank" / "examples" / "provider-patterns"
PATTERN_FILES = [
    PATTERN_DIR / "source-acquisition-web-access.md",
    PATTERN_DIR / "social-listening-xiaohongshu.md",
    PATTERN_DIR / "media-processing-yt-dlp-whisper.md",
    PATTERN_DIR / "knowledge-persistence-obsidian.md",
    PATTERN_DIR / "media-production-research-to-video.md",
]
REQUIRED_TERMS = [
    "pattern_documented",
    "available_if_user_installs_provider",
    "requires_user_environment",
    "not_bundled",
    "provider_boundary:",
    "route_selected:",
    "dispatch_decision:",
    "invoked_providers:",
    "not_invoked_providers:",
    "verification_status:",
]
FORBIDDEN_CLAIMS = [
    "think-tank supports xiaohongshu",
    "think-tank integrates yt-dlp",
    "think-tank provides Obsidian persistence",
    "All peer skills are invoked automatically",
]


def fail(message: str) -> None:
    raise SystemExit(f"provider integration patterns 检查失败: {message}")


def read_required(path: Path) -> str:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    paths = [DOC, *PATTERN_FILES]
    for path in paths:
        text = read_required(path)
        for term in REQUIRED_TERMS:
            if term not in text:
                fail(f"{path.relative_to(ROOT)} 缺少: {term}")
        for claim in FORBIDDEN_CLAIMS:
            if claim in text and "Do not write" not in text:
                fail(f"{path.relative_to(ROOT)} 出现未限定能力承诺: {claim}")

    doc_text = read_required(DOC)
    for link in [
        "source-acquisition-web-access.md",
        "social-listening-xiaohongshu.md",
        "media-processing-yt-dlp-whisper.md",
        "knowledge-persistence-obsidian.md",
        "media-production-research-to-video.md",
    ]:
        if link not in doc_text:
            fail(f"provider pattern index 缺少: {link}")

    print("provider integration patterns 检查通过")


if __name__ == "__main__":
    main()
