#!/usr/bin/env python3
"""Capability slot resolver and validator."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class CapabilityResolution:
    capability: str
    required: bool
    candidate_implementations: list[str]
    selected_implementation: str | None
    availability: str
    invocation_status: str
    capability_status: str
    boundary: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def resolve_capability(
    capability: str,
    platform_mapping: dict[str, list[str]],
    available_implementations: set[str],
    required: bool = False,
) -> CapabilityResolution:
    candidates = platform_mapping.get(capability, [])
    selected = next((candidate for candidate in candidates if candidate in available_implementations), None)
    if selected:
        return CapabilityResolution(
            capability=capability,
            required=required,
            candidate_implementations=candidates,
            selected_implementation=selected,
            availability="available",
            invocation_status="skipped",
            capability_status="verified_partial",
            boundary="Implementation is available but runtime invocation must still be verified.",
        )
    return CapabilityResolution(
        capability=capability,
        required=required,
        candidate_implementations=candidates,
        selected_implementation=None,
        availability="unavailable",
        invocation_status="skipped",
        capability_status="unavailable",
        boundary="Required capability missing; degrade or stop." if required else "Optional capability omitted with boundary.",
    )


def resolve_slots(
    required_capabilities: list[str],
    optional_capabilities: list[str],
    platform_mapping: dict[str, list[str]],
    available_implementations: set[str],
) -> dict[str, Any]:
    resolutions = [
        resolve_capability(cap, platform_mapping, available_implementations, required=True)
        for cap in required_capabilities
    ]
    resolutions.extend(
        resolve_capability(cap, platform_mapping, available_implementations, required=False)
        for cap in optional_capabilities
    )
    missing_required = [
        item.capability for item in resolutions if item.required and item.availability != "available"
    ]
    return {
        "resolutions": [item.to_dict() for item in resolutions],
        "missing_required": missing_required,
        "can_continue": not missing_required,
        "boundaries": [item.boundary for item in resolutions if item.boundary],
    }


if __name__ == "__main__":
    import json

    mapping = {
        "source-acquisition": ["local_static_reader", "web.run"],
        "browser-automation": ["browser", "playwright"],
    }
    result = resolve_slots(["source-acquisition"], ["browser-automation"], mapping, {"local_static_reader"})
    print(json.dumps(result, ensure_ascii=False, indent=2))
