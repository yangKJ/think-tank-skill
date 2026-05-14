# Agent Selection

本文件定义 think-tank 如何选择参与角色和平台 agent。

这里的“agent selection”分两层：

- 协议层角色选择：选择 `collector`、`domain_expert`、`skeptic`、`builder`、`synthesizer` 等角色。
- 平台层 agent 映射：由 Claude Code、Codex 或其他平台把协议角色映射到具体 agent、subagent、工具或执行片段。

## 选择原则

1. 场景驱动，不固定凑人数。
2. 优先覆盖问题的关键维度。
3. 标准任务选择 2 到 4 个角色。
4. 高风险任务必须包含 `skeptic`。
5. 需要落地计划时必须包含 `builder`。
6. 所有流程最终必须包含 `synthesizer`。

## 基础场景映射

| 场景 | 推荐协议角色 | 说明 |
|------|--------------|------|
| 技术方案、技术策略 | `domain_expert` + `skeptic` + `builder` | 方案可行性、风险和落地路径 |
| 架构、设计模式 | `domain_expert` + `builder` + `skeptic` | 架构判断、执行成本和反例 |
| 安全、漏洞、权限 | `skeptic` + `domain_expert` + `builder` | 风险优先，兼顾修复 |
| 代码质量、重构 | `collector` + `skeptic` + `builder` | 先读现状，再审查和修复 |
| 性能优化、效率 | `collector` + `domain_expert` + `builder` | 先定位瓶颈，再制定优化路径 |
| 竞品调研、最佳实践 | `collector` + `domain_expert` + `synthesizer` | 多渠道收集和归纳 |
| 流程、CI/CD、自动化 | `collector` + `builder` + `skeptic` | 当前流程、改进路径和风险 |
| 无障碍、测试、质量 | `collector` + `skeptic` + `builder` | 缺陷发现和修复建议 |
| 项目结构、模块关系 | `collector` + `domain_expert` + `skeptic` | 结构理解和风险审查 |
| 多 agent 协作系统 | `domain_expert` + `skeptic` + `builder` | 协议、执行和可靠性 |
| 产品、需求、优先级 | `domain_expert` + `skeptic` + `builder` | 价值、风险和路线 |

## Claude Code 旧 agent 映射参考

旧 agent-council 中的 Claude Code agent 可作为平台映射参考，但不是协议要求。

| 旧 Agent | 推荐协议角色 |
|----------|--------------|
| `Code Reviewer` | `skeptic` 或 `builder` |
| `Security Engineer` | `skeptic` |
| `Software Architect` | `domain_expert` |
| `project-analyzer` | `collector` |
| `Accessibility Auditor` | `skeptic` |
| `Web Researcher` | `collector` |
| `Workflow Optimizer` | `builder` |
| `skill-manager` | `domain_expert` |
| `Feedback Synthesizer` | `synthesizer` |

旧 research think-tank 中的 capability slots 映射：

| 旧 Slot | 推荐协议角色 |
|---------|--------------|
| `source_research` | `collector` |
| `trend_analysis` | `domain_expert` |
| `critic` | `skeptic` |
| `synthesis` | `synthesizer` |

## 选择流程

1. 解析用户任务目标。
2. 根据 `mode-selection.md` 选择 mode。
3. 根据场景关键词选择初始角色组合。
4. 根据风险、执行需求和证据需求补充角色。
5. 移除重复职责角色。
6. 确保 `synthesizer` 存在。
7. 交给平台 adapter 映射为具体 agent 或执行单元。

## 角色数量建议

| 任务类型 | 建议数量 |
|----------|----------|
| 轻量讨论 | 2 |
| 标准研究或审议 | 3 到 4 |
| 高风险评审 | 4 到 5 |
| 大型战略讨论 | 4 到 6 |

超过 6 个角色时，必须说明为什么不能拆成多轮 think-tank。

## 输出记录

每次选择应记录：

```yaml
selected_mode: ""
selected_roles: []
selection_reason: ""
platform_agents: []
status:
  role_selection: verified
  platform_mapping: verified | planned | mock | tracking
```

轻量输出可以不展示全部字段，但 adapter 内部必须保留这些语义。

