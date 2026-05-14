# Quality Gates

think-tank 每次输出前必须通过质量门禁。

## 必过门禁

- 是否明确采用了哪个 mode
- 是否包含 Runtime Provenance，并说明执行方式、数据来源和结果回收方式
- 是否说明了核心结论
- 是否区分事实、推断和建议
- 是否列出关键风险或分歧
- 是否给出可执行下一步
- 是否标注未验证或受限部分

## Runtime Provenance 门禁

所有 think-tank 风格输出都必须包含 `runtime_provenance`：

```yaml
runtime_provenance_present: true
execution_method_clear: true
data_collection_clear: true
provider_invocation_truthful: true
multi_agent_truthful: true
recovery_truthful: true
```

必须区分：

- `direct_assistant_tool`：助手直接调用工具，不等于 think-tank provider dispatch。
- `single_agent_multi_profile`：单 agent 扮演多个 profile，不等于真实多 agent。
- `manual_synthesis`：手工汇总，不等于自动 result recovery contract。
- `protocol_only`：只执行协议推理，不代表外部能力已调用。

完整规则见 `protocol/runtime-provenance.md`。

## 高风险任务追加门禁

当任务涉及代码发布、架构决策、商业承诺、法律、财务、医疗、安全或高成本行动时，追加检查：

- 是否需要更多来源或实时信息
- 是否需要用户确认范围
- 是否需要运行测试、审查代码或验证数据
- 是否存在不能由当前平台完成的能力缺口

## 平台能力声明

平台适配必须区分：

- `planned`：设计目标，尚未实现
- `mock`：只在模拟路径中验证
- `installed`：provider 文件或工具入口存在
- `discovered`：平台 adapter 已发现 provider 并读取元数据
- `selected`：policy 或 planner 为本次请求选择了 provider
- `dispatched`：调用前已形成 dispatch decision
- `invoked`：真实调用了 provider 或工具
- `recovered`：provider 输出已回收到 think-tank 输出契约
- `verified_partial`：真实路径可用，但范围有限或仍有人工步骤
- `verified`：有可复验流程、结果回收和质量门禁证据
- `blocked`：当前环境或约束下无法继续
- `failed`：真实调用发生但失败
- `tracking`：只记录状态，不代表真实执行完成

不得把 `installed`、`selected`、`mock` 或 `tracking` 写成 `verified`。
完整状态机见 `protocol/capability-evidence-state-machine.md`。

## v0.2 共识门禁

当 mode 包含 deliberation 或 council 行为时，必须追加：

- 是否记录各角色 `position`
- 是否记录 `agree`、`disagree` 或 `abstain`
- 是否存在 blocking objection
- 是否说明继续讨论或停止讨论的条件
- 是否保留少数意见
- 是否说明为什么现在可以进入结论

完整规则见 `protocol/consensus-contract.md`。
