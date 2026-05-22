# think-tank-skill

**Language:** English | [中文](README_CN.md)

Stable, protocol-first home of **think-tank**: a cross-platform high-level Skill for research, review, council, and strategy workflows on a verified Codex-first runtime path.

![think-tank hero](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/think-tank-hero-image2.png)

The high-level Skill lives in [`think-tank/`](think-tank/).
The leader orchestration layer is being split into a standalone sibling project on the Desktop.

## Why use think-tank?

- One protocol surface for research, review, council, and strategy work.
- A clear split between orchestration and tools:
  `think-tank = task understanding + role organization + capability routing + evidence synthesis + boundary declaration`.
- Explicit evidence states: `verified`, `verified_partial`, `planned`, `blocked`.
- Public release gates that check protocol integrity, privacy boundaries, package scope, and stable posture.

## Quick Start

1. Pick your install path:

- Codex install:

```bash
python3 "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" --repo yangKJ/think-tank-skill --path think-tank
```

- Manual install:

```text
think-tank/
```

Copy it into your platform's skill directory, or clone this repository and reference `think-tank/` directly.

2. Restart your agent runtime after installation.

For Codex, restart the app or session so the new skill can be discovered.

3. Run the first-install check:

```bash
test -f "$HOME/.codex/skills/think-tank/SKILL.md" && echo "think-tank installed"
```

4. Try one of the public templates:

```text
think-tank/examples/public/research-request.md
think-tank/examples/public/council-decision.md
think-tank/examples/public/review-acceptance.md
```

5. Read [`think-tank/README.md`](think-tank/README.md) and [`think-tank/docs/open-source-quickstart.md`](think-tank/docs/open-source-quickstart.md) for the protocol surface and runtime boundaries.

Continue with the user-operation path:

- [`think-tank/docs/first-run-guide.md`](think-tank/docs/first-run-guide.md)
- [`think-tank/docs/operator-manual.md`](think-tank/docs/operator-manual.md)
- [`think-tank/docs/cookbook.md`](think-tank/docs/cookbook.md)
- [`think-tank/docs/progression-guide.md`](think-tank/docs/progression-guide.md)

6. Run the public release gate:

```bash
python3 checks/open_source_release_suite.py
```

7. Run the stable gate:

```bash
python3 checks/stable_release_check.py
```

If both pass, you are on the repository's current stable public path.

## First-Install Expectations

What you get immediately after installing `think-tank`:

- protocol-first research, review, council, and strategy workflows
- mode selection, profile simulation, and structured output
- local file analysis and user-provided material analysis
- explicit boundary declaration through evidence states

What you should not expect from a fresh install:

- every optional peer skill to be present automatically
- browser, social, media, or knowledge-base providers to be pre-authorized
- full multi-agent runtime parity across platforms
- "installed" to mean "already invoked and verified"

## Platform Install Targets

| Platform | Install target | Post-install action |
|---|---|---|
| Codex | `~/.codex/skills/think-tank` | Restart Codex or the current session |
| Claude Code | `~/.claude/skills/think-tank/` | Restart Claude Code session |
| Other runtimes | Your runtime's skill directory | Re-index or restart that runtime |

## First-Install Validation

Use this shortest path when validating a first install:

1. Confirm the entry file exists.
2. Restart the runtime.
3. Send a small prompt that should trigger research, review, or strategy behavior.
4. Check that the response uses `think-tank` style boundary-aware structure rather than generic freeform output.

Minimal file check for Codex:

```bash
test -f "$HOME/.codex/skills/think-tank/SKILL.md" && echo "think-tank installed"
```

Suggested first prompt:

```text
Use think-tank to review these notes, separate facts from assumptions, and give me a boundary-aware recommendation.
```

## Troubleshooting First Install

- If the install script fails with HTTPS certificate errors, use a manual `git clone` or zip download path and copy only `think-tank/`.
- If the destination already exists, remove or rename the old `~/.codex/skills/think-tank` directory before reinstalling.
- If the runtime does not recognize the skill, restart the app or session before debugging deeper.
- Do not copy `.think-tank/`, `.codex/`, `.claude/`, or generated output folders into the public skill directory.

## Use Cases

| Research | Council | Review |
|---|---|---|
| ![research scenario](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/research-card-image2.png) | ![council scenario](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/council-card-image2.png) | ![review scenario](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/review-card-image2.png) |

## Provider Ecosystem Patterns

