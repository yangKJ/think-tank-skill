# Research Trigger Migration

本文记录旧 research agent 触发词和组合技能如何迁移到新的 think-tank 主体系。

更通用的平台无关触发路由已经提升到：

```text
protocol/intent-routing.md
recipes/
```

本文只保留旧 research agent 迁移解释，不作为新的唯一真相源。

## 已吸收的旧能力

旧 research agent 的能力可以分成四类：

1. 身份规则：研究员负责外部资料、竞品、行业、市场、新技术调研。
2. 触发词：快速了解、研究一下、深度研究、竞品分析、舆情分析、持续监控、开会讨论。
3. 组合技能：`web-access`、`summarize`、`omni-research`、`xiaohongshu`、`yt-dlp`、`whisper`、`obsidian` 等组合。
4. 专业 subagent：source collector、trend analyst、social listener、feedback synthesizer、report architect、skeptic 等角色。

迁移后的归属：

```yaml
research_agent_identity: replaced_by_think_tank_research_mode
trigger_words: platforms/codex/trigger-routing.md
generic_intents: protocol/intent-routing.md
task_recipes: recipes/
tool_combinations: peer_skills_under_.codex/skills
legacy_competitive_orchestrator: replaced_by_yaml_provider_policy
specialist_roles: think-tank/profiles
subagent_runtime_contract: think-tank/protocol/subagent-runtime-contract.md
private_domain_knowledge: excluded_from_core
```

## 用户以后怎么说

### 轻量研究

```text
研究一下 [主题]，先给我快速结论、依据、风险和下一步。
```

### 深度研究

```text
深度研究 [主题]。
按旧 research agent 的深度研究逻辑，但用新的 think-tank 架构执行：
先说明 mode、profiles、capabilities、候选同级 skills，再输出结论、依据、分歧、风险和行动建议。
```

### 竞品分析

```text
竞品分析 [产品/公司/功能]。
重点看新技术、用户反馈、可借鉴策略、对我项目的优先级建议。
```

### 舆情分析

```text
分析小红书/社媒上关于 [主题] 的用户反馈。
如果没有真实调用 xiaohongshu，就用我提供的样本或本地材料，并明确标注 not_verified。
```

### 会议讨论

```text
开会讨论 [议题]。
让 source-collector、trend-analyst、skeptic、product-strategist、report-architect 分别给观点，最后汇总裁决。
```

### 持续监控

```text
帮我设计一个 [主题] 的持续监控方案。
先不要创建自动化，先输出监控指标、来源、频率、风险和触发条件。
```

### 项目记忆候选

```text
用 think-tank 生成项目记忆候选：[要沉淀的经验]
think-tank memory candidate: [lesson]
```

不要在公开默认 policy 中使用 `记下来` 这类通用触发词。它可能属于 Codex、
Claude Code 或用户自己的平台级记忆系统。think-tank 的默认语义只负责生成
项目本地 memory candidate，不表示写入平台长期记忆。

## Codex 执行要求

每次触发旧 research agent 风格任务时，Codex 必须先输出或内部形成：

```yaml
selected_mode:
selected_profiles:
selected_capabilities:
candidate_peer_skills:
execution_method:
capability_status:
boundaries:
```

如果调用同级 skill，必须区分：

- `installed`：文件存在。
- `selected`：本次路由选择。
- `invoked`：本次真实调用。
- `verified`：调用成功并回收结构化结果。

## 迁移判断

```yaml
old_trigger_words_migrated: documented
old_skill_combinations_migrated: mapped_to_peer_skills
legacy_competitive_orchestrator: replaced_by_policy_route
old_research_agent_required: false
external_peer_skills_are_optional: true
think_tank_core_depends_on_peer_skills: false
real_external_execution: per_skill_validation_required
```

这意味着：旧 research agent 的触发体验已经可以迁移；但每个外部工具 skill 的真实执行能力仍按单次任务验证，不能一次性泛化为全量 verified。
