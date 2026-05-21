#!/usr/bin/env python3
"""检查本地 Obsidian 轻量知识模式。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "think-tank" / "platforms" / "codex" / "runtime"
POLICY_RUNTIME = RUNTIME_DIR / "provider_policy.py"
PREFLIGHT_RUNTIME = RUNTIME_DIR / "provider_preflight.py"
PROJECT_SKILLS = ROOT / ".codex" / "skills"
LOCAL_POLICY = ROOT / ".think-tank" / "provider-policy.yaml"
LOCAL_PREFLIGHT = ROOT / ".think-tank" / "provider-preflight.yaml"


def fail(message: str) -> None:
    raise SystemExit(f"Obsidian knowledge mode 检查失败: {message}")


def load_module(path: Path, name: str):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"无法加载模块: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if not (PROJECT_SKILLS / "obsidian" / "SKILL.md").exists():
        fail("缺少 .codex/skills/obsidian/SKILL.md")
    if not LOCAL_POLICY.exists():
        fail("缺少 .think-tank/provider-policy.yaml")
    if not LOCAL_PREFLIGHT.exists():
        fail("缺少 .think-tank/provider-preflight.yaml")

    policy_data = yaml.safe_load(LOCAL_POLICY.read_text(encoding="utf-8"))
    routes = {route["id"]: route for route in policy_data.get("routes", [])}
    route = routes.get("local-obsidian-knowledge-mode")
    if not route:
        fail("本地 policy 缺少 local-obsidian-knowledge-mode")
    if route.get("priority", 0) <= 175:
        fail("Obsidian 知识模式优先级应高于通用查资料路线")
    if route["providers"]["prefer"][0] != "obsidian":
        fail("Obsidian 知识模式必须优先选择 obsidian")
    for denied in ["web-access", "google-ai-mode-skill", "xiaohongshu", "yt-dlp"]:
        if denied not in route["providers"].get("deny", []):
            fail(f"Obsidian 知识模式必须默认排除外部采集 provider: {denied}")
    write_policy = route.get("write_policy", {})
    if write_policy.get("default") != "read_only":
        fail("Obsidian 知识模式默认必须 read_only")
    if write_policy.get("obsidian_write_requires_confirmation") is not True:
        fail("Obsidian 写入必须显式确认")

    policy_module = load_module(POLICY_RUNTIME, "provider_policy")
    loaded_policy = policy_module.load_policy(LOCAL_POLICY)
    provider_registry = policy_module.registry(PROJECT_SKILLS)
    result = policy_module.resolve_request(
        "查我的 Obsidian，看看之前有没有产品竞品资料",
        loaded_policy,
        provider_registry["providers"],
    )
    if result.get("route_id") != "local-obsidian-knowledge-mode":
        fail(f"Obsidian 查询未命中正确 route: {result.get('route_id')}")
    if result["skill_route"]["selected_provider"] != "obsidian":
        fail("Obsidian 查询必须选择 obsidian provider")
    if "web-access" in result["skill_route"]["candidate_providers"]:
        fail("Obsidian 查询不应把 web-access 作为候选 provider")

    preflight_data = yaml.safe_load(LOCAL_PREFLIGHT.read_text(encoding="utf-8"))
    obsidian_rule = preflight_data.get("providers", {}).get("obsidian", {})
    if "obsidian-cli" not in obsidian_rule.get("requires", {}).get("commands", []):
        fail("Obsidian preflight 必须检查 obsidian-cli")
    if obsidian_rule.get("risk") != "private_knowledge_write_guarded":
        fail("Obsidian preflight 必须标记 private_knowledge_write_guarded")
    notes = "\n".join(obsidian_rule.get("notes", []))
    for term in ["默认只读检索", "写入", ".think-tank/inbox"]:
        if term not in notes:
            fail(f"Obsidian preflight notes 缺少: {term}")

    preflight_module = load_module(PREFLIGHT_RUNTIME, "provider_preflight")
    effective_preflight, _ = preflight_module.load_effective_preflight()
    preflight = preflight_module.preflight_provider("obsidian", effective_preflight)
    if preflight["provider"] != "obsidian":
        fail("Obsidian preflight provider 字段错误")
    if preflight.get("requires_permission") is not True:
        fail("Obsidian preflight 必须声明 requires_permission")
    if "kb-retriever" not in preflight.get("fallbacks", []):
        fail("Obsidian preflight 必须提供 kb-retriever 降级")
    if preflight["status"] not in {"ready", "available_unverified", "needs_install"}:
        fail(f"Obsidian preflight 状态异常: {preflight['status']}")

    print("Obsidian knowledge mode 检查通过")


if __name__ == "__main__":
    main()
