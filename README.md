# think-tank-skill

Stable, protocol-first home of **think-tank**: a cross-platform high-level Skill for research, review, council, and strategy workflows on a verified Codex-first runtime path.

The high-level Skill lives in [`think-tank/`](think-tank/).
The leader orchestration layer is being split into a standalone sibling project on the Desktop.

## Why use think-tank?

- One protocol surface for research, review, council, and strategy work.
- A clear split between orchestration and tools:
  `think-tank = task understanding + role organization + capability routing + evidence synthesis + boundary declaration`.
- Explicit evidence states: `verified`, `verified_partial`, `planned`, `blocked`.
- Public release gates that check protocol integrity, privacy boundaries, package scope, and stable posture.

## Quick Start

1. Read [`think-tank/README.md`](think-tank/README.md) and [`think-tank/docs/open-source-quickstart.md`](think-tank/docs/open-source-quickstart.md).
2. Install or copy the skill core:

```text
think-tank/
```

into your platform's skill directory, or clone this repository and reference `think-tank/` directly.

3. Try one of the public templates:

```text
think-tank/examples/public/research-request.md
think-tank/examples/public/council-decision.md
think-tank/examples/public/review-acceptance.md
```

4. Run the public release gate:

```bash
python3 checks/open_source_release_suite.py
```

5. Run the stable gate:

```bash
python3 checks/stable_release_check.py
```

If both pass, you are on the repository's current stable public path.

## Repository Layout

```text
think-tank-skill/
├── README.md
├── LICENSE
├── .gitignore
├── think-tank/
│   ├── SKILL.md
│   ├── README.md
│   ├── protocol/
│   ├── capabilities/
│   ├── profiles/
│   ├── platforms/
│   ├── modes/
│   ├── templates/
│   ├── runtime/
│   ├── domain-packs/
│   ├── docs/
│   └── examples/
```

## Key Directories

- [`think-tank/SKILL.md`](think-tank/SKILL.md): Skill entrypoint.
- [`think-tank/protocol/`](think-tank/protocol/): Platform-independent protocol source of truth.
- [`think-tank/capabilities/`](think-tank/capabilities/): Capability slots for external skills and tools.
- [`think-tank/profiles/`](think-tank/profiles/): Cross-platform role profiles.
- [`think-tank/platforms/`](think-tank/platforms/): Claude Code, Codex, and future platform adapters.
- [`think-tank/modes/`](think-tank/modes/): Research, council, review, and strategy modes.
- [`think-tank/runtime/`](think-tank/runtime/): Platform-neutral minimal runtime primitives.
- [`think-tank/templates/`](think-tank/templates/): Cross-platform report and kickoff templates.
- [`think-tank/domain-packs/`](think-tank/domain-packs/): Optional domain packs.
- [`think-tank/schemas/`](think-tank/schemas/): Machine-readable input and output schemas.
- [`think-tank/examples/`](think-tank/examples/): Reusable examples that demonstrate the protocol.
- `leader-runtime`: standalone sibling project, no longer part of the default Skill release bundle.

## Stable Posture

Public release posture:

```yaml
release_posture: stable_release
target_users:
  - Codex-first teams with explicit capability boundaries
  - protocol-first contributors and integrators
  - teams willing to work with explicit capability boundaries
not_target_users:
  - users expecting every optional provider to work out of the box
  - users expecting full multi-agent runtime across platforms
```

This repository is ready to be shared publicly as a stable protocol-first release with explicit capability boundaries. It is not an "install once and every provider just works" distribution.

## Stable Means

- Stable protocol surface in `think-tank/`
- Stable Codex-first default path
- Stable public release gates
- Stable evidence-based capability claims

## Stable Does Not Mean

- Every optional provider works by default
- Cross-platform runtime parity is complete
- External login flows, social scraping, or private knowledge-base writes are default capabilities
- Every installed peer skill is automatically invoked and recovered

## Evidence At A Glance

| area | status | source |
|------|--------|--------|
| Codex foundation | verified | [`think-tank/docs/codex-readiness-matrix.md`](think-tank/docs/codex-readiness-matrix.md) |
| Provider invocation proofs | 4 public proofs | [`think-tank/examples/stable-release-readiness.yaml`](think-tank/examples/stable-release-readiness.yaml) |
| External browser readonly | verified_partial | [`think-tank/examples/codex-browser-external-readonly.md`](think-tank/examples/codex-browser-external-readonly.md) |
| Beyond-readonly subagent runtime | verified_partial | [`think-tank/examples/codex-subagent-lifecycle-validation.md`](think-tank/examples/codex-subagent-lifecycle-validation.md) |
| Long-running subagent lifecycle | verified_partial | [`think-tank/docs/stable-readiness-matrix.md`](think-tank/docs/stable-readiness-matrix.md) |
| Claude Code runtime | deferred | [`think-tank/docs/support-matrix.md`](think-tank/docs/support-matrix.md) |

## Who Should Not Use This

- Teams expecting zero-configuration access to every optional provider
- Users who do not want explicit runtime and evidence boundaries
- Users who need default support for external login automation or private knowledge-base writes
- Users who need full cross-platform multi-agent parity today

## Moved Creator Media System

