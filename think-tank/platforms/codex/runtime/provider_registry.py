#!/usr/bin/env python3
"""Discover project-local Codex peer skills as think-tank providers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
PROJECT_SKILLS = ROOT / ".codex" / "skills"


KNOWN_PROVIDER_RULES: dict[str, dict[str, Any]] = {
    "36kr-hotlist": {
        "capabilities": ["source-acquisition"],
        "access_level": "network",
        "requires_permission": False,
        "recovery_targets": ["sources", "evidence"],
    },
    "research-to-video-production": {
        "capabilities": ["media-processing", "knowledge-persistence"],
        "access_level": "write",
        "requires_permission": True,
        "recovery_targets": ["artifact", "role_result"],
    },
    "apple-reminders": {
        "capabilities": ["knowledge-persistence"],
        "access_level": "private",
        "requires_permission": True,
        "recovery_targets": ["artifact", "boundary_only"],
    },
    "google-ai-mode-skill": {
        "capabilities": ["source-acquisition"],
        "access_level": "network",
        "requires_permission": False,
        "recovery_targets": ["sources", "evidence"],
    },
    "gpt-image-2": {
        "capabilities": ["media-processing", "knowledge-persistence"],
        "access_level": "write",
        "requires_permission": True,
        "recovery_targets": ["artifact", "role_result", "boundary_only"],
    },
    "juejin-search": {
        "capabilities": ["source-acquisition"],
        "access_level": "network",
        "requires_permission": False,
        "recovery_targets": ["sources", "evidence"],
    },
    "jimeng-visual-prompt-pack": {
        "capabilities": ["media-processing", "knowledge-persistence"],
        "access_level": "readonly",
        "requires_permission": False,
        "recovery_targets": ["artifact", "role_result", "boundary_only"],
    },
    "kb-retriever": {
        "capabilities": ["source-acquisition", "knowledge-persistence"],
        "access_level": "readonly",
        "requires_permission": False,
        "recovery_targets": ["sources", "evidence", "role_result"],
    },
    "knowledge-graph-builder": {
        "capabilities": ["knowledge-persistence"],
        "access_level": "write",
        "requires_permission": True,
        "recovery_targets": ["artifact", "role_result"],
    },
    "mcp-cli": {
        "capabilities": ["source-acquisition"],
        "access_level": "privileged",
        "requires_permission": True,
        "recovery_targets": ["sources", "evidence", "boundary_only"],
    },
    "notebooklm": {
        "capabilities": ["knowledge-persistence"],
        "access_level": "private",
        "requires_permission": True,
        "recovery_targets": ["artifact", "boundary_only"],
    },
    "obsidian": {
        "capabilities": ["knowledge-persistence"],
        "access_level": "private",
        "requires_permission": True,
        "recovery_targets": ["artifact", "boundary_only"],
    },
    "omni-research": {
        "capabilities": ["source-acquisition"],
        "access_level": "network",
        "requires_permission": False,
        "recovery_targets": ["sources", "evidence", "role_result"],
    },
    "openai-whisper": {
        "capabilities": ["media-processing"],
        "access_level": "readonly",
        "requires_permission": False,
        "recovery_targets": ["artifact", "evidence"],
    },
    "ollama-local-inference": {
        "capabilities": ["knowledge-persistence"],
        "access_level": "private",
        "requires_permission": False,
        "recovery_targets": ["role_result", "evidence", "boundary_only"],
    },
    "pdf-extraction": {
        "capabilities": ["source-acquisition"],
        "access_level": "readonly",
        "requires_permission": False,
        "recovery_targets": ["sources", "evidence", "artifact"],
    },
    "playwright-cli": {
        "capabilities": ["browser-automation", "source-acquisition"],
        "access_level": "network",
        "requires_permission": False,
        "recovery_targets": ["sources", "evidence", "artifact"],
    },
    "research-workflow": {
        "capabilities": ["source-acquisition"],
        "access_level": "network",
        "requires_permission": False,
        "recovery_targets": ["sources", "evidence", "role_result"],
    },
    "revieworg-audit-provider": {
        "capabilities": ["knowledge-persistence"],
        "access_level": "write",
        "requires_permission": True,
        "recovery_targets": ["artifact", "evidence", "role_result", "boundary_only"],
    },
    "social-media-analyzer": {
        "capabilities": ["social-listening"],
        "access_level": "readonly",
        "requires_permission": False,
        "recovery_targets": ["evidence", "role_result"],
    },
    "product-intro-video": {
        "capabilities": ["media-processing", "knowledge-persistence"],
        "access_level": "write",
        "requires_permission": True,
        "recovery_targets": ["artifact", "role_result"],
    },
    "sketch-animation-video": {
        "capabilities": ["media-processing", "knowledge-persistence"],
        "access_level": "write",
        "requires_permission": True,
        "recovery_targets": ["artifact", "role_result"],
    },
    "sound-fx-for-video": {
        "capabilities": ["media-processing"],
        "access_level": "write",
        "requires_permission": True,
        "recovery_targets": ["artifact", "role_result"],
    },
    "stable-diffusion-image-generation": {
        "capabilities": ["media-processing"],
        "access_level": "write",
        "requires_permission": True,
        "recovery_targets": ["artifact", "boundary_only"],
    },
    "summarize": {
        "capabilities": ["source-acquisition", "media-processing"],
        "access_level": "readonly",
        "requires_permission": False,
        "recovery_targets": ["evidence", "role_result"],
    },
    "taskflow": {
        "capabilities": ["knowledge-persistence"],
        "access_level": "write",
        "requires_permission": True,
        "recovery_targets": ["artifact", "boundary_only"],
    },
    "vision-analysis": {
        "capabilities": ["media-processing"],
        "access_level": "readonly",
        "requires_permission": False,
        "recovery_targets": ["evidence", "role_result"],
    },
    "voxcpm-tts": {
        "capabilities": ["media-processing", "knowledge-persistence"],
        "access_level": "write",
        "requires_permission": True,
        "recovery_targets": ["artifact", "evidence", "role_result"],
    },
    "web-access": {
        "capabilities": ["source-acquisition", "browser-automation"],
        "access_level": "network",
        "requires_permission": False,
        "recovery_targets": ["sources", "evidence", "artifact"],
    },
    "web-design-engineer": {
        "capabilities": ["media-processing", "knowledge-persistence"],
        "access_level": "write",
        "requires_permission": True,
        "recovery_targets": ["artifact", "role_result"],
    },
    "web-video-presentation": {
        "capabilities": ["media-processing", "knowledge-persistence"],
        "access_level": "write",
        "requires_permission": True,
        "recovery_targets": ["artifact", "role_result"],
    },
    "xiaohongshu": {
        "capabilities": ["social-listening"],
        "access_level": "network",
        "requires_permission": True,
        "recovery_targets": ["sources", "evidence", "boundary_only"],
    },
    "xiaoyuzhou-transcribe": {
        "capabilities": ["media-processing"],
        "access_level": "network",
        "requires_permission": True,
        "recovery_targets": ["artifact", "evidence"],
    },
    "yt-dlp": {
        "capabilities": ["media-processing"],
        "access_level": "network",
        "requires_permission": True,
        "recovery_targets": ["artifact", "boundary_only"],
    },
}


def first_heading(skill_file: Path) -> str:
    for line in skill_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return skill_file.parent.name


def provider_for_skill(skill_file: Path) -> dict[str, Any]:
    skill_name = skill_file.parent.name
    rule = KNOWN_PROVIDER_RULES.get(
        skill_name,
        {
            "capabilities": [],
            "access_level": "readonly",
            "requires_permission": True,
            "recovery_targets": ["boundary_only"],
        },
    )
    return {
        "id": skill_name,
        "title": first_heading(skill_file),
        "source": str(skill_file.relative_to(ROOT)),
        "platform": "codex",
        "provider_type": "local_peer_skill",
        "capabilities": rule["capabilities"],
        "access_level": rule["access_level"],
        "requires_permission": rule["requires_permission"],
        "recovery_targets": rule["recovery_targets"],
        "status": "available",
        "verification": "unknown",
    }


def discover_providers(skills_dir: Path = PROJECT_SKILLS) -> list[dict[str, Any]]:
    if not skills_dir.exists():
        return []
    providers: list[dict[str, Any]] = []
    for skill_file in sorted(skills_dir.glob("*/SKILL.md")):
        if skill_file.parent.name == "think-tank":
            continue
        providers.append(provider_for_skill(skill_file))
    return providers


def registry(skills_dir: Path = PROJECT_SKILLS) -> dict[str, Any]:
    providers = discover_providers(skills_dir)
    return {
        "adapter": "codex",
        "registry_source": str(skills_dir.relative_to(ROOT)) if skills_dir.exists() else str(skills_dir),
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
    parser.add_argument("--skills-dir", type=Path, default=PROJECT_SKILLS)
    args = parser.parse_args()
    print(json.dumps(registry(args.skills_dir), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
