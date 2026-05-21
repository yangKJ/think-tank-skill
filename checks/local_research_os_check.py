#!/usr/bin/env python3
"""检查 .think-tank 本地研究操作系统骨架。"""

from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".think-tank"

REQUIRED_DIRS = [
    "inbox",
    "sources",
    "trends",
    "curation",
    "artifacts",
    "artifacts/reports",
    "artifacts/briefs",
    "artifacts/media",
    "competitors",
    "signals",
    "backlog",
    "decisions",
    "experiments",
    "runbooks",
    "promotion",
    "metrics",
    "calendar",
    "creators",
    "promotion/assets",
    "promotion/assets/before-after",
    "promotion/assets/feature-demos",
    "promotion/assets/app-store-screenshots",
    "promotion/assets/xiaohongshu-covers",
    "promotion/assets/short-video-clips",
    "promotion/assets/proof",
    "promotion/specs",
    "promotion/scripts",
    "promotion/ideas",
    "promotion/checklists",
    "domain-packs",
    "templates",
]

REQUIRED_FILES = [
    "routes.md",
    "providers.md",
    "operations.md",
    "sources/ledger.jsonl",
    "sources/source-template.yaml",
    "sources/source-ledger-candidate-template.yaml",
    "trends/README.md",
    "trends/trend-template.yaml",
    "trends/trend-to-action-template.md",
    "curation/README.md",
    "curation/post-run-curation-template.yaml",
    "curation/artifact-plan-template.yaml",
    "artifacts/artifact-template.md",
    "competitors/competitor-template.yaml",
    "signals/user-signal-template.yaml",
    "signals/signal-to-backlog-template.md",
    "backlog/opportunity-template.yaml",
    "backlog/backlog-item-template.yaml",
    "decisions/decision-template.md",
    "experiments/experiment-template.yaml",
    "runbooks/runbook-template.md",
    "runbooks/weekly-competitor-scan.md",
    "runbooks/weekly-user-signal-review.md",
    "runbooks/monthly-positioning-review.md",
    "runbooks/release-readiness-review.md",
    "runbooks/content-idea-generation.md",
    "runbooks/app-store-review-analysis.md",
    "runbooks/weekly-promotion-ideas.md",
    "runbooks/app-store-page-optimization.md",
    "runbooks/ugc-creator-brief-review.md",
    "runbooks/competitor-ad-swipe-review.md",
    "promotion/README.md",
    "promotion/campaign-template.yaml",
    "promotion/creative-brief-template.md",
    "promotion/before-after-showcase-template.md",
    "promotion/ugc-script-template.md",
    "promotion/xiaohongshu-note-template.md",
    "promotion/app-store-cpp-template.yaml",
    "promotion/trend-response-template.yaml",
    "promotion/performance-review-template.md",
    "promotion/assets/README.md",
    "promotion/specs/xiaohongshu-spec.md",
    "promotion/specs/short-video-spec.md",
    "promotion/specs/app-store-screenshot-spec.md",
    "promotion/specs/app-preview-video-spec.md",
    "promotion/specs/bilibili-spec.md",
    "promotion/scripts/short-video-15s-template.md",
    "promotion/scripts/tutorial-video-template.md",
    "promotion/scripts/app-preview-video-template.md",
    "promotion/scripts/xiaohongshu-carousel-template.md",
    "promotion/scripts/trend-video-template.md",
    "promotion/ideas/idea-template.yaml",
    "promotion/ideas/hooks-library.md",
    "promotion/ideas/content-pillars.yaml",
    "promotion/checklists/pre-publish-checklist.md",
    "promotion/checklists/claim-safety-checklist.md",
    "promotion/checklists/asset-rights-checklist.md",
    "promotion/reuse-matrix.md",
    "runbooks/content-production-pipeline.md",
    "runbooks/post-run-curation.md",
    "metrics/README.md",
    "metrics/metric-dictionary.yaml",
    "metrics/channel-metrics-template.yaml",
    "metrics/campaign-result-template.yaml",
    "calendar/README.md",
    "calendar/content-calendar-template.yaml",
    "calendar/weekly-publishing-plan.md",
    "creators/README.md",
    "creators/creator-template.yaml",
    "creators/outreach-template.md",
    "creators/collaboration-tracker.yaml",
    "templates/source-template.yaml",
    "templates/artifact-template.md",
    "templates/competitor-template.yaml",
    "templates/decision-template.md",
    "templates/experiment-template.yaml",
    "templates/runbook-template.md",
]


