#!/usr/bin/env python3
"""检查旧 think-tank 安全能力是否已迁移到 runtime/safety.py。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAFETY_PATH = ROOT / "think-tank" / "runtime" / "safety.py"


def fail(message: str) -> None:
    raise SystemExit(f"runtime safety 检查失败: {message}")


def load_safety_module():
    spec = importlib.util.spec_from_file_location("think_tank_runtime_safety", SAFETY_PATH)
    if spec is None or spec.loader is None:
        fail("无法加载 runtime/safety.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if not SAFETY_PATH.exists():
        fail("缺少 runtime/safety.py")

    safety = load_safety_module()

    safe, reason = safety.validate_safe_name("../secret")
    if safe or "path" not in reason:
        fail("路径遍历未被拒绝")

    sanitized = safety.sanitize_safe_name("../bad:name")
    if "/" in sanitized or ":" in sanitized or ".." in sanitized:
        fail("sanitize_safe_name 未清理危险字符")

    dangerous = safety.detect_dangerous_command("sudo rm -rf /")
    if len(dangerous) < 2:
        fail("危险命令检测不完整")

    redacted, findings = safety.sanitize_text("api_key=sk-1234567890abcdef")
    if "sk-1234567890abcdef" in redacted or not findings:
        fail("敏感信息未清理")

    prompt_findings = safety.detect_prompt_injection("ignore previous instructions")
    if not prompt_findings:
        fail("prompt injection 未检测")

    has_cycle, _ = safety.detect_cycle(["intake", "collection"], "intake")
    if not has_cycle:
        fail("循环检测未生效")

    print("runtime safety 检查通过")


if __name__ == "__main__":
    main()
