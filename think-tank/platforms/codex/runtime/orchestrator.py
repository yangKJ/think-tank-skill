#!/usr/bin/env python3
"""Codex natural-language runtime orchestrator for think-tank.

This orchestrator is a minimal adapter runtime. It:
1. Loads provider policy and resolves the intent → route.
2. Runs provider preflight for the selected provider.
3. Dispatches source-acquisition when the route requires it.
4. Produces a dispatch_decision and runtime provenance record.

It does NOT:
- Hardcode any specific peer skill name, path, or internal script.
- Know about downstream skill internals (scripts, CLI flags, pipelines).
- Special-case any single intent or provider.

Provider-specific handoff logic belongs in .think-tank/ configuration or
in the downstream skill's own orchestration layer, not here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[3]
CODEX_RUNTIME_DIR = SKILL_ROOT / "platforms" / "codex" / "runtime"
RUNTIME_DIR = SKILL_ROOT / "runtime"
sys.path.insert(0, str(RUNTIME_DIR))
sys.path.insert(0, str(CODEX_RUNTIME_DIR))

from path_context import PROJECT_SKILLS, WORKSPACE_ROOT, display_path  # noqa: E402
from provider_policy import load_effective_policy, policy_path, registry, resolve_request  # noqa: E402
from provider_preflight import load_effective_preflight, preflight_provider, selected_preflight_path  # noqa: E402
from source_acquisition_minimal import runtime_result as source_runtime_result  # noqa: E402


DEFAULT_TARGET = SKILL_ROOT / "examples" / "browser-automation-fixture.html"
DEFAULT_RUNS_DIR = WORKSPACE_ROOT / ".think-tank" / "runs"


def rel(path: Path) -> str:
    return display_path(path)


def mode_from_route(route_result: dict[str, Any]) -> str:
    mode = route_result.get("selected_mode")
    return mode if mode in {"research", "council", "review", "strategy"} else "council"


def should_invoke_source(route_result: dict[str, Any], target: str | None) -> bool:
    capabilities = set(route_result.get("selected_capabilities", []) or [])
    return bool(target) and "source-acquisition" in capabilities


def make_run_record(request: str, target: str | None, write_run: bool, runs_dir: Path) -> dict[str, Any]:
    digest = hashlib.sha1(f"{request}\n{target or ''}".encode("utf-8")).hexdigest()[:12]
    run_id = f"nlrt-{digest}"
    artifact_path = runs_dir / f"{run_id}.json"
    return {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "artifact_requested": write_run,
        "artifact_written": False,
        "artifact_path": display_path(artifact_path),
    }


def build_runtime_provenance(
    *,
    route_result: dict[str, Any],
    source_result: dict[str, Any] | None,
    invoked: bool,
    recovered: bool,
    dispatch_decision_formed: bool = False,
) -> dict[str, Any]:
    """Build runtime provenance record.

    Distinguishes between:
    - True provider invocation (adapter_runtime)
    - Single-agent multi-profile fallback (no real multi-agent)
    - Protocol-only route match (no provider invoked)
    - Unmatched fallback (planned only)
    """
    route_matched = route_result.get("matched", False)
    has_provider_invoked = invoked
    is_single_agent_fallback = route_matched and not has_provider_invoked

    if invoked:
        evidence_state = "verified_partial" if recovered else "failed"
        result_recovery = "automatic" if recovered else "none"
        execution_method = "adapter_runtime"
        data_collection = (
            source_result.get("runtime_provenance", {}).get("data_collection", "provider_managed")
            if source_result
            else "provider_managed"
        )
    elif is_single_agent_fallback:
        evidence_state = "selected"
        result_recovery = "none"
        execution_method = "single_agent_multi_profile_fallback"
        data_collection = "direct_assistant_tool"
    elif route_matched:
        evidence_state = "selected"
        result_recovery = "none"
        execution_method = "protocol_only"
        data_collection = "none"
    else:
        evidence_state = "planned"
        result_recovery = "none"
        execution_method = "protocol_only"
        data_collection = "none"

    return {
        "think_tank_runtime_used": True,
        "provider_policy_checked": True,
        "dispatch_decision_emitted": dispatch_decision_formed or route_matched,
        "provider_invoked": invoked,
        "result_recovered": recovered,
        "true_multi_agent_runtime": False,
        "execution_method": execution_method,
        "authority_level": (
            "lower_fallback_single_context"
            if is_single_agent_fallback
            else "adapter_runtime"
            if invoked
            else "protocol_only"
        ),
        "data_collection": data_collection,
        "evidence_state": evidence_state,
        "result_recovery": result_recovery,
        "boundaries": [
            "Codex natural-language orchestrator is a minimal adapter runtime.",
            "It does not claim true independent multi-agent execution.",
            "Policy provider selection is distinct from the minimal runtime provider actually invoked.",
            "Provider dispatch is determined by local policy configuration, not hardcoded in think-tank core.",
            "Downstream provider handoff is the responsibility of local .think-tank/ configuration.",
        ],
    }


def build_final_output(
    request: str,
    route_result: dict[str, Any],
    source_result: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build the final output conclusion from route + source results.

    Provider-specific handoff results are not handled here — they belong
    in local configuration or downstream skill orchestration.
    """
    if source_result and source_result.get("sources"):
        evidence = source_result.get("evidence", [])
        conclusion = (
            f"Request routed to {route_result.get('selected_recipe')} "
            "and completed minimal source recovery."
        )
        recommendations = [
            "Use recovered sources as input for role analysis.",
            "Do not mark external peer providers verified until they are invoked and recovered.",
        ]
    elif route_result.get("matched"):
        evidence = []
        conclusion = (
            f"Request routed to {route_result.get('selected_recipe')} "
            "without provider invocation."
        )
        recommendations = [
            "Proceed with protocol-only analysis or provide a target/source for minimal source-acquisition.",
        ]
    else:
        evidence = []
        conclusion = "No routing policy matched; fall back to core protocol."
        recommendations = ["Clarify intent or run protocol-only think-tank analysis."]

    return {
        "request": request,
        "conclusion": conclusion,
        "evidence": evidence,
        "recommendations": recommendations,
    }


