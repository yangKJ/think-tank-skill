#!/usr/bin/env python3
"""检查 README 视觉资产治理规则。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "think-tank" / "assets"
BRAND = ASSETS / "brand"
PROMPTS = ASSETS / "prompts"
REQUIRED_FILES = [
    ASSETS / "README.md",
    BRAND / "README.md",
    PROMPTS / "README.md",
    BRAND / "think-tank-hero-image2.png",
    BRAND / "think-tank-hero-cn-image2.png",
    BRAND / "think-tank-hero-v2-image2.png",
    BRAND / "research-card-image2.png",
    BRAND / "council-card-image2.png",
    BRAND / "review-card-image2.png",
    BRAND / "provider-ecosystem-image2.png",
    BRAND / "research-os-memory-runtime-image2.png",
    PROMPTS / "hero-image2-prompt.md",
    PROMPTS / "hero-v2-image2-prompt.md",
    PROMPTS / "hero-v2-cn-image2-prompt.md",
    PROMPTS / "provider-ecosystem-image2-prompt.md",
    PROMPTS / "research-os-memory-runtime-image2-prompt.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"visual assets 检查失败: {message}")


def main() -> None:
    for path in REQUIRED_FILES:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")

    svg_files = [path for path in ASSETS.rglob("*.svg")]
    if svg_files:
        fail("不应重新引入 SVG 主展示资产: " + ", ".join(str(p.relative_to(ROOT)) for p in svg_files))

    asset_readme = (ASSETS / "README.md").read_text(encoding="utf-8")
    for term in ["Use PNG images", "Do not add SVG", "Every README image link"]:
        if term not in asset_readme:
            fail(f"think-tank/assets/README.md 缺少治理规则: {term}")

    brand_readme = (BRAND / "README.md").read_text(encoding="utf-8")
    for term in ["readme_visual_format: png", "source_prompt_required: true", "svg_primary_visuals: disallowed"]:
        if term not in brand_readme:
            fail(f"think-tank/assets/brand/README.md 缺少: {term}")

    print("visual assets 检查通过")


if __name__ == "__main__":
    main()
