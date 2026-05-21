#!/usr/bin/env python3
"""检查 capability 验证队列是否保持低风险顺序和边界。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT / "think-tank" / "docs" / "capability-validation-roadmap.md"


ORDER = [
    "### 1. Source Acquisition",
    "### 2. Browser Automation",
    "### 3. Knowledge Persistence",
    "### 4. Media Processing",
    "### 5. Social Listening",
]

REQUIRED_SNIPPETS = [
    "next_goal: minimal_runtime_verified_after_repeatable_procedure",
    "failure path does not fabricate sources or evidence",
    "no_login",
    "no_download",
    "repository_markdown",
    "user_provided_transcript",
    "user_provided_samples",
    "xiaohongshu_scraping",
    "login_or_cookie_flows",
    "不把 optional capability 写成 core dependency",
]


def fail(message: str) -> None:
    raise SystemExit(f"capability 队列检查失败: {message}")


def main() -> None:
    if not ROADMAP.exists():
        fail(f"缺少文件: {ROADMAP.relative_to(ROOT)}")
    content = ROADMAP.read_text(encoding="utf-8")
    positions = []
    for heading in ORDER:
        index = content.find(heading)
        if index < 0:
            fail(f"缺少队列项: {heading}")
        positions.append(index)
    if positions != sorted(positions):
        fail("capability 验证顺序被打乱")
    missing = [snippet for snippet in REQUIRED_SNIPPETS if snippet not in content]
    if missing:
        fail("缺少边界内容: " + ", ".join(missing))
    print("capability 队列检查通过")


if __name__ == "__main__":
    main()
