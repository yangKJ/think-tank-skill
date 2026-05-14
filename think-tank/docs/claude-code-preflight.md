# Claude Code Preflight

本文定义把 think-tank 切到 Claude Code 平台验证前必须确认的事项。

目标不是把旧 research agent 或 agent-council 原样搬进来，而是验证 Claude Code 能否作为 think-tank 的一个平台适配层执行主协议。

## 验证原则

```yaml
platform: claude-code
protocol_source: think-tank/protocol
allowed_source_material:
  - old_research_agent
  - old_agent_council
not_allowed_as_protocol_source:
  - old_research_parent_structure
  - old_agent_council_independent_protocol
  - platform_specific_state_files
```

Claude Code 验证必须证明：

1. 能触发 think-tank，而不是触发旧 research 子技能。
2. 能按 `modes/` 选择 research 或 council。
3. 能按 `profiles/` 选择角色。
4. 能按 `capabilities/` 调用或降级外部 skills。
5. 能回收角色结果。
6. 能输出结论、依据、分歧、风险、行动建议和边界。

## Preflight Checklist

### 1. 入口检查

```yaml
check: skill_entrypoint
required:
  - Claude Code 能读取 think-tank/SKILL.md
  - 入口文案把 think-tank 定义为主 Skill
  - 不要求用户先进入 research agent
pass_condition: 用户用 think-tank 指令即可触发协议流程
fail_condition: 必须依赖旧 research agent 作为父级入口
```

### 2. Research Mode 检查

首个 Claude Code research 验证任务建议使用：

```text
使用 think-tank research mode，研究一个跨平台 Skill 应如何在只有核心协议、没有外部工具时保持可用，并输出结论、依据、风险和行动建议。
```

要求：

```yaml
mode: research
profiles:
  required:
    - source-collector
    - skeptic
    - report-architect
  optional:
    - trend-analyst
    - product-strategist
capabilities:
  required:
    - source-acquisition
  optional:
    - browser-automation
    - knowledge-persistence
pass_condition:
  - 输出结构符合协议
  - 能说明哪些来源来自本地、哪些外部能力不可用
  - 不把未调用的外部 skill 写成已验证
```

### 3. Council Mode 检查

首个 Claude Code council 验证任务建议使用：

```text
使用 think-tank council mode，讨论：think-tank 是否应该内置 yt-dlp、obsidian、playwright-cli、xiaohongshu 等技能，还是只通过 capability 槽位调度它们？
```

要求：

```yaml
mode: council
profiles:
  required:
    - facilitator
    - product-strategist
    - skeptic
    - report-architect
  optional:
    - source-collector
    - social-listener
capabilities:
  optional:
    - media-processing
    - social-listening
    - browser-automation
    - knowledge-persistence
pass_condition:
  - 至少形成两种不同观点
  - 明确共识、分歧和裁决依据
  - 如果没有真实 subagent 执行，必须标注为 single-agent simulation 或 tracking
```

### 4. Agent Mapping 检查

```yaml
source: think-tank/platforms/claude-code/agent-mapping.md
required_checks:
  - 每个旧 subagent 只能映射到 profile
  - profile 职责不能被旧 subagent frontmatter 覆盖
  - 图像编辑领域知识不能进入 core profile
pass_condition: 旧 subagent 被吸收为可选平台实现，而不是协议来源
```

### 5. Skill Mapping 检查

```yaml
source: think-tank/platforms/claude-code/skill-mapping.md
required_checks:
  - 每个旧 skill 都映射到 capability
  - capability 不要求固定 skill 名称
  - skill 不可用时有降级策略
pass_condition: 外部 skills 是 optional enhancement，不是 core dependency
```

### 6. Result Recovery 检查

Claude Code 若真实派发 subagent，必须回收如下结构：

```yaml
role: ""
agent_name: ""
phase: collect | discuss | conclude
claim: ""
evidence: []
concerns: []
recommendations: []
confidence: low | medium | high
boundary: []
```

验收判断：

```yaml
verified:
  meaning: 真实派发、真实回收、最终输出引用了角色结果
tracking:
  meaning: 只记录状态或任务计划，没有角色结果
mock:
  meaning: 使用模拟 agent 或静态样例
planned:
  meaning: 文档已定义但尚未执行
```

## 首轮验收输出

Claude Code 平台首轮验证结束后，应新增：

```text
think-tank/examples/claude-code-research-validation.md
think-tank/examples/claude-code-council-validation.md
think-tank/docs/claude-code-validation-report.md
```

如果未能验证成功，也必须写入失败原因：

```yaml
status: blocked
blocked_by:
  - missing_subagent_runtime
  - no_result_recovery
  - missing_external_skill
  - permission_or_environment
boundary: ""
next_action: ""
```

## 禁止通过标准

以下情况不能标记为 `verified`：

- 只读了旧 research agent 文件。
- 只生成了计划，没有执行。
- 只写了状态文件，没有回收结果。
- 只调用了一个工具 skill，却没有进入 think-tank 的角色讨论和汇总。
- 输出没有边界声明。

## 当前建议

在切换 Claude Code 前，本仓库应保持：

```yaml
codex_core_modes: verified
codex_browser_optional: verified_optional
codex_local_source_markdown_artifact: verified
codex_external_source_readonly: verified
codex_browser_external_dom: blocked
claude_code_runtime: planned
next_action: run_claude_code_preflight
```

当前 Codex readiness 已记录于：

```text
think-tank/docs/codex-readiness-matrix.md
```

因此下一步一旦切换到 Claude Code，应只验证 Claude Code 平台适配，不再重新定义 think-tank 主协议。

## 当前验证进度

```yaml
research_mode_preflight: verified_with_format_gap
council_mode_preflight: verified_as_single_agent_council_preflight
skill_discovery: verified
capability_auto_mapping: verified_partial_pre_invocation_decision
external_source_readonly: verified_partial
adapter_dispatch_attempt: adapter_dispatch_not_executed_verified_partial
dispatch_contract_validation: verified_partial_with_order_gap
dispatch_pre_invocation_decision: verified_partial
result_recovery_contract: partial_manual_mapping
minimal_runtime_contract: implemented_as_repeatable_contract
minimal_runtime_success_sample: think-tank/examples/claude-runtime-sample.json
minimal_runtime_failure_sample: think-tank/examples/claude-runtime-failure-sample.json
claude_code_validation_report: think-tank/docs/claude-code-validation-report.md
```
