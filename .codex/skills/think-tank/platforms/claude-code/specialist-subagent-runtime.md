# Claude Code Specialist Subagent Runtime

本文定义 Claude Code 平台如何执行 think-tank v0.5 专业 subagent runtime。

## 当前状态

```yaml
claude_code_specialist_subagent_runtime: specified
agent_team_full_runtime: not_verified
subagent_dispatch_contract: specified
```

旧 research agent 和 agent-council 证明 Claude Code 有专业 subagent/Agent Team 方向，但也暴露出生命周期、状态回收和稳定性限制。

## Mapping

| think-tank profile | Claude Code source |
|--------------------|-------------------|
| `source-collector` | Research Sub Researcher |
| `trend-analyst` | Research Sub Trend Researcher |
| `social-listener` | Research Sub Xiaohongshu Researcher |
| `feedback-synthesizer` | Research Sub Feedback Synthesizer / Feedback Synthesizer |
| `report-architect` | Research Sub Research Report Architect |
| `skeptic` | Critic / Code Reviewer / Security Engineer |
| `product-strategist` | Research Sub Product Manager |
| `facilitator` | main agent as neutral host |

## Dispatch Rule

Claude Code adapter 必须先形成：

```yaml
subagent_task:
  profile: ""
  subagent_type: ""
  objective: ""
  required_capabilities: []
  expected_output_schema: role-result
```

回收时必须得到：

```yaml
role_result:
  execution_method: specialist_subagent
  profile: ""
  claim: ""
  evidence: []
  risks: []
  objections: []
  recommendations: []
  boundaries: []
```

## 禁止声明

不得把以下情况标记为 `specialist_subagent`：

- 主 agent 自己补写所有角色。
- 子 agent 没有返回结构化结果。
- 只创建 Team 但没有回收 role-result。
- 只安装了 `.claude/agents` 但没有实际调用。

