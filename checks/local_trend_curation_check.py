#!/usr/bin/env python3
"""检查本地趋势研究和任务收口链路。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".think-tank"
RUNTIME_DIR = ROOT / "think-tank" / "platforms" / "codex" / "runtime"
POLICY_RUNTIME = RUNTIME_DIR / "provider_policy.py"
PROJECT_SKILLS = ROOT / ".codex" / "skills"


def fail(message: str) -> None:
    raise SystemExit(f"local trend curation 检查失败: {message}")


def load_policy_module():
    sys.path.insert(0, str(RUNTIME_DIR))
    spec = importlib.util.spec_from_file_location("provider_policy", POLICY_RUNTIME)
    if spec is None or spec.loader is None:
        fail("无法加载 provider_policy.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require_text(relative: str, terms: list[str]) -> None:
    path = LOCAL / relative
    if not path.exists():
        fail(f"缺少文件: .think-tank/{relative}")
    text = path.read_text(encoding="utf-8")
    for term in terms:
        if term not in text:
            fail(f".think-tank/{relative} 缺少: {term}")


def main() -> None:
    policy = yaml.safe_load((LOCAL / "provider-policy.yaml").read_text(encoding="utf-8"))
    routes = {route["id"]: route for route in policy.get("routes", [])}
    trend_route = routes.get("local-trend-radar")
    if not trend_route:
        fail("缺少 local-trend-radar route")
    patterns = "\n".join(trend_route.get("triggers", {}).get("patterns", []))
    for term in ["行业趋势", "市场趋势", "热门文章"]:
        if term not in patterns:
            fail(f"local-trend-radar 缺少触发词: {term}")

    module = load_policy_module()
    provider_registry = module.registry(PROJECT_SKILLS)
    result = module.resolve_request(
        "分析一下 AI 的行业趋势",
        policy,
        provider_registry["providers"],
    )
    if result.get("route_id") != "local-trend-radar":
        fail(f"AI 行业趋势未命中 local-trend-radar: {result.get('route_id')}")
    if result.get("selected_mode") != "research":
        fail("趋势分析必须进入 research mode")
    if "trend-analyst" not in result.get("selected_profiles", []):
        fail("趋势分析必须包含 trend-analyst profile")
    if not result.get("skill_route", {}).get("candidate_providers"):
        fail("趋势分析必须产生 provider 候选")

    require_text("trends/trend-template.yaml", ["source_ids", "opportunities", "risks", "next_review_at"])
    require_text("trends/trend-to-action-template.md", ["Trend to Action", "Action Mapping"])
    require_text("curation/post-run-curation-template.yaml", ["source_candidates", "artifact_plan", "trend_candidates"])
    require_text("sources/source-ledger-candidate-template.yaml", ["used_for", "verification_status"])
    require_text("runbooks/post-run-curation.md", ["Required Closing Questions", "source_candidates"])

    print("local trend curation 检查通过")


if __name__ == "__main__":
    main()
