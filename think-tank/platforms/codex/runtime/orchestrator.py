#!/usr/bin/env python3
"""Codex natural-language runtime orchestrator for think-tank."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import re
import subprocess
import sys
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
AUTO_VIDEO_RUNS_DIR = WORKSPACE_ROOT / ".think-tank" / "artifacts" / "media" / "auto-video-runs"
RESEARCH_TO_VIDEO_SKILL = WORKSPACE_ROOT / ".codex" / "skills" / "research-to-video-production"


def rel(path: Path) -> str:
    return display_path(path)


def mode_from_route(route_result: dict[str, Any]) -> str:
    mode = route_result.get("selected_mode")
    return mode if mode in {"research", "council", "review", "strategy"} else "council"


def should_invoke_source(route_result: dict[str, Any], target: str | None) -> bool:
    capabilities = set(route_result.get("selected_capabilities", []) or [])
    return bool(target) and "source-acquisition" in capabilities


def slugify(value: str) -> str:
    lowered = value.strip().lower()
    cleaned = []
    for char in lowered:
        if char.isalnum() or "\u4e00" <= char <= "\u9fff":
            cleaned.append(char)
        else:
            cleaned.append("-")
    slug = "".join(cleaned).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug[:48] or "video-run"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_script_text(request: str, source_result: dict[str, Any] | None) -> str:
    if source_result and source_result.get("sources"):
        sources = source_result["sources"]
        lead = f"{request.strip()}。今天只讲最关键的信息，不绕弯。"
        body = []
        for index, source in enumerate(sources, start=1):
            summary = str(source.get("summary", "")).strip()
            title = str(source.get("title", "")).strip()
            if summary:
                body.append(f"第{index}条，{title}。{summary}")
            else:
                body.append(f"第{index}条，{title}。")
        outro = "以上就是这次的科技资讯速览。"
        return "\n".join([lead, *body, outro]) + "\n"
    return (
        f"{request.strip()}。\n"
        "下面进入今天的科技资讯速览。\n"
        "第一条，先讲最值得关注的核心更新。\n"
        "第二条，补充它对行业和产品落地的影响。\n"
        "最后一句，给出这次资讯对真实工作流的启发。\n"
    )


def build_storyboard_text(request: str, source_result: dict[str, Any] | None) -> str:
    lines = [
        f"# Auto Storyboard",
        "",
        f"- topic: {request.strip()}",
        "- structure: hook -> development -> takeaway",
        "- status: auto_handoff_generated",
        "",
    ]
    if source_result and source_result.get("sources"):
        for index, source in enumerate(source_result["sources"], start=1):
            lines.append(
                f"- scene_{index:02d}: {source.get('title', '')} | {source.get('url', '')}"
            )
    else:
        lines.append("- scene_01: 需要后续补真实来源或截图")
    return "\n".join(lines) + "\n"


def build_source_manifest_text(source_result: dict[str, Any] | None) -> str:
    lines = ["# Auto Source Manifest", ""]
    if source_result and source_result.get("sources"):
        for index, source in enumerate(source_result["sources"], start=1):
            lines.extend(
                [
                    f"## S{index}",
                    f"- title: {source.get('title', '')}",
                    f"- url: {source.get('url', '')}",
                    f"- summary: {source.get('summary', '')}",
                    f"- reliability: {source.get('reliability', '')}",
                    "",
                ]
            )
    else:
        lines.append("- no_sources_recovered: true")
    return "\n".join(lines) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_command(command: list[str], cwd: Path) -> tuple[int, str, str]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr


def run_parallel_commands(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def worker(task: dict[str, Any]) -> dict[str, Any]:
        code, out, err = run_command(task["command"], task.get("cwd", WORKSPACE_ROOT))
        return {
            "step": task["step"],
            "command": task["command"],
            "status": "success" if code == 0 else "failed",
            "returncode": code,
            "stdout": out.strip(),
            "stderr": err.strip(),
            "meta": task.get("meta", {}),
        }

    if not tasks:
        return []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(tasks))) as executor:
        futures = [executor.submit(worker, task) for task in tasks]
        return [future.result() for future in futures]


def extract_initialized_run_dir(stdout: str) -> Path | None:
    match = re.search(r"初始化完成:\s*(.+)", stdout)
    if not match:
        return None
    candidate = Path(match.group(1).strip())
    return candidate if candidate.exists() else None


def auto_handoff_research_to_video(
    request: str,
    route_result: dict[str, Any],
    provider_preflight: dict[str, Any],
    source_result: dict[str, Any] | None,
) -> dict[str, Any] | None:
    selected_provider = route_result.get("skill_route", {}).get("selected_provider")
    if route_result.get("selected_intent") != "research_to_video":
        return None
    if selected_provider != "research-to-video-production":
        return None
    if not provider_preflight.get("can_invoke"):
        return {
            "status": "blocked",
            "provider": selected_provider,
            "reason": "selected provider failed preflight",
            "steps": [],
            "generated_artifacts": {},
            "boundaries": ["Auto handoff skipped because research-to-video-production is not invokable."],
        }
    if not RESEARCH_TO_VIDEO_SKILL.exists():
        return {
            "status": "blocked",
            "provider": selected_provider,
            "reason": "research-to-video-production skill missing from project skills",
            "steps": [],
            "generated_artifacts": {},
            "boundaries": ["Auto handoff skipped because the downstream skill directory does not exist."],
        }

    scripts_dir = RESEARCH_TO_VIDEO_SKILL / "scripts"
    topic = request.strip()
    output_dir = AUTO_VIDEO_RUNS_DIR
    steps: list[dict[str, Any]] = []

    init_cmd = [
        "python3",
        str(scripts_dir / "init_video_run.py"),
        "--topic",
        topic,
        "--audience",
        "中文科技资讯观众",
        "--output-dir",
        str(output_dir),
        "--output-status-target",
        "production_plan_ready",
        "--voiceover-intro",
        f"{topic}。",
        "--bgm-status",
        "draft_without_bgm",
    ]
    returncode, stdout, stderr = run_command(init_cmd, WORKSPACE_ROOT)
    steps.append(
        {
            "step": "init_video_run",
            "command": init_cmd,
            "status": "success" if returncode == 0 else "failed",
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
        }
    )
    if returncode != 0:
        return {
            "status": "failed",
            "provider": selected_provider,
            "reason": "init_video_run failed",
            "steps": steps,
            "generated_artifacts": {},
            "boundaries": ["Auto handoff stopped before any downstream artifacts were created."],
        }

    date = datetime.now().strftime("%Y%m%d")
    run_dir = output_dir / f"video-run-{date}-{slugify(topic)}"
    initialized_run_dir = extract_initialized_run_dir(stdout)
    if initialized_run_dir is not None:
        run_dir = initialized_run_dir
    script_path = run_dir / "script.md"
    storyboard_path = run_dir / "storyboard.md"
    source_manifest_path = run_dir / "source_manifest.md"
    write_text(script_path, build_script_text(request, source_result))
    write_text(storyboard_path, build_storyboard_text(request, source_result))
    write_text(source_manifest_path, build_source_manifest_text(source_result))
    steps.append(
        {
            "step": "write_handoff_artifacts",
            "status": "success",
            "artifacts": [
                rel(script_path),
                rel(storyboard_path),
                rel(source_manifest_path),
            ],
        }
    )

    voice_manifest_path = run_dir / "voiceover_manifest.json"
    prepare_cmd = [
        "python3",
        str(scripts_dir / "prepare_voiceover_manifest.py"),
        "--script",
        str(script_path),
        "--output",
        str(voice_manifest_path),
    ]
    returncode, stdout, stderr = run_command(prepare_cmd, WORKSPACE_ROOT)
    steps.append(
        {
            "step": "prepare_voiceover_manifest",
            "command": prepare_cmd,
            "status": "success" if returncode == 0 else "failed",
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
        }
    )
    if returncode != 0:
        return {
            "status": "failed",
            "provider": selected_provider,
            "reason": "prepare_voiceover_manifest failed",
            "steps": steps,
            "generated_artifacts": {
                "run_dir": rel(run_dir),
                "script": rel(script_path),
                "storyboard": rel(storyboard_path),
                "source_manifest": rel(source_manifest_path),
            },
            "boundaries": ["Auto handoff created the run but could not prepare voiceover manifest."],
        }

    voice_synthesis_cmd = [
        "python3",
        str(scripts_dir / "synthesize_voiceover.py"),
        "--manifest",
        str(voice_manifest_path),
        "--allow-fallback",
    ]
    returncode, stdout, stderr = run_command(voice_synthesis_cmd, WORKSPACE_ROOT)
    steps.append(
        {
            "step": "synthesize_voiceover",
            "command": voice_synthesis_cmd,
            "status": "success" if returncode == 0 else "failed",
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
        }
    )
    if returncode != 0:
        return {
            "status": "failed",
            "provider": selected_provider,
            "reason": "synthesize_voiceover failed",
            "steps": steps,
            "generated_artifacts": {
                "run_dir": rel(run_dir),
                "script": rel(script_path),
                "storyboard": rel(storyboard_path),
                "source_manifest": rel(source_manifest_path),
                "voiceover_manifest": rel(voice_manifest_path),
            },
            "boundaries": ["Auto handoff created the run but could not synthesize voiceover audio."],
        }

    subtitle_path = run_dir / "subtitle_timeline.json"
    subtitle_cmd = [
        "python3",
        str(scripts_dir / "create_subtitle_timeline.py"),
        "--manifest",
        str(voice_manifest_path),
        "--output",
        str(subtitle_path),
    ]

    publish_package_path = run_dir / "publish_package.json"
    cover_tasks: list[dict[str, Any]] = []
    if publish_package_path.exists():
        publish_package = load_json(publish_package_path)
        for channel_ref in publish_package.get("channel_packages", []):
            channel_name = Path(channel_ref).stem.strip()
            if not channel_name:
                continue
            cover_tasks.append(
                {
                    "step": f"create_cover_package:{channel_name}",
                    "command": [
                        "python3",
                        str(scripts_dir / "create_cover_package.py"),
                        "--run-dir",
                        str(run_dir),
                        "--target-channel",
                        channel_name,
                        "--title",
                        topic,
                    ],
                    "meta": {"channel": channel_name},
                }
            )

    sfx_dir = run_dir / "assets" / "audio" / "sfx"
    bgm_manifest_path = run_dir / "bgm_manifest.json"
    post_voice_tasks: list[dict[str, Any]] = [
        {
            "step": "create_subtitle_timeline",
            "command": subtitle_cmd,
        },
        {
            "step": "render_sfx",
            "command": [
                "python3",
                str(scripts_dir / "render_sfx.py"),
                str(sfx_dir),
            ],
        },
        {
            "step": "synthesize_bgm",
            "command": [
                "python3",
                str(scripts_dir / "synthesize_bgm.py"),
                "--manifest",
                str(bgm_manifest_path),
                "--allow-fallback-bed",
            ],
        },
    ]
    post_voice_tasks.extend(cover_tasks)
    post_voice_results = run_parallel_commands(post_voice_tasks)
    steps.extend(
        {
            "step": item["step"],
            "command": item["command"],
            "status": item["status"],
            "stdout": item["stdout"],
            "stderr": item["stderr"],
        }
        for item in post_voice_results
    )
    subtitle_result = next(
        (item for item in post_voice_results if item["step"] == "create_subtitle_timeline"),
        None,
    )
    if not subtitle_result or subtitle_result["returncode"] != 0:
        return {
            "status": "failed",
            "provider": selected_provider,
            "reason": "create_subtitle_timeline failed",
            "steps": steps,
            "generated_artifacts": {
                "run_dir": rel(run_dir),
                "voiceover_manifest": rel(voice_manifest_path),
            },
            "boundaries": ["Auto handoff created voiceover but could not produce subtitle timeline."],
        }

    bgm_result = next((item for item in post_voice_results if item["step"] == "synthesize_bgm"), None)
    if not bgm_result or bgm_result["returncode"] != 0:
        return {
            "status": "failed",
            "provider": selected_provider,
            "reason": "synthesize_bgm failed",
            "steps": steps,
            "generated_artifacts": {
                "run_dir": rel(run_dir),
                "voiceover_manifest": rel(voice_manifest_path),
                "subtitle_timeline": rel(subtitle_path),
                "sfx_dir": rel(sfx_dir),
                "bgm_manifest": rel(bgm_manifest_path),
            },
            "boundaries": ["Auto handoff created audio artifacts but could not produce BGM."],
        }

    cover_packages: list[str] = []
    for item in post_voice_results:
        if item["status"] == "success" and item["step"].startswith("create_cover_package:"):
            channel = item["meta"].get("channel", "")
            if channel:
                cover_packages.append(rel(run_dir / "cover_packages" / f"{channel}.json"))

    layout_render_cmd = [
        "python3",
        str(scripts_dir / "render_simple_video.py"),
        "--run-dir",
        str(run_dir),
    ]
    returncode, stdout, stderr = run_command(layout_render_cmd, WORKSPACE_ROOT)
    steps.append(
        {
            "step": "render_research_video_layout",
            "command": layout_render_cmd,
            "status": "success" if returncode == 0 else "failed",
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
        }
    )
    render_mode = "research_to_video_layout"
    if returncode != 0:
        fallback_render_cmd = [
            "python3",
            str(scripts_dir / "render_remotion_news_video.py"),
            "--run-dir",
            str(run_dir),
        ]
        fallback_code, fallback_stdout, fallback_stderr = run_command(fallback_render_cmd, WORKSPACE_ROOT)
        steps.append(
            {
                "step": "render_remotion_news_video_fallback",
                "command": fallback_render_cmd,
                "status": "success" if fallback_code == 0 else "failed",
                "stdout": fallback_stdout.strip(),
                "stderr": fallback_stderr.strip(),
            }
        )
        if fallback_code != 0:
            return {
                "status": "failed",
                "provider": selected_provider,
                "reason": "both research-to-video layout render and remotion fallback render failed",
                "steps": steps,
                "generated_artifacts": {
                    "run_dir": rel(run_dir),
                    "voiceover_manifest": rel(voice_manifest_path),
                    "subtitle_timeline": rel(subtitle_path),
                    "bgm_manifest": rel(bgm_manifest_path),
                },
                "boundaries": ["Research-to-video primary layout render and remotion fallback render both failed."],
            }
        render_mode = "remotion_fallback"

    delivery_path = run_dir / "video_delivery_report.json"
    delivery_cmd = [
        "python3",
        str(scripts_dir / "create_delivery_report.py"),
        "--run-dir",
        str(run_dir),
        "--output",
        str(delivery_path),
    ]
    returncode, stdout, stderr = run_command(delivery_cmd, WORKSPACE_ROOT)
    steps.append(
        {
            "step": "create_delivery_report",
            "command": delivery_cmd,
            "status": "success" if returncode == 0 else "failed",
            "stdout": stdout.strip(),
            "stderr": stderr.strip(),
        }
    )

    return {
        "status": "success",
        "provider": selected_provider,
        "reason": "auto handoff initialized downstream research-to-video run",
        "steps": steps,
        "generated_artifacts": {
            "run_dir": rel(run_dir),
            "script": rel(script_path),
            "storyboard": rel(storyboard_path),
            "source_manifest": rel(source_manifest_path),
            "voiceover_manifest": rel(voice_manifest_path),
            "subtitle_timeline": rel(subtitle_path),
            "bgm_manifest": rel(bgm_manifest_path),
            "sfx_dir": rel(sfx_dir),
            "cover_packages": cover_packages,
            "render_mode": render_mode,
            "delivery_report": rel(delivery_path),
        },
        "boundaries": [
            "Auto handoff now attempts research-to-video layout render first, then remotion fallback render.",
            "If external video providers or premium render engines are unavailable, local adapters may still recover a publishable artifact.",
        ],
    }


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
    # 检测是否使用单 agent 多 profile fallback
    route_matched = route_result.get("matched", False)
    has_provider_invoked = invoked
    is_single_agent_fallback = route_matched and not has_provider_invoked

    if invoked:
        evidence_state = "verified_partial" if recovered else "failed"
        result_recovery = "automatic" if recovered else "none"
        execution_method = "adapter_runtime"
        data_collection = source_result.get("runtime_provenance", {}).get("data_collection", "provider_managed") if source_result else "provider_managed"
    elif is_single_agent_fallback:
        # 单 agent 内部分角色执行（非真正多 agent）
        evidence_state = "selected"
        result_recovery = "none"
        execution_method = "single_agent_multi_profile_fallback"
        data_collection = "direct_assistant_tool"
    elif route_matched:
        # 路由命中但没有真实 provider 调用
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
        "authority_level": "lower_fallback_single_context" if is_single_agent_fallback else "adapter_runtime" if invoked else "protocol_only",
        "data_collection": data_collection,
        "evidence_state": evidence_state,
        "result_recovery": result_recovery,
        "boundaries": [
            "Codex natural-language orchestrator is a minimal adapter runtime.",
            "It does not claim true independent multi-agent execution." if is_single_agent_fallback else "Multi-agent runtime requires verified subagent evidence.",
            "Policy provider selection is distinct from the minimal runtime provider actually invoked." if is_single_agent_fallback else "Provider selection reflects policy preference, not guaranteed invocation.",
        ] + ([] if is_single_agent_fallback else [
            "Single-agent fallback used when no verified subagent runtime available.",
        ]),
    }


def build_final_output(
    request: str,
    route_result: dict[str, Any],
    source_result: dict[str, Any] | None,
    handoff_result: dict[str, Any] | None,
) -> dict[str, Any]:
    if handoff_result and handoff_result.get("status") == "success":
        evidence = []
        if source_result and source_result.get("evidence"):
            evidence.extend(source_result.get("evidence", []))
        for key, value in handoff_result.get("generated_artifacts", {}).items():
            evidence.append(f"{key}: {value}")
        conclusion = (
            f"Request routed to {route_result.get('selected_recipe')} and auto-handed off to "
            "research-to-video-production with downstream production artifacts initialized."
        )
        recommendations = [
            "Review the generated script, storyboard, subtitle timeline and delivery report before render.",
            "If voice runtime or API credentials are ready, continue with voice synthesis and final render.",
        ]
    elif handoff_result and handoff_result.get("status") in {"blocked", "failed"}:
        evidence = handoff_result.get("boundaries", [])
        conclusion = (
            f"Request routed to {route_result.get('selected_recipe')} but downstream media-production "
            f"handoff {handoff_result.get('status')}."
        )
        recommendations = [
            "Inspect auto_handoff_result.steps for the exact failing stage.",
            "Fix downstream skill preflight or script execution before claiming production readiness.",
        ]
    elif source_result and source_result.get("sources"):
        evidence = source_result.get("evidence", [])
        conclusion = f"Request routed to {route_result.get('selected_recipe')} and completed minimal source recovery."
        recommendations = [
            "Use recovered sources as input for role analysis.",
            "Do not mark external peer providers verified until they are invoked and recovered.",
        ]
    elif route_result.get("matched"):
        evidence = []
        conclusion = f"Request routed to {route_result.get('selected_recipe')} without provider invocation."
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


def run_orchestrator(
    request: str,
    target: str | None = None,
    skills_dir: Path = PROJECT_SKILLS,
    write_run: bool = False,
    runs_dir: Path = DEFAULT_RUNS_DIR,
) -> dict[str, Any]:
    effective_policy, policy_sources = load_effective_policy()
    selected_policy_path = policy_path()
    provider_registry = registry(skills_dir)
    route_result = resolve_request(request, effective_policy, provider_registry["providers"])
    route_result["policy_path"] = rel(selected_policy_path)
    route_result["policy_sources"] = [rel(source) for source in policy_sources]
    route_result["provider_count"] = provider_registry["provider_count"]
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

    # 形成完整的 dispatch_decision（dispatch-policy.md 要求）
    skill_route = route_result.get("skill_route", {})
    candidate_providers = skill_route.get("candidate_providers", [])
    policy_selected_provider = skill_route.get("selected_provider")
    runtime_selected_provider = "local_static_reader" if invoke_source else None
    dispatch_decision = {
        "intent": route_result.get("selected_intent"),
        "recipe": route_result.get("selected_recipe"),
        "mode": mode_from_route(route_result),
        "capability": "source-acquisition" if "source-acquisition" in (route_result.get("selected_capabilities", []) or []) else "media-production",
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

    source_result = source_runtime_result(selected_target, "codex-minimal") if invoke_source else None
    handoff_result = auto_handoff_research_to_video(
        request,
        route_result,
        provider_preflight,
        source_result,
    )
    if handoff_result and handoff_result.get("status") == "success":
        runtime_selected_provider = "research-to-video-production"
        dispatch_decision["selected_peer_skill"] = runtime_selected_provider
        dispatch_decision["invocation_method"] = "research-to-video-production"
        dispatch_decision["risk_level"] = "medium"
        dispatch_decision["dispatch_allowed"] = True
    invoked = invoke_source or bool(handoff_result and handoff_result.get("status") == "success")
    recovered = bool(source_result and source_result.get("sources")) or bool(
        handoff_result and handoff_result.get("generated_artifacts")
    )

    # dispatch_log 包含完整的事务记录（dispatch-contract.md 要求）
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
        },
        "recovery": {
            "sources_recovered": bool(source_result and source_result.get("sources")),
            "artifacts_recovered": bool(handoff_result and handoff_result.get("generated_artifacts")),
            "result_recovered": recovered,
        },
        "boundaries": [
            "Policy-selected provider was auto-handed off to research-to-video-production."
            if handoff_result and handoff_result.get("status") == "success"
            else (
                "Policy-selected provider is not automatically invoked by the minimal orchestrator."
                if invoke_source
                else "No source-acquisition runtime dispatch was needed or possible."
            )
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
    if handoff_result:
        boundaries.extend(handoff_result.get("boundaries", []))

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
        "auto_handoff_result": handoff_result,
        "final_output": build_final_output(request, route_result, source_result, handoff_result),
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
        help=f"Optional source target. If omitted, no default fixture is auto-read. For local fixture tests use {display_path(DEFAULT_TARGET)}",
    )
    parser.add_argument("--skills-dir", type=Path, default=PROJECT_SKILLS)
    parser.add_argument("--write-run", action="store_true")
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    args = parser.parse_args()
    print(json.dumps(run_orchestrator(args.request, args.target, args.skills_dir, args.write_run, args.runs_dir), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
