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
  optional_user_supplied_assets:
    required: when_declared
    checks:
      - accepted formats and preferred destination are visible to the user
      - missing optional assets produce a draft or review-candidate status instead of silent failure
      - upgrade path is explicit, such as attach_bgm_and_rerender
```

## Status Rules

- `verified` requires all required gates to pass with reproducible evidence.
- `verified_partial` is allowed when the artifact is usable but has explicit gaps, such as missing BGM, partial source verification, limited rights review, or manual-only inspection.
- `draft_without_bgm` or similar draft status is acceptable when BGM is required only for final polish and the user has a clear upgrade path.
- `failed` means a required gate failed and no acceptable fallback artifact was produced.
- `blocked` means production could not proceed because a required provider, permission, source, or asset was unavailable.

Do not call an artifact final if a required gate is missing. Use `draft`, `partial`, `review_candidate`, or `blocked` language instead.

## Anti-Patterns

- Treating a successful route selection as artifact production.
- Treating provider preflight as render verification.
- Treating a file path as proof the file is valid without probing it.
- Treating one screenshot as full video review.
- Treating generated art or fake UI as evidence for factual news.
- Treating internal-review editorial assets as commercial-release cleared.
- Omitting known gaps because the final file exists.

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
