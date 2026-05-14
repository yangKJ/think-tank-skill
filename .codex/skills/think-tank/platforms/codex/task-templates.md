# Codex Task Templates

本文提供 Codex 平台上调用 think-tank 的任务模板。

模板不是协议的替代品。它们只是让用户更容易触发同一套 think-tank 协议。

## Research Mode

适合：调研、资料整理、竞品、技术现状、外部情报。

```text
用 think-tank research mode 调研：

目标：
约束：
已知材料：
需要输出：
不要做：
```

默认 profiles：

```yaml
profiles:
  - source-collector
  - trend-analyst
  - skeptic
  - report-architect
```

## Council Mode

适合：是否应该做、路线争议、方案选择、观点碰撞。

```text
用 think-tank council mode 讨论：

议题：
候选方案：
约束：
希望保留哪些不同观点：
最终要形成什么决策：
```

默认 profiles：

```yaml
profiles:
  - facilitator
  - product-strategist
  - skeptic
  - report-architect
```

## Review Mode

适合：审查代码、文档、架构、产出质量、验收。

```text
用 think-tank review mode 审查：

对象：
验收标准：
重点风险：
已运行验证：
希望输出格式：
```

默认 profiles：

```yaml
profiles:
  - source-collector
  - skeptic
  - product-strategist
  - report-architect
```

## Strategy Mode

适合：长期路线、产品定位、架构演进、优先级。

```text
用 think-tank strategy mode 制定路线：

长期目标：
当前阶段：
资源约束：
候选路径：
不可接受的风险：
希望输出：
```

默认 profiles：

```yaml
profiles:
  - product-strategist
  - skeptic
  - source-collector
  - report-architect
```

## Minimal Install Template

适合：用户只有 think-tank，没有外部工具。

```text
用 think-tank 在最小安装能力下分析：

我提供的材料：
我的问题：
请不要假设你能联网、打开浏览器、下载视频、抓取社媒或写入 Obsidian。
请明确说明哪些判断基于材料，哪些只是推断。
```

## Optional Capability Template

适合：需要尝试 Browser、Playwright、yt-dlp、Obsidian、小红书等能力。

```text
用 think-tank 处理这个任务，并判断是否需要 optional capability：

任务：
可能需要的能力：
如果能力不可用：
  - 不要伪装执行
  - 说明降级方案
  - 告诉我需要补充什么材料
```

## Codex 验收模板

适合：验证 think-tank 本身。

```text
用 think-tank review mode 验收 Codex 平台当前能力：

检查对象：
验收命令：
必须证明：
不能声称：
输出：
  - 通过项
  - 未通过项
  - 风险
  - 下一步
```

