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

## v0.2 Research Hardening

research mode 的 deep research 必须强化以下字段：

```yaml
research_depth: quick_scan | deep_research | continuous_monitoring | autonomous_research
source_authority: A | B | C
confidence_level: low | medium | high
source_timestamp: timestamp
content_hash: optional
cross_validation: required_for_high_confidence
acknowledgement: required_for_subagent_reports_when_available
```

来源等级：

| 等级 | 定义 | 示例 |
|------|------|------|
| A | 权威来源或多方验证 | 官方文档、论文、原始公告 |
| B | 可信二手来源 | 行业报告、新闻、专业博客 |
| C | 单一或弱验证来源 | 论坛、社媒、个人观点 |

deep research 输出必须包含：

- 研究领域分解
- 每个领域的 evidence table
- source authority
- confidence level
- evidence gaps
- 至少一个反证或反对意见
- 决策日志或 why-stop-now 说明

continuous monitoring 输出必须额外包含：

- 监控主题
- 触发条件
- 下次检查条件
- 变化检测边界

## 输出重点

- 研究结论
- 关键证据
- 证据缺口
- 置信度
- 后续验证路径

## Post-run Curation

research mode 如果使用外部来源、本地资料、用户材料或工具输出，必须在最终输出中判断是否需要 `post_run_curation`。

至少应包含：

- `source_candidates`：本次研究用到或值得沉淀的来源候选
- `trend_candidates`：如果任务涉及趋势、行业变化、用户行为或平台变化
- `action_candidates`：需要继续验证、监控、实验或转成 backlog 的动作
- `artifact_plan`：是否建议形成报告、brief、run record 或资料卡
- `persistence_decision`：是否已写入文件；如果没有写入，说明原因

该能力属于 think-tank core，不依赖某个项目是否存在 `.think-tank/`。平台或项目 adapter 只决定实际落点。

## 触发边界

单人调研、普通搜索、简单资料查询不应强制触发完整 think-tank。只有当任务需要多渠道、多角色、讨论或证据冲突处理时，才使用 research mode。

## 能力状态要求

如果平台只完成了并行收集，没有进入讨论、质疑、共识判断和汇总阶段，不能称为完整 research mode。