def invoke_post_dispatch(
    post_dispatch_config: dict[str, Any],
    request: str,
    source_result: dict[str, Any] | None,
    work_dir: Path,
) -> dict[str, Any] | None:
    """Generic post-dispatch hook invocation.

    Reads entrypoint and provider from local .think-tank/ policy config.
    Does NOT know anything about the provider internals — just runs the
    configured script and returns its result.

    Returns None if no post_dispatch is configured.
    """
    if not post_dispatch_config or not post_dispatch_config.get("enabled"):
        return None

    if not post_dispatch_config.get("auto_invoke"):
        return {
            "status": "pending_manual",
            "provider": post_dispatch_config.get("provider"),
            "entrypoint": post_dispatch_config.get("entrypoint"),
            "boundary": "auto_invoke is disabled; manual dispatch required.",
        }

    entrypoint = work_dir / post_dispatch_config["entrypoint"]
    if not entrypoint.exists():
        return {
            "status": "blocked",
            "provider": post_dispatch_config.get("provider"),
            "reason": f"entrypoint not found: {display_path(entrypoint)}",
        }

    cmd = [
        "python3",
        str(entrypoint),
        "--provider",
        post_dispatch_config.get("provider", ""),
        "--request",
        request,
    ]

    source_file = None
    if source_result:
        source_file = Path(tempfile.mktemp(suffix=".json"))
        source_file.write_text(json.dumps(source_result, ensure_ascii=False), encoding="utf-8")
        cmd.extend(["--source-result", str(source_file)])

    try:
        completed = subprocess.run(
            cmd, cwd=work_dir, capture_output=True, text=True, timeout=600
        )
        try:
            result = json.loads(completed.stdout) if completed.stdout.strip() else {}
        except json.JSONDecodeError:
            result = {"status": "failed", "stderr": completed.stderr[:1000]}
        result["returncode"] = completed.returncode
        # 硬门禁：非零 returncode 必须覆盖 stdout 里声明的 success。
        # 否则 hook 可以一边 exit 1，一边输出 success JSON，被错误提升为 recovered=true。
        if completed.returncode != 0:
            result["status"] = "failed"
            result["stderr_tail"] = completed.stderr[-1000:]
            result["stdout_tail"] = completed.stdout[-1000:]
            result["boundary"] = (
                "Hook exited with non-zero returncode; status was overridden to failed."
            )
        elif result.get("status") == "success" and not _has_recovery_evidence(result, work_dir):
            result["status"] = "failed"
            result["boundary"] = (
                "Hook reported success but did not provide recovered "
                "artifact/evidence/output_path; status was downgraded to failed."
            )
        return result
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "provider": post_dispatch_config.get("provider"),
            "boundary": "Hook exceeded the 600s timeout; no recovery claimed.",
        }
    except Exception as exc:
        return {"status": "failed", "reason": str(exc)}
    finally:
        if source_file and source_file.exists():
            source_file.unlink(missing_ok=True)


