#!/usr/bin/env python3
"""Discover project-local Codex peer skills as think-tank providers."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from path_context import PROJECT_SKILLS, SKILL_DIRS, display_path



def parse_frontmatter_capabilities(skill_file: Path) -> list[str]:
    """Extract capabilities from SKILL.md YAML frontmatter.

    Reads the YAML frontmatter block (between ``---`` markers) and extracts the
    ``capabilities`` list. Returns an empty list if the file has no frontmatter or
    no capabilities field.

    This keeps think-tank/ provider-agnostic: capability declarations live in each
    skill's own SKILL.md, not in a hardcoded adapter registry.
    """
    text = skill_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return []

    # Locate the closing --- marker.
    end_idx: int | None = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return []

    # Walk the frontmatter block looking for a capabilities list.
    capabilities: list[str] = []
    in_capabilities = False
    for line in lines[1:end_idx]:
        stripped = line.strip()
        if stripped.startswith("capabilities:"):
            in_capabilities = True
        elif in_capabilities and stripped.startswith("- "):
            capabilities.append(stripped[2:].strip())
        elif in_capabilities and not stripped.startswith("-"):
            # We've left the capabilities list block.
            in_capabilities = False

    return capabilities


def first_heading(skill_file: Path) -> str:
    for line in skill_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return skill_file.parent.name


def provider_for_skill(skill_file: Path) -> dict[str, Any]:
    """Build a provider record from a skill's SKILL.md.

    Capabilities are read dynamically from the SKILL.md YAML frontmatter
    (``capabilities:`` list). When no capabilities are declared the skill is
    marked ``["unknown"]`` so it is still visible in the registry but never
    matched by capability-aware routing.

    Other fields use conservative defaults suitable for an unverified peer skill.
    Concrete provider policy (permission gates, recovery targets, access level
    overrides) belongs in ``.think-tank/provider-policy.yaml``, not here.
    """
    skill_name = skill_file.parent.name
    capabilities = parse_frontmatter_capabilities(skill_file)

    # Conservative defaults when SKILL.md does not declare capabilities.
    # These are intentionally broad — .think-tank/provider-policy.yaml is the
    # correct place to narrow access_level, requires_permission, and
    # recovery_targets per skill.
    if not capabilities:
        capabilities = ["unknown"]

    return {
        "id": skill_name,
        "title": first_heading(skill_file),
        "source": display_path(skill_file),
        "platform": "codex",
        "provider_type": "local_peer_skill",
        "capabilities": capabilities,
        "access_level": "readonly",
        "requires_permission": True,
        "recovery_targets": ["boundary_only"],
        "status": "available",
        "verification": "unknown",
    }


def discover_providers(skills_dirs: list[Path] | tuple[Path, ...] | Path | None = None) -> list[dict[str, Any]]:
    """Discover peer skills from global and project scopes.

    Global skills are loaded first. Project-local skills with the same name then
    override them, so project policy can specialize a provider without duplicate
    entries or ambiguous selection.

    Capability discovery is dynamic: each skill's capabilities are read from its
    ``SKILL.md`` YAML frontmatter rather than a hardcoded registry. Skills that
    do not declare capabilities are marked ``["unknown"]`` and are excluded from
    capability-aware routing.
    """

    if skills_dirs is None:
        search_dirs = SKILL_DIRS
    elif isinstance(skills_dirs, Path):
        search_dirs = [skills_dirs]
    else:
        search_dirs = list(skills_dirs)

    providers_by_id: dict[str, dict[str, Any]] = {}
    source_order: list[str] = []
    for skills_dir in search_dirs:
        if not skills_dir.exists():
            continue
        source_order.append(display_path(skills_dir))
        for skill_file in sorted(skills_dir.glob("*/SKILL.md")):
            if skill_file.parent.name == "think-tank":
                continue
            providers_by_id[skill_file.parent.name] = provider_for_skill(skill_file)
    return [providers_by_id[key] for key in sorted(providers_by_id)]


def registry(skills_dir: Path | None = None) -> dict[str, Any]:
    search_dirs = [skills_dir] if skills_dir is not None else SKILL_DIRS
    providers = discover_providers(search_dirs)
    return {
        "adapter": "codex",
        "registry_sources": [display_path(path) for path in search_dirs if path.exists()],
        "registry_source": ",".join(display_path(path) for path in search_dirs if path.exists()),
        "provider_count": len(providers),
        "providers": providers,
        "boundaries": [
            "Provider discovery does not invoke any skill.",
            "Provider availability does not mean the capability is verified.",
            "Concrete peer skill names belong to the Codex adapter or local registry, not the core protocol.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Discover Codex peer skills as think-tank providers.")
    parser.add_argument("--skills-dir", type=Path, default=None)
    args = parser.parse_args()
    print(json.dumps(registry(args.skills_dir), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
