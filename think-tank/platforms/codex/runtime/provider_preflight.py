#!/usr/bin/env python3
"""Evaluate provider execution prerequisites without invoking providers."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml

from path_context import SKILL_ROOT, WORKSPACE_ROOT, display_path

DEFAULT_PREFLIGHT = SKILL_ROOT / "platforms" / "codex" / "provider-preflight.example.yaml"
LOCAL_WORKSPACE_PREFLIGHT = WORKSPACE_ROOT / ".think-tank" / "provider-preflight.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Preflight policy must be a mapping: {path}")
    return data


def merge_preflight(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    if not base:
        return overlay
    if not overlay:
        return base
    merged = dict(base)
    merged["defaults"] = {**(base.get("defaults", {}) or {}), **(overlay.get("defaults", {}) or {})}
    base_providers = dict(base.get("providers", {}) or {})
    overlay_providers = dict(overlay.get("providers", {}) or {})
    merged["providers"] = {**base_providers, **overlay_providers}
    return merged


def load_effective_preflight(explicit: Path | None = None) -> tuple[dict[str, Any], list[Path]]:
    if explicit is not None:
        return load_yaml(explicit), [explicit]
    default = load_yaml(DEFAULT_PREFLIGHT)
    if LOCAL_WORKSPACE_PREFLIGHT.exists():
        local = load_yaml(LOCAL_WORKSPACE_PREFLIGHT)
        return merge_preflight(default, local), [DEFAULT_PREFLIGHT, LOCAL_WORKSPACE_PREFLIGHT]
    return default, [DEFAULT_PREFLIGHT]


def selected_preflight_path(explicit: Path | None = None) -> Path:
    if explicit is not None:
        return explicit
    if LOCAL_WORKSPACE_PREFLIGHT.exists():
        return LOCAL_WORKSPACE_PREFLIGHT
    return DEFAULT_PREFLIGHT


def rel(path: Path) -> str:
    return display_path(path)


def command_available(command: str) -> bool:
    return shutil.which(command) is not None


def python_importable(module: str) -> bool:
    completed = subprocess.run(
        ["python3", "-c", f"import {module}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.returncode == 0


def env_present(name: str) -> bool:
    return bool(os.environ.get(name))


def file_exists(path: str) -> bool:
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = WORKSPACE_ROOT / candidate
    return candidate.exists()


def ollama_model_available(model: str, base_url: str = "http://127.0.0.1:11434") -> tuple[bool, bool]:
    try:
        with urllib.request.urlopen(f"{base_url.rstrip('/')}/api/tags", timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return False, False
    models = payload.get("models", [])
    names = {item.get("name") for item in models if isinstance(item, dict)}
    aliases = {item.get("model") for item in models if isinstance(item, dict)}
    return model in names or model in aliases, True


def evaluate_checks(requirements: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    missing: list[str] = []
    present: list[str] = []
    skipped: list[str] = []

    for item in requirements.get("commands", []) or []:
        name = str(item)
        (present if command_available(name) else missing).append(f"command:{name}")

    for item in requirements.get("python_imports", []) or []:
        name = str(item)
        (present if python_importable(name) else missing).append(f"python_import:{name}")

    for item in requirements.get("env", []) or []:
        name = str(item)
        (present if env_present(name) else missing).append(f"env:{name}")

    for item in requirements.get("files", []) or []:
        name = str(item)
        (present if file_exists(name) else missing).append(f"file:{name}")

    ollama_base_url = str(requirements.get("ollama_base_url", "http://127.0.0.1:11434"))
    for item in requirements.get("ollama_models", []) or []:
        name = str(item)
        model_present, service_reachable = ollama_model_available(name, ollama_base_url)
        if model_present:
            present.append(f"ollama_model:{name}")
        elif service_reachable:
            missing.append(f"ollama_model:{name}")
        else:
            missing.append(f"service:{ollama_base_url}/api/tags")

    for item in requirements.get("manual", []) or []:
        skipped.append(f"manual:{item}")

    return missing, present, skipped


def status_for(provider_rule: dict[str, Any], missing: list[str], skipped: list[str]) -> tuple[str, bool]:
    if provider_rule.get("blocked", False):
        return "blocked", False
    if missing:
        if any(item.startswith("env:") for item in missing):
            return "needs_key_or_env", False
        if any(item.startswith("ollama_model:") for item in missing):
            return "needs_local_model", False
        if any(item.startswith("python_import:") or item.startswith("command:") for item in missing):
            return "needs_install", False
        if any(item.startswith("file:") for item in missing):
            return "needs_local_file", False
        if any(item.startswith("service:") for item in missing):
            return "service_unavailable", False
        return "degraded", False
    if skipped and provider_rule.get("manual_required_is_blocking", False):
        return "needs_manual_confirmation", False
    if skipped:
        return "available_unverified", False
    return "ready", True


def preflight_provider(provider_id: str, policy: dict[str, Any]) -> dict[str, Any]:
    providers = policy.get("providers", {}) or {}
    defaults = policy.get("defaults", {}) or {}
    rule = providers.get(provider_id)
    if not rule:
        return {
            "provider": provider_id,
            "status": defaults.get("missing_provider_behavior", "unknown"),
            "can_invoke": False,
            "missing": [],
            "present": [],
            "manual_checks": [],
            "fallbacks": defaults.get("fallbacks", ["core_protocol"]),
            "boundaries": ["No provider preflight rule exists."],
        }

    requirements = rule.get("requires", {}) or {}
    missing, present, skipped = evaluate_checks(requirements)
    status, can_invoke = status_for(rule, missing, skipped)
    return {
        "provider": provider_id,
        "status": status,
        "can_invoke": can_invoke,
        "missing": missing,
        "present": present,
        "manual_checks": skipped,
        "fallbacks": rule.get("fallbacks", defaults.get("fallbacks", ["core_protocol"])),
        "requires_permission": bool(rule.get("requires_permission", False)),
        "risk": rule.get("risk", "normal"),
        "notes": rule.get("notes", []),
        "boundaries": [
            "Preflight checks prerequisites only; it does not invoke the provider.",
            "A ready status does not prove end-to-end result recovery.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate a Codex provider preflight decision tree.")
    parser.add_argument("provider")
    parser.add_argument("--preflight", type=Path)
    args = parser.parse_args()

    policy, sources = load_effective_preflight(args.preflight)
    result = preflight_provider(args.provider, policy)
    selected_path = selected_preflight_path(args.preflight)
    result["preflight_path"] = rel(selected_path)
    result["preflight_sources"] = [rel(source) for source in sources]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
