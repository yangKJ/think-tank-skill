# Agent Council Runtime Migration

本文记录旧 agent-council runtime 工程经验如何进入当前 think-tank。

## 来源

- `references/state_contract.md`
- `references/steps.md`
- `scripts/state_manager.py`
- `scripts/state/atomic_writer.py`
- `scripts/state/circuit_breaker.py`
- `scripts/coordinator/round_coordinator.py`
- `scripts/research/*.py`

## 当前落点

```text
runtime/council.py
protocol/state-result-contract.md
protocol/consensus-contract.md
platforms/claude-code/legacy-team-runtime.md
```

## 状态机

旧阶段：

```text
collect -> discuss -> conclude -> complete
```

新映射：

| agent-council | think-tank protocol |
|---------------|---------------------|
| collect | collection |
| discuss | deliberation |
| conclude | synthesis + recommendation |
| complete | quality_check |

`runtime/council.py` 提供平台无关状态 helper；文件锁、HMAC、manifest 和权限属于 adapter 实现。

## 安全和可靠性迁移

| 旧机制 | 新处置 |
|--------|--------|
| dynamic nonce | state-result contract 的 adapter 可选完整性字段 |
| state_hash | adapter 可选完整性校验 |
| HMAC signature | Claude Code adapter 安全经验，不是 core 必需 |
| chmod 700/600 | 平台文件系统策略 |
| atomic writer | adapter 实现要求 |
| heartbeat | state-result contract 可选 heartbeat |
| retry / skipped agents | adapter reliability policy |
| circuit breaker | adapter reliability policy |
| checkpoint recovery | recovery contract |

## Research 子系统迁移

旧 `scripts/research/*` 的价值：

- Finding schema
- Task queue
- Result store
- Conflict resolver
- Aggregator
- Router
- Coordinator

新位置：

- Finding schema -> `templates/evidence-table.md` 和 `protocol/state-result-contract.md`
- Conflict resolver -> `protocol/consensus-contract.md`
- Aggregator -> `templates/expert-meeting.md`
- Router -> `protocol/agent-selection.md`
- Task queue / Result store -> adapter responsibility

## 状态

```yaml
council_runtime_helpers: implemented
agent_council_state_machine: abstracted
hmac_manifest_runtime: documented_only
atomic_file_runtime: documented_only
circuit_breaker_runtime: documented_only
full_claude_code_team_runtime_verified: false
```

