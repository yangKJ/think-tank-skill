# Review Mode

## 定位

review mode 用于审查代码、文档、报告、设计方案、实现产物或迁移计划。

## 适用场景

- 代码审查
- 方案验收
- 报告可信度评估
- 实现与协议一致性检查
- 发布或交付前质量检查

## 默认角色

- `collector`：读取被审查对象和相关上下文
- `skeptic`：寻找缺陷、遗漏和过度自信
- `builder`：判断修复成本和落地路径
- `synthesizer`：给出验收结论和优先级

## 流程重点

1. 明确审查对象和验收标准
2. 收集当前实现、测试和文档证据
3. 按严重程度列出问题
4. 区分确认问题、疑似风险和测试缺口
5. 输出修复建议和验收结论

## 输出重点

- 严重问题优先
- 文件或证据定位
- 影响范围
- 修复建议
- 残余风险

## Post-run Curation

review mode 如果发现需要后续修复、补测、补文档、调整协议或形成验收记录的问题，必须判断 `post_run_curation`。

重点字段：

- `source_candidates`：被审查对象、日志、报告、测试输出或用户材料
- `action_candidates`：确认问题、补测项、修复建议、后续审查项
- `artifact_plan`：是否建议形成 review record、acceptance report、backlog 或 run record
- `persistence_decision`：说明是否实际写入；不得把口头建议说成已创建任务或文件

这保证审查结果可以被复盘和执行，而不是只存在于一次对话中。
