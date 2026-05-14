#!/usr/bin/env python3
"""检查 routing 层是否承担 peer skill 中间连接职责且不绑定 core。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THINK_TANK = ROOT / "think-tank"
ROUTING = THINK_TANK / "routing"

REQUIRED_FILES = [
    ROUTING / "README.md",
    ROUTING / "policy-schema.md",
    ROUTING / "skill-router.md",
    ROUTING / "dispatch-policy.md",
    ROUTING / "result-recovery.md",
]

REQUIRED_ROUTING_TERMS = {
    "README.md": [
        "connect_capabilities_to_optional_peer_skills",
        "think_tank_core_depends_on_peer_skills: false",
        "旧任务编排技能",
        "recipes/competitive-intelligence.md",
        "routing/skill-router.md",
        "platforms/<platform>/",
    ],
    "skill-router.md": [
        "selected_intent:",
        "selected_recipe:",
        "selected_capabilities:",
        "available_providers:",
        "skill_route:",
        "dispatch_allowed:",
        "Capability Provider Requirements",
        "provider_requirements:",
        "Anti-Patterns",
    ],
    "policy-schema.md": [
        "routing policy",
        "routes:",
        "triggers:",
        "providers:",
        "missing_policy_behavior: use_adapter_defaults_or_core_protocol",
    ],
    "dispatch-policy.md": [
        "dispatch_request:",
        "dispatch_decision:",
        "Require Explicit Permission",
        "installed -> verified",
        "selected -> invoked",
        "invoked -> recovered",
    ],
    "result-recovery.md": [
        "recovery_targets:",
        "sources",
        "evidence",
        "role_result",
        "boundaries",
        "Failure Recovery",
    ],
}

ENTRYPOINT_TERMS = [
    "routing/skill-router.md",
    "routing/dispatch-policy.md",
    "routing/result-recovery.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"routing layer 检查失败: {message}")


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not path.exists()]
    if missing:
        fail("缺少 routing 文件: " + ", ".join(str(path.relative_to(ROOT)) for path in missing))

    for path in REQUIRED_FILES:
        content = path.read_text(encoding="utf-8")
        for term in REQUIRED_ROUTING_TERMS[path.name]:
            if term not in content:
                fail(f"{path.relative_to(ROOT)} 缺少: {term}")

    for rel in [
        "SKILL.md",
        "README.md",
        "protocol/intent-routing.md",
        "platforms/codex/trigger-routing.md",
        "platforms/codex/capability-mapping.md",
        "platforms/codex/provider-registry.md",
    ]:
        content = (THINK_TANK / rel).read_text(encoding="utf-8")
        for term in ENTRYPOINT_TERMS:
            if term not in content and rel in {"SKILL.md", "platforms/codex/trigger-routing.md"}:
                fail(f"{rel} 缺少 routing 入口: {term}")
        if rel == "README.md" and "技能路由中间层" not in content:
            fail("README.md 缺少 routing 层定位")
        if rel == "protocol/intent-routing.md" and "recipe 只声明" not in content:
            fail("intent-routing.md 缺少 recipe 与 routing 分工")
        if rel == "platforms/codex/capability-mapping.md" and "skill_route" not in content:
            fail("Codex capability mapping 缺少 skill_route 执行步骤")

    router = (ROUTING / "skill-router.md").read_text(encoding="utf-8")
    for forbidden in [
        "`竞品分析` 直接等于调用某个固定竞品分析 skill",
        "当前机器安装了某个知识库 skill 就默认写用户私有库",
        "当前机器安装了某个媒体 skill 就默认下载视频",
        "在主协议或通用 router 中维护平台私有 skill 名单",
    ]:
        if forbidden not in router:
            fail(f"skill-router.md 缺少反模式: {forbidden}")

    concrete_skill_terms = [
        "web-access",
        "playwright-cli",
        "xiaohongshu",
        "yt-dlp",
        "obsidian",
        "juejin-search",
        "36kr-hotlist",
        "mcp-cli",
    ]
    for term in concrete_skill_terms:
        if term in router:
            fail(f"skill-router.md 不应写死具体平台 skill: {term}")

    print("routing layer 检查通过")


if __name__ == "__main__":
    main()
