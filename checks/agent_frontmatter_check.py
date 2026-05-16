#!/usr/bin/env python3
"""检查 Claude agent frontmatter 到 leader-runtime candidate 的桥接契约。"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEADER_RUNTIME = ROOT / "leader-runtime"
FRONTMATTER = LEADER_RUNTIME / "runtime" / "agent_frontmatter.py"
SAMPLE = LEADER_RUNTIME / "examples" / "claude-agent-frontmatter.sample.md"
SCHEMA = LEADER_RUNTIME / "schemas" / "source-agent-frontmatter.schema.json"
LOCAL_CLAUDE_AGENTS = ROOT / ".claude" / "agents"


def fail(message: str) -> None:
    raise SystemExit(f"agent frontmatter 检查失败: {message}")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"无法加载模块: {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    for path in [FRONTMATTER, SAMPLE, SCHEMA]:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for field in [
        "source_platform",
        "source_path",
        "source_domain",
        "agent_id",
        "name",
        "description",
        "tools",
        "authority_scope_hint",
        "conversion_status",
        "boundaries",
    ]:
        if field not in schema["required"]:
            fail(f"source-agent-frontmatter.schema.json required 缺少: {field}")

    module = load_module(FRONTMATTER, "leader_runtime_agent_frontmatter")
    sample = module.normalize_frontmatter(SAMPLE, LEADER_RUNTIME / "examples")
    if sample["name"] != "Product Strategy Analyst":
        fail("样例 frontmatter name 解析失败")
    if sample["source_platform"] != "claude-code":
        fail("source_platform 必须是 claude-code")
    if sample["conversion_status"] != "candidate":
        fail("frontmatter 输出必须保持 candidate 状态")
    if sample["authority_scope_hint"] != "strategy":
        fail("authority_scope_hint 推断不正确")
    if not sample["tools"]:
        fail("tools 必须被解析为列表")

    candidates = module.iter_frontmatter_candidates(LOCAL_CLAUDE_AGENTS)
    summary = module.summarize_candidates(candidates)
    if LOCAL_CLAUDE_AGENTS.exists() and summary["candidate_count"] == 0:
        fail("本地 .claude/agents 存在时应能解析至少一个 candidate")
    if summary["conversion_boundary"] != "candidate_only":
        fail("summary 必须声明 candidate_only 边界")

    print("agent frontmatter 检查通过")


if __name__ == "__main__":
    main()
