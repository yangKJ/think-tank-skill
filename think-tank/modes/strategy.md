# Strategy Mode

## 定位

strategy mode 用于产品、架构、路线、资源分配和长期演进决策。

## 适用场景

- 产品定位
- 技术路线选择
- 架构演进
- 多阶段建设计划
- 资源和优先级取舍

## 默认角色

- `domain_expert`：判断行业、产品或技术可行性
- `skeptic`：挑战目标、假设和风险
- `builder`：拆解执行路径和成本
- `synthesizer`：形成路线图和优先级

## 流程重点

1. 明确长期目标和当前约束
2. 拆解关键选择和不可逆决策
3. 比较备选路径
4. 识别短期可执行动作
5. 输出阶段路线、风险和决策点

## 输出重点

- 战略判断
- 路线图
- 优先级
- 关键风险
- 下一阶段行动

## Post-run Curation

strategy mode 只要输出可执行路线、资源取舍、产品策略、技术路线或增长动作，就必须判断 `post_run_curation`。

重点字段：

- `action_candidates`：可转成 backlog、experiment、decision、runbook、promotion 或 monitoring 的候选动作
- `artifact_plan`：是否建议沉淀为 strategy brief、roadmap、decision record 或 backlog
- `persistence_decision`：说明是否已写入；未写入时说明需要用户确认、缺少目标路径或只是候选建议

策略建议不能只停留在聊天结论。若暂不持久化，也要给出结构化候选，方便平台 adapter 或项目工作区后续接收。
