#!/usr/bin/env python3
"""检查 Codex provider policy YAML 是否能配置触发词和 provider 偏好。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "think-tank" / "platforms" / "codex" / "runtime"
POLICY_RUNTIME = RUNTIME_DIR / "provider_policy.py"
POLICY_EXAMPLE = ROOT / "think-tank" / "platforms" / "codex" / "provider-policy.example.yaml"
POLICY_SCHEMA = ROOT / "think-tank" / "routing" / "policy-schema.md"
PROJECT_SKILLS = ROOT / ".codex" / "skills"
SKILL_LOCAL_POLICY = ROOT / "think-tank" / "think-tank.provider-policy.yaml"


def fail(message: str) -> None:
    raise SystemExit(f"Codex provider policy 检查失败: {message}")


def load_module():
    sys.path.insert(0, str(RUNTIME_DIR))
    spec = importlib.util.spec_from_file_location("provider_policy", POLICY_RUNTIME)
    if spec is None or spec.loader is None:
        fail("无法加载 provider_policy.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if not POLICY_RUNTIME.exists():
        fail("缺少 provider_policy.py")
    if not POLICY_EXAMPLE.exists():
        fail("缺少 provider-policy.example.yaml")
    if not POLICY_SCHEMA.exists():
        fail("缺少 routing/policy-schema.md")

    schema = POLICY_SCHEMA.read_text(encoding="utf-8")
    for term in [
        "think-tank core 只定义",
        "policy 定义",
        "user_explicit_instruction",
        "project_local_policy",
        "Provider Rules",
    ]:
        if term not in schema:
            fail(f"policy-schema.md 缺少: {term}")

    policy = yaml.safe_load(POLICY_EXAMPLE.read_text(encoding="utf-8"))
    if not isinstance(policy, dict):
        fail("example policy 必须是 YAML mapping")
    if policy.get("version") != 1:
        fail("example policy version 必须是 1")
    routes = policy.get("routes")
    if not isinstance(routes, list) or not routes:
        fail("example policy 必须包含 routes")

    required_route_terms = {
        "id",
        "priority",
        "enabled",
        "triggers",
        "intent",
        "mode",
        "recipe",
        "capabilities",
        "providers",
        "fallback",
    }
    for route in routes:
        missing = required_route_terms - set(route)
        if missing:
            fail(f"route 缺少字段: {route.get('id')} -> {sorted(missing)}")

    module = load_module()
    if module.SKILL_LOCAL_POLICY != SKILL_LOCAL_POLICY:
        fail("provider_policy.py 的 skill-local policy 路径不正确")

    loaded_policy = module.load_policy(POLICY_EXAMPLE)
    provider_registry = module.registry(PROJECT_SKILLS)

    general = module.resolve_request("研究一下跨平台 Skill", loaded_policy, provider_registry["providers"])
    if not general["matched"] or general["selected_intent"] != "general_research":
        fail("研究一下 未命中 general_research policy route")

    competitive = module.resolve_request("竞品分析 Cursor 和 Windsurf", loaded_policy, provider_registry["providers"])
    if not competitive["matched"] or competitive["selected_intent"] != "competitive_intelligence":
        fail("竞品分析 未命中 competitive_intelligence policy route")
    competitive_route = competitive["skill_route"]
    if not competitive_route["selected_provider"]:
        fail("默认竞品分析路由应能选择一个通用 provider 或降级")

    council = module.resolve_request("开会讨论 routing policy 是否应该进入 adapter", loaded_policy, provider_registry["providers"])
    if not council["matched"] or council["selected_mode"] != "council":
        fail("开会讨论 未命中 council policy route")

    local_override = {
        "version": 1,
        "defaults": {"fallback": "core_protocol"},
        "routes": [
            {
                "id": "xiaohongshu-only",
                "priority": 100,
                "enabled": True,
                "triggers": {"match": "regex", "patterns": ["(上网研究|研究一下)"]},
                "intent": "user_feedback_analysis",
                "mode": "research",
                "recipe": "user-feedback-analysis",
                "profiles": ["source-collector"],
                "capabilities": ["social-listening", "source-acquisition"],
                "providers": {
                    "prefer": ["xiaohongshu"],
                    "allow": ["xiaohongshu"],
                    "deny": ["web-access", "google-ai-mode-skill"],
                },
                "fallback": "ask_user",
            }
        ],
    }
    override = module.resolve_request("上网研究这个产品的用户反馈", local_override, provider_registry["providers"])
    if not override["matched"]:
        fail("本地 override policy 未命中")
    skill_route = override["skill_route"]
    if "web-access" in skill_route["candidate_providers"]:
        fail("allow/deny policy 未排除 web-access")
    if PROJECT_SKILLS.exists() and (PROJECT_SKILLS / "xiaohongshu" / "SKILL.md").exists():
        if skill_route["selected_provider"] != "xiaohongshu":
            fail("小红书优先 policy 未选择 xiaohongshu")

    print("Codex provider policy 检查通过")


if __name__ == "__main__":
    main()
