"""从 Claude Code agent frontmatter 生成 leader-runtime 专家候选。"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CLAUDE_AGENTS = ROOT / ".claude" / "agents"


def parse_frontmatter_text(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ValueError("agent file must start with YAML frontmatter")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError("agent file frontmatter is not closed")
    raw_frontmatter = text[4:end]
    body = text[end + 4 :].lstrip("\n")
    data = yaml.safe_load(raw_frontmatter) or {}
    if not isinstance(data, dict):
        raise ValueError("agent frontmatter must be a mapping")
    return data, body


def parse_agent_file(path: Path) -> tuple[dict[str, Any], str]:
    return parse_frontmatter_text(path.read_text(encoding="utf-8", errors="ignore"))


def _slug(value: str) -> str:
    lowered = value.lower()
    replaced = re.sub(r"[^a-z0-9]+", "_", lowered).strip("_")
    return replaced or "unnamed_agent"


def _tools_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value).split(",") if item.strip()]


def infer_domain(path: Path, root: Path = DEFAULT_CLAUDE_AGENTS) -> str:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return "unknown"
    parts = relative.parts
    return parts[0] if len(parts) > 1 else "root"


def infer_authority_scope(description: str, tools: list[str]) -> str:
    lowered = description.lower()
    if any(word in lowered for word in ["audit", "review", "qa", "checker", "compliance"]):
        return "review"
    if any(word in lowered for word in ["strategy", "strategist", "roadmap", "growth"]):
        return "strategy"
    if any(tool in tools for tool in ["Write", "Edit", "Bash"]):
        return "execution"
    return "analysis"


def normalize_frontmatter(path: Path, root: Path = DEFAULT_CLAUDE_AGENTS) -> dict[str, Any]:
    frontmatter, _body = parse_agent_file(path)
    name = str(frontmatter.get("name", "")).strip()
    description = str(frontmatter.get("description", "")).strip()
    if not name or not description:
        raise ValueError(f"agent frontmatter missing name or description: {path}")
    tools = _tools_list(frontmatter.get("tools"))
    domain = infer_domain(path, root)
    return {
        "source_platform": "claude-code",
        "source_path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
        "source_domain": domain,
        "agent_id": _slug(name),
        "name": name,
        "description": description,
        "color": frontmatter.get("color"),
        "emoji": frontmatter.get("emoji"),
        "vibe": frontmatter.get("vibe"),
        "tools": tools,
        "authority_scope_hint": infer_authority_scope(description, tools),
        "conversion_status": "candidate",
        "boundaries": [
            "Frontmatter parsing only creates a candidate; it does not register or invoke the agent.",
            "Local Claude Code agent content must be reviewed before entering public leader registry.",
        ],
    }


def iter_frontmatter_candidates(root: Path = DEFAULT_CLAUDE_AGENTS) -> list[dict[str, Any]]:
    if not root.exists():
        return []
    candidates: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.md")):
        try:
            candidates.append(normalize_frontmatter(path, root))
        except Exception:
            continue
    return candidates


def summarize_candidates(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    domains: dict[str, int] = {}
    authority_scopes: dict[str, int] = {}
    with_tools = 0
    for candidate in candidates:
        domains[candidate["source_domain"]] = domains.get(candidate["source_domain"], 0) + 1
        scope = candidate["authority_scope_hint"]
        authority_scopes[scope] = authority_scopes.get(scope, 0) + 1
        if candidate["tools"]:
            with_tools += 1
    return {
        "candidate_count": len(candidates),
        "with_tools": with_tools,
        "domains": dict(sorted(domains.items())),
        "authority_scopes": dict(sorted(authority_scopes.items())),
        "conversion_boundary": "candidate_only",
    }


if __name__ == "__main__":
    summary = summarize_candidates(iter_frontmatter_candidates())
    print(yaml.safe_dump(summary, allow_unicode=True, sort_keys=False))