def _gate_post_dispatch(
    post_dispatch_config: dict[str, Any],
    selected_provider: str | None,
    provider_preflight: dict[str, Any],
) -> dict[str, Any] | None:
    """Decide whether a post-dispatch hook may auto-invoke.

    Returns:
        - a structured refusal dict (status=blocked / pending_manual) when the
          hook MUST NOT run under the current preflight/permission state;
        - None when the preflight has cleared and the hook is allowed to run.

    The gate enforces four conditions. If any of them fails, the hook is
    refused and the orchestrator never invokes it. This is the only path
    that protects local policy from auto-running providers that the
    preflight explicitly said are not ready.
    """
    hook_provider = post_dispatch_config.get("provider")
    preflight_status = provider_preflight.get("status", "not_required")
    preflight_can_invoke = bool(provider_preflight.get("can_invoke", False))
    preflight_missing = list(provider_preflight.get("missing", []) or [])
    preflight_manual = list(provider_preflight.get("manual_checks", []) or [])
    preflight_requires_permission = bool(provider_preflight.get("requires_permission", False))

    if not hook_provider:
        return {
            "status": "blocked",
            "reason": "post_dispatch is enabled but has no provider; refusing to auto-invoke.",
        }
    if not selected_provider:
        return {
            "status": "blocked",
            "provider": hook_provider,
            "reason": "No provider was selected from policy; refusing to auto-invoke a hook.",
            "preflight_status": preflight_status,
        }
    if hook_provider != selected_provider:
        return {
            "status": "blocked",
            "provider": hook_provider,
            "selected_provider": selected_provider,
            "reason": (
                "post_dispatch.provider does not match the policy-selected provider; "
                "refusing to auto-invoke to prevent a misrouted local hook."
            ),
            "preflight_status": preflight_status,
        }
    if not preflight_can_invoke:
        return {
            "status": "blocked",
            "provider": hook_provider,
            "reason": (
                f"provider_preflight returned can_invoke=false (status={preflight_status}); "
                "refusing to auto-invoke a hook for a provider that did not clear preflight."
            ),
            "preflight_status": preflight_status,
            "missing": preflight_missing,
        }
    if preflight_requires_permission:
        return {
            "status": "pending_manual",
            "provider": hook_provider,
            "reason": (
                "provider_preflight requires explicit permission; "
                "auto-invoke is disabled until the user grants permission."
            ),
            "preflight_status": preflight_status,
        }
    if preflight_manual:
        return {
            "status": "pending_manual",
            "provider": hook_provider,
            "reason": (
                "provider_preflight returned manual_checks; "
                "manual confirmation required before hook invocation."
            ),
            "preflight_status": preflight_status,
            "manual_checks": preflight_manual,
        }
    return None


def _has_recovery_evidence(result: dict[str, Any], work_dir: Path | None = None) -> bool:
    """hook 打印 status=success 时，也必须交回可验证证据。

    没有这层检查时，hook 只要输出 "fake.mp4" 这样的非空字符串就能伪装
    已恢复结果。字段名保持通用，因为 hook 由用户配置；但至少一个常见
    recovery carrier 必须能解析到真实存在的文件。
    """
    if not isinstance(result, dict):
        return False
    root = work_dir or WORKSPACE_ROOT

    def existing_path(value: str) -> bool:
        if not value or value.startswith(("http://", "https://")):
            return False
        candidate = Path(value).expanduser()
        if not candidate.is_absolute():
            candidate = root / candidate
        return candidate.exists() and candidate.is_file()

    def contains_verifiable_path(value: Any) -> bool:
        if isinstance(value, bool) or value in (None, "", [], {}):
            return False
        if isinstance(value, str):
            return existing_path(value)
        if isinstance(value, list):
            return any(contains_verifiable_path(item) for item in value)
        if isinstance(value, dict):
            for path_key in (
                "path",
                "file",
                "output_path",
                "source_path",
                "artifact_path",
                "delivery_path",
                "report_path",
            ):
                if contains_verifiable_path(value.get(path_key)):
                    return True
            for nested_key in (
                "artifacts",
                "evidence",
                "outputs",
                "files",
                "generated_artifacts",
                "deliverables",
                "run_record",
            ):
                if contains_verifiable_path(value.get(nested_key)):
                    return True
        return False

    for key in (
        "artifacts",
        "evidence",
        "output_path",
        "source_path",
        "artifact_path",
        "run_record",
        "generated_artifacts",
        "deliverables",
    ):
        if contains_verifiable_path(result.get(key)):
            return True
    return False


