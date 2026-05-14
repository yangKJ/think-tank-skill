# Council Mode

## 定位

council mode 收编 agent-council 的多角色讨论能力。agent-council 是历史实现分支，不是新体系中心。

## 适用场景

- 需要多个角色审议同一问题
- 需要正反观点碰撞
- 需要暴露方案风险和取舍
- 需要形成可执行的最终判断

## 默认角色

- `domain_expert`：提出专业主张
- `skeptic`：挑战假设和寻找反例
- `builder`：评估落地成本和执行路径
- `synthesizer`：组织共识、分歧和结论

## 主持人原则

council mode 中，主 Agent 默认扮演主持人：

- 负责议题澄清、角色选择、流程推进和结果汇总
- 不提前发表技术观点
- 不压制少数意见
- 只有在超时、低共识或轮次耗尽时进入裁决

这个原则来自旧 agent-council，但现在属于 think-tank 的 council mode。

## 流程重点

1. 明确议题和决策目标
2. 各角色独立给出初始判断
3. 进行交叉质询和反驳
4. 修正观点并收敛分歧
5. 输出最终建议、少数意见和风险

## 共识层级

| 层级 | 含义 | 动作 |
|------|------|------|
| L1 | 达成可执行共识 | 进入汇总 |
| L2 | 存在分歧但可继续调和 | 追加一轮针对分歧的讨论 |
| L3 | 超时、低共识或轮次耗尽 | 主持人裁决，并记录少数意见 |

L3 裁决不是抹平分歧。最终输出必须记录被裁决掉的关键反对意见。

## v0.2 显式投票

council mode 不再只要求“讨论过”，还要求显式记录：

```yaml
position:
  profile: ""
  proposal: ""
  objections: []
  vote:
    main: agree | disagree | abstain
  confidence: low | medium | high
```

如果 `skeptic` 或其他角色给出 blocking objection，不能标记 L1 共识。必须继续一轮针对性讨论，或者进入 L3 裁决并记录少数意见。

完整规则见 `protocol/consensus-contract.md`。

## 输出重点

- 共识结论
- 分歧点
- 关键反对意见
- 风险和缓解措施
- 决策建议

## 旧 agent-council 映射

旧 agent-council 的 collect、discuss、conclude、complete 应分别映射为 think-tank 主协议的 collection、deliberation、synthesis、quality_check。

旧状态机、HMAC、manifest 和文件权限设计属于 Claude Code 平台实现经验，不属于 council mode 的平台无关要求。
