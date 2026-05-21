# Minimal Conclusion Contract

本文定义 think-tank 在 `research`、`council`、`review`、`strategy` 四种 mode 下都可复用的最小结论契约。

目标不是替代完整 run record、deep research、expert meeting 或 review 报告，而是保证每次 think-tank 使用后，至少都能收敛出一份结构一致、可继续执行、可被宿主 agent 消费的结论摘要。

## 适用场景

在下列任一情况，最终输出中都应包含 `minimal_conclusion`：

- 任务需要给宿主 agent 一个可执行下一步
- 任务是中间审议、验收、任务包增强、方案取舍
- 任务证据不完整，但必须明确说明还能做什么
- 任务不值得生成完整长报告，但仍需要可审计收口

## 设计原则

- 平台无关
- 项目无关
- 不绑定任何特定 provider、skill、路径或业务术语
- 不要求一定生成文件，但要求结构明确
- 可以嵌入更长报告，也可以单独输出

## 最小结构

```yaml
minimal_conclusion:
  request:
  route:
    selected_intent:
    selected_mode:
    selected_recipe:
    trigger_status: explicit | inferred | fallback
  conclusion:
  decision:
  evidence:
    summary:
    evidence_state: selected | invoked | recovered | verified_partial | verified | blocked | failed | tracking
    confidence: low | medium | high
  risks: []
  next_step:
  boundaries: []
```

## 字段要求

### `request`

- 用一句话描述本轮 think-tank 实际在回答什么问题
- 不能只写原始用户全文

### `route`

- `selected_intent`、`selected_mode`、`selected_recipe` 必须显式
- `trigger_status` 用于说明：
  - `explicit`：用户明确触发
  - `inferred`：由宿主根据意图推断
  - `fallback`：无明确匹配，保守降级

### `conclusion`

- 总结当前最重要的判断
- 不要求很长，但必须具体
- 不能只写“需要进一步分析”

### `decision`

- 明确本轮建议采取什么方向
- 如果任务本质上是 review，也要给出是否采纳、是否接管、是否继续补证据等决策

### `evidence`

- `summary` 说明当前结论主要基于哪些类型的证据
- `evidence_state` 必须使用 capability/state 协议中的统一状态词
- `confidence` 说明当前结论把握度

### `risks`

- 至少列出主要残余风险
- 如果没有明显风险，写空数组而不是省略字段

### `next_step`

- 必须是宿主 agent 或后续执行者可以直接采取的下一步
- 如果需要补证据，必须明确补什么
- 如果需要外派，必须说明是“先增强任务包再派”还是“可直接派”

### `boundaries`

- 明确当前结论没有覆盖的边界
- 如果没有额外边界，也写空数组而不是省略

## 使用规则

### 1. 不替代完整产物

`minimal_conclusion` 只是最小收口层，不替代：

- `deep-research.md`
- `expert-meeting.md`
- `think-tank-run-record.md`
- provider invocation ledger

### 2. 可嵌入完整报告

长报告、meeting minutes、review 文档可以在结尾附上 `minimal_conclusion`，用于：

- 宿主快速消费
- 后续 dispatch
- 结果回放
- 结构化记忆筛选

### 3. 证据不足时也必须收口

如果证据仍然不足，不要停止在“证据不足”这句话上，仍然应输出：

- 当前可得结论
- 残余风险
- 明确下一步补证据动作

### 4. 不得伪装为执行完成

如果 `next_step` 仍然是“需要继续执行”“需要继续验证”“需要 provider 真调用”，不得把 `decision` 写成已经完成闭环。

## 最小质量门禁

```yaml
minimal_conclusion_quality_check:
  request_explicit: true
  route_explicit: true
  conclusion_specific: true
  decision_actionable: true
  evidence_state_labeled: true
  confidence_labeled: true
  next_step_present: true
  boundaries_present: true
```

## Verification Status

```yaml
minimal_conclusion_contract_v0_1: specified
project_binding: none
provider_binding: none
intended_use:
  - host_agent_summary
  - worker_acceptance_review
  - decision_council_summary
  - task_packet_enhancement_summary
```
