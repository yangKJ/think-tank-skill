# Shutdown Contract

本文定义 think-tank Agent/Skill 生命周期的终止边界保证。

## 目的

保证 agent/skill 生命周期有明确的终止边界，防止：
- 资源泄漏
- zombie process
- zombie team
- 用户看到"已完成"但进程仍在运行

## 触发条件

| 条件 | 说明 |
|------|------|
| 用户明确取消 | 用户主动中断任务 |
| 任务正常完成 | 所有 profile 都返回结果 |
| 超时 | 超过 timeout 阈值 |
| 上游 shutdown_request | 主 agent 发送终止信号 |

## 保证条款

### 1. Termination Ack

收到 `shutdown_request` 后必须响应 `shutdown_approved`：

```yaml
shutdown_flow:
  main_agent:
    - 发送 shutdown_request
    - 等待 shutdown_approved (超时 15s)
  subagent:
    - 收到 shutdown_request
    - 响应 shutdown_approved
    - 立即停止新操作
```

### 2. Clean Exit

响应 `shutdown_approved` 后必须：
- 停止创建新子任务
- 将 pending 状态写入 artifact
- 释放占用的资源

### 3. State Flush

退出前必须确保：
- `phase: terminating`
- `termination_timestamp` 记录
- `pending_work` 已转移到主 agent 或写入 artifact

### 4. TeamDelete 前置

主 agent 调用 `TeamDelete` 前必须：
- 收到所有 subagent 的 `shutdown_approved`
- 检测所有 agent 状态为 `terminated`
- 如有 agent 卡在 `in-process`，标记为 zombie 并提示用户

## 死锁场景声明

### 已知死锁场景

```
触发条件：shutdown_request 发送后未收到 system teammate_terminated 信号

场景 1:
  1. subagent 响应 shutdown_approved
  2. 但 agent 状态机卡在 in-process
  3. TeamDelete 检测到仍有 active member
  4. 清理失败，team 残留

场景 2:
  1. subagent 无限次响应 shutdown_approved
  2. 但永不退出 (idle 状态持续)
  3. TeamDelete 永远失败
```

### 应对策略

```yaml
deadlock_handling:
  detection:
    - 检查 config.json 中 tmuxPaneId 状态
    - tmuxPaneId === "in-process" 表示卡住
  timeout:
    - graceful: 15s
    - force: 30s
  fallback:
    - 手动清理: rm -rf ~/.claude/teams/{team_name}/
    - 用户提示: 在输出中包含 cleanup command
```

## 用户提示标准化

当 team cleanup 失败时，必须在输出中包含：

```yaml
error_response_template:
  code: "TEAM_CLEANUP_FAILED"
  message: "任务完成，但 team 资源清理失败"
  details:
    team_name: "{team_name}"
    residual_members: ["{member_list}"]
  user_action: |
    运行以下命令手动清理：
    rm -rf ~/.claude/teams/{team_name}/
  artifact:
    - path: ".think-tank/artifacts/zombie-teams/{timestamp}.json"
      description: "残留 team 清单"
```

## 相关文档

- `think-tank/protocol/session-gc-contract.md` - Session GC 协议（事后修复）
- `think-tank/protocol/filesystem-message-bus.md` - 文件系统消息总线（事前规避）
- `think-tank/protocol/runtime-contract.md` - 运行时契约
- `think-tank/protocol/state-result-contract.md` - 状态结果契约
- `think-tank/platforms/claude-code/specialist-subagent-runtime.md` - Claude Code 适配

## 状态

```yaml
shutdown_contract: specified
termination_ack: specified
clean_exit: specified
state_flush: specified
team_cleanup前置: specified
deadlock_handling: documented
gc_mechanism: specified
teamless_mode: specified
implementation: pending
```