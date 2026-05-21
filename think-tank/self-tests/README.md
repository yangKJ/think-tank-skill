# Skill Self Tests

`self-tests/` contains public fixtures that help agents and maintainers check
whether `think-tank` is being invoked with the right boundaries.

These are not hidden runtime runs. They are small, reviewable fixtures for
trigger decisions, anti-trigger decisions, provider boundaries, composition,
and memory/runtime routing.

## Cases

- `research-trigger.json`: a complex research task should use `think-tank`.
- `anti-trigger-simple-command.json`: a simple command should not use
  `think-tank`.
- `provider-boundary.json`: provider selection must not be described as
  invocation.
- `run-record-memory.json`: persistent records require explicit write intent.
- `composition-guide.json`: `think-tank` coordinates; peer skills execute.

## Boundary

Self-test fixtures prove expected decision structure. They do not prove that a
provider exists, is authorized, or was invoked.