`think-tank` does not bundle concrete tools. It documents provider integration patterns and routes capability slots to optional peer skills only when the current platform exposes them and the task has permission to use them.

![provider ecosystem](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/provider-ecosystem-image2.png)

Representative peer skill pattern examples:

| capability slot | example peer skills | status boundary |
|---|---|---|
| source-acquisition | `web-access`, `agent-reach` | pattern documented, evidence required |
| browser-automation | `browser`, `playwright-cli` | verified_partial for readonly paths |
| social-listening | `xiaohongshu` | pattern documented, login and permission required |
| media-processing | `yt-dlp`, `openai-whisper` | pattern documented, rights and permission required |
| knowledge-persistence | `obsidian` | pattern documented, private write confirmation required |
| media-production | `research-to-video-production` | verified_partial, scoped production workflow |

See [`think-tank/docs/provider-ecosystem-examples.md`](think-tank/docs/provider-ecosystem-examples.md) and [`think-tank/docs/provider-integration-patterns.md`](think-tank/docs/provider-integration-patterns.md).

## Research OS And Memory Runtime

The **Research OS + Memory Runtime** layer helps repeatable research work produce run records, memory candidates, provider ledgers, handoffs, guardrails, and eval fixtures.

![Research OS and Memory Runtime](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/research-os-memory-runtime-image2.png)

- **Run Record:** [`think-tank/protocol/run-record.md`](think-tank/protocol/run-record.md)
- **Project Memory Runtime:** [`think-tank/protocol/project-memory-runtime.md`](think-tank/protocol/project-memory-runtime.md)
- **Provider Invocation Ledger:** [`think-tank/protocol/provider-invocation-ledger.md`](think-tank/protocol/provider-invocation-ledger.md)
- **Handoff Protocol:** [`think-tank/protocol/handoff-protocol.md`](think-tank/protocol/handoff-protocol.md)
- **Guardrails:** [`think-tank/protocol/guardrails.md`](think-tank/protocol/guardrails.md)
- **Research OS:** [`think-tank/protocol/research-os.md`](think-tank/protocol/research-os.md)
- **Eval Pack:** [`think-tank/protocol/eval-pack.md`](think-tank/protocol/eval-pack.md)

## Open Source Usability

- **Contributor docs:** [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md), [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), [`SUPPORT.md`](SUPPORT.md), issue templates, and PR template.
- **Research OS Starter Kit:** [`think-tank/templates/research-workspace/`](think-tank/templates/research-workspace/).
- **Eval Pack Starter:** [`think-tank/evals/`](think-tank/evals/).
- **Provider Test Matrix:** [`think-tank/docs/provider-test-matrix.md`](think-tank/docs/provider-test-matrix.md).
- **Docs Site:** [`think-tank/docs/index.md`](think-tank/docs/index.md), concepts, guides, reference, and release sections.
- **Platform Distribution:** [`think-tank/docs/platform-publishing.md`](think-tank/docs/platform-publishing.md), [`think-tank/docs/codex-installation.md`](think-tank/docs/codex-installation.md), and [`think-tank/docs/claude-code-installation.md`](think-tank/docs/claude-code-installation.md).

## Skill Experience Layer

The **Skill Experience Layer** helps agents decide when to use
`think-tank`, form a clear invocation contract, load references progressively,
compose optional peer skills safely, and self-test common boundaries.

Trigger words are not built into the public core. They belong in user-owned YAML
policy; `think-tank` documents intent categories and routing contracts.

- **Skill Trigger Intelligence:** [`think-tank/protocol/skill-trigger-intelligence.md`](think-tank/protocol/skill-trigger-intelligence.md)
- **Skill Invocation Contract:** [`think-tank/protocol/skill-invocation-contract.md`](think-tank/protocol/skill-invocation-contract.md)
- **Progressive Disclosure:** [`think-tank/protocol/progressive-disclosure.md`](think-tank/protocol/progressive-disclosure.md)
- **Agent Compatibility Matrix:** [`think-tank/docs/agent-compatibility-matrix.md`](think-tank/docs/agent-compatibility-matrix.md)
- **Skill Composition Guide:** [`think-tank/docs/skill-composition-guide.md`](think-tank/docs/skill-composition-guide.md)
- **Skill Quality Score:** [`think-tank/docs/skill-quality-score.md`](think-tank/docs/skill-quality-score.md)
- **Skill Experience Examples:** [`think-tank/examples/v3/`](think-tank/examples/v3/)
- **Skill Self Tests:** [`think-tank/self-tests/`](think-tank/self-tests/)

