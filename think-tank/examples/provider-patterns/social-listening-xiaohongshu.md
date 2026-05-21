# Social Listening Provider Pattern

This example documents a social-listening pattern using `xiaohongshu` as a representative peer skill name. It does not claim that social scraping, login, or platform access is bundled with think-tank.

```yaml
pattern_status:
  pattern_documented: true
  available_if_user_installs_provider: true
  requires_user_environment: MCP service, user login, platform permission, rate and content policy
  not_bundled: true
```

## User Intent

Collect a small social sample for product positioning or audience language analysis.

## think-tank Role

- Clarify whether the request is research, social listening, or marketing strategy.
- Define sampling goals, exclusion criteria, and privacy boundaries.
- Route to `social-listening` only when a provider is available and allowed.
- Summarize patterns without exposing private account state.

## Provider Boundary

```yaml
provider_boundary:
  route_selected: social-listening
  provider_preflight: check login, account permission, MCP health, and platform limits
  dispatch_decision: invoke only for user-authorized read paths
  invoked_providers: []
  not_invoked_providers:
    - xiaohongshu
  recovery: no provider output recovered in this pattern document
  boundaries:
    - think-tank documents the pattern, not default platform access
    - user login state and platform permission are outside the public skill core
    - collected samples need source, timestamp, and usage boundary
  verification_status: pattern_documented
```

## Expected Output Shape

```yaml
selected_intent: market_research
selected_mode: research
selected_capabilities:
  - social-listening
invoked_providers: []
not_invoked_providers:
  - xiaohongshu: requires_user_environment
boundaries:
  - Social data collection is optional and user-authorized.
verification_status: pattern_documented
```
