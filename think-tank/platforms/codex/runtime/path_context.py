#!/usr/bin/env python3
"""Resolve skill and workspace paths for copied or symlinked think-tank installs."""

from __future__ import annotations

import os
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[3]
SOURCE_REPO_ROOT = SKILL_ROOT.parent


def _env_workspace_root() -> Path | None:
    value = os.environ.get("THINK_TANK_WORKSPACE_ROOT")
    if not value:
        return None
    return Path(value).expanduser().resolve()


def _looks_like_workspace(path: Path) -> bool:
    return any((path / marker).exists() for marker in [".think-tank", ".codex", ".claude", "AGENTS.md"])


def workspace_root(start: Path | None = None) -> Path:
    explicit = _env_workspace_root()
    if explicit is not None:
        return explicit

    current = (start or Path.cwd()).resolve()
    candidates = [current, *current.parents]
    for candidate in candidates:
        if _looks_like_workspace(candidate):
            return candidate
    return SOURCE_REPO_ROOT


WORKSPACE_ROOT = workspace_root()


def default_project_skills(root: Path = WORKSPACE_ROOT) -> Path:
    candidates = [root / ".codex" / "skills", root / ".claude" / "skills"]
    for candidate in candidates:
        if candidate.exists() and any(path.parent.name != "think-tank" for path in candidate.glob("*/SKILL.md")):
            return candidate
    for candidate in candidates:
        if candidate.exists() and any(candidate.glob("*/SKILL.md")):
            return candidate
    return candidates[0]


PROJECT_SKILLS = default_project_skills()


def display_path(path: Path) -> str:
    resolved = path.resolve() if path.exists() else path
    for root in [WORKSPACE_ROOT, SKILL_ROOT, SOURCE_REPO_ROOT]:
        try:
            return str(resolved.relative_to(root))
        except ValueError:
            continue
    return str(path)
