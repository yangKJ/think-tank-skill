# Artifact Quality Gates

## Purpose

Artifact quality gates define how think-tank verifies generated deliverables before claiming they are complete.

They apply to generated reports, briefs, media projects, rendered videos, slide decks, spreadsheets, runnable demos, run records, and other reusable artifacts.

These gates do not replace domain-specific checks. They provide a platform-independent contract for proving what was produced, what was inspected, what failed, and what remains partial.

## Required When

Use artifact quality gates when a run produces or modifies any durable artifact, including:

- generated media files
- source manifests
- research reports or briefs
- reusable examples or samples
- run records
- project documents
- rendered screenshots or videos
- code-backed demos or local previews

If no artifact is produced, mark the gate as `not_applicable` rather than claiming success.

## Gate Record

```yaml
artifact_quality_gates:
  required: true
  artifact_type: report | brief | video | audio | slide_deck | spreadsheet | demo | run_record | sample | other
  artifact_paths: []
  gates:
    source_traceability:
      status: pass | fail | partial | not_applicable
      evidence: []
      gaps: []
    asset_presence:
      status: pass | fail | partial | not_applicable
      evidence: []
      gaps: []
    structure_validation:
      status: pass | fail | partial | not_applicable
      evidence: []
      gaps: []
    render_or_export_probe:
      status: pass | fail | partial | not_applicable
      evidence: []
      gaps: []
    visual_or_layout_review:
      status: pass | fail | partial | not_applicable
      evidence: []
      gaps: []
    audio_or_timing_review:
      status: pass | fail | partial | not_applicable
      evidence: []
      gaps: []
    rights_and_privacy_boundary:
      status: pass | fail | partial | not_applicable
      evidence: []
      gaps: []
    provider_boundary:
      status: pass | fail | partial | not_applicable
      evidence: []
      gaps: []
  verification_status: verified | verified_partial | failed | blocked
  boundaries: []
```

## Media Production Gates

For `media-production`, apply these media-specific checks:

```yaml
media_artifact_gates:
  source_manifest:
    required: true
    checks:
      - every factual story has a source identity
      - source freshness and reliability are labeled
      - unsupported claims are marked as inference or missing
  real_asset_presence:
    required: true
    checks:
      - every news or product card has at least one traceable visual asset
      - every required asset appears on screen or is marked missing
      - generated or abstract visuals are not the only evidence for factual news
  narration_subtitle_alignment:
    required: true
    checks:
      - every narration segment has a visible subtitle segment
      - subtitles do not appear before their segment or remain visible after it
      - subtitle text stays inside safe areas
  render_probe:
    required: true
    checks:
      - final file exists and is non-empty
      - duration is within expected bounds
      - resolution and frame rate match the target
      - audio stream exists when narration is required
      - audio loudness or silence risk is labeled when audio is present
      - preview frame is nonblank when visual output is expected
  keyframe_review:
    required: true
    checks:
      - intro frame renders
      - each major scene renders with the expected asset
      - no future subtitle, stale scene, blank screen, or severe overlap is visible
  rights_boundary:
    required: true
    checks:
      - source and asset license/usage risk is labeled
      - internal-review assets are not claimed as commercial-release ready
  provider_boundary:
    required: true
    checks:
      - external image, TTS, SFX, render, and publish providers are each labeled invoked or not_invoked
      - API keys, cookies, account tokens, and login states are not stored in artifacts
      - command previews are not claimed as real invocations
      - provider responses are sanitized before persistence
  optional_user_supplied_assets:
    required: when_declared
    checks:
      - accepted formats and preferred destination are visible to the user
      - missing optional assets produce a draft or review-candidate status instead of silent failure
      - upgrade path is explicit, such as attach_bgm_and_rerender
```

## Cover Artifact Gate

Use this gate when a run creates a public-facing cover, thumbnail, first frame, poster image, video card, or platform-specific share image.

The gate is provider-neutral. It defines whether the cover package is ready for prompt handoff, preview review, generation, revision, or publication. It does not require any specific image model, design tool, or video engine.