Version history lives in [`CHANGELOG.md`](CHANGELOG.md).

## User Operation Path

- **First Run Guide:** [`think-tank/docs/first-run-guide.md`](think-tank/docs/first-run-guide.md)
- **Operator Manual:** [`think-tank/docs/operator-manual.md`](think-tank/docs/operator-manual.md)
- **Cookbook:** [`think-tank/docs/cookbook.md`](think-tank/docs/cookbook.md)
- **Progression Guide:** [`think-tank/docs/progression-guide.md`](think-tank/docs/progression-guide.md)

| First Run Guide | Progression Guide |
|:---:|:---:|
| [![First Run Guide](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/first-run-guide-image2.png)](think-tank/docs/first-run-guide.md) | [![Progression Guide](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/progression-guide-image2.png)](think-tank/docs/progression-guide.md) |
| Cookbook | Operator Manual |
| [![Cookbook](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/cookbook-image2.png)](think-tank/docs/cookbook.md) | [![Operator Manual](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/operator-manual-image2.png)](think-tank/docs/operator-manual.md) |

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
│   ├── self-tests/
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
- [`think-tank/self-tests/`](think-tank/self-tests/): Public skill experience self-test fixtures.
- [`think-tank/domain-packs/`](think-tank/domain-packs/): Optional domain packs.
- [`think-tank/schemas/`](think-tank/schemas/): Machine-readable input and output schemas.
- [`think-tank/examples/`](think-tank/examples/): Reusable examples that demonstrate the protocol.

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
- [`think-tank/docs/provider-ecosystem-examples.md`](think-tank/docs/provider-ecosystem-examples.md)
- [`think-tank/docs/provider-integration-patterns.md`](think-tank/docs/provider-integration-patterns.md)
- [`think-tank/docs/codex-installation.md`](think-tank/docs/codex-installation.md)
- [`think-tank/docs/claude-code-installation.md`](think-tank/docs/claude-code-installation.md)
- [`think-tank/docs/platform-publishing.md`](think-tank/docs/platform-publishing.md)
- [`think-tank/docs/index.md`](think-tank/docs/index.md)
- [`think-tank/docs/faq.md`](think-tank/docs/faq.md)
- [`think-tank/docs/troubleshooting.md`](think-tank/docs/troubleshooting.md)
  - [`think-tank/docs/provider-test-matrix.md`](think-tank/docs/provider-test-matrix.md)
  - [`think-tank/docs/open-source-release.md`](think-tank/docs/open-source-release.md)
- Stable release references:
  - [`think-tank/docs/stable-release-criteria.md`](think-tank/docs/stable-release-criteria.md)
  - [`think-tank/docs/stable-readiness-matrix.md`](think-tank/docs/stable-readiness-matrix.md)
  - [`think-tank/docs/stable-release-checklist.md`](think-tank/docs/stable-release-checklist.md)
  - [`think-tank/docs/release-tagging.md`](think-tank/docs/release-tagging.md)
- Codex runtime references:
  - [`think-tank/docs/codex-validation-report.md`](think-tank/docs/codex-validation-report.md)
  - [`think-tank/docs/codex-acceptance.md`](think-tank/docs/codex-acceptance.md)
  - [`think-tank/docs/codex-readiness-matrix.md`](think-tank/docs/codex-readiness-matrix.md)
  - [`think-tank/platforms/codex/operating-guide.md`](think-tank/platforms/codex/operating-guide.md)
  - [`think-tank/platforms/codex/capability-status.md`](think-tank/platforms/codex/capability-status.md)
- Protocol and governance references:
  - [`public-release-manifest.yaml`](public-release-manifest.yaml)
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

Generate platform distribution artifacts:

```bash
python3 scripts/package_agent_distributions.py
```

Version history and release packaging references:

```text
CHANGELOG.md
think-tank/docs/release-tagging.md
```

## Design Boundary

The protocol layer defines what think-tank means. Platform adapters define how think-tank runs in a specific environment. Modes define scenario defaults.

Platform-specific behavior must not redefine the core protocol.

`leader-runtime` is intentionally separate. It defines how a Codex-style main agent becomes a leader that can orchestrate expert pools and acceptance governance. `think-tank/` remains a reusable Skill core, not the entire leader operating layer.
