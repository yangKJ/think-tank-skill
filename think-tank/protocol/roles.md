# Roles

本文件定义 think-tank 的角色选择机制。角色是协议层概念，不绑定任何平台的 agent、subagent、线程或脚本。

## 设计原则

1. 角色服务任务，不固定凑人数。
2. 每个角色必须有清晰职责和输出。
3. 同一平台可以用真实 subagent、单 agent 模拟、人工分段或脚本执行角色职责。
4. 角色之间必须先独立分析，再进入讨论，避免过早共识。
5. 输出时要保留角色差异，不能只给一个混合结论。

## 基础角色

### collector

职责：

- 收集信息、证据、上下文、约束和已有实现。
- 标注来源边界和证据可靠性。
- 区分已验证事实、用户提供背景和待确认信息。

适合：

- research mode
- review mode
- 需要本地仓库或外部资料支撑的任务

不负责：

- 直接做最终决策
- 把缺证据的推断包装成事实

### domain_expert

职责：

- 从领域专业角度解释问题。
- 判断方案、证据或事实的含义。
- 给出主要机会、限制和关键判断。

适合：

- research mode
- council mode
- strategy mode

不负责：

- 忽视执行成本
- 以专家判断替代证据

### skeptic

职责：

- 寻找漏洞、反例、风险、遗漏和过度自信。
- 挑战输入假设、证据质量和结论跳跃。
- 标出需要进一步验证的部分。

适合：

- council mode
- review mode
- strategy mode
- 高风险任务

不负责：

- 为了反对而反对
- 只列风险不提供可验证路径

### builder

职责：

- 评估落地路径、实现成本、迁移顺序和执行阻力。
- 把结论转成可执行计划。
- 识别最小可行下一步。

适合：

- council mode
- review mode
- strategy mode

不负责：

- 跳过分析直接开工
- 用执行便利性覆盖协议目标

### synthesizer

职责：

- 汇总共识、分歧、风险和行动建议。
- 保持结论可追溯。
- 执行输出前质量门禁。

适合：

- 所有 mode

不负责：

- 抹平未解决分歧
- 隐藏证据不足或平台限制

## 角色选择规则

最低规则：

- 所有 think-tank 流程必须包含 `synthesizer`。
- 涉及资料、代码、文档或外部信息时，应包含 `collector`。
- 涉及争议、重大取舍或高风险判断时，应包含 `skeptic`。
- 涉及执行、迁移、修复或路线规划时，应包含 `builder`。
- 涉及专业领域判断时，应包含 `domain_expert`。

更细的场景驱动选择见 `agent-selection.md`。

## 默认组合

```yaml
research:
  - collector
  - domain_expert
  - skeptic
  - synthesizer

council:
  - domain_expert
  - skeptic
  - builder
  - synthesizer

review:
  - collector
  - skeptic
  - builder
  - synthesizer

strategy:
  - domain_expert
  - skeptic
  - builder
  - synthesizer
```

## 角色输出契约

每个角色输出应包含：

```yaml
role: ""
claim: ""
evidence: []
concerns: []
recommendations: []
confidence: low | medium | high
boundary: []
```

## 角色数量控制

- 低风险任务：2 到 3 个角色即可。
- 标准 think-tank 任务：3 到 5 个角色。
- 高风险或复杂任务：可以增加专门角色，但必须说明新增理由。

不允许为了显得复杂而增加角色。
