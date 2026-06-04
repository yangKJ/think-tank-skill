#!/usr/bin/env python3
"""Codex post-dispatch hook safety regression test.

通过直接导入 _gate_post_dispatch 和 invoke_post_dispatch，对 orchestrator
的 post-dispatch 门禁做单元回归测试。验证：

  1. A hook that prints status=success but exits with returncode != 0
     is overridden to status=failed.
  2. A hook that exits 0 with status=success but provides no recovery
     evidence (artifacts/evidence/output_path/...) is downgraded to
     status=failed.
  3. (positive control) A well-behaved hook that exits 0 with status=success
     and recovery evidence is allowed through.
  4. The gate refuses to call any hook when the preflight is not cleared:
     - hook provider missing
     - selected provider missing
     - hook provider != policy-selected provider (mismatch)
     - preflight.can_invoke = False
     - preflight.requires_permission = True
     - preflight.manual_checks non-empty
  5. The gate passes (returns None) only when every precondition holds.

This is a regression test for findings from the Codex adversarial review on
the previous 10 commits — specifically that a hook could fake a successful
recovery just by printing {"status":"success"} to stdout, and that
post_dispatch auto-invocation ignored provider_preflight results.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "think-tank" / "platforms" / "codex" / "runtime"
sys.path.insert(0, str(RUNTIME_DIR))

from orchestrator import _gate_post_dispatch, _has_recovery_evidence, invoke_post_dispatch  # noqa: E402


def fail(message: str) -> None:
    raise SystemExit(f"Codex post-dispatch safety 检查失败: {message}")


def make_hook(workdir: Path, name: str, body: str) -> Path:
    path = workdir / name
    path.write_text(body, encoding="utf-8")
    return path


def run_hook(hook: Path, extra_cfg: dict | None = None) -> dict:
    cfg = {
        "provider": "throwaway-test-provider",
        "entrypoint": str(hook.relative_to(hook.parent.parent)),
        "enabled": True,
        "auto_invoke": True,
    }
    if extra_cfg:
        cfg.update(extra_cfg)
    return invoke_post_dispatch(cfg, "regression test request", None, hook.parent.parent)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)

        # -------------------------------------------------------------------------
        # 场景 1：returncode != 0 必须覆盖 status=success
        # -------------------------------------------------------------------------
        bad_hook = make_hook(
            workdir,
            "fake_success_but_exit1.py",
            'import json, sys\n'
            'print(json.dumps({"status": "success", "artifacts": ["fake.mp4"]}))\n'
            'sys.exit(1)\n',
        )
        r = run_hook(bad_hook)
        if r.get("status") != "failed":
            fail(f"[returncode!=0] expected status=failed, got {r.get('status')!r}: {r}")
        if r.get("returncode") != 1:
            fail(f"[returncode!=0] expected returncode=1, got {r.get('returncode')!r}")
        if "non-zero returncode" not in r.get("boundary", ""):
            fail(f"[returncode!=0] boundary missing 'non-zero returncode': {r.get('boundary')!r}")
        print("  ✓ returncode != 0 with stdout status=success -> overridden to failed")

        # -------------------------------------------------------------------------
        # 场景 2：status=success 但没有 recovery evidence
        # -------------------------------------------------------------------------
        no_evidence = make_hook(
            workdir,
            "no_evidence_success.py",
            'import json, sys\n'
            'print(json.dumps({"status": "success"}))\n'
            'sys.exit(0)\n',
        )
        r = run_hook(no_evidence)
        if r.get("status") != "failed":
            fail(f"[no evidence] expected status=failed, got {r.get('status')!r}: {r}")
        if r.get("returncode") != 0:
            fail(f"[no evidence] expected returncode=0, got {r.get('returncode')!r}")
        if "recovered artifact/evidence" not in r.get("boundary", ""):
            fail(f"[no evidence] boundary missing 'recovered artifact/evidence': {r.get('boundary')!r}")
        print("  ✓ returncode=0 but no recovery evidence -> downgraded to failed")

        # -------------------------------------------------------------------------
        # 场景 3：行为正确的 hook（正向对照）
        # -------------------------------------------------------------------------
        good_hook = make_hook(
            workdir,
            "well_behaved.py",
            'import json, sys\n'
            'from pathlib import Path\n'
            'Path("real.mp4").write_text("rendered", encoding="utf-8")\n'
            'print(json.dumps({"status": "success", "artifacts": ["real.mp4"]}))\n'
            'sys.exit(0)\n',
        )
        r = run_hook(good_hook)
        if r.get("status") != "success":
            fail(f"[positive control] expected status=success, got {r.get('status')!r}: {r}")
        if r.get("returncode") != 0:
            fail(f"[positive control] expected returncode=0, got {r.get('returncode')!r}")
        print("  ✓ returncode=0 with real recovery evidence -> success (positive control)")

        # -------------------------------------------------------------------------
        # Scenario 4: 布尔假值不能被当作恢复证据（Codex review P1 回归）
        # -------------------------------------------------------------------------
        false_recovered = make_hook(
            workdir,
            "false_recovered.py",
            'import json, sys\n'
            'print(json.dumps({"status": "success", "recovered": False, "artifacts": False}))\n'
            'sys.exit(0)\n',
        )
        r = run_hook(false_recovered)
        if r.get("status") != "failed":
            fail(f"[bool false] expected status=failed, got {r.get('status')!r}: {r}")
        if "recovered artifact/evidence" not in r.get("boundary", ""):
            fail(f"[bool false] boundary missing 'recovered artifact/evidence': {r.get('boundary')!r}")
        print("  ✓ recovered=false / artifacts=false -> downgraded to failed (regression)")

        # -------------------------------------------------------------------------
        # Scenario 5: 非空 artifact 字段但文件不存在，不能算真实恢复证据。
        # -------------------------------------------------------------------------
        fake_artifact = make_hook(
            workdir,
            "fake_artifact_success.py",
            'import json, sys\n'
            'print(json.dumps({"status": "success", "artifacts": ["missing-output.mp4"]}))\n'
            'sys.exit(0)\n',
        )
        r = run_hook(fake_artifact)
        if r.get("status") != "failed":
            fail(f"[fake artifact path] expected status=failed, got {r.get('status')!r}: {r}")
        if "recovered artifact/evidence" not in r.get("boundary", ""):
            fail(
                "[fake artifact path] boundary missing 'recovered artifact/evidence': "
                f"{r.get('boundary')!r}"
            )
        print("  ✓ non-empty missing artifact path -> downgraded to failed")

    # -------------------------------------------------------------------------
    # _gate_post_dispatch negative cases
    # -------------------------------------------------------------------------
    cleared_pf = {
        "can_invoke": True,
        "status": "ready",
        "requires_permission": False,
        "missing": [],
        "manual_checks": [],
    }

    cases = [
        (
            "hook provider missing",
            {},
            "remotion-render",
            cleared_pf,
            "blocked",
            "no provider",
        ),
        (
            "selected provider missing",
            {"provider": "remotion-render"},
            None,
            cleared_pf,
            "blocked",
            "No provider was selected",
        ),
        (
            "hook provider != policy-selected provider",
            {"provider": "evil-hook"},
            "remotion-render",
            cleared_pf,
            "blocked",
            "does not match",
        ),
        (
            "preflight.can_invoke = False",
            {"provider": "remotion-render"},
            "remotion-render",
            {**cleared_pf, "can_invoke": False, "status": "needs_key_or_env", "missing": ["env:API_KEY"]},
            "blocked",
            "can_invoke=false",
        ),
        (
            "preflight.requires_permission = True",
            {"provider": "remotion-render"},
            "remotion-render",
            {**cleared_pf, "requires_permission": True},
            "pending_manual",
            "explicit permission",
        ),
        (
            "preflight.manual_checks non-empty",
            {"provider": "remotion-render"},
            "remotion-render",
            {**cleared_pf, "manual_checks": ["confirm_vault_path"]},
            "pending_manual",
            "manual_checks",
        ),
    ]
    for label, cfg, selected, pf, expected_status, expected_phrase in cases:
        decision = _gate_post_dispatch(cfg, selected, pf)
        if decision is None:
            fail(f"[{label}] expected {expected_status}, got None (gate passed)")
        if decision.get("status") != expected_status:
            fail(
                f"[{label}] expected status={expected_status}, got "
                f"{decision.get('status')!r}: {decision}"
            )
        if expected_phrase not in decision.get("reason", ""):
            fail(
                f"[{label}] expected reason to contain {expected_phrase!r}, got "
                f"{decision.get('reason', '')!r}"
            )
        print(f"  ✓ gate: {label} -> {expected_status}")

    # -------------------------------------------------------------------------
    # 门禁正向场景：全部前置条件成立
    # -------------------------------------------------------------------------
    decision = _gate_post_dispatch(
        {"provider": "remotion-render"},
        "remotion-render",
        cleared_pf,
    )
    if decision is not None:
        fail(f"[all preconditions clear] expected None, got {decision}")
    print("  ✓ gate: all preconditions clear -> None (allow invoke)")

    # -------------------------------------------------------------------------
    # _has_recovery_evidence boundary sanity
    # -------------------------------------------------------------------------
    assert _has_recovery_evidence({}) is False
    assert _has_recovery_evidence({"status": "success"}) is False
    assert _has_recovery_evidence({"status": "success", "artifacts": []}) is False
    assert _has_recovery_evidence({"status": "success", "evidence": []}) is False
    assert _has_recovery_evidence({"status": "success", "artifacts": ["x.mp4"]}) is False
    assert _has_recovery_evidence({"status": "success", "evidence": ["x"]}) is False
    assert _has_recovery_evidence({"status": "success", "recovered": True}) is False
    assert _has_recovery_evidence({"status": "success", "output_path": "/x.mp4"}) is False
    with tempfile.TemporaryDirectory() as tmp:
        artifact_root = Path(tmp)
        real_artifact = artifact_root / "x.mp4"
        real_artifact.write_text("rendered", encoding="utf-8")
        assert _has_recovery_evidence(
            {"status": "success", "artifacts": ["x.mp4"]}, artifact_root
        ) is True
        assert _has_recovery_evidence(
            {"status": "success", "evidence": [{"path": "x.mp4"}]}, artifact_root
        ) is True
        assert _has_recovery_evidence(
            {"status": "success", "output_path": "x.mp4"}, artifact_root
        ) is True
    # 回归：布尔假值不能被当作恢复证据（Codex review P1）
    assert _has_recovery_evidence({"status": "success", "recovered": False}) is False
    assert _has_recovery_evidence({"status": "success", "artifacts": False}) is False
    assert _has_recovery_evidence({"status": "success", "evidence": False}) is False
    assert _has_recovery_evidence({"status": "success", "recovered": False, "artifacts": []}) is False
    # 回归：0 不是可验证 artifact/evidence，不能算恢复证据。
    assert _has_recovery_evidence({"status": "success", "artifacts": 0}) is False
    # 回归：多键混合时，键顺序中靠前的 False 不能否决靠后的 True
    assert _has_recovery_evidence({"status": "success", "artifacts": False, "recovered": True}) is False
    assert _has_recovery_evidence({"status": "success", "artifacts": False, "evidence": ["x"]}) is False
    print("  ✓ _has_recovery_evidence boundary cases all correct")

    print("Codex post-dispatch safety 检查通过")


if __name__ == "__main__":
    main()
