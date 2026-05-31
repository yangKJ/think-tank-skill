#!/usr/bin/env python3
"""检查 Codex provider preflight 决策树。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "think-tank" / "platforms" / "codex" / "runtime"
PREFLIGHT_RUNTIME = RUNTIME_DIR / "provider_preflight.py"
PREFLIGHT_EXAMPLE = ROOT / "think-tank" / "platforms" / "codex" / "provider-preflight.example.yaml"
PROJECT_LOCAL_PREFLIGHT = ROOT / ".think-tank" / "provider-preflight.yaml"
LOCAL_PREFLIGHT = (
    PROJECT_LOCAL_PREFLIGHT
    if (ROOT / ".think-tank").exists()
    else (Path.home() / ".think-tank" / "provider-preflight.yaml").resolve()
)


def fail(message: str) -> None:
    raise SystemExit(f"Codex provider preflight 检查失败: {message}")


def load_module():
    sys.path.insert(0, str(RUNTIME_DIR))
    spec = importlib.util.spec_from_file_location("provider_preflight", PREFLIGHT_RUNTIME)
    if spec is None or spec.loader is None:
        fail("无法加载 provider_preflight.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if not PREFLIGHT_RUNTIME.exists():
        fail("缺少 provider_preflight.py")
    if not PREFLIGHT_EXAMPLE.exists():
        fail("缺少 provider-preflight.example.yaml")

    example = yaml.safe_load(PREFLIGHT_EXAMPLE.read_text(encoding="utf-8"))
    if not isinstance(example, dict) or example.get("version") != 1:
        fail("example preflight 必须是 version=1 YAML mapping")
    providers = example.get("providers")
    if not isinstance(providers, dict) or not providers:
        fail("example preflight 必须包含 providers mapping")
    for required in ["revieworg-audit-provider", "ollama-local-inference", "voxcpm-tts", "gpt-image-2", "xiaohongshu", "obsidian", "web-access"]:
        if required not in providers:
            fail(f"example preflight 缺少 provider: {required}")

    module = load_module()
    if module.LOCAL_WORKSPACE_PREFLIGHT != LOCAL_PREFLIGHT:
        fail("provider_preflight.py 的 local preflight 路径不正确")

    effective_policy, sources = module.load_effective_preflight()
    if module.DEFAULT_PREFLIGHT not in sources:
        fail("effective preflight 必须包含默认 preflight")
    if PROJECT_LOCAL_PREFLIGHT.exists() and PROJECT_LOCAL_PREFLIGHT not in sources:
        fail("effective preflight 必须包含 project-local .think-tank preflight")

    # Provider assertions must use the public example, not the user's global
    # ~/.think-tank overlay, otherwise the release check depends on local state.
    policy = example

    voxcpm = module.preflight_provider("voxcpm-tts", policy)
    if voxcpm["status"] not in {"ready", "needs_install", "needs_key_or_env", "available_unverified"}:
        fail(f"voxcpm-tts 状态异常: {voxcpm['status']}")
    if "narration_manifest" not in voxcpm["fallbacks"]:
        fail("voxcpm-tts 必须提供 narration_manifest 降级")
    if voxcpm["can_invoke"] and voxcpm["missing"]:
        fail("有缺失项时不得 can_invoke=true")

    ollama = module.preflight_provider("ollama-local-inference", policy)
    if ollama["status"] not in {"ready", "needs_install", "needs_local_model", "service_unavailable"}:
        fail(f"ollama-local-inference 状态异常: {ollama['status']}")
    if "codex_host_model" not in ollama["fallbacks"]:
        fail("ollama-local-inference 必须提供 codex_host_model 降级")

    revieworg = module.preflight_provider("revieworg-audit-provider", policy)
    if revieworg["status"] not in {"ready", "needs_install", "available_unverified"}:
        fail(f"revieworg-audit-provider 状态异常: {revieworg['status']}")
    if not revieworg["requires_permission"]:
        fail("revieworg-audit-provider 必须声明 requires_permission=true")
    if "think_tank_review_mode" not in revieworg["fallbacks"]:
        fail("revieworg-audit-provider 必须提供 think_tank_review_mode 降级")

    xhs = module.preflight_provider("xiaohongshu", policy)
    if "user_exported_samples" not in xhs["fallbacks"]:
        fail("xiaohongshu 必须提供 user_exported_samples 降级")
    if not xhs["manual_checks"]:
        fail("xiaohongshu 必须声明登录态/MCP 手动检查")

    notebooklm = module.preflight_provider("notebooklm", policy)
    if notebooklm["status"] not in {"ready", "needs_install", "available_unverified"}:
        fail(f"notebooklm 状态异常: {notebooklm['status']}")
    if not notebooklm["requires_permission"] and not notebooklm["manual_checks"]:
        fail("notebooklm 必须声明登录态或人工确认边界")
    if notebooklm["fallbacks"][:3] != ["kb-retriever", "summarize", "obsidian"]:
        fail("notebooklm 必须优先降级到 kb-retriever / summarize / obsidian")
    if notebooklm["risk"] != "private_login":
        fail("notebooklm 必须标记 private_login")

    unknown = module.preflight_provider("unknown-provider", policy)
    if unknown["status"] != "unknown" or unknown["can_invoke"] is not False:
        fail("未知 provider 必须返回 unknown 且不可调用")

    print("Codex provider preflight 检查通过")


if __name__ == "__main__":
    main()
