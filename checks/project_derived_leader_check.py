#!/usr/bin/env python3
"""检查 leader-runtime 第二阶段项目派生能力。"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEADER_RUNTIME = ROOT / "leader-runtime"
DERIVATION = LEADER_RUNTIME / "runtime" / "project_derivation.py"


def fail(message: str) -> None:
    raise SystemExit(f"project derived leader 检查失败: {message}")


def load_module(path: Path, name: str):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"无法加载模块: {path.relative_to(ROOT)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def require_schema(name: str, required: list[str]) -> None:
    path = LEADER_RUNTIME / "schemas" / name
    if not path.exists():
        fail(f"缺少 schema: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    for field in required:
        if field not in data["required"]:
            fail(f"{name} required 缺少: {field}")


def main() -> None:
    for path in [
        LEADER_RUNTIME / "docs" / "project-derived-leader-model.md",
        LEADER_RUNTIME / "project-templates" / "README.md",
        LEADER_RUNTIME / "project-templates" / "project-leader.template.yaml",
        LEADER_RUNTIME / "project-templates" / "project-team-pack.template.yaml",
        DERIVATION,
    ]:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")

    require_schema(
        "project-leader.schema.json",
        ["project_id", "leader_id", "inherits_from", "team_pack_id", "acceptance_profile"],
    )
    require_schema(
        "project-team-pack.schema.json",
        ["pack_id", "project_id", "inherits_from_registry", "include_experts", "exclude_experts"],
    )

    module = load_module(DERIVATION, "leader_runtime_project_derivation")
    team_pack = module.default_project_team_pack("packs", ["packs", "ios"])
    if team_pack["pack_id"] != "packs-core-pack":
        fail("default_project_team_pack.pack_id 不正确")
    leader = module.default_project_leader("packs", "Packs", team_pack["pack_id"])
    if leader["inherits_from"] != "think_tank_global_leader":
        fail("default_project_leader.inherits_from 必须是 think_tank_global_leader")
    derived_registry = module.derive_project_registry(team_pack)
    if derived_registry["scope"] != "project":
        fail("derive_project_registry.scope 必须是 project")
    if not derived_registry["experts"]:
        fail("derive_project_registry 必须返回 experts")
    if any(item["owner_layer"] != "project" for item in derived_registry["experts"]):
        fail("项目派生 registry 的 owner_layer 必须全部是 project")
    derived_leader = module.derive_project_leader("packs", "Packs", team_pack)
    if derived_leader["team_pack_id"] != team_pack["pack_id"]:
        fail("derive_project_leader.team_pack_id 不匹配")
    if derived_leader["acceptance_profile"]["retry_limit"] != team_pack["acceptance_overrides"]["retry_limit"]:
        fail("项目 leader 未继承 acceptance override")

    print("project derived leader 检查通过")


if __name__ == "__main__":
    main()
