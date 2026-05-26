# Filesystem Message Bus

本文定义 think-tank 文件系统消息总线协议，作为 Claude Code Team API 的降级替代通信机制。

## 目的

当平台 Team API（TeamCreate/TeamDelete/SendMessage）不可靠或存在 shutdown 死锁时，通过文件系统实现 agent 间的异步消息传递和结果回收。

## 目录结构

```yaml
bus_root: ".think-tank/runs/{run_id}/bus/"

subdirs:
  dispatch:
    description: "主 agent 派发给 subagent 的任务"
    naming: "{timestamp}-{profile}-task.json"
  results:
    description: "subagent 返回的结果"
    naming: "{timestamp}-{profile}-result.json"
  signals:
    description: "控制信号 (shutdown, heartbeat, ack)"
    naming: "{timestamp}-{from}-{signal_type}.json"
  state:
    description: "共享状态文件"
    naming: "state.json"
```

## 消息信封格式

```yaml
message_envelope:
  message_id: "uuid v4"
  from: "sender_profile (或 'facilitator')"
  to: "recipient_profile (或 'broadcast')"
  type: "task | result | shutdown_request | shutdown_approved | heartbeat | ack"
  timestamp: "ISO8601"
  correlation_id: "可选，关联请求/响应"
  payload: {}                     # 根据 type 变化
  ttl_seconds: 300
```

## 消息类型定义

### Task 消息

```yaml
task_message:
  type: task
  payload:
    task_id: ""
    profile: ""
    mode: ""
    objective: ""
    input_context: []
    required_capabilities: []
    expected_output_schema: "role-result"
```

### Result 消息

```yaml
result_message:
  type: result
  payload:
    task_id: ""
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

### Control 信号

```yaml
control_messages:
  shutdown_request:
    from: facilitator
    to: broadcast
    payload:
      reason: ""
      deadline: "ISO8601"
  
  shutdown_approved:
    from: subagent_profile
    to: facilitator
    payload:
      accepted: true
  
  heartbeat:
    from: subagent_profile
    to: facilitator
    payload:
      status: "running | completing | waiting_shutdown"
      progress: 0.0-1.0
  
  ack:
    from: recipient
    to: sender
    payload:
      received_message_id: ""
      action: "received | processing | completed"
```

## 文件命名规范

```
格式: {timestamp_ms}-{to_profile}-{from_profile}-{msg_type}-{message_id}.json
示例: 1716552000000-collector-facilitator-task-a1b2c3d4.json
```

- 时间戳用毫秒级 epoch，天然保证排序
- to_profile 在前，接收方可按自己的 profile 名匹配文件
- from_profile 记录发送方，便于审计
- message_id 防止重复处理

## 并发安全

```yaml
concurrency:
  write_pattern: "atomic write"
  method: "写入临时文件 (.tmp) 后 os.rename 到目标路径"
  advantage: "无锁，读操作不会看到半写入文件"
  
  read_pattern: "list + sort by timestamp"
  method: "扫描目录获取文件列表，按时间戳排序"
  
  conflict_resolution: "last-writer-wins + correlation_id 去重"
  
  lock_free: true
```

## 轮询策略

```yaml
polling:
  default_interval: 1.0s
  max_interval: 5.0s
  backoff_multiplier: 1.5
  timeout_graceful: 15s
  timeout_force: 30s
```

## 生命周期

```yaml
lifecycle:
  created: "主 agent 调用 create_bus() 创建目录结构"
  active: "agent 读写消息"
  draining: "主 agent 发送 shutdown_request，等待所有 shutdown_approved"
  terminated: "所有 agent 已确认终止，主 agent 调用 cleanup_bus()"
  timeout: "超时未收到所有确认，标记为 partial_shutdown"
```

## 降级策略

```yaml
degradation:
  primary: "Team API (TeamCreate + SendMessage + TeamDelete)"
  fallback: "Filesystem Message Bus (本协议)"
  final_fallback: "single_agent_multi_profile_fallback"
  
  auto_degradation_conditions:
    - "TeamDelete 连续失败 2 次"
    - "shutdown_approved 后 agent 未终止超过 30s"
    - "用户明确指示 '用文件模式'"
```

## 相关文档

- `think-tank/protocol/shutdown-contract.md` — 正常 shutdown 流程
- `think-tank/protocol/session-gc-contract.md` — Zombie team 清理
- `think-tank/platforms/claude-code/teamless-collaboration.md` — Claude Code 使用指南

## 状态

```yaml
filesystem_message_bus_contract: specified
message_format: specified
directory_structure: specified
concurrency: specified
lifecycle: specified
implementation: pending
```