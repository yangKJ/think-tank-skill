# Media Production Provider Pattern

This example documents a media-production pattern using `ai-research-to-video-production` as a representative peer skill. It does not claim automatic publishing, rendering, or asset ownership.

```yaml
pattern_status:
  pattern_documented: true
  available_if_user_installs_provider: true
  requires_user_environment: source rights, visual assets, voice settings, render target, platform policy
  not_bundled: true
```

## User Intent

Convert a research brief into a production-ready video package.

## think-tank Role

- Convert research into positioning, script outline, storyboard, and acceptance criteria.
- Define artifact quality gates.
- Route to `media-production` only when production provider and source rights are clear.
- Distinguish planning output from rendered media.

## Provider Boundary

```yaml
provider_boundary:
  route_selected: media-production
  provider_preflight: check source rights, production provider, output format, and review gate
  dispatch_decision: invoke only when production scope is explicit
  invoked_providers: []
  not_invoked_providers:
    - ai-research-to-video-production
  recovery: no provider output recovered in this pattern document
  boundaries:
    - storyboard is not rendered video
    - publishing is outside the default think-tank public core
    - generated assets need provenance and acceptance checks
  verification_status: pattern_documented
```

## Expected Output Shape

```yaml
selected_intent: media_production_planning
selected_mode: strategy
selected_capabilities:
  - media-production
invoked_providers: []
not_invoked_providers:
  - ai-research-to-video-production: available_if_user_installs_provider
boundaries:
  - Production execution depends on user-installed provider and asset rights.
verification_status: pattern_documented
```
