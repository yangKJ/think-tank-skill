# capabilities

`capabilities/` 定义 think-tank 可编排的能力槽。

能力槽不是具体 skill，也不是平台 API。它描述 think-tank 在完成任务时可能需要的外部能力，以及这些能力的输入输出契约、候选技能和降级策略。

## 为什么需要能力槽

think-tank 是高阶协议 Skill，不应该复制 `yt-dlp`、`obsidian`、`playwright-cli`、`xiaohongshu` 等工具型 skill。

正确关系是：

```text
think-tank
  -> 识别任务和 mode
  -> 选择 roles/profiles
  -> 选择 capabilities
  -> 由平台 adapter 调用可用 skills
  -> 回收结果并按协议汇总
```

## 第一批能力槽

- `source-acquisition.md`：网页、官方来源、社区、报告、数据源获取
- `media-processing.md`：视频、音频、播客、字幕和转录
- `social-listening.md`：社媒内容、评论、互动和舆情
- `knowledge-persistence.md`：报告、brief、笔记和知识库沉淀
- `browser-automation.md`：需要真实浏览器或交互环境的网页任务

## 设计边界

能力槽可以列出候选 skills，但不能依赖某个 skill 必然存在。

平台 adapter 负责：

- 发现当前可用 skills
- 选择最合适的 skill
- 处理权限和失败
- 将结果转换回 think-tank 输出契约

