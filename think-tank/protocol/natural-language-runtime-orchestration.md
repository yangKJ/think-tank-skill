# Natural Language Runtime Orchestration

This protocol closes the gap between a user request and a minimal repeatable
think-tank runtime path.

## Goal

```yaml
feature: natural_language_runtime_orchestration
scope: codex_minimal_runtime
purpose: turn a user request into policy route, dispatch, invocation, recovery, final output, and run record
```

## Flow

```text
user_request
  -> provider_policy route
  -> runtime_provenance initialization
  -> dispatch_record
  -> minimal provider invocation when supported
  -> result_recovery
  -> final_output
  -> run_record
```

## Minimal Supported Runtime

```yaml
platform: codex
runtime: codex-natural-language-orchestrator
supported_invocation:
  source-acquisition:
    runtime_provider: local_static_reader
    target: local file or static public URL
unsupported_by_minimal_runtime:
  - external web-access provider invocation
  - social platform scraping
  - media download
  - private knowledge write
  - true independent multi-agent runtime
```

## Provider Boundary

The route may select a peer provider such as `web-access`, `xiaohongshu`, or
`summarize`. The minimal orchestrator must not pretend to invoke that provider
unless a real provider wrapper is executed.

```yaml
policy_selected_provider: may_be_external_peer_skill
runtime_selected_provider: local_static_reader | null
provider_selection_is_invocation: false
```

## Run Record

Every orchestrated run must include:

```yaml
run_record:
  run_id:
  created_at:
  artifact_requested:
  artifact_written:
  artifact_path:
```

Writing the run artifact is optional. If written, it belongs in `.think-tank/runs/`
or another project-local ignored directory.

## Output Contract

```yaml
runtime:
runtime_provenance:
request:
mode:
run_record:
policy_route:
dispatch_record:
source_result:
final_output:
quality_check:
boundaries:
```

## Quality Gates

```yaml
provider_policy_checked: true
runtime_provenance_present: true
provider_invocation_truthful: true
result_recovery_truthful: true
run_record_present: true
no_external_provider_overclaim: true
```

