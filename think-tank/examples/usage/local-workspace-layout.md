# Local Workspace Layout Example

This example shows where a project should keep local think-tank instance data.

```text
project-root/
├── think-tank/              # optional vendored or symlinked Skill source
├── .codex/skills/think-tank # optional Codex install entry
└── .think-tank/
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
    └── artifacts/
```

`.think-tank/` is usually ignored by Git. It belongs to the project instance,
not to the public Skill core.

