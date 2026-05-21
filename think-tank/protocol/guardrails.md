# Guardrails

Guardrails are the 2.0 safety and quality gates for provider usage, memory writes, external access, generated artifacts, and release claims.

## Goal

```yaml
feature: guardrails
version: "2.0"
default_behavior: fail_closed_on_permission_or_privacy_risk
```

## Guardrail Categories

```yaml
permission_gate:
  use_for: external access, private writes, media download, social platform reads, publishing
privacy_gate:
  use_for: secrets, private paths, account identifiers, private project material
evidence_gate:
  use_for: claims, source citations, provider invocation, release status
artifact_gate:
  use_for: generated files, reports, media, demos, run records
memory_gate:
  use_for: memory candidate promotion and persistence
security_gate:
  use_for: MCP/provider execution, local shell, untrusted content, prompt injection risk
```

## Required Guardrail Result

```yaml
guardrail_result:
  gate:
  status: pass | fail | blocked | needs_user_confirmation
  reason:
  evidence_refs: []
  required_action:
  fallback:
```

## High-Risk Operations

These operations require explicit permission or a platform-specific approval gate:

- writing to private knowledge systems
- downloading or transforming media
- social platform collection
- invoking external login-dependent providers
- publishing, sending, deleting, or modifying remote content
- running untrusted MCP servers or tools
- promoting private project memory to public docs

## Failure Boundary

When a guardrail fails, think-tank should still produce useful output when possible, but must downgrade the execution method and verification status.
