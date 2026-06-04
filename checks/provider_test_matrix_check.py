#!/usr/bin/env python3
"""检查 v2.4 provider test matrix 和样例 ledger。"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "think-tank" / "docs" / "provider-test-matrix.md"
LEDGER_DIR = ROOT / "think-tank" / "examples" / "providers" / "ledgers"
LEDGERS = [
    "source-acquisition-web-access.json",
    "social-listening-xiaohongshu.json",
    "media-processing-yt-dlp-whisper.json",
    "knowledge-persistence-obsidian.json",
    "media-production-research-to-video.json",
]
REQUIRED_KEYS = ["capability_slot", "provider_name", "state", "preflight", "dispatch", "invocation", "recovery", "verification", "failure_boundary"]


def fail(message: str) -> None:
    raise SystemExit(f"provider test matrix 检查失败: {message}")


def main() -> None:
    text = MATRIX.read_text(encoding="utf-8") if MATRIX.exists() else ""
    for term in ["Provider Test Matrix", "selected != invoked != recovered != verified", "failure boundary"]:
        if term not in text:
            fail(f"provider-test-matrix.md 缺少: {term}")
    for name in LEDGERS:
        path = LEDGER_DIR / name
        if not path.exists():
            fail(f"缺少 provider ledger: {name}")
        data = json.loads(path.read_text(encoding="utf-8"))
        for key in REQUIRED_KEYS:
            if key not in data:
                fail(f"{name} 缺少字段: {key}")
        if data["invocation"].get("invoked") is not False:
            fail(f"{name} public sample 不应标记 invoked=true")
        if "evidence_refs" not in data["verification"]:
            fail(f"{name} verification 缺少 evidence_refs")
    print("provider test matrix 检查通过")


if __name__ == "__main__":
    main()
