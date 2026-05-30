# Source Acquisition Provider Pattern

This example documents a pattern. It is not proof that a web provider is installed, invoked, or recovered in the current user's environment.

```yaml
pattern_status:
  pattern_documented: true
  available_if_user_installs_provider: true
  requires_user_environment: network access, provider permission, source URL policy
  not_bundled: true
```

## User Intent

Research a current technical topic using external sources, then produce a source-grounded brief.

## think-tank Role

- Select `research` mode.
- Define source quality requirements.
- Route to the `source-acquisition` capability slot if the platform exposes a provider.
- Separate discovered, selected, invoked, and recovered provider states.

## Provider Boundary

```yaml
provider_boundary:
  route_selected: source-acquisition
  provider_preflight: check provider exists, network is allowed, source policy is clear
  dispatch_decision: invoke only after task permission and source scope are clear
  invoked_providers: []
  not_invoked_providers:
    - web-access
    - agent-reach
  recovery: no provider output recovered in this pattern document
  boundaries:
    - route selection is not provider invocation
    - snippets or URLs must be attributed when actually used
    - paywalled, login-only, or restricted sources require user permission
  verification_status: pattern_documented
```

## Expected Output Shape

```yaml
selected_intent: research
selected_mode: research
selected_capabilities:
  - source-acquisition
invoked_providers: []
not_invoked_providers:
  - web-access: available_if_user_installs_provider
boundaries:
  - External source acquisition requires the user's provider and permission.
verification_status: pattern_documented
```
