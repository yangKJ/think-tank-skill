# End-to-End Research Example

本示例展示 think-tank 如何处理一个通用 research mode 任务。

## 用户请求

```text
研究一个跨平台 Skill 仓库应该如何组织目录结构，要求给出通用建议、风险和下一步行动。
```

## Step 1: Mode Selection

```yaml
selected_mode: research
selection_reason: 用户需要研究通用结构，并形成建议和行动步骤。
```

## Step 2: Profile Selection

```yaml
profiles:
  - source-collector
  - trend-analyst
  - skeptic
  - report-architect
```

## Step 3: Capability Selection

```yaml
capabilities:
  - source-acquisition
  - knowledge-persistence
```

## Step 4: Platform Execution

Codex 路径：

```yaml
execution:
  platform: codex
  method: single_agent_profile_simulation
  status: verified_for_local_repository_context
```

Claude Code 路径：

```yaml
execution:
  platform: claude-code
  method: subagent_or_agent_team_mapping
  status: planned
```

## Step 5: Expected Output Shape

```text
结论
依据
角色观点
分歧与风险
行动建议
边界
```

## 关键边界

该示例验证的是协议执行路径，不验证外部 skills 或真实多 agent 并发。

