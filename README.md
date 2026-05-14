# think-tank-skill

think-tank-skill is the main repository for **think-tank**, a cross-platform reusable Skill for multi-role information gathering, collaborative analysis, deliberation, synthesis, and actionable recommendations.

The Skill itself lives in [`think-tank/`](think-tank/).

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
└── think-tank/
    ├── SKILL.md
    ├── README.md
    ├── protocol/
    ├── capabilities/
    ├── profiles/
    ├── platforms/
    ├── modes/
    ├── templates/
    ├── runtime/
    ├── domain-packs/
    ├── docs/
    └── examples/
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

## Protocol Core

- [`think-tank/protocol/think-tank-protocol.md`](think-tank/protocol/think-tank-protocol.md): Core workflow.
- [`think-tank/protocol/roles.md`](think-tank/protocol/roles.md): Role selection and responsibilities.
- [`think-tank/protocol/agent-selection.md`](think-tank/protocol/agent-selection.md): Scenario-driven agent selection.
- [`think-tank/protocol/mode-selection.md`](think-tank/protocol/mode-selection.md): Mode selection rules.
- [`think-tank/protocol/quality-gates.md`](think-tank/protocol/quality-gates.md): Quality gates.
- [`think-tank/protocol/versioning.md`](think-tank/protocol/versioning.md): Protocol versioning.

## Current Status

This repository is in the early foundation stage.

The first goal is to stabilize the structure and protocol before migrating older research think-tank or agent-council assets into the new system.

Readiness status:

- [`think-tank/docs/v0.1-readiness.md`](think-tank/docs/v0.1-readiness.md)
- [`think-tank/docs/codex-validation-report.md`](think-tank/docs/codex-validation-report.md)
- [`think-tank/docs/codex-acceptance.md`](think-tank/docs/codex-acceptance.md)
- [`think-tank/docs/codex-readiness-matrix.md`](think-tank/docs/codex-readiness-matrix.md)
- [`think-tank/platforms/codex/operating-guide.md`](think-tank/platforms/codex/operating-guide.md)
- [`think-tank/platforms/codex/capability-status.md`](think-tank/platforms/codex/capability-status.md)
- [`think-tank/examples/codex-smoke-research.md`](think-tank/examples/codex-smoke-research.md)

## Validation

Run:

```bash
python3 checks/protocol_check.py
python3 checks/codex_validation_check.py
python3 checks/claude_code_validation_check.py
python3 checks/claude_dispatch_sample_check.py
python3 checks/claude_runtime_sample_check.py
python3 checks/minimal_runtime_execution_check.py
python3 checks/capability_queue_check.py
python3 checks/schema_sample_check.py
python3 checks/runtime_contract_check.py
python3 checks/slot_contract_check.py
python3 checks/consensus_contract_check.py
python3 checks/research_protocol_check.py
python3 checks/runtime_planner_check.py
python3 checks/slot_resolver_check.py
python3 checks/state_model_check.py
python3 checks/consensus_runtime_check.py
python3 checks/runtime_result_schema_check.py
python3 checks/codex_runtime_pipeline_check.py
python3 checks/claude_runtime_pipeline_spec_check.py
python3 checks/runtime_e2e_fixture_check.py
python3 checks/runtime_safety_check.py
python3 checks/template_check.py
python3 checks/legacy_think_tank_migration_check.py
python3 checks/research_agent_full_migration_check.py
python3 checks/agent_council_full_migration_check.py
python3 checks/council_runtime_check.py
python3 checks/subagent_runtime_check.py
python3 checks/role_result_schema_check.py
python3 checks/specialist_runtime_contract_check.py
python3 checks/codex_installed_skill_check.py
python3 checks/codex_external_skills_check.py
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
- Current local Codex installation is validated via `checks/codex_installed_skill_check.py`.
- Legacy research external skills are installed as peer Codex skills and checked via `checks/codex_external_skills_check.py`.
- Codex provider invocation matrix is established; selected peer skills still require per-provider invocation validation before they can be called verified.

## Design Boundary

The protocol layer defines what think-tank means. Platform adapters define how think-tank runs in a specific environment. Modes define scenario defaults.

Platform-specific behavior must not redefine the core protocol.