def fail(message: str) -> None:
    raise SystemExit(f"local research OS 检查失败: {message}")


def require_text(relative: str, terms: list[str]) -> None:
    path = LOCAL / relative
    if not path.exists():
        fail(f"缺少文件: .think-tank/{relative}")

    text = path.read_text(encoding="utf-8")
    for term in terms:
        if term not in text:
            fail(f".think-tank/{relative} 缺少: {term}")


def main() -> None:
    for directory in REQUIRED_DIRS:
        if not (LOCAL / directory).is_dir():
            fail(f"缺少目录: .think-tank/{directory}")

    for file in REQUIRED_FILES:
        if not (LOCAL / file).is_file():
            fail(f"缺少文件: .think-tank/{file}")

    config = yaml.safe_load((LOCAL / "config.yaml").read_text(encoding="utf-8"))
    workspace = config.get("workspace", {})
    for key in [
        "inbox_dir",
        "sources_dir",
        "trends_dir",
        "curation_dir",
        "competitors_dir",
        "signals_dir",
        "backlog_dir",
        "decisions_dir",
        "experiments_dir",
        "runbooks_dir",
        "promotion_dir",
        "metrics_dir",
        "calendar_dir",
        "creators_dir",
        "templates_dir",
        "domain_packs_dir",
    ]:
        if key not in workspace:
            fail(f"config.yaml workspace 缺少 {key}")

    research_os = config.get("research_os", {})
    if research_os.get("source_ledger") != ".think-tank/sources/ledger.jsonl":
        fail("research_os.source_ledger 路径不正确")
    if research_os.get("source_candidate_template") != ".think-tank/sources/source-ledger-candidate-template.yaml":
        fail("research_os.source_candidate_template 路径不正确")
    if research_os.get("default_trends_dir") != ".think-tank/trends":
        fail("research_os.default_trends_dir 路径不正确")
    if research_os.get("default_curation_dir") != ".think-tank/curation":
        fail("research_os.default_curation_dir 路径不正确")
    if research_os.get("write_policy") != "local_only":
        fail("research_os.write_policy 必须是 local_only")
    if research_os.get("default_signal_dir") != ".think-tank/signals":
        fail("research_os.default_signal_dir 路径不正确")
    if research_os.get("default_backlog_dir") != ".think-tank/backlog":
        fail("research_os.default_backlog_dir 路径不正确")
    if research_os.get("default_promotion_dir") != ".think-tank/promotion":
        fail("research_os.default_promotion_dir 路径不正确")
    if research_os.get("default_metrics_dir") != ".think-tank/metrics":
        fail("research_os.default_metrics_dir 路径不正确")
    if research_os.get("default_calendar_dir") != ".think-tank/calendar":
        fail("research_os.default_calendar_dir 路径不正确")
    if research_os.get("default_creators_dir") != ".think-tank/creators":
        fail("research_os.default_creators_dir 路径不正确")

    ledger_first = (LOCAL / "sources" / "ledger.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()[0]
    try:
        json.loads(ledger_first)
    except json.JSONDecodeError as error:
        fail(f"sources/ledger.jsonl 首行不是合法 JSON: {error}")

    require_text(
        "README.md",
        [
            "本地研究操作系统",
            "sources/",
            "trends/",
            "curation/",
            "signals/",
            "backlog/",
            "decisions/",
            "experiments/",
            "runbooks/",
            "promotion/",
            "metrics/",
            "calendar/",
            "creators/",
            "产品研究到运营闭环",
            "宣传运营闭环",
        ],
    )
    require_text(
        "routes.md",
        [
            "产物落点建议",
            "sources/ledger.jsonl",
            "trends/",
            "curation/",
            "signals/",
            "backlog/",
            "promotion/",
            "metrics/",
            "calendar/",
            "creators/",
            "研究到运营闭环",
        ],
    )
    require_text("providers.md", ["Provider 到资产层的映射", "preflight ready"])
    require_text(
        "operations.md",
        ["研究资产沉淀流程", "sources/ledger.jsonl", "trends/", "curation:", "promotion/", "任务收口契约"],
    )
    require_text("sources/source-ledger-candidate-template.yaml", ["candidate_reason", "used_for", "should_append_to_ledger"])
    require_text("trends/trend-template.yaml", ["impact:", "opportunities", "decision:"])
    require_text("trends/trend-to-action-template.md", ["Trend to Action", "Action Mapping", "backlog item"])
    require_text("curation/post-run-curation-template.yaml", ["artifact_plan", "source_candidates", "obsidian_candidate"])
    require_text("curation/artifact-plan-template.yaml", ["artifact_type", "privacy_boundary", "verification_status"])
    require_text("signals/user-signal-template.yaml", ["pain_points", "opportunity_candidates", "privacy_boundary"])
    require_text("backlog/opportunity-template.yaml", ["expected_impact", "confidence", "next_step"])
    require_text("backlog/backlog-item-template.yaml", ["acceptance_criteria", "evidence", "metrics"])
    require_text("promotion/README.md", ["Promotion Engine", "creative brief", "performance review"])
    require_text("promotion/campaign-template.yaml", ["goal:", "channels:", "metrics:", "experiment:"])
    require_text("promotion/creative-brief-template.md", ["Audience", "Product Proof", "Measurement"])
    require_text("promotion/before-after-showcase-template.md", ["Before / After", "Quality Bar"])
    require_text("promotion/ugc-script-template.md", ["UGC Script", "Creator Notes"])
    require_text("promotion/app-store-cpp-template.yaml", ["keyword_cluster", "screenshot_sequence", "test_plan"])
    require_text("promotion/performance-review-template.md", ["Campaign Performance Review", "User Signals", "Next Actions"])
    require_text("runbooks/weekly-promotion-ideas.md", ["content angles", "creative briefs", "campaign candidates"])
    require_text("promotion/specs/short-video-spec.md", ["0-2s", "3-second hold rate", "CTA"])
    require_text("promotion/scripts/short-video-15s-template.md", ["Timeline", "Required Assets", "Boundaries"])
    require_text("promotion/ideas/content-pillars.yaml", ["result_showcase", "tutorial", "trend"])
    require_text("promotion/checklists/pre-publish-checklist.md", ["hook", "before / after", "CTA"])
    require_text("promotion/checklists/claim-safety-checklist.md", ["未上线功能", "竞品"])
    require_text("promotion/checklists/asset-rights-checklist.md", ["授权", "用户隐私"])
    require_text("promotion/reuse-matrix.md", ["Content Reuse Matrix", "platform-specific variant"])
    require_text("runbooks/content-production-pipeline.md", ["idea", "creative brief", "performance review"])
    require_text("runbooks/post-run-curation.md", ["source candidate", "artifact_plan", "obsidian_candidate"])
    require_text("metrics/metric-dictionary.yaml", ["activation", "first_successful_edit", "retention_d7"])
    require_text("metrics/campaign-result-template.yaml", ["primary_metric", "channel_results", "data_quality"])
    require_text("calendar/content-calendar-template.yaml", ["slots:", "review_date", "primary_metric"])
    require_text("creators/creator-template.yaml", ["fit_for_awakening", "past_collaboration", "brand_safety"])
    require_text("creators/collaboration-tracker.yaml", ["brief_path", "deliverables", "performance"])
    domain_pack_files = [
        path
        for path in (LOCAL / "domain-packs").rglob("*")
        if path.is_file() and path.name in {"README.md", "messaging-house.md"}
    ]
    if not domain_pack_files:
        fail("domain-packs 必须至少包含 README.md 或 messaging-house.md")

    print("local research OS 检查通过")


if __name__ == "__main__":
    main()
