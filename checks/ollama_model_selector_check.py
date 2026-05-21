#!/usr/bin/env python3
"""检查 Ollama 本地模型选择决策树。"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELECTOR = ROOT / ".codex" / "skills" / "ollama-local-inference" / "scripts" / "select-model.py"


def fail(message: str) -> None:
    raise SystemExit(f"Ollama model selector 检查失败: {message}")


def run_selector(prompt: str, *models: str, quality: str = "auto") -> dict:
    command = [
        "python3",
        str(SELECTOR),
        "--prompt",
        prompt,
        "--quality",
        quality,
    ]
    for model in models:
        command.extend(["--installed-model", model])
    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if completed.returncode != 0:
        fail(completed.stderr or completed.stdout)
    return json.loads(completed.stdout)


def main() -> None:
    if not SELECTOR.exists():
        fail("缺少 select-model.py")

    strong = run_selector(
        "用本地模型深入分析这个项目，不要忽悠",
        "qwen3.6:35b",
        "qwen2.5-coder:7b",
    )
    if strong["selected_model"] != "qwen3.6:35b" or strong["desired_tier"] != "strong":
        fail(f"深度任务必须优先强模型: {strong}")

    degraded = run_selector(
        "用本地模型深入分析这个项目，不要忽悠",
        "qwen2.5-coder:7b",
    )
    if degraded["selected_model"] != "qwen2.5-coder:7b":
        fail(f"强模型缺失时必须降级到已安装快模型: {degraded}")
    if not any("preferred model is not installed" in item for item in degraded["boundaries"]):
        fail("降级时必须说明首选模型未安装")

    fast = run_selector(
        "本地运行时后台快速总结一下这段代码",
        "qwen3.6:35b",
        "qwen2.5-coder:7b",
    )
    if fast["selected_model"] != "qwen2.5-coder:7b" or fast["desired_tier"] != "fast":
        fail(f"本地运行时快速任务必须优先快模型: {fast}")

    smoke = run_selector(
        "hello 是否可用",
        "qwen2.5-coder:1.5b",
        "qwen2.5-coder:7b",
    )
    if smoke["selected_model"] != "qwen2.5-coder:1.5b" or smoke["desired_tier"] != "smoke":
        fail(f"连通性测试必须优先 smoke 模型: {smoke}")

    print("Ollama model selector 检查通过")


if __name__ == "__main__":
    main()
