# Post-run Curation

## Purpose

Post-run curation is a platform-independent closing contract for turning a think-tank result into reusable assets.

It prevents research, strategy, review, council, and promotion planning from ending as a one-off chat answer when the result contains reusable sources, trends, decisions, actions, or artifacts.

## Required For

Post-run curation is required when a task includes any of:

- research or trend analysis
- competitive intelligence
- market research
- user feedback analysis
- strategy planning
- review findings with follow-up work
- monitoring plans
- promotion or content planning
- any answer that cites external sources
- any answer that proposes backlog, experiment, decision, or runbook actions

For very small tasks, curation may be marked `should_persist: false`, but the boundary must be explicit.

## Contract

Every required curation block must include:

```yaml
post_run_curation:
  required: true
  should_persist: true | false
  source_candidates: []
  trend_candidates: []
  action_candidates: []
  generated_artifacts: []
  artifact_plan: {}
  persistence_decision: {}
  boundaries: []
```

## Source Candidates

Use source candidates when the run used web pages, local files, user-provided materials, generated media, social sources, PDFs, audio, video, or direct tool output.

```yaml
source_candidates:
  - title: ""
    url_or_path: ""
    source_type: web | local_file | user_provided | social | pdf | video | audio | generated | tool_output
    reliability: high | medium | low | unknown
    freshness: current | stale | unknown
    used_for:
      - claim: ""
        confidence: low | medium | high
    verification_status: verified | partial | unverified | contradicted
    should_append_to_ledger: true | false
```

Source candidates do not mean the platform has written to a ledger. They are a structured handoff for a local workspace, note system, project documentation, or user confirmation step.

## Trend Candidates

Use trend candidates when the run identifies a market, technology, platform, product, policy, or social behavior trend.

```yaml
trend_candidates:
  - name: ""
    category: ai | product | market | social | technology | platform | policy | monetization | other
    summary: ""
    source_refs: []
    confidence: low | medium | high
    impact:
      product: low | medium | high
      marketing: low | medium | high
      operations: low | medium | high
      technology: low | medium | high
    opportunities: []
    risks: []
    decision: act | test | watch | ignore
```

Trends are not actions by themselves. They must be mapped to actions or explicitly marked as watch-only.

## Action Candidates

Use action candidates when the run recommends concrete work.

```yaml
action_candidates:
  - type: backlog | experiment | decision | runbook | promotion | monitoring | follow_up_research
    title: ""
    rationale: ""
    evidence_refs: []
    priority: P0 | P1 | P2 | P3
    confidence: low | medium | high
    next_step: ""
```

Action candidates are proposals. They do not create issues, tasks, notes, automations, or project files unless the platform adapter has explicit write permission or the user requested writing.

## Generated Artifacts

Use generated artifacts when the run produced or assembled a durable file, source bundle, rendered media, report, slide deck, spreadsheet, run record, sample, or demo.

```yaml
generated_artifacts:
  - title: ""
    artifact_type: report | brief | video | audio | slide_deck | spreadsheet | demo | run_record | sample | source_bundle | other
    path: ""
    source_refs: []
    verification_refs: []
    known_gaps: []
    rights_boundary: public_safe | local_only | internal_review | publish_candidate | commercial_release | private_do_not_share | unknown
    verification_status: verified | verified_partial | partial | unverified | failed | blocked
```

Generated artifact candidates do not prove persistence by themselves. They must be paired with `persistence_decision` to say whether files were actually written and with artifact quality evidence when the artifact is claimed as verified or partially verified.

For media production, generated artifacts should reference the source or asset manifest, render output, probe evidence, keyframe checks, subtitle or audio checks, and known gaps such as missing BGM, partial rights review, provider fallback, or manual-only inspection.

## Artifact Plan

Use artifact plans when the answer should become a report, brief, review record, run record, backlog, sample, or project document.

```yaml
artifact_plan:
  should_write: true | false
  artifact_type: report | brief | trend_radar | strategy | review | backlog | run_record | sample | protocol_doc | other
  suggested_destination: ""
  title: ""
  source_refs: []
  requires_confirmation: true | false
  privacy_boundary: public_safe | local_only | private_do_not_share
  verification_status: verified | partial | unverified
```

`suggested_destination` is advisory in the protocol. Platform adapters decide actual paths.

## Persistence Decision

The final curation block must say what happened:

```yaml
persistence_decision:
  wrote_files: true | false
  write_requested_by_user: true | false
  write_permission_obtained: true | false
  destinations: []
  skipped_destinations: []
  reason: ""
```

If the run only produces candidates and writes nothing, say so clearly.

## Boundaries

The curation block must not overstate execution:

- Do not say a source was appended to a ledger unless it was actually written.
- Do not say an artifact was saved unless a file was actually written.
- Do not say a note was written to Obsidian, NotebookLM, or another private knowledge system unless it was actually written with permission.
- Do not mark source candidates `verified` if they were only glanced at, inferred, generated, or partially checked.
- Do not convert weak trends into backlog without confidence and evidence boundaries.

## Minimal Closing Block

For any required task, the final answer should include at least:

```yaml
post_run_curation:
  required: true
  should_persist: true | false
  source_candidates: []
  trend_candidates: []
  action_candidates: []
  generated_artifacts: []
  artifact_plan:
    should_write: true | false
    requires_confirmation: true | false
  persistence_decision:
    wrote_files: false
    reason: ""
  boundaries: []
```

This block is part of think-tank core behavior. Project-local files such as `.think-tank/` are only possible landing zones, not the source of this capability.
