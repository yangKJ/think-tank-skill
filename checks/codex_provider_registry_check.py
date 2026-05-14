#!/usr/bin/env python3
"""检查 Codex provider registry 是否把本地 peer skills 暴露为可选 providers。"""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "think-tank" / "platforms" / "codex" / "runtime" / "provider_registry.py"
REGISTRY_DOC = ROOT / "think-tank" / "platforms" / "codex" / "provider-registry.md"
PROJECT_SKILLS = ROOT / ".codex" / "skills"


def fail(message: str) -> None:
    raise SystemExit(f"Codex provider registry 检查失败: {message}")


def load_module():
    spec = importlib.util.spec_from_file_location("provider_registry", REGISTRY_PATH)
    if spec is None or spec.loader is None:
        fail("无法加载 provider_registry.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if not REGISTRY_PATH.exists():
        fail("缺少 provider_registry.py")
    if not REGISTRY_DOC.exists():
        fail("缺少 provider-registry.md")

    doc = REGISTRY_DOC.read_text(encoding="utf-8")
    for term in [
        "required_for_core_think_tank: false",
        "missing_registry_behavior: degrade_to_core_protocol",
        "发现 provider 不等于调用 provider",
        "routing/skill-router.md",
    ]:
        if term not in doc:
            fail(f"provider-registry.md 缺少边界声明: {term}")

    module = load_module()
    empty_registry = module.registry(ROOT / ".codex" / "missing-skills")
    if empty_registry["provider_count"] != 0 or empty_registry["providers"]:
        fail("缺失 .codex/skills 时必须返回空 provider registry")

    if not PROJECT_SKILLS.exists():
        print("Codex provider registry 检查跳过本地 provider: .codex/skills 不存在")
        return

    current_registry = module.registry(PROJECT_SKILLS)
    providers = current_registry["providers"]
    provider_ids = {provider["id"] for provider in providers}
    for required in ["web-access", "summarize", "yt-dlp", "obsidian", "xiaohongshu"]:
        if (PROJECT_SKILLS / required / "SKILL.md").exists() and required not in provider_ids:
            fail(f"本地 skill 未注册为 provider: {required}")

    for provider in providers:
        for field in [
            "id",
            "platform",
            "provider_type",
            "capabilities",
            "access_level",
            "requires_permission",
            "recovery_targets",
            "status",
            "verification",
        ]:
            if field not in provider:
                fail(f"provider 缺少字段 {field}: {provider}")
        if provider["id"] != "think-tank" and provider["status"] != "available":
            fail(f"已发现 provider 状态必须是 available: {provider['id']}")
        if provider["verification"] != "unknown":
            fail(f"发现 provider 不能自动标记 verified: {provider['id']}")

    print(f"Codex provider registry 检查通过: providers={len(providers)}")


if __name__ == "__main__":
    main()
