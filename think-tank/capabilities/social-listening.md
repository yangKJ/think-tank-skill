# Social Listening

## 目的

收集和分析社交平台、社区、评论、笔记和互动数据中的用户反馈、情绪、痛点和趋势。

## 适用场景

- 用户反馈研究
- 舆情分析
- 竞品口碑观察
- 内容趋势研究
- 社媒互动表现分析

## 输入

```yaml
topic: ""
platforms: []
time_window: ""
sample_size: ""
metrics_required:
  - engagement
  - sentiment
  - topics
  - representative_quotes
```

## 输出

```yaml
platform: ""
sample_size: 0
topics: []
sentiment: ""
engagement_summary: ""
representative_quotes: []
risks: []
confidence: low | medium | high
```

## 候选 skills

- `xiaohongshu`
- `juejin-search`
- `social-media-analyzer`
- `web-access`

## 示例实现

以下为示例，非协议规范。实际 provider 选择由本地 policy 配置决定。

- 社交平台专用 provider
- 社媒分析 provider
- 通用网页抓取 provider
- 内容摘要 provider

## 降级策略

- 平台专用 skill 不可用时，使用公开网页、搜索结果或用户提供样本。
- 样本不足时，不输出总体结论，只输出观察。
- 情绪判断必须标注样本量和置信度。
