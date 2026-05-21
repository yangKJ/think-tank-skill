# think-tank-skill

think-tank-skill is the main repository for **think-tank**, a cross-platform reusable Skill for multi-role information gathering, collaborative analysis, deliberation, synthesis, and actionable recommendations.

The high-level Skill lives in [`think-tank/`](think-tank/).
The leader orchestration layer is being split into a standalone sibling project on the Desktop.

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

## Release Posture

Public release posture:

```yaml
release_posture: public_beta
target_users:
  - Codex-first early adopters
  - protocol-first contributors
  - teams willing to work with explicit capability boundaries
not_target_users:
  - users expecting every optional provider to work out of the box
  - users expecting full multi-agent runtime across platforms
```

This repository is ready to be shared publicly as a protocol-first beta. It is not yet a "install once and every provider just works" product distribution.

## Moved Creator Media System

Creator media, comic-drama, TTS, image-production, and video-production resources have moved to a separate closed production repository.

This repository now keeps only the public, reusable `think-tank/` core and non-project-specific governance. Do not add self-media, comic-drama episode assets, generated videos, local TTS runs, or creator production queues back into `think-tank-skill`.

## Protocol Core

- [`think-tank/protocol/think-tank-protocol.md`](think-tank/protocol/think-tank-protocol.md): Core workflow.
- [`think-tank/protocol/roles.md`](think-tank/protocol/roles.md): Role selection and responsibilities.
- [`think-tank/protocol/agent-selection.md`](think-tank/protocol/agent-selection.md): Scenario-driven agent selection.
- [`think-tank/protocol/mode-selection.md`](think-tank/protocol/mode-selection.md): Mode selection rules.
- [`think-tank/protocol/quality-gates.md`](think-tank/protocol/quality-gates.md): Quality gates.
- [`think-tank/protocol/artifact-quality-gates.md`](think-tank/protocol/artifact-quality-gates.md): Artifact and media production quality gates.
- [`think-tank/protocol/versioning.md`](think-tank/protocol/versioning.md): Protocol versioning.

## Current Status

This repository has completed the foundation, legacy migration, Codex runtime hardening, peer-skill routing, and workspace design stages.

The current public Skill source is `think-tank/`. Project-specific policy, run logs, artifacts, and memory candidates should stay outside the public Skill core.

Readiness status:

- [`think-tank/docs/v0.1-readiness.md`](think-tank/docs/v0.1-readiness.md)
- [`think-tank/docs/codex-validation-report.md`](think-tank/docs/codex-validation-report.md)
- [`think-tank/docs/codex-acceptance.md`](think-tank/docs/codex-acceptance.md)
- [`think-tank/docs/codex-readiness-matrix.md`](think-tank/docs/codex-readiness-matrix.md)
- [`think-tank/docs/open-source-quickstart.md`](think-tank/docs/open-source-quickstart.md)
- [`think-tank/docs/support-matrix.md`](think-tank/docs/support-matrix.md)
- [`think-tank/docs/open-source-release.md`](think-tank/docs/open-source-release.md)
- [`think-tank/docs/stable-release-criteria.md`](think-tank/docs/stable-release-criteria.md)
- [`think-tank/docs/stable-readiness-matrix.md`](think-tank/docs/stable-readiness-matrix.md)
- [`think-tank/docs/stable-release-checklist.md`](think-tank/docs/stable-release-checklist.md)
- [`open-source-packages.yaml`](open-source-packages.yaml)
- [`think-tank/platforms/codex/operating-guide.md`](think-tank/platforms/codex/operating-guide.md)
- [`think-tank/platforms/codex/capability-status.md`](think-tank/platforms/codex/capability-status.md)
- [`think-tank/examples/codex-smoke-research.md`](think-tank/examples/codex-smoke-research.md)
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

Stable gate is stricter and currently expected to fail until more runtime evidence exists:

```bash
python3 checks/stable_release_check.py
```

Codex foundation status:

- Four core modes are verified through Codex single-agent multi-profile execution.
- Capability degradation is verified.
- Browser automation is verified as an optional localhost fixture integration.
- External readonly source acquisition is verified through Codex source acquisition.
- Codex minimal runtime mirror is verified with a local static fixture.
- Browser external DOM recovery is blocked in the current environment and is not claimed as verified.
- JSON input/output samples are checked.
- Codex true multi-agent council is verified_partial for readonly subagent role-result recovery.
- Claude Code runtime remains deferred.
- v0.2 runtime hardening contracts are specified and checked.
- v0.2 platform-neutral minimal runtime library is implemented and checked.
- v0.2 Codex runtime pipeline and platform-neutral runtime result schema are checked.
- Legacy Claude Code think-tank assets have been migrated by abstraction into protocol, runtime, templates, and Claude Code adapter documentation.
- Legacy research agent assets have been fully classified and migrated by disposition in v0.3.
- Legacy agent-council assets have been fully classified and migrated by disposition in v0.4.
- Specialist subagent runtime contracts and runtime primitives are implemented in v0.5, with fallback labeling when true independent subagents are unavailable.
- Current local Codex installation is validated by ignored local checks.
- Legacy research external skills are installed as peer Codex skills and validated by ignored local checks.
- Codex provider invocation matrix is established; selected peer skills still require per-provider invocation validation before they can be called verified.
- Project-local workspace data is separated from the public Skill core.
- Project memory capture is implemented as propose-then-review; it does not auto-select persistence providers or auto-write private knowledge stores.
- v2.1 capability evidence states distinguish installed, discovered, selected, dispatched, invoked, recovered, verified_partial, and verified.
- v2.1 memory promotion policy controls whether memory stays local, moves to AGENTS.md, becomes project docs, or is generalized into public protocol.
- v2.2 runtime provenance gate requires every think-tank-style output to disclose runtime, provider invocation, data collection, result recovery, and multi-agent truthfulness.
- v2.3 Codex natural-language orchestrator routes a user request through policy, minimal dispatch, source recovery, final output, and optional local run records.

## Design Boundary

The protocol layer defines what think-tank means. Platform adapters define how think-tank runs in a specific environment. Modes define scenario defaults.

Platform-specific behavior must not redefine the core protocol.

`leader-runtime` is intentionally separate. It defines how a Codex-style main agent becomes a leader that can orchestrate expert pools and acceptance governance. `think-tank/` remains a reusable Skill core, not the entire leader operating layer.
