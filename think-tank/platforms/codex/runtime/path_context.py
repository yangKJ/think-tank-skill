#!/usr/bin/env python3
"""Resolve skill, project, and user-level think-tank paths for Codex installs."""

from __future__ import annotations

import os
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[3]
SOURCE_REPO_ROOT = SKILL_ROOT.parent
CODEX_HOME = Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser().resolve()
GLOBAL_SKILLS = CODEX_HOME / "skills"


def _env_path(name: str) -> Path | None:
    value = os.environ.get(name)
    if not value:
        return None
    return Path(value).expanduser().resolve()


def _user_think_tank_root() -> Path:
    return _env_path("THINK_TANK_GLOBAL_WORKSPACE_ROOT") or (Path.home() / ".think-tank").resolve()


USER_THINK_TANK_ROOT = _user_think_tank_root()


def _env_workspace_root() -> Path | None:
    return _env_path("THINK_TANK_WORKSPACE_ROOT")


def _is_inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _is_runtime_excluded(path: Path) -> bool:
    return (
        _is_inside(path, SKILL_ROOT)
        or _is_inside(path, CODEX_HOME)
        or path == USER_THINK_TANK_ROOT
        or _is_inside(path, USER_THINK_TANK_ROOT)
    )


def _looks_like_project_root(path: Path) -> bool:
    markers = [".think-tank", ".codex", ".claude", "AGENTS.md"]
    return any((path / marker).exists() for marker in markers)


def _fallback_project_roots(start: Path | None = None) -> list[Path]:
    """Return additional project candidates when normal traversal finds nothing.

    In some execution contexts (例如由平台直接启动适配器但 cwd 不在仓库内)，
    基于当前目录的自动发现会失效，此时尝试使用本插件安装目录中的本地配置。
    """
    candidate_roots = []
    if start is not None and (start / ".think-tank").exists():
        candidate_roots.append(start)
    skill_repo_root = SKILL_ROOT.parent
    if (skill_repo_root / ".think-tank").exists():
        candidate_roots.append(skill_repo_root)
    return candidate_roots


def project_root(start: Path | None = None) -> Path | None:
    """Return the nearest project root for project skills and path display."""

    explicit = _env_workspace_root()
    if explicit is not None:
        return explicit

    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if _is_runtime_excluded(candidate):
            continue
        if _looks_like_project_root(candidate):
            return candidate
    for candidate in _fallback_project_roots(current):
        if candidate is not None and _looks_like_project_root(candidate):
            return candidate
    return None


def project_think_tank_root(start: Path | None = None) -> Path | None:
    """Return the nearest project root that actually owns a .think-tank directory."""

    explicit = _env_workspace_root()
    if explicit is not None:
        return explicit if (explicit / ".think-tank").exists() else None

    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if _is_runtime_excluded(candidate):
            continue
        if (candidate / ".think-tank").exists():
            return candidate
    for candidate in _fallback_project_roots(current):
        if (candidate / ".think-tank").exists():
            return candidate
    return None


def workspace_root(start: Path | None = None) -> Path:
    """Return the active think-tank runtime workspace.

    Project-local ``.think-tank`` wins. If no project-local runtime exists, use
    the user-level ``~/.think-tank`` fallback instead of creating hidden runtime
    state in an arbitrary project.
    """

    return project_think_tank_root(start) or USER_THINK_TANK_ROOT


PROJECT_WORKSPACE_ROOT = project_root()
PROJECT_THINK_TANK_ROOT = project_think_tank_root()
WORKSPACE_ROOT = workspace_root()


def default_project_skills(root: Path | None = PROJECT_WORKSPACE_ROOT) -> Path | None:
    if root is None:
        return None
    candidates = [root / ".codex" / "skills", root / ".claude" / "skills"]
    for candidate in candidates:
        if candidate.exists() and any(path.parent.name != "think-tank" for path in candidate.glob("*/SKILL.md")):
            return candidate
    for candidate in candidates:
        if candidate.exists() and any(candidate.glob("*/SKILL.md")):
            return candidate
    return None


PROJECT_SKILLS = default_project_skills()
SKILL_DIRS = [path for path in [GLOBAL_SKILLS, PROJECT_SKILLS] if path is not None]


def display_path(path: Path) -> str:
    resolved = path.resolve() if path.exists() else path
    roots = [
        PROJECT_WORKSPACE_ROOT,
        USER_THINK_TANK_ROOT,
        GLOBAL_SKILLS,
        CODEX_HOME,
        SKILL_ROOT,
        SOURCE_REPO_ROOT,
    ]
    for root in roots:
        if root is None:
            continue
        try:
            return str(resolved.relative_to(root))
        except ValueError:
            continue
    return str(path)
