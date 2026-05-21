#!/usr/bin/env python3
"""检查 Ollama 服务启动决策树不耦合 think-tank core。"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".codex" / "skills" / "ollama-local-inference"
ENSURE = SKILL_DIR / "scripts" / "ensure-service.py"
CHAT = SKILL_DIR / "scripts" / "chat.py"
CORE = ROOT / "think-tank"


def fail(message: str) -> None:
    raise SystemExit(f"Ollama service decision 检查失败: {message}")


def main() -> None:
    if not ENSURE.exists():
        fail("缺少 ensure-service.py")

    completed = subprocess.run(
        [
            "python3",
            str(ENSURE),
            "--base-url",
            "http://127.0.0.1:9",
            "--start",
            "--dry-run",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        fail(completed.stderr or completed.stdout)
    result = json.loads(completed.stdout)
    if result["status"] != "would_start":
        fail(f"dry-run 必须返回 would_start: {result}")
    if result["start_method"] != "ollama serve":
        fail("启动方式必须显式记录为 ollama serve")
    if "codex_host_model" not in result["fallbacks"]:
        fail("启动失败路径必须提供 Codex host model 兜底")

    chat_text = CHAT.read_text(encoding="utf-8")
    for term in ["ensure-service.py", "--start", "service_state", "model_selection", "invocation", "fallback"]:
        if term not in chat_text:
            fail(f"chat.py 缺少服务决策连接: {term}")

    failed = subprocess.run(
        [
            "python3",
            str(CHAT),
            "--base-url",
            "http://127.0.0.1:9",
            "--prompt",
            "用一句中文回答：你是否可用？",
            "--quality",
            "smoke",
            "--no-auto-start",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if failed.returncode == 0:
        fail("不可用服务下 chat.py 不应返回成功")
    payload = json.loads(failed.stdout)
    for field in ["service_state", "model_selection", "invocation", "fallback", "boundaries"]:
        if field not in payload:
            fail(f"失败输出缺少字段: {field}")
    if payload["invocation"]["attempted"]:
        fail("服务不可用时不得尝试模型调用")
    if not payload["fallback"]["used"]:
        fail("服务不可用时必须声明 fallback.used=true")

    core_mentions = [
        path
        for path in CORE.rglob("*")
        if path.is_file()
        and path.suffix in {".md", ".py", ".yaml", ".yml", ".json"}
        and "ollama serve" in path.read_text(encoding="utf-8", errors="ignore")
    ]
    if core_mentions:
        sample = ", ".join(str(path.relative_to(ROOT)) for path in core_mentions[:5])
        fail(f"公开 think-tank core 不应耦合 Ollama 启动命令: {sample}")

    print("Ollama service decision 检查通过")


if __name__ == "__main__":
    main()
