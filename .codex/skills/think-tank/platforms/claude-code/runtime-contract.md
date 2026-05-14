# Claude Code Runtime Contract

本文定义 think-tank 在 Claude Code 中执行时的运行契约。

该契约来自旧 research think-tank 和 agent-council 的经验，但已收敛到 think-tank 主体系。

## 能力边界

Claude Code adapter 当前应保守标注：

```yaml
agent_team_execution: planned
subagent_dispatch: planned
send_message_deliberation: planned
state_file_coordination: planned
result_recovery: planned
legacy_mock_path: mock
legacy_tracking_path: tracking
```

只有在真实运行、回收结果并验证后，才能改为 `verified`。

## 推荐执行流程

```text
intake
  -> mode_selection
  -> role_planning
  -> collection
  -> deliberation
  -> synthesis
  -> recommendation
  -> quality_check
```

Claude Code 可以将流程映射为：

```text
创建会话目录
  -> 写入状态文件
  -> 并发派发收集角色
  -> 合并收集结果
  -> 派发讨论角色
  -> 交叉质询
  -> 派发 synthesizer
  -> 写入结论
  -> 清理或归档
```

## 状态阶段

Claude Code 可使用状态文件协调流程：

```yaml
phase: collect | discuss | conclude | complete
round: 0
agents: []
agents_completed: []
next_action: dispatch_next | merge_results | dispatch_synthesizer | complete
consensus_level: none | L1 | L2 | L3
consensus_support: 0.0
final_decision: null
```

状态文件是 Claude Code 平台实现细节，不是 think-tank 协议层硬要求。

## 结果目录

推荐运行目录：

```text
.think-tank/{session-id}/
├── state.json
├── collect/
├── discuss/
└── conclusion.md
```

对于需要长期沉淀的结论，可另存：

```text
.think-tank/conclusions/
```

具体路径可由项目适配覆盖。

## 主 Agent 职责

在 Claude Code 中，主 Agent 默认是主持人：

- 解析任务
- 选择 mode 和角色
- 派发 agent
- 检查状态
- 控制轮次
- 触发汇总
- 执行质量门禁

主 Agent 不应在 council mode 中提前发表技术观点，除非进入 L3 裁决。

## 讨论结束条件

Claude Code adapter 可使用：

- 共识达到阈值
- 轮次达到上限
- 超时
- 用户中断
- 主 Agent 裁决
- 关键证据不足，继续讨论无收益

## L1/L2/L3

```yaml
L1:
  meaning: 达成可执行共识
  action: 进入汇总

L2:
  meaning: 分歧可调和
  action: 继续一轮针对分歧的讨论

L3:
  meaning: 超时、低共识或轮次耗尽
  action: 主 Agent 裁决并记录少数意见
```

## 结果回收要求

每个角色结果至少包含：

```yaml
role: ""
agent_name: ""
phase: ""
claim: ""
evidence: []
concerns: []
recommendations: []
confidence: low | medium | high
boundary: []
```

如果无法回收某个角色结果，必须在最终输出的 `边界` 中说明。

## 禁止声明

- 不得把只写入状态文件称为真实完成。
- 不得把只派发但未回收结果称为已验证。
- 不得把旧 agent-council 的脚本状态直接等同于 think-tank 协议。
- 不得把 Claude Code 的 Team 机制写成其他平台必须实现的协议要求。

