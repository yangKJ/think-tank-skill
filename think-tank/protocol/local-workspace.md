# Local Workspace Protocol

`think-tank/` is the portable Skill source. `.think-tank/` is the project-local
workspace created by a user project that runs think-tank.

The two directories must not be confused:

```text
think-tank/   # public Skill protocol, modes, adapters, examples
.think-tank/  # project-local instance data, usually ignored by Git
```

## Purpose

`.think-tank/` stores local configuration, provider policy, memory, run traces,
and artifacts for one project. It is not part of the open-source Skill core.

## Recommended Layout

```text
.think-tank/
├── config.yaml
├── provider-policy.yaml
├── memory/
│   ├── index.json
│   ├── architecture.md
│   ├── workflows.md
│   ├── conventions.md
│   ├── pitfalls.md
│   └── decisions.md
├── runs/
│   └── .gitkeep
├── artifacts/
│   └── .gitkeep
└── README.md
```

## Git Policy

Default policy:

```yaml
git_policy: ignored
```

Projects may choose to commit a sanitized `.think-tank/README.md` or example
configuration, but real memory, local provider preferences, run logs, and
artifacts should be treated as project-local data.

## Config Contract

`config.yaml` defines project-local behavior:

```yaml
version: 1
workspace:
  default_privacy: project_local
  default_memory_target: .think-tank/memory/
  write_requires_confirmation: true
policy:
  provider_policy: .think-tank/provider-policy.yaml
memory:
  enabled: true
  propose_only_by_default: true
  allowed_targets:
    - AGENTS.md
    - .think-tank/memory/
```

## Provider Policy Contract

`provider-policy.yaml` is the preferred local YAML policy path. It overlays the
bundled example policy without modifying the public Skill source. Local policy
must not erase the default research, council, review, and strategy routes unless
the user explicitly supplies a full replacement policy with `--policy`.

Recommended Codex load order:

```yaml
policy_load_order:
  - explicit --policy
  - think-tank/platforms/codex/provider-policy.example.yaml
  - .think-tank/provider-policy.yaml
```

Default behavior: load the bundled example first, then merge `.think-tank`
routes and defaults as project-local overrides.

No legacy project-local policy path is supported in 2.0. The local instance
policy belongs in `.think-tank/provider-policy.yaml`.

## Quality Gates

- Do not write private project memory into `think-tank/`.
- Do not commit `.think-tank/` by default.
- Do not treat provider selection as provider invocation.
- Do not store secrets, tokens, credentials, or closed-source implementation
  details in memory artifacts.
- Every memory item must carry scope, privacy, source evidence, and staleness
  risk.
