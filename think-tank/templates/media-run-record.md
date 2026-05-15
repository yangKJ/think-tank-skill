# Media Run Record

## Metadata

```yaml
mode:
intent: research_to_video
recipe: research-to-video
profiles:
capabilities:
runtime_provenance:
output_status:
started_at:
completed_at:
disagreements:
risks:
boundaries:
action_recommendations:
quality_check:
```

## Dispatch

```yaml
route_selected:
provider_preflight:
dispatch_decision:
invoked_providers:
not_invoked_providers:
recovery:
verification_status:
```

## Inputs

```yaml
topic:
brief_path:
storyboard_path:
source_manifest_path:
user_supplied_assets:
  bgm:
    requested_from_user:
    provided:
    path:
    expected_position:
    effect_if_missing:
  brand_assets:
  footage:
```

## Generated Artifacts

| artifact_type | path | status | verification_status | notes |
|---------------|------|--------|---------------------|-------|
| brief | | | | |
| storyboard | | | | |
| narration_audio | | | | |
| subtitles | | | | |
| render | | | | |

## Commands Or Provider Actions

| step | provider_or_command | input | output | status | evidence |
|------|---------------------|-------|--------|--------|----------|
|      |                     |       |        |        |          |

## Artifact Quality Gates

```yaml
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

## Known Gaps

- 事实缺口：
- 素材缺口：
- BGM 缺口：
- 工具缺口：
- 用户确认缺口：

## Upgrade Path

```yaml
next_action:
attach_bgm_and_rerender:
replace_assets:
rerender_required:
publish_ready_after:
```

## Disagreements

- 执行争议：
- 质量争议：
- 是否可发布争议：

## Risks

- 来源风险：
- 授权风险：
- BGM 风险：
- 渲染风险：
- 平台限制：

## Boundaries

```yaml
what_was_verified:
what_was_not_verified:
manual_checks_required:
```

## Action Recommendations

- 立即修复：
- 可发布前修复：
- 后续模板化：

## Quality Check

```yaml
run_record_complete:
generated_artifacts_listed:
output_status_declared:
upgrade_path_declared:
```
