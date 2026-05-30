# Knowledge Persistence Provider Pattern

This example documents a knowledge-persistence pattern using `obsidian` as a representative peer skill. It does not claim default private knowledge-base writes.

```yaml
pattern_status:
  pattern_documented: true
  available_if_user_installs_provider: true
  requires_user_environment: vault path, write permission, user confirmation, retention policy
  not_bundled: true
```

## User Intent

After a research or council run, save durable conclusions as a reviewed note.

## think-tank Role

- Propose memory candidates.
- Separate facts, decisions, risks, and follow-up actions.
- Ask for explicit write confirmation before any private vault write.
- Keep local vault paths out of public examples unless they are placeholders.

## Provider Boundary

```yaml
provider_boundary:
  route_selected: knowledge-persistence
  provider_preflight: check vault path, target note, write permission, and user approval
  dispatch_decision: do not invoke until explicit write confirmation exists
  invoked_providers: []
  not_invoked_providers:
    - obsidian
  recovery: no provider output recovered in this pattern document
  boundaries:
    - proposed memory is not persisted memory
    - private knowledge-base writes require explicit user confirmation
    - user vault structure is outside the public skill core
  verification_status: pattern_documented
```

## Expected Output Shape

```yaml
selected_intent: post_run_curation
selected_mode: review
selected_capabilities:
  - knowledge-persistence
invoked_providers: []
not_invoked_providers:
  - obsidian: requires_user_environment
boundaries:
  - The note is a proposal until the user confirms a write.
verification_status: pattern_documented
```
