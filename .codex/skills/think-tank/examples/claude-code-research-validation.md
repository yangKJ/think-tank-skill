# Claude Code Research Validation

本文件记录 Claude Code 平台对 think-tank `research mode` 的首轮 preflight 验证。

## 测试任务

```text
/think-tank research mode，研究一个跨平台 Skill 应如何在只有核心协议、没有外部工具时保持可用，并输出结论、依据、风险和行动建议。
```

## 执行声明

```yaml
platform: claude-code
mode: research
execution_method: claude_code_single_agent_skill_execution
source_material:
  - think-tank protocol files
  - think-tank architecture files
  - think-tank capabilities files
external_skills_invoked: false
subagents_invoked: false
status: verified_with_format_gap
verified:
  - skill_entrypoint_triggered
  - local_protocol_files_read
  - research_mode_semantics_followed
  - conclusion_evidence_risks_actions_boundaries_output
  - no_external_tool_overclaim
not_verified:
  - true_subagent_dispatch
  - structured_profile_result_recovery
  - external_skill_invocation
  - full_status_yaml_output
format_gaps:
  - 未显式列出 selected profiles
  - 未显式列出 selected capabilities 的状态
  - 未输出统一 execution declaration YAML
```

## 结论

Claude Code 可以通过新的 think-tank 入口执行 `research mode`，并基于本地协议文件完成一次无外部工具的研究报告。

本次可标记为 `verified_with_format_gap`，不能标记为完整 Claude Code runtime verified。

## 验证依据

Claude Code 输出显示：

- 已读取 6 个文件和 2 个目录。
- 结论聚焦 `capability slot + 降级策略 + 平台 adapter`。
- 依据来自 `think-tank-protocol.md`、`architecture.md`、capability 降级策略和 platforms adapter 职责。
- 输出包含结论、依据、风险、行动建议和边界。
- 明确说明部分内容未验证，未把外部工具或多 agent runtime 说成已完成。

## 通过项

```yaml
pass:
  skill_entrypoint: true
  protocol_as_source: true
  research_mode: true
  boundary_declaration: true
  no_old_research_parent_claim: true
  no_external_skill_overclaim: true
```

## 缺口

```yaml
gaps:
  profile_selection_explicit: missing
  capability_status_explicit: partial
  result_recovery_contract: not_applicable_single_agent
  subagent_execution: not_tested
```

## 判断

这次验证证明：

- 新 think-tank 可以作为 Claude Code skill 入口被调用。
- research mode 可以不依赖旧 research agent 父级体系执行。
- 仅核心协议、无外部工具时，think-tank 仍能输出可用研究结论。

这次没有证明：

- Claude Code subagent 调度可用。
- `.claude/agents` profile 映射可用。
- `.claude/skills` capability 映射可用。
- 多角色结果可真实回收。

## 行动建议

1. 将本次 research preflight 记为 `verified_with_format_gap`。
2. 下一次 Claude Code 输出应强制包含：

```yaml
selected_mode: ""
selected_profiles: []
selected_capabilities: []
capability_status: {}
execution_method: ""
verified: []
not_verified: []
```

3. 继续执行 `council mode` preflight。
4. council preflight 通过后，再更新 Claude Code 总验证状态。

## 边界

本次验证基于用户粘贴的 Claude Code 输出归档；Codex 没有直接运行 Claude Code，也没有回收 Claude Code 的内部执行日志。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

