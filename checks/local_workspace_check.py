#!/usr/bin/env python3
"""检查 .think-tank 本地工作区协议、模板和 Codex policy 加载顺序。"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "think-tank" / "platforms" / "codex" / "runtime"
POLICY_RUNTIME = RUNTIME_DIR / "provider_policy.py"
LOCAL_PROTOCOL = ROOT / "think-tank" / "protocol" / "local-workspace.md"
CONFIG_TEMPLATE = ROOT / "think-tank" / "templates" / "local-workspace-config.yaml"
PROVIDER_TEMPLATE = ROOT / "think-tank" / "templates" / "local-provider-policy.yaml"
WORKSPACE_SCHEMA = ROOT / "think-tank" / "schemas" / "local-workspace.schema.json"
LAYOUT_EXAMPLE = ROOT / "think-tank" / "examples" / "local-workspace-layout.md"
GITIGNORE = ROOT / ".gitignore"
OLD_SKILL_POLICY_PATH = "think-tank/" + "think-tank.provider" + "-policy.yaml"
OLD_POLICY_KEY = "legacy" + "_policy_paths"
OLD_RUNTIME_ATTRS = ["PROJECT" + "_POLICY", "SKILL" + "_LOCAL_POLICY"]


def fail(message: str) -> None:
    raise SystemExit(f"local workspace 检查失败: {message}")


def load_policy_module():
    sys.path.insert(0, str(RUNTIME_DIR))
    spec = importlib.util.spec_from_file_location("provider_policy", POLICY_RUNTIME)
    if spec is None or spec.loader is None:
        fail("无法加载 provider_policy.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require_text(path: Path, terms: list[str]) -> str:
    if not path.exists():
        fail(f"缺少文件: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    for term in terms:
        if term not in text:
            fail(f"{path.relative_to(ROOT)} 缺少: {term}")
    return text


def main() -> None:
    require_text(
        LOCAL_PROTOCOL,
        [
            ".think-tank/",
            "project-local",
            "policy_load_order",
            ".think-tank/provider-policy.yaml",
            "No legacy project-local policy path is supported in 2.0",
        ],
    )
    require_text(
        LAYOUT_EXAMPLE,
        [
            ".think-tank/",
            "config.yaml",
            "provider-policy.yaml",
            "memory/",
            "runs/",
            "artifacts/",
        ],
    )
    gitignore = require_text(GITIGNORE, [".think-tank/", ".codex/", "AGENTS.md"])
    if OLD_SKILL_POLICY_PATH in gitignore:
        fail(".gitignore 不应保留旧 skill-local provider policy 路径")

    config = yaml.safe_load(CONFIG_TEMPLATE.read_text(encoding="utf-8"))
    if config["policy"]["provider_policy"] != ".think-tank/provider-policy.yaml":
        fail("local workspace config provider_policy 路径不正确")
    if OLD_POLICY_KEY in config.get("policy", {}):
        fail("local workspace config 不应包含旧 policy 路径列表")
    if "think-tank/" not in config["memory"].get("forbidden_targets", []):
        fail("local workspace config 必须禁止默认写入 think-tank/")

    provider_policy = yaml.safe_load(PROVIDER_TEMPLATE.read_text(encoding="utf-8"))
    route_ids = {route["id"] for route in provider_policy.get("routes", [])}
    if "local-project-memory-capture" not in route_ids:
        fail("local provider policy 模板缺少 project memory capture route")
    memory_route = next(route for route in provider_policy["routes"] if route["id"] == "local-project-memory-capture")
    if memory_route["providers"].get("auto_select") is not False:
        fail("local project memory capture route 必须关闭 provider auto_select")

    schema = json.loads(WORKSPACE_SCHEMA.read_text(encoding="utf-8"))
    policy_props = schema["properties"]["policy"]["properties"]
    if OLD_POLICY_KEY in policy_props:
        fail("local workspace schema 不应允许旧 policy 路径列表")

    module = load_policy_module()
    if module.LOCAL_WORKSPACE_POLICY != ROOT / ".think-tank" / "provider-policy.yaml":
        fail("provider_policy.py 未使用 .think-tank/provider-policy.yaml")
    for attr in OLD_RUNTIME_ATTRS:
        if hasattr(module, attr):
            fail(f"provider_policy.py 不应保留旧属性: {attr}")
    effective_policy, sources = module.load_effective_policy()
    if module.DEFAULT_POLICY not in sources:
        fail("effective policy 必须包含默认 Codex policy")
    if module.LOCAL_WORKSPACE_POLICY.exists() and module.LOCAL_WORKSPACE_POLICY not in sources:
        fail("effective policy 必须包含 .think-tank provider policy")
    route_ids = {route["id"] for route in effective_policy.get("routes", [])}
    if "strategy-planning" not in route_ids:
        fail("本地 policy overlay 不应覆盖掉默认 strategy-planning route")
    if "local-project-memory-capture" not in route_ids:
        fail("effective policy 必须包含本地 project memory capture route")

    print("local workspace 检查通过")


if __name__ == "__main__":
    main()
