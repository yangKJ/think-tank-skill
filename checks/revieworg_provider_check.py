#!/usr/bin/env python3
"""检查 ReviewORG provider 以非耦合方式接入 think-tank。"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".codex" / "skills" / "revieworg-audit-provider"
DECIDE = SKILL_DIR / "scripts" / "decide.py"
RUN_REVIEW = SKILL_DIR / "scripts" / "run-review.py"
CHECK_ENV = SKILL_DIR / "scripts" / "check-env.sh"
CORE = ROOT / "think-tank"


def fail(message: str) -> None:
    raise SystemExit(f"ReviewORG provider 检查失败: {message}")


def run_json(command: list[str]) -> tuple[int, dict]:
    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        fail(completed.stderr or completed.stdout)
    return completed.returncode, payload


def main() -> None:
    for path in [SKILL_DIR / "SKILL.md", DECIDE, RUN_REVIEW, CHECK_ENV]:
        if not path.exists():
            fail(f"缺少文件: {path.relative_to(ROOT)}")

    check_env = subprocess.run([str(CHECK_ENV)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if check_env.returncode != 0:
        fail(check_env.stderr or check_env.stdout)

    with tempfile.TemporaryDirectory(prefix="revieworg-provider-") as tmp:
        project = Path(tmp)
        (project / "app.py").write_text("def hello():\n    return 'ok'\n", encoding="utf-8")

        returncode, decision = run_json(
            [
                "python3",
                str(DECIDE),
                "--path",
                str(project),
                "--goal",
                "quality-review",
            ]
        )
        if returncode != 0 or decision["status"] not in {"success", "degraded"}:
            fail(f"只读 decide 失败: {decision}")
        if (project / ".revieworg").exists():
            fail("只读 decide 不得写入 .revieworg")
        if not str(decision["operation"]).startswith("decide_readonly"):
            fail("decide.py 必须标记 operation=decide_readonly*")

        blocked_code, blocked = run_json(
            [
                "python3",
                str(RUN_REVIEW),
                "--path",
                str(project),
                "--profile",
                "code-review",
                "--goal",
                "quality-review",
            ]
        )
        if blocked_code == 0 or blocked["status"] != "blocked_requires_permission":
            fail(f"run-review 默认必须阻止写入: {blocked}")
        if (project / ".revieworg").exists():
            fail("被阻止的 run-review 不得写入 .revieworg")

    forbidden_terms = ["revieworg run", "revieworg decide", ".revieworg/"]
    leaks: list[str] = []
    for path in CORE.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".py", ".yaml", ".yml", ".json"}:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        if any(term in content for term in forbidden_terms):
            leaks.append(str(path.relative_to(ROOT)))
    if leaks:
        fail(f"公开 think-tank core 不应写死 ReviewORG CLI 命令或私有资产目录: {', '.join(leaks[:5])}")

    print("ReviewORG provider 检查通过")


if __name__ == "__main__":
    main()