```yaml
cover_artifact_gate:
  required_when:
    - artifact_type_is_cover_thumbnail_first_frame_or_poster
    - artifact_is_used_as_public_entry_point
    - media_artifact_depends_on_click_or_first_screen_readability
  cover_package:
    status: planned_only | prompt_only | handoff_ready | preview_candidate | generated_candidate | publish_candidate | verified_partial | verified | blocked | failed
    platform: xiaohongshu | douyin | shipinhao | bilibili | youtube | newsletter | website | other
    aspect_ratio: 3:4 | 4:5 | 1:1 | 4:3 | 16:9 | 9:16 | other
    source_materials: []
    title_options: []
    selected_title:
    subtitle:
    visual_strategy: result | conflict | curiosity | before_after | character_emotion | product_focus | editorial | other
    main_subject:
    layout_brief:
    provider_boundary:
      selected_provider:
      provider_invoked: true | false
      invocation_evidence: []
      prompt_only_is_generation: false
  readability_checks:
    mobile_thumbnail_readable: pass | partial | fail | not_applicable
    title_length_fit: pass | partial | fail | not_applicable
    title_safe_area: pass | partial | fail | not_applicable
    visual_hierarchy_clear: pass | partial | fail | not_applicable
    one_second_comprehension: pass | partial | fail | not_applicable
  content_checks:
    click_reason_present: pass | partial | fail
    content_consistency: pass | partial | fail
    no_misleading_claim_or_fake_result: pass | partial | fail
    platform_fit: pass | partial | fail
  safety_checks:
    no_secrets_or_private_paths: pass | partial | fail
    unreleased_product_or_internal_ui_sanitized: pass | partial | fail | not_applicable
    rights_and_asset_boundary_labeled: pass | partial | fail
    likeness_or_brand_consent: confirmed | required | not_applicable | missing
  scorecard:
    total_score:
    pass_threshold: 80
    blocking_dimensions:
      - privacy_safety
      - rights_safety
      - title_readability
      - content_consistency
    recommended_fixes: []
  decision:
    passed: true | false
    batch_unlock_allowed: true | false
    next_action: revise_title | revise_layout | change_strategy | generate_preview | review_generated_image | publish_ready | blocked
```

Rules:

- A cover prompt is not a generated cover. Mark it as `prompt_only` or `handoff_ready` until a real provider returns an image artifact.
- A generated image is not publish-ready until text legibility, layout, rights, privacy, and content consistency checks pass.
- If the cover uses private code, internal UI, unreleased product screens, real faces, brand marks, or user-provided assets, run `public_output_sanitization` and `ai_media_identity_and_consent` when applicable.
- For scarce quota or paid providers, produce one cover package and the smallest representative preview before batch generation.
- If text is unreadable, the fix belongs upstream in title, layout, typography, or prompt design; do not keep rerunning the provider without changing the failed input.
- Platform variants may share a concept, but each variant needs its own safe area and readability check.

## Public Output Sanitization

Use this gate when local, private, proprietary, user-provided, or project-internal material is transformed into an artifact that may be shared outside the current private workspace.

```yaml
public_output_sanitization:
  required_when:
    - artifact_is_public_or_shareable
    - source_material_is_private_or_project_local
    - artifact_is_written_to_public_skill_or_project_docs
    - artifact_contains_screenshots_media_logs_or_generated_examples
  source_review:
    source_material_type: local_code | local_docs | git_history | user_provided | generated_media | tool_output | other
    private_material_present: true | false
    user_permission_for_public_use: true | false | not_applicable
  disclosure_level:
    value: public_safe | abstract_only | internal_review | private_reference | blocked
    reason:
  sanitization_checks:
    no_secrets_or_credentials: true | false
    no_private_paths_or_account_identifiers: true | false
    no_internal_api_database_schema_or_auth_details: true | false
    no_unverified_product_business_or_runtime_claims: true | false
    no_unlicensed_or_uncleared_assets_claimed_as_publish_ready: true | false
  output_policy:
    public_safe: may_publish_after_quality_gates
    abstract_only: remove implementation details and keep only generalized lessons
    internal_review: keep in local artifacts until reviewed
    private_reference: do not generate public-facing copy
    blocked: stop and record blocked reason
```

Selection for public output is not publication. A sanitized candidate only becomes a public artifact after the write, publish, or delivery action is explicitly invoked and recovered.

## AI Media Identity And Consent Gate

Use this gate when an artifact uses synthetic voices, voice cloning, face likeness, avatar likeness, identity simulation, or AI-generated media that could imply a real person appeared, spoke, endorsed, or approved the content.

```yaml
ai_media_identity_and_consent:
  required_when:
    - synthetic_voice_or_voice_clone_used
    - face_or_likeness_reference_used
    - real_person_identity_or_brand_presence_implied
    - generated_media_may_be_public_or_shareable
  consent_review:
    real_person_or_owned_asset_involved: true | false
    authorization_status: confirmed | required | not_applicable | missing
    license_or_consent_reference:
  disclosure_review:
    ai_generated_label_required: true | false
    public_release_disclosure_ready: true | false
    endorsement_or_impersonation_risk: none | low | medium | high
  blocked_uses:
    - impersonation
    - fraud_or_deception
    - undisclosed_public_release_implying_real_speech
    - fake_endorsement
    - harassment_or_bypassing_consent
  safer_fallbacks:
    - fictional_voice_or_character
    - neutral_narrator
    - manifest_only
    - human_recording_direction_sheet
```

If authorization is missing or unclear, do not generate or claim publish-ready media that imitates a real person. Use an original fictional voice, neutral narrator, or planning manifest instead.

## Scorecard Gate

Use scorecards to make review criteria explicit, but do not let a high total score hide a critical failure.

