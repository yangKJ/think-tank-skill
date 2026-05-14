# Codex Strategy Validation

本文件记录 Codex 平台对 strategy mode 的验证。

## 测试任务

```text
为 think-tank v0.1 之后的建设制定下一阶段路线：先继续验证 Codex 外部能力，还是切换到 Claude Code 平台验证？
```

## 执行声明

```yaml
platform: codex
execution_method: single_agent_profile_simulation
mode: strategy
profiles:
  - product-strategist
  - skeptic
  - source-collector
  - report-architect
capabilities:
  - source-acquisition
  - browser-automation
verified:
  - strategy_mode_selection
  - roadmap_tradeoff_analysis
  - milestone_definition
  - risk_prioritization
  - actionable_next_steps
not_verified:
  - claude_code_runtime_strategy_execution
  - true_multi_agent_strategy_session
  - external_network_research
```

## 结论

下一阶段应优先完成 Codex 平台的最小闭环，再切换到 Claude Code 平台验证。

原因：

1. Codex 是当前实际运行环境，可以继续用本仓库直接验证协议、mode、profile 和 capability 降级边界。
2. Browser 作为第一个 optional capability 已经完成 localhost fixture 验证，但仍需要把能力状态和最低安装场景继续收敛。
3. Claude Code 验证依赖旧 `.claude/skills`、`.claude/agents` 和平台 runtime，切换前需要先准备验收清单，避免把旧实现习惯重新带回主协议。

## 路线选择

### 选项 A: 继续 Codex 验证

收益：

- 能快速验证 `strategy mode`、最低安装场景和 optional capability 边界。
- 不依赖外部平台切换。
- 有利于先把协议语言写稳定。

风险：

- 只能证明 Codex 单 agent 多 profile 执行。
- 不能证明 Claude Code subagent 调度。

判断：

```yaml
support_level: strong
reason: 当前最接近可控验收闭环
```

### 选项 B: 立即切换 Claude Code 验证

收益：

- 能验证旧 research agent 和 agent-council 的真实来源平台。
- 能检查 `.claude/skills` 和 `.claude/agents` 映射是否足够。

风险：

- 容易被旧路径和旧实现细节带偏。
- 如果协议还不够稳定，平台适配会反向污染 core。

判断：

```yaml
support_level: mixed
reason: 必须做，但不应早于 Codex foundation 收敛
```

## 推荐路线

```yaml
phase_1:
  name: codex_foundation_closure
  goal: 关闭四个核心 mode 的 Codex 内部验证
  exit_criteria:
    - research_mode: verified
    - council_mode: verified
    - review_mode: verified
    - strategy_mode: verified
    - protocol_check: pass

phase_2:
  name: optional_capability_boundary
  goal: 明确只安装 think-tank 时和安装 optional skills 时的行为差异
  exit_criteria:
    - minimal_install_behavior: documented
    - browser_automation_optional: verified
    - unavailable_capability_degradation: verified

phase_3:
  name: claude_code_preflight
  goal: 准备 Claude Code 平台验证清单
  exit_criteria:
    - agent_mapping_reviewed
    - skill_mapping_reviewed
    - runtime_contract_reviewed
    - old_research_assets_classified

phase_4:
  name: claude_code_runtime_validation
  goal: 在 Claude Code 中验证 research mode 和 council mode
  exit_criteria:
    - research_mode_claude_code: verified_or_blocked_with_reason
    - council_mode_claude_code: verified_or_blocked_with_reason
```

## 风险

```yaml
risks:
  - id: R1
    risk: 把 optional capability 当成 core dependency
    mitigation: 所有外部能力文档必须保留降级策略和状态标注
  - id: R2
    risk: Claude Code 验证时旧 research agent 重新成为父级体系
    mitigation: 只迁移能力，不迁移父子关系
  - id: R3
    risk: profile 和 capability 继续膨胀
    mitigation: 新增前必须证明它不能由既有 profile/capability 表达
```

## 行动建议

1. 将 `strategy mode` 标记为 Codex 内部 verified。
2. 更新 `codex-validation-report.md` 和 `v0.1-readiness.md`。
3. 下一步准备 Claude Code preflight，而不是直接复制旧 `.claude` 目录。
4. 在 Claude Code 验证前，先写清楚验收任务、预期输出和失败边界。

## 边界

本次验证没有调用 Claude Code runtime，没有执行真实多 agent 会话，也没有进行外部网络调研。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```