Creator media, comic-drama, TTS, image-production, and video-production resources have moved to a separate closed production repository.

This repository now keeps only the public, reusable `think-tank/` core and non-project-specific governance. Do not add self-media, comic-drama episode assets, generated videos, local TTS runs, or creator production queues back into `think-tank-skill`.

## What Is think-tank?

think-tank is a higher-level Skill and protocol system. It is designed to be used by Claude Code, Codex, other local projects, and future users without being tied to one runtime or one private project.

It is not:

- A platform-specific script wrapper
- A private prompt collection
- A child module of a research agent
- A renamed agent-council implementation

It is:

- The primary Skill
- The primary protocol source
- A reusable cross-platform capability framework
- A place to consolidate research, council, review, and strategy workflows

## Protocol Core

- [`think-tank/protocol/think-tank-protocol.md`](think-tank/protocol/think-tank-protocol.md): Core workflow.
- [`think-tank/protocol/roles.md`](think-tank/protocol/roles.md): Role selection and responsibilities.
- [`think-tank/protocol/agent-selection.md`](think-tank/protocol/agent-selection.md): Scenario-driven agent selection.
- [`think-tank/protocol/mode-selection.md`](think-tank/protocol/mode-selection.md): Mode selection rules.
- [`think-tank/protocol/quality-gates.md`](think-tank/protocol/quality-gates.md): Quality gates.
- [`think-tank/protocol/artifact-quality-gates.md`](think-tank/protocol/artifact-quality-gates.md): Artifact and media production quality gates.
- [`think-tank/protocol/versioning.md`](think-tank/protocol/versioning.md): Protocol versioning.

## Read Next

- Start here:
  - [`think-tank/README.md`](think-tank/README.md)
  - [`think-tank/docs/open-source-quickstart.md`](think-tank/docs/open-source-quickstart.md)
  - [`think-tank/docs/support-matrix.md`](think-tank/docs/support-matrix.md)
  - [`think-tank/docs/validation-tiers.md`](think-tank/docs/validation-tiers.md)
  - [`think-tank/docs/open-source-release.md`](think-tank/docs/open-source-release.md)
- Stable release references:
  - [`think-tank/docs/stable-release-criteria.md`](think-tank/docs/stable-release-criteria.md)
  - [`think-tank/docs/stable-readiness-matrix.md`](think-tank/docs/stable-readiness-matrix.md)
  - [`think-tank/docs/stable-release-checklist.md`](think-tank/docs/stable-release-checklist.md)
  - [`think-tank/docs/v1.0.0-release-notes.md`](think-tank/docs/v1.0.0-release-notes.md)
  - [`think-tank/docs/release-tagging.md`](think-tank/docs/release-tagging.md)
- Codex runtime references:
  - [`think-tank/docs/codex-validation-report.md`](think-tank/docs/codex-validation-report.md)
  - [`think-tank/docs/codex-acceptance.md`](think-tank/docs/codex-acceptance.md)
  - [`think-tank/docs/codex-readiness-matrix.md`](think-tank/docs/codex-readiness-matrix.md)
  - [`think-tank/platforms/codex/operating-guide.md`](think-tank/platforms/codex/operating-guide.md)
  - [`think-tank/platforms/codex/capability-status.md`](think-tank/platforms/codex/capability-status.md)
- Protocol and governance references:
  - [`open-source-packages.yaml`](open-source-packages.yaml)
  - [`think-tank/docs/history.md`](think-tank/docs/history.md)
  - [`think-tank/protocol/local-workspace.md`](think-tank/protocol/local-workspace.md)
  - [`think-tank/protocol/memory-curation.md`](think-tank/protocol/memory-curation.md)
  - [`think-tank/protocol/capability-evidence-state-machine.md`](think-tank/protocol/capability-evidence-state-machine.md)
  - [`think-tank/protocol/memory-promotion-policy.md`](think-tank/protocol/memory-promotion-policy.md)
  - [`think-tank/protocol/runtime-provenance.md`](think-tank/protocol/runtime-provenance.md)
  - [`think-tank/protocol/natural-language-runtime-orchestration.md`](think-tank/protocol/natural-language-runtime-orchestration.md)

## Validation

Validation is performed locally. Public protocol changes should still be reviewed against the relevant protocol, schema, template, and README files before release.

Release gate commands:

```bash
python3 checks/open_source_release_suite.py
python3 checks/protocol_check.py
python3 checks/codex_validation_check.py
python3 checks/schema_sample_check.py
python3 checks/minimal_runtime_execution_check.py
python3 checks/release_privacy_check.py
python3 checks/open_source_release_check.py
```

Stable gate:

```bash
python3 checks/stable_release_check.py
```

Release packaging references:

```text
think-tank/docs/v1.0.0-release-notes.md
think-tank/docs/release-tagging.md
```

## Design Boundary

The protocol layer defines what think-tank means. Platform adapters define how think-tank runs in a specific environment. Modes define scenario defaults.

Platform-specific behavior must not redefine the core protocol.

`leader-runtime` is intentionally separate. It defines how a Codex-style main agent becomes a leader that can orchestrate expert pools and acceptance governance. `think-tank/` remains a reusable Skill core, not the entire leader operating layer.
