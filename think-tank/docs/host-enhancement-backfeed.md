# Host Enhancement Backfeed

本文件记录哪些能力应留在项目本地，哪些应上升为 `think-tank` 的宿主增强层。

## 原则

```yaml
project_specific_facts_stay_local: true
cross_project_methods_promote_to_think_tank: true
legacy_platform_baggage_discarded: true
```

## 适合反哺到 think-tank 的能力

### 研究结论转行动

当宿主 agent 做完调研、竞品分析或反馈归纳后，最常见的问题不是“资料不够”，而是“下一步到底该做什么”。

因此 `think-tank` 应显式支持：

- 影响判断
- 动作优先级
- 非目标
- 验证方式
- 证据不足时的观察态

这类结构属于跨项目方法，不绑定任何特定代码仓、PRD 流程或后端服务。

### skeptic 反证机制

研究类任务容易出现顺着单一叙事越想越对的问题。`skeptic` 的职责不是唱反调，而是强制区分：

- 已验证事实
- 高置信推断
- 低证据猜测

这类反证机制属于 `think-tank` 的核心价值，应优先内置到 recipe 和模板里。

### research 到 backlog 的中间层

研究输出不应直接冒充“已决定开发”。宿主增强层更适合提供：

- action brief
- strategy_to_backlog
- 观察项与执行项分离

这样宿主 agent 可以把研究结论安全转译成后续任务，而不是跳过边界。

## 不应反哺的内容

- 项目专属页面结构、接口合同和运行前置
- 某个仓库的产品域知识
- Obsidian、tmux、Claude Code 等平台耦合约束
- 旧工具栈和私有输出路径

## 当前落点

- `recipes/research-to-action.md`
- `templates/research-action-brief.md`
- `recipes/evidence-synthesis.md`
- `recipes/competitive-intelligence.md`
- `recipes/user-feedback-analysis.md`
