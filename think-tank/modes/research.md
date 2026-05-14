# Research Mode

## 定位

research mode 承接原 research 体系里的 think-tank 用法，但在新主仓中它只是 think-tank 的一个场景模式，不再是父级系统。

## 适用场景

- 需要多渠道信息收集
- 需要整理证据、来源和背景
- 需要从资料中形成研究结论
- 需要把不确定信息转化为可判断边界

## 默认角色

- `collector`：收集资料和证据
- `domain_expert`：解释领域含义
- `skeptic`：检查来源可靠性和证据缺口
- `synthesizer`：整合结论和行动建议

## 旧 research think-tank 映射

旧 research agent 中的 capability slots 应映射为协议角色：

| 旧 slot | 新角色 |
|---------|--------|
| `source_research` | `collector` |
| `trend_analysis` | `domain_expert` |
| `critic` | `skeptic` |
| `synthesis` | `synthesizer` |

旧 `research-discuss` 工作流应收敛为 research mode 的标准流程。旧 `simple-discuss` 和 `full` 不属于 research 专有能力，应分别归入 council 或 strategy 场景。

## 流程重点

1. 明确研究问题和成功标准
2. 确认信息来源边界
3. 收集并分级证据
4. 分析证据支持和反证
5. 输出研究结论、置信度和后续验证建议

## 输出重点

- 研究结论
- 关键证据
- 证据缺口
- 置信度
- 后续验证路径

## 触发边界

单人调研、普通搜索、简单资料查询不应强制触发完整 think-tank。只有当任务需要多渠道、多角色、讨论或证据冲突处理时，才使用 research mode。

## 能力状态要求

如果平台只完成了并行收集，没有进入讨论、质疑、共识判断和汇总阶段，不能称为完整 research mode。