```yaml
scorecard_gate:
  required_when:
    - artifact_has_publish_or_delivery_candidate_status
    - artifact_quality_depends_on_multiple_dimensions
    - artifact_may_trigger_batch_or_external_invocation
  scoring:
    total_score:
    pass_threshold:
    excellent_threshold:
    dimension_scores:
      - dimension_id:
        score:
        max_score:
        minimum_required:
        blocking: true | false
        reason:
  decision:
    passed: true | false
    candidate_status: draft | review_candidate | publish_candidate | verified_partial | verified | blocked
    blocking_dimensions: []
    recommended_fixes: []
    batch_unlock_allowed: true | false
```

Rules:

- A total score is advisory unless required dimensions also pass.
- Any blocking dimension below its minimum must keep the artifact out of `verified`, `publish_candidate`, and full-batch execution.
- Scorecards must name the evidence used for each dimension or mark the score as manual judgment.
- `excellent_threshold` can justify prioritization, but it does not override privacy, rights, provider, render, or source gates.

## Status Rules

- `verified` requires all required gates to pass with reproducible evidence.
- `verified_partial` is allowed when the artifact is usable but has explicit gaps, such as missing BGM, partial source verification, limited rights review, or manual-only inspection.
- `draft_without_bgm` or similar draft status is acceptable when BGM is required only for final polish and the user has a clear upgrade path.
- `failed` means a required gate failed and no acceptable fallback artifact was produced.
- `blocked` means production could not proceed because a required provider, permission, source, or asset was unavailable.

Do not call an artifact final if a required gate is missing. Use `draft`, `partial`, `review_candidate`, or `blocked` language instead.

## High-Cost Artifact Progression

Use this progression when an artifact requires paid quota, scarce local compute, external provider calls, destructive writes, public publishing, or expensive manual review.

```yaml
high_cost_artifact_progression:
  upstream_lock:
    required: true
    fields:
      - input_lock_status
      - source_traceability_status
      - privacy_or_rights_boundary
    allowed_to_continue: locked | review_candidate
    blocked_values:
      - unlocked
      - private_reference
      - blocked
  preview_package:
    required_before_invocation: true
    examples:
      - manifest_only
      - command_preview
      - prompt_only
      - adapter_payload
      - dry_run_report
    provider_invoked: false
  first_pass_gate:
    required_before_batch: true
    sample_scope: smallest_representative_batch
    decision: accept | repair_same_item | change_upstream_plan | blocked
  quota_and_cost_gate:
    required_when_provider_or_compute_is_limited: true
    must_record:
      - quota_source
      - estimated_units
      - reserved_units_for_repair
      - fallback_when_insufficient
  batch_unlock:
    allowed_only_after:
      - first_pass_gate_passed
      - required_quality_gates_passed
      - provider_boundary_recorded
      - user_confirmation_when_external_or_public
  output_status:
    allowed_values:
      - planned_only
      - prompt_only
      - dry_run
      - review_candidate
      - partial
      - verified_partial
      - verified
      - blocked
      - failed
```

`ready_for_*` flags only describe eligibility for the next stage. They do not prove that the next stage ran. For example, `ready_for_render: true`, `ready_for_tts: true`, or `ready_for_publish: true` must not be reported as rendered, synthesized, or published unless invocation and recovery evidence exists.

## Repair And Batch Safety

Failed gates should shrink the blast radius instead of expanding production.

```yaml
repair_policy:
  default_scope: failed_item_only
  preserve_original_input: true
  preserve_failed_output_reference: true
  retry_budget:
    max_attempts_per_item:
    escalation_after_attempts:
      - change_prompt_or_parameters
      - change_upstream_plan
      - switch_provider_candidate
      - block_batch
  batch_safety:
    local_planning_can_batch: true
    external_invocation_requires_gate: true
    full_batch_requires_first_pass_acceptance: true
```

If the same item repeatedly fails, return to the upstream plan, prompt, storyboard, schema, layout, or requirement that produced the bad artifact. Do not keep spending quota or compute on full-batch retries.

## Anti-Patterns

- Treating a successful route selection as artifact production.
- Treating provider preflight as render verification.
- Treating a file path as proof the file is valid without probing it.
- Treating one screenshot as full video review.
- Treating generated art or fake UI as evidence for factual news.
- Treating internal-review editorial assets as commercial-release cleared.
- Omitting known gaps because the final file exists.
- Treating `ready_for_*` as proof that the next stage was actually invoked.
- Running a full batch before the smallest representative sample passes review.
- Repeating expensive provider calls when the failed item indicates an upstream planning or prompt problem.

## Recovery Into Final Output

Artifact gate results should be recovered into:

```yaml
runtime_provenance:
  evidence_state: verified | verified_partial | failed | blocked
post_run_curation:
  generated_artifacts: []
  artifact_plan: {}
  persistence_decision: {}
boundaries: []
```

When gates fail, the final answer should identify the failed gate, the reason, the produced fallback if any, and the next action needed to upgrade status.
