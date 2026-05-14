# Versioning

本文件定义 think-tank 协议和主 Skill 的版本演进规则。

## 版本对象

think-tank 至少包含三类版本：

- `protocol_version`：协议层版本，影响输入、流程、角色、输出和质量门禁。
- `skill_version`：Skill 包装版本，影响文档、示例、平台适配和发布内容。
- `adapter_version`：平台适配版本，影响某个平台的执行方式。

当前协议版本：

```yaml
protocol_version: 0.1.0
```

## 语义化版本

使用 `MAJOR.MINOR.PATCH`：

- `MAJOR`：破坏性协议变更
- `MINOR`：向后兼容的新能力、新 mode、新角色或新平台适配
- `PATCH`：澄清、修正文档、补充示例或不改变语义的改动

## Breaking Change

以下属于破坏性变更：

- 删除或重命名核心阶段
- 改变标准输出结构的字段语义
- 改变 mode 的核心含义
- 改变角色职责导致旧输出不再兼容
- 放宽质量门禁导致旧验收标准失效
- 把平台适配规则上升为协议要求

## 兼容性变更

以下通常属于兼容变更：

- 新增 mode
- 新增可选角色
- 新增平台适配
- 新增输出字段但不改变旧字段语义
- 收紧高风险任务的质量门禁
- 增加示例和迁移说明

## Patch 变更

以下属于 patch：

- 修正错别字
- 澄清说明
- 增加非规范性示例
- 修复目录链接
- 改善 README 可读性

## 版本记录要求

每次协议变更都应记录：

```yaml
version: ""
date: ""
type: major | minor | patch
changed:
  - ""
reason: ""
migration: ""
```

根目录 `CHANGELOG.md` 负责公开记录版本变化。协议层文件只定义版本规则。

## 状态标注

所有平台能力必须标注状态：

- `verified`：真实执行并验证过
- `mock`：只在模拟路径中验证
- `tracking`：只记录状态，不代表真实执行完成
- `planned`：设计目标，尚未实现

版本发布时，不允许把 `mock`、`tracking` 或 `planned` 能力描述为 `verified`。

