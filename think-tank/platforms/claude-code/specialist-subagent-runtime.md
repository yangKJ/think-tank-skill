# Claude Code Specialist Subagent Runtime

本文定义 Claude Code 平台如何执行 think-tank v0.5 专业 subagent runtime。

## 当前状态

```yaml
claude_code_specialist_subagent_runtime: verified
team_create: verified
task_create: verified
agent_spawn: verified
send_message: verified
shutdown: verified
team_delete: verified
message_recovery: verified
true_parallel_subagent_runtime: verified
```

**重要更新 (2026-05-24)**：Agent Team Runtime 已通过真实测试验证。以下是完整的调用流程和限制。

## 完整调用流程

```
用户请求
  → TeamCreate                    ✅ 同步创建
  → TaskCreate (可选)             ✅ 同步创建
  → Agent (spawn)                ✅ 并行派发 subagent
  → SendMessage (subagent→main)   ✅ 结果回收
  → SendMessage (main→subagent)   ✅ shutdown_request
  → TeamDelete                    ✅ 清理 team
```

## TeamCreate

```yaml
TeamCreate(team_name="think-tank-council", description="讨论任务")
# 返回: team_name, team_file_path, lead_agent_id
```

**实测结果**：
- 同步执行，立即返回
- 创建了 `/Users/condy/.claude/teams/{team_name}/config.json`
- lead_agent_id 格式: `team-lead@{team_name}`

## TaskCreate

```yaml
TaskCreate(
  subject="收集 think-tank 核心能力信息",
  description="作为 collector，从...收集...",
  activeForm="收集 think-tank 核心能力信息"
)
# 返回: task_id (数字)
```

**实测结果**：
- 同步执行，返回 task_id
- 必须用 `taskId` 参数更新状态
- 状态不会自动更新，需手动管理

## Agent Spawn

```yaml
Agent(
  description="收集 think-tank 核心能力",  # 显示名称
  name="collector",                          # teammate name，用于 SendMessage
  prompt="你是 collector 角色，负责...",
  subagent_type="general-purpose",           # 或专业 subagent 类型
  team_name="think-tank-council",            # 所属 team
  run_in_background=true                    # 后台异步执行
)
# 返回: agent_id, name, team_name
```

**实测结果**：
- `run_in_background=true` 时异步执行，主 agent 不阻塞
- 多个 agent 并行启动，约 30-60 秒完成
- agent_id 格式: `collector@think-tank-council`

## 消息回收机制

### Subagent 发送消息

```yaml
# 在 subagent prompt 中调用
SendMessage(
  to="team-lead@think-tank-council",  # 格式: team-lead@team_name
  message={...}                        # 结构化对象或字符串
)
```

**实测结果**：
- subagent 完成后主动发送消息
- 消息自动送达主 agent，无需轮询
- `summary` 字段用于消息预览
- 支持结构化 JSON

## Shutdown 机制

```yaml
SendMessage(
  to="collector",
  message={
    "type": "shutdown_request",
    "request_id": "council-shutdown-001",
    "reason": "讨论已完成，感谢参与"
  }
)
# subagent 返回: shutdown_approved
# 系统发送: teammate_terminated
```

## Shutdown 保护流程（推荐实现）

Claude Code 存在已知 shutdown 死锁 bug，建议实现以下保护流程：

```yaml
safe_shutdown:
  timeout_graceful: 15s
  timeout_force: 30s
  retry_interval: 2s
  max_retries: 3
```

### 状态机转换

```
sending_shutdown_request
  → waiting_approval (15s timeout)
    → approved → team_delete
    → timeout → force_terminate (30s timeout)
      → success → team_delete
      → failure → mark_zombie → user_prompt
```

### 完整流程代码

