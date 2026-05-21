# Agent Compatibility Matrix

This matrix explains how `think-tank` degrades across Codex, Claude Code, and
generic agent environments.

It describes expected skill experience, not a guarantee that every provider is
installed or invoked.

| capability | Codex | Claude Code | Generic Agent | boundary |
|---|---|---|---|---|
| Skill entrypoint | `SKILL.md` supported | `SKILL.md` supported | manual copy or prompt reference | platform loading differs |
| Progressive disclosure | supported by file reads | supported by file reads | manual or tool-dependent | agent must avoid loading everything |
| User YAML policy | supported when local files are readable | supported when local files are readable | optional | trigger words are user-owned |
| Shell checks | available with permission model | available with permission model | optional | commands may be blocked |
| Browser automation | available when browser tools are enabled | platform/tool dependent | optional | readonly and login boundaries apply |
| MCP or peer tools | tool-dependent | tool-dependent | optional | selection is not invocation |
| Subagents | available in some Codex contexts | platform-dependent | usually unavailable | fallback must be disclosed |
| Memory runtime | file-based protocol | file-based protocol | manual artifact | private workspace is not public core |
| Image/video skills | optional peer skills | optional peer skills | optional | rights and provider access required |
| Long-running runs | platform-dependent | platform-dependent | manual | do not claim full lifecycle by default |

## Recommended Defaults

### Codex

Use Codex as the current primary verified path, but still disclose:

```yaml
execution_method:
provider_invoked:
true_multi_agent_runtime:
evidence_state:
```

### Claude Code

Use the same protocol and adapter structure, but keep runtime parity claims
conservative unless the specific adapter path is verified.

### Generic Agent

Use `think-tank` as a protocol and output contract. If no filesystem, shell, or
provider tools are available, run in `protocol_only` mode.

## Compatibility Rule

Every platform must preserve the same core distinction:

```text
intent inference != trigger policy
route selection != provider invocation
single-context profiles != true multi-agent runtime
example fixture != verified execution
```
