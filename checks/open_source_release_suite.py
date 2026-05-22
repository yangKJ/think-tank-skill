#!/usr/bin/env python3
"""运行公开发布所需的核心检查集合。"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    ["python3", "checks/protocol_check.py"],
    ["python3", "checks/intent_recipe_check.py"],
    ["python3", "checks/template_check.py"],
    ["python3", "checks/codex_validation_check.py"],
    ["python3", "checks/schema_sample_check.py"],
    ["python3", "checks/project_competitive_strategy_check.py"],
    ["python3", "checks/host_enhancement_backfeed_check.py"],
    ["python3", "checks/minimal_runtime_execution_check.py"],
    ["python3", "checks/runtime_provenance_check.py"],
    ["python3", "checks/codex_runtime_verification_matrix_check.py"],
    ["python3", "checks/codex_runtime_pipeline_check.py"],
    ["python3", "checks/release_privacy_check.py"],
    ["python3", "checks/markdown_image_links_check.py"],
    ["python3", "checks/provider_integration_patterns_check.py"],
    ["python3", "checks/workflow_patterns_check.py"],
    ["python3", "checks/readme_language_sync_check.py"],
    ["python3", "checks/visual_assets_check.py"],
    ["python3", "checks/v1_1_release_check.py"],
    ["python3", "checks/v2_0_release_check.py"],
    ["python3", "checks/contributor_docs_check.py"],
    ["python3", "checks/research_workspace_template_check.py"],
    ["python3", "checks/eval_pack_check.py"],
    ["python3", "checks/provider_test_matrix_check.py"],
    ["python3", "checks/docs_site_check.py"],
    ["python3", "checks/skill_experience_check.py"],
    ["python3", "checks/public_package_boundary_check.py"],
    ["python3", "checks/open_source_release_check.py"],
]


def fail(message: str) -> None:
    raise SystemExit(f"open source release suite 失败: {message}")


def main() -> None:
    for command in COMMANDS:
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        if completed.returncode != 0:
            stdout = completed.stdout.strip()
            stderr = completed.stderr.strip()
            detail = stdout or stderr or f"exit={completed.returncode}"
            fail(f"{' '.join(command)} -> {detail}")
    print("open source release suite 通过")


if __name__ == "__main__":
    main()