```typescript
async function safeTeamShutdown(teamName: string) {
  const state = {
    teamName,
    phase: 'sending',
    startedAt: Date.now(),
    shutdownRequestId: `shutdown-${teamName}-${Date.now()}`,
  };

  try {
    // Step 1: 发送 shutdown_request
    await sendShutdownRequest(state);
    
    // Step 2: 等待 approval (15s timeout)
    const approved = await waitForApproval(state, 15000);
    if (approved) {
      return await teamDelete(teamName);
    }
    
    // Step 3: 超时后 force terminate (30s timeout)
    await forceTerminate(teamName);
    return await teamDelete(teamName);
  } catch (error) {
    // Step 4: 失败处理 - 标记 zombie 并提示用户
    return handleZombieTeam(teamName);
  }
}

async function waitForApproval(state, timeout) {
  const deadline = Date.now() + timeout;
  while (Date.now() < deadline) {
    const status = await checkAgentStatus(state.teamName);
    if (status === 'terminated') return true;
    if (status === 'zombie') return false;
    await sleep(2000);
  }
  return false;
}

async function handleZombieTeam(teamName) {
  const teamPath = `${process.env.HOME}/.claude/teams/${teamName}`;
  return {
    success: false,
    requiresManualCleanup: true,
    cleanupCommand: `rm -rf ${teamPath}/`,
    userMessage: `⚠️ Team "${teamName}" 清理失败\n\n手动清理：rm -rf ${teamPath}/`,
  };
}
```

## TeamDelete 清理

```yaml
TeamDelete()
# 返回: success, team_name
```

**实测结果**：
- 清理 team 和 task 目录
- 必须等所有 agent shutdown 后才能成功
- **已知 Bug**：shutdown_deadlock 时会失败，需手动 `rm -rf`

## Mapping

| think-tank profile | Claude Code source |
|--------------------|-------------------|
| `source-collector` | `general-purpose` + collector prompt |
| `trend-analyst` | `general-purpose` + trend analyst prompt |
| `social-listener` | `general-purpose` + social listener prompt |
| `feedback-synthesizer` | `Feedback Synthesizer` |
| `report-architect` | `Feedback Synthesizer` |
| `product-strategist` | `general-purpose` + product strategist prompt |
| `domain-expert` | `Software Architect` |
| `skeptic` | `Code Reviewer` / `Security Engineer` |
| `builder` | `Senior Developer` |
| `synthesizer` | `Feedback Synthesizer` |
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

- 主 agent 自己补写所有角色
- 子 agent 没有返回结构化结果
- 只创建 Team 但没有回收 role-result
- 只安装了 `.claude/agents` 但没有实际调用

## 已知限制

| 限制 | 说明 | 状态 | 解决方案 |
|------|------|------|----------|
| 任务状态不自动更新 | agent 完成后 task 不会自动标记 completed | known limitation | 手动调用 TaskUpdate 更新状态 |
| TeamDelete 需等待所有 agent | 必须先 shutdown 再 delete | by design | 按顺序先发 shutdown 再 delete |
| shutdown_deadlock | shutdown_approved 响应后 TeamDelete 仍可能失败 | **known_bug** | Session GC + Teamless 协作模式 |
| agent 数量上限 | 未测试大规模并发 | not verified | - |
| peer-to-peer 通信 | subagent 间直接通信未测试 | not verified | Filesystem Message Bus 替代 |

## Shutdown 死锁缓解方案

已实现两个互补方案：

1. **Session GC**（事后修复）：自动检测和清理 zombie team。见 `think-tank/platforms/claude-code/session-gc.md`
2. **Teamless 协作**（事前规避）：完全绕过 Team API，通过文件系统通信。见 `think-tank/platforms/claude-code/teamless-collaboration.md`

详细实现：
- `think-tank/protocol/session-gc-contract.md`
- `think-tank/protocol/filesystem-message-bus.md`
- `think-tank/runtime/session_gc.py` (8/8 tests pass)
- `think-tank/runtime/filesystem_bus.py` (10/10 tests pass)

## 下一步待验证

- [ ] agent 间 peer-to-peer SendMessage
- [ ] 状态文件协调机制
- [ ] 大规模并发 (5+ agents)
- [ ] 跨 team 通信

