---
intent: research_to_video
default_mode: research
core_question: 如何把选题研究或资料调研转成有证据、有素材、有质量门禁、可继续升级的视频产物？
optional_peer_skills_are_dependencies: false
profiles:
  - source-collector
  - trend-analyst
  - report-architect
  - skeptic
capabilities:
  - source-acquisition
  - media-production
  - knowledge-persistence
# Provider selection is configured in .think-tank/provider-policy.yaml
---

# Research To Video

## Triggers

适用于用户希望从一个主题、资料包、链接集合、新闻线索、调研结论或研究报告继续生成视频的任务。

典型表达包括：

- “研究一下这个选题并生成视频”
- “把这份调研资料做成视频”
- “把调研资料做成视频 brief”
- “把竞品/市场/技术调研做成短视频脚本和成片”
- “先调研，再给我做成可发布的视频”

触发词只用于 routing policy。recipe 本身不绑定具体平台、工具或 peer skill。

## Defaults

```yaml
intent: research_to_video
mode: research
recipe: research-to-video
profiles:
  - source-collector
  - trend-analyst
  - report-architect
  - skeptic
capabilities:
  - source-acquisition
  - media-production
  - knowledge-persistence
optional_peer_skills_are_dependencies: false
missing_peer_skill_behavior: degrade_to_core_protocol
```

## Workflow

1. 选题界定：明确主题、受众、时长、比例、发布平台、信息密度和成片状态目标。
2. 来源获取：收集可追溯来源，区分一手资料、二手报道、社媒信号和用户提供资料。
3. 证据综合：把来源整理为 claim、evidence、confidence 和 use_in_video，避免无来源断言。
4. 叙事策划：形成开场钩子、核心观点、转折、结论和行动建议。
5. 素材可行性：为每个镜头判断是否有真实素材、可生成素材、可替代素材或必须降级。
6. 用户素材契约：明确 BGM、品牌资产、授权图片、产品录屏等可选用户素材是否已提供。
7. 脚本与分镜：输出可执行口播稿、字幕稿、镜头表、素材表、音频/SFX 位置和质量门禁。
8. 媒体执行：如果平台具备 media-production provider，可进入渲染；否则产出 production-ready plan。
9. 质量验收：按 `protocol/artifact-quality-gates.md` 检查音频、字幕、画面、素材、时长和导出文件。
10. 收尾沉淀：按 `protocol/post-run-curation.md` 记录 sources、generated_artifacts、known_gaps 和 upgrade_path。

## Runtime Provenance

输出必须区分：

```yaml
route_selected:
provider_preflight:
dispatch_decision:
invoked_providers:
not_invoked_providers:
recovery:
verification_status:
```

禁止把 recipe 命中、provider selection、preflight 或本地文件存在说成真实视频生成已完成。

## Output Status

```yaml
output_status:
  enum:
    - research_brief_only
    - script_ready
    - storyboard_ready
    - production_plan_ready
    - draft_without_bgm
    - review_candidate
    - final_with_bgm
    - blocked
```

状态含义：

- `research_brief_only`：只完成资料研究。
- `script_ready`：已形成可录制口播和字幕稿。
- `storyboard_ready`：已形成镜头级分镜与素材需求。
- `production_plan_ready`：已具备执行计划，但未调用渲染 provider。
- `draft_without_bgm`：已有可审看视频，但缺少用户 BGM 或授权音乐。
- `review_candidate`：已通过最低成片检查，可供用户审看。
- `final_with_bgm`：已集成 BGM，并通过最终导出检查。
- `blocked`：来源、素材、权限、登录态、工具或用户输入不足导致无法推进。

## Required Gates

必须至少覆盖：

```yaml
quality_gates:
  topic_fit:
  source_traceability:
  evidence_claim_alignment:
  asset_feasibility:
  optional_user_supplied_assets:
  narration_subtitle_alignment:
  render_probe:
  keyframe_review:
  post_run_curation:
```

BGM 不是默认静默假设。用户未提供 BGM 时，应明确：

```yaml
optional_user_supplied_assets:
  bgm:
    requested_from_user: true
    provided: false
    effect_if_missing: output_status=draft_without_bgm
    upgrade_path: attach_bgm_and_rerender
```

## Output

最终输出应包含：

- 结论：当前能交付到哪个 `output_status`。
- 依据：来源表、证据表、素材表和执行记录。
- 分歧：不同来源、角色判断或素材策略的冲突。
- 风险：事实、版权、素材、BGM、平台限制、渲染和发布时间风险。
- 行动建议：下一步是补来源、补素材、补 BGM、重剪、发布还是沉淀。
- 边界：哪些 provider 被调用，哪些只是候选，哪些能力未验证。

推荐配套模板：

```text
templates/research-to-video-brief.md
templates/video-storyboard.md
templates/media-run-record.md
```
