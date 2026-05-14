# Migration from Research Think Tank

旧 research agent 中的 think-tank 是新主仓的重要来源，但在新体系中 research 只是 think-tank 的一个 mode。

## 来源

```text
legacy research think-tank skill
```

完整 research agent 全仓来源另见：

```text
legacy research workspace
```

v0.3 完整处置记录：

```text
docs/research-agent-full-inventory.md
docs/v0.3-research-agent-migration.md
```

## 应保留的设计

### 触发边界

旧体系明确区分：

- 单人调研：不触发 think-tank
- 协作调研：触发多人调研和讨论
- 会议讨论：触发完整讨论
- 简单讨论：触发轻量讨论

新体系应保留这个边界，但将其写入 `protocol/mode-selection.md`，而不是写死在 Claude Code skill 配置里。

### capability slots

旧体系的能力槽：

```yaml
source_research
trend_analysis
synthesis
critic
```

新体系迁移为：

| 旧 slot | 新协议角色 |
|---------|------------|
| `source_research` | `collector` |
| `trend_analysis` | `domain_expert` |
| `synthesis` | `synthesizer` |
| `critic` | `skeptic` |

平台适配可以继续把这些角色映射到 Claude Code 的 `subagent_type`，但协议层不依赖具体 subagent 名称。

### 工作流

旧工作流迁移关系：

| 旧工作流 | 新 mode |
|----------|---------|
| `simple-discuss` | `council` 的轻量配置 |
| `full` | `council` 或 `strategy` 的完整配置 |
| `research-discuss` | `research` |

### 输出沉淀

旧体系将结论写入：

```text
.think-tank/conclusions/
```

新体系应保留“结论可沉淀”的思想，但沉淀路径属于平台适配，不属于协议层硬编码。

## 应修正的问题

### 不再把 research 当父级

旧路径位于：

```text
agents/research/.claude/skills/think-tank
```

新体系中：

```text
think-tank = 主 Skill
research = think-tank 的 mode
```

### 不混淆 mock、tracking 和真实执行

旧记忆中记录过：mock 路径可验证不等于真实 Claude Code Team 路径完成。

新体系必须保持能力状态标注：

- `verified`
- `mock`
- `tracking`
- `planned`

### 不把平台触发写成协议

旧 Claude Code 的 Slash Command、TeamCreate、SendMessage、TeamDelete 都属于平台适配。

协议层只保留：

- 触发语义
- 阶段顺序
- 角色职责
- 输出结构
- 质量门禁

## 迁移步骤

1. 将旧触发词归并到 `protocol/mode-selection.md`。
2. 将 capability slots 映射写入 `protocol/roles.md`。
3. 将 `research-discuss` 的流程强化到 `modes/research.md`。
4. 将 Claude Code Agent Team 环境变量、subagent 映射、结果回收写入 `platforms/claude-code/`。
5. 将旧结论样例筛选后放入 `examples/`，但不带项目私有上下文。

## v0.3 状态

```yaml
research_agent_migration: complete
agents_disposed: 7
skills_disposed: 25
knowledge_files_disposed: 35
core_protocol_dependency_on_old_research: none
```