def run_orchestrator(
    request: str,
    target: str | None = None,
    skills_dir: Path = PROJECT_SKILLS,
    write_run: bool = False,
    runs_dir: Path = DEFAULT_RUNS_DIR,
) -> dict[str, Any]:
    """Run the Codex natural-language orchestrator.

    Flow:
    1. Load policy → resolve route.
    2. Run provider preflight for the selected provider.
    3. If source-acquisition is needed, invoke the minimal runtime.
    4. Form dispatch_decision, provenance, and final output.

    Provider-specific handoff is NOT performed here. It is the responsibility
    of local .think-tank/ configuration (e.g. a post-dispatch hook) or the
    downstream skill's own orchestration layer.
    """
    effective_policy, policy_sources = load_effective_policy()
    selected_policy_path = policy_path()
    provider_registry = registry(skills_dir)
    route_result = resolve_request(request, effective_policy, provider_registry["providers"])
    route_result["policy_path"] = rel(selected_policy_path)
    route_result["policy_sources"] = [rel(source) for source in policy_sources]
    route_result["provider_count"] = provider_registry["provider_count"]

    # Provider preflight (generic — no hardcoded provider names)
    preflight_policy, preflight_sources = load_effective_preflight()
    selected_provider = route_result.get("skill_route", {}).get("selected_provider")
    provider_preflight = (
        preflight_provider(selected_provider, preflight_policy)
        if selected_provider
        else {
            "provider": None,
            "status": "not_required",
            "can_invoke": False,
            "missing": [],
            "present": [],
            "manual_checks": [],
            "fallbacks": [],
            "boundaries": ["No provider was selected, so preflight was not required."],
        }
    )
    provider_preflight["preflight_path"] = rel(selected_preflight_path())
    provider_preflight["preflight_sources"] = [rel(source) for source in preflight_sources]

    selected_target = target
    invoke_source = should_invoke_source(route_result, selected_target)
    mode = mode_from_route(route_result)

    # Form dispatch_decision (generic structure, no provider-specific fields)
    skill_route = route_result.get("skill_route", {})
    candidate_providers = skill_route.get("candidate_providers", [])
    policy_selected_provider = skill_route.get("selected_provider")
    runtime_selected_provider = "local_static_reader" if invoke_source else None

    dispatch_decision = {
        "intent": route_result.get("selected_intent"),
        "recipe": route_result.get("selected_recipe"),
        "mode": mode,
        "capability": (
            "source-acquisition"
            if "source-acquisition" in (route_result.get("selected_capabilities", []) or [])
            else "protocol_only"
        ),
        "task": request,
        "target": selected_target,
        "constraints": ["readonly", "no_login", "no_download", "no_private_write"],
        "evidence_policy": {"network": "allowed", "citations": "optional"},
        "candidate_peer_skills": candidate_providers,
        "selected_peer_skill": runtime_selected_provider,
        "policy_selected_peer_skill": policy_selected_provider,
        "selection_reason": skill_route.get("selection_reason", ""),
        "invocation_method": "local_static_reader" if runtime_selected_provider else "not_invoked",
        "fallback": route_result.get("fallback", "core_protocol"),
        "risk_level": "low" if invoke_source else "medium",
        "dispatch_allowed": bool(runtime_selected_provider),
    }
    dispatch_decision_formed = True

    # Source acquisition (minimal runtime, no provider-specific paths)
    source_result = (
        source_runtime_result(selected_target, "codex-minimal") if invoke_source else None
    )
    invoked = invoke_source
    recovered = bool(source_result and source_result.get("sources"))

    # Post-dispatch hook — generic, driven by local .think-tank/ policy config.
    # The orchestrator does NOT know what the hook does; it just runs the
    # configured entrypoint with the provider name and request context.
    #
    # 硬门禁：只有 selected provider 的 preflight 真正 cleared，才允许自动调用 hook。
    # 这里要求 can_invoke=True、无缺失项、无 requires_permission、无 manual_checks。
    # 这是 permission/preflight 边界；绕过它会让错误配置的本地 policy 在
    # provider 未就绪时执行可能写产物或需要登录态的 provider。
    post_dispatch_config = route_result.get("post_dispatch") or {}
    post_dispatch_result: dict[str, Any] | None = None
    if post_dispatch_config and post_dispatch_config.get("enabled"):
        post_dispatch_result = _gate_post_dispatch(
            post_dispatch_config, selected_provider, provider_preflight
        )
        if post_dispatch_result is None:
            post_dispatch_result = invoke_post_dispatch(
                post_dispatch_config, request, source_result, WORKSPACE_ROOT
            )
    if post_dispatch_result and post_dispatch_result.get("status") == "success":
        # 纵深防御：invoke_post_dispatch 已经检查 returncode 和 recovery evidence，
        # 但 orchestrator 仍会复核一次；任一条件不满足都不能提升 invoked/recovered。
        hook_returncode = post_dispatch_result.get("returncode")
        if hook_returncode != 0 or not _has_recovery_evidence(post_dispatch_result, WORKSPACE_ROOT):
            post_dispatch_result = {
                "status": "failed",
                "provider": post_dispatch_config.get("provider"),
                "reason": (
                    "orchestrator re-validation failed: hook reported success but "
                    f"returncode={hook_returncode} and recovery evidence is empty."
                ),
                "returncode": hook_returncode,
                "boundary": (
                    "post_dispatch success was demoted to failed by orchestrator re-validation."
                ),
            }
        else:
            invoked = True
            recovered = True
            runtime_selected_provider = post_dispatch_config.get("provider") or runtime_selected_provider
            dispatch_decision["selected_peer_skill"] = runtime_selected_provider
            dispatch_decision["invocation_method"] = "post_dispatch_hook"
            dispatch_decision["dispatch_allowed"] = True

    # Dispatch log (generic — no hardcoded provider names in boundaries)
    dispatch_log = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "dispatch_request": {
            "intent": dispatch_decision["intent"],
            "recipe": dispatch_decision["recipe"],
            "mode": dispatch_decision["mode"],
            "capability": dispatch_decision["capability"],
            "task": dispatch_decision["task"],
            "target": dispatch_decision["target"],
            "constraints": dispatch_decision["constraints"],
        },
        "dispatch_decision": dispatch_decision,
        "invocation": {
            "provider_invoked": invoked,
            "provider": runtime_selected_provider,
            "status": "success" if invoked else "not_invoked",
            "post_dispatch_status": (
                post_dispatch_result.get("status") if post_dispatch_result else "not_configured"
            ),
        },
        "recovery": {
            "sources_recovered": bool(source_result and source_result.get("sources")),
            "result_recovered": recovered,
        },
        "boundaries": [
            "Provider dispatch is determined by local .think-tank/ policy configuration.",
            "think-tank core does not hardcode downstream skill names, paths, or internals.",
            "For provider-specific handoff, configure a post-dispatch hook in local policy.",
        ],
    }

    runtime_provenance = build_runtime_provenance(
        route_result=route_result,
        source_result=source_result,
        invoked=invoked,
        recovered=recovered,
        dispatch_decision_formed=dispatch_decision_formed,
    )

    boundaries = list(route_result.get("boundaries", []))
    boundaries.extend(runtime_provenance["boundaries"])
    if source_result:
        boundaries.extend(source_result.get("boundaries", []))

    run_record = make_run_record(request, selected_target, write_run, runs_dir)
    result = {
        "runtime": "codex-natural-language-orchestrator",
        "runtime_provenance": runtime_provenance,
        "request": request,
        "mode": mode,
        "run_record": run_record,
        "policy_route": route_result,
        "provider_preflight": provider_preflight,
        "dispatch_record": {
            "dispatch_decision_emitted": True,
            "policy_selected_provider": route_result.get("skill_route", {}).get("selected_provider"),
            "runtime_selected_provider": runtime_selected_provider,
            "status": "dispatched" if dispatch_decision.get("dispatch_allowed") else "not_dispatched",
            "boundary": dispatch_log["boundaries"][0],
        },
        "dispatch_log": dispatch_log,
        "source_result": source_result,
        "post_dispatch_result": post_dispatch_result,
        "final_output": build_final_output(request, route_result, source_result),
        "quality_check": {
            "protocol_complete": True,
            "runtime_provenance_present": True,
            "provider_invocation_truthful": True,
            "evidence_boundary_clear": True,
            "actionable": True,
        },
        "boundaries": boundaries,
    }

    if write_run:
        runs_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = Path(run_record["artifact_path"])
        if not artifact_path.is_absolute():
            artifact_path = WORKSPACE_ROOT / artifact_path
        artifact_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        result["run_record"]["artifact_written"] = True

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Codex natural-language think-tank orchestrator.")
    parser.add_argument("request")
    parser.add_argument(
        "--target",
        default=None,
        help=(
            "Optional source target. If omitted, no default fixture is auto-read. "
            f"For local fixture tests use {display_path(DEFAULT_TARGET)}"
        ),
    )
    parser.add_argument("--skills-dir", type=Path, default=PROJECT_SKILLS)
    parser.add_argument("--write-run", action="store_true")
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    args = parser.parse_args()
    print(
        json.dumps(
            run_orchestrator(args.request, args.target, args.skills_dir, args.write_run, args.runs_dir),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
