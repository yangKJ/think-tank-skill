# Agent Council Full Inventory

本文逐项记录旧 agent-council 的资产分类和迁移去向。

来源：

```text
/Users/condy/Desktop/ios-automation-mcp/.claude/skills/agent-council
```

## 目录级处置

| 旧目录或文件 | 当前处置 | 新位置 |
|--------------|----------|--------|
| `SKILL.md` | 协议和 mode 来源 | `modes/council.md`、`docs/migration-from-agent-council.md` |
| `references/agents.md` | 动态角色选择和 Feedback Synthesizer 来源 | `protocol/agent-selection.md`、`profiles/`、`templates/expert-meeting.md` |
| `references/scenes.md` | 场景到角色映射来源 | `protocol/agent-selection.md`、`modes/council.md` |
| `references/steps.md` | collect/discuss/conclude 流程来源 | `runtime/council.py`、`protocol/state-result-contract.md` |
| `references/format.md` | 讨论文档格式来源 | `templates/expert-meeting.md` |
| `references/state_contract.md` | 状态机、安全和恢复来源 | `docs/agent-council-runtime-migration.md` |
| `scripts/state_manager.py` | 状态转换、安全签名经验 | `runtime/council.py`、`docs/agent-council-runtime-migration.md` |
| `scripts/state/atomic_writer.py` | 原子写入经验 | adapter responsibility，记录在 runtime migration |
| `scripts/state/circuit_breaker.py` | 熔断降级经验 | adapter/runtime reliability policy |
| `scripts/coordinator/round_coordinator.py` | 轮次策略来源 | `runtime/council.py` |
| `scripts/research/*.py` | 多 Agent 调研子系统来源 | `modes/research.md`、`templates/evidence-table.md`、`protocol/consensus-contract.md` |
| `scripts/registry/agent_registry.py` | 角色注册经验 | `protocol/agent-selection.md` |
| `scripts/observability/observer.py` | 可观测性经验 | adapter responsibility |
| `scripts/discussion.sh`、`scripts/merge.sh`、`scripts/monitor.sh` | Claude Code 文件流辅助 | 不进入 core |
| `history/*` | 历史样例和测试结果 | `docs/agent-council-history-index.md` |
| `.DS_Store`、`__pycache__`、`.pytest_cache` | 缓存 | 不迁移 |

## 关键设计迁移

| 旧设计 | 新抽象 | 状态 |
|--------|--------|------|
| 主 Agent 纯主持人 | `modes/council.md` 主持人原则 | migrated |
| 场景驱动选择 2-3 个 Agent | `protocol/agent-selection.md` | migrated |
| collect -> discuss -> conclude -> complete | `runtime/council.py` 和主协议阶段 | migrated |
| L1/L2/L3 共识、调和、裁决 | `runtime/consensus.py`、`protocol/consensus-contract.md` | migrated |
| Feedback Synthesizer | `templates/expert-meeting.md`、profiles synthesizer 类角色 | migrated |
| state_hash / nonce / heartbeat / expiry | `state-result-contract.md` 和 runtime migration 文档 | migrated_as_contract |
| HMAC / manifest / chmod 700/600 | Claude Code adapter 安全经验 | documented_only |
| atomic writer / circuit breaker | runtime reliability policy | documented_only |
| research findings / conflicts / aggregation | research mode 和 evidence table | migrated |

## 状态

```yaml
references_disposed: 5
top_level_discussion_files_disposed: 4
history_items_disposed: true
scripts_disposed: true
runtime_helpers_added: true
agent_council_migration_status: complete
```
