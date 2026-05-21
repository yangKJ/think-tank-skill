# Contributing

Thank you for helping improve `think-tank`.

This repository is a protocol-first, cross-platform AI collaboration Skill. Contributions should make the public Skill core clearer, more reusable, more truthful about runtime evidence, or easier to validate.

## Project Scope

`think-tank` is not a grab bag of scripts. It is a reusable Skill and protocol system for research, review, council decisions, strategy work, Research OS, run records, memory runtime, provider ledgers, handoffs, guardrails, and eval fixtures.

The public core may include:

- protocol documents
- capability slots
- role profiles
- modes and recipes
- routing contracts
- platform adapters
- schemas
- templates
- public examples and fixtures
- public visual assets and prompts
- release checks

The public core must not include:

- private project memory
- local runtime state
- credentials, tokens, account identifiers, or secrets
- generated output batches
- machine-specific caches
- closed-source runtime implementation details
- provider login state
- private workspace contents

## Repository Boundaries

Use these locations intentionally:

- `think-tank/protocol/`: platform-neutral source of truth.
- `think-tank/capabilities/`: capability slots, not bundled provider implementations.
- `think-tank/platforms/`: platform adapters and runtime-specific boundaries.
- `think-tank/modes/`: scenario defaults.
- `think-tank/recipes/`: reusable task patterns.
- `think-tank/routing/`: provider route, dispatch, and recovery rules.
- `think-tank/schemas/`: machine-readable contracts.
- `think-tank/templates/`: reusable output templates.
- `think-tank/examples/`: public examples and fixtures.
- `think-tank/assets/`: public README and documentation visuals.
- `checks/`: deterministic release, privacy, protocol, and fixture checks.

Do not move local project policy, private memory, or runtime state into the public Skill core.

## Evidence And Claim Rules

Contributors must keep capability claims evidence-based.

Do not claim:

- route selection means provider invocation
- provider preflight means provider execution
- installed means verified
- selected means invoked
- recovered means verified
- single-agent multi-profile reasoning means true multi-agent runtime
- optional provider examples mean bundled provider support

Use explicit states such as:

- `pattern_documented`
- `available_if_user_installs_provider`
- `requires_user_environment`
- `not_bundled`
- `selected`
- `preflight_checked`
- `invoked`
- `recovered`
- `verified_partial`
- `verified`
- `blocked`

When provider behavior is involved, include a boundary block with:

```yaml
route_selected:
provider_preflight:
dispatch_decision:
invoked_providers:
not_invoked_providers:
recovery:
boundaries:
verification_status:
```

## Protocol Changes

When changing `think-tank/protocol/`, check whether the change affects:

- input or output semantics
- mode selection
- role responsibilities
- runtime provenance
- provider evidence state
- post-run curation
- memory promotion
- Research OS workspace contracts
- quality gates
- versioning expectations

If the change affects public behavior, update the relevant schema, template, example, and check in the same contribution.

## Adding Or Changing Modes

A mode contribution should define:

- when to use the mode
- when not to use it
- default profiles
- default capabilities
- workflow stages
- expected output
- quality gates
- runtime and provider boundaries

Also update:

- `think-tank/modes/README.md`
- `think-tank/protocol/mode-selection.md`
- relevant examples
- relevant checks

## Adding Provider Patterns

Provider examples are patterns, not bundled capabilities.

When adding a provider pattern:

- describe the capability slot first
- state that the provider is optional and user-installed
- state permission, login, runtime, network, rights, or security prerequisites
- include `invoked_providers` and `not_invoked_providers`
- include fallback and recovery behavior
- avoid provider logos, private account state, and private URLs

If the example proves a real invocation, include evidence and limitations. If it does not, mark it as `pattern_documented`.

## Adding 2.0 Runtime Features

For Research OS, run records, memory runtime, provider ledger, handoff, guardrails, or eval pack changes:

- update the protocol document
- update or add a schema
- update or add a template
- add a public fixture under `think-tank/examples/`
- update the relevant release check
- keep local workspace contents out of the repository

2.0 features must preserve this boundary:

```yaml
public_core_defines_contracts: true
user_workspace_owns_project_data: true
```

## Visual Assets

README-facing visuals should be PNG files with prompt records in `think-tank/assets/prompts/`.

Rules:

- Do not add SVG diagrams as primary README visuals.
- Do not add raw design files, private screenshots, or large generated batches.
- Keep labels readable at README size.
- Do not imply providers are bundled or automatically verified.
- Update `checks/visual_assets_check.py` when adding required public visuals.

## Privacy And Safety

Before opening a PR, inspect your changes for:

- secrets or tokens
- private paths
- private project names
- local workspace data
- generated output batches
- cached files
- provider login state
- raw social, media, or private knowledge-base data

If a contribution uses external sources or tools, document rights, permissions, and verification boundaries.

## Validation

Run the broad public release gate before submitting:

```bash
python3 checks/open_source_release_suite.py
python3 checks/stable_release_check.py
```

For focused changes, also run the relevant checks:

```bash
python3 checks/protocol_check.py
python3 checks/markdown_image_links_check.py
python3 checks/visual_assets_check.py
python3 checks/v1_1_release_check.py
python3 checks/v2_0_release_check.py
```

If you add a new protocol, schema, template, fixture, or public visual, add or update a check so the behavior remains regression-testable.

## Pull Request Checklist

Before submitting a pull request:

- [ ] The change fits the public Skill core.
- [ ] Private local data is not included.
- [ ] Provider claims are evidence-bounded.
- [ ] Protocol changes include schema, template, example, or check updates when needed.
- [ ] README or index files are updated when public entry points change.
- [ ] Release checks pass locally.
- [ ] Any remaining limitations are documented.

## Versioning

Follow `think-tank/protocol/versioning.md`.

In general:

- Documentation-only clarifications are patch-level.
- New non-breaking protocols, schemas, examples, or checks are minor-level.
- Changes that break public contracts, expected output shape, or stable release posture require a major version decision.
