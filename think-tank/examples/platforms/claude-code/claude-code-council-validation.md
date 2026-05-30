# Claude Code Council Validation

本文件记录 Claude Code 平台对 think-tank `council mode` 的首轮 preflight 验证。

## 测试任务

```text
使用 think-tank council mode，讨论：think-tank 是否应该内置 yt-dlp、obsidian、playwright-cli、xiaohongshu 等技能，还是只通过 capability 槽位调度它们？
```

## 执行声明

```yaml
platform: claude-code
mode: council
execution_method: single_agent_multi_profile_simulation
selected_profiles:
  - facilitator
  - architect
  - skeptic
  - product-strategist
selected_capabilities:
  - browser-automation
  - media-processing
  - knowledge-persistence
capability_status:
  browser-automation: mock
  media-processing: mock
  knowledge-persistence: mock
verified:
  - skill_loaded
  - selected_mode_declared
  - selected_profiles_declared
  - selected_capabilities_declared
  - capability_status_declared
  - execution_method_declared
  - no_external_skill_overclaim
  - council_deliberation_structure
not_verified:
  - external_skill_invocation
  - true_multi_agent_execution
  - subagent_result_recovery
  - runtime_capability_fallback
status: verified_as_single_agent_council_preflight
```

## 结论

Claude Code 可以使用新 think-tank 入口执行 `council mode`，并以单 agent 多 profile 模拟方式完成多观点审议。

本次验证可标记为 `verified_as_single_agent_council_preflight`，不能标记为真实多 agent runtime verified。

## 验证依据

Claude Code 输出显示：

- `Skill(think-tank)` 成功加载。
- 显式列出 `selected_mode: council`。
- 显式列出 profiles、capabilities、capability_status、execution_method。
- 明确 capability 状态为 `mock`，没有声称外部 skill 已真实调用。
- 输出包含共识、角色观点、分歧与风险、行动建议、边界和结论。
- 结论保持主协议边界：think-tank 编排外部 skills，但不拥有它们。

## 通过项

```yaml
pass:
  skill_entrypoint: true
  council_mode: true
  explicit_execution_declaration: true
  multi_profile_discussion: true
  disagreement_and_adjudication: true
  boundary_declaration: true
  no_external_skill_overclaim: true
```

## 缺口

```yaml
gaps:
  true_subagent_dispatch: not_tested
  result_recovery_contract: not_tested
  external_skill_invocation: not_tested
  runtime_skill_availability_detection: not_implemented
```

## 分歧与裁决

```yaml
consensus:
  - think-tank 不应内置外部工具型 skills
  - capabilities 应作为能力槽，由 platform adapter 映射到当前可用工具
  - 外部 skill 不可用时必须走降级策略并声明边界

main_disagreement:
  architect: capability 槽位保护跨平台可移植性和协议边界
  skeptic: capability-only 设计如果没有 adapter 端到端验证，容易成为空壳

adjudication:
  decision: 维持 capability 槽位模式
  condition: 必须补 platform adapter 端到端验证和 skill 可用性预检
```

## 行动建议

1. 将本次 council preflight 记为 `verified_as_single_agent_council_preflight`。
2. 不把它标记为真实 Claude Code multi-agent verified。
3. 下一阶段验证 Claude Code adapter 是否能真实发现和调用外部 skills。
4. 若继续验证，应优先选择低风险 `browser-automation` 或 `source-acquisition` 路径，而不是直接测试 xiaohongshu、yt-dlp 或 Obsidian。

## 边界

本次验证基于用户粘贴的 Claude Code 输出归档；Codex 没有直接运行 Claude Code，也没有回收 Claude Code 内部日志。

本次没有真实创建 Claude Code subagent 团队，没有真实调用 `yt-dlp`、`obsidian`、`playwright-cli` 或 `xiaohongshu`。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

