# Capability Degradation: Social Listening

## 测试任务

```text
用户要求分析某产品在小红书上的用户反馈；当前不调用 xiaohongshu 或 social-media-analyzer。
```

## 执行声明

```yaml
platform: codex
mode: research
capability: social-listening
external_skills:
  xiaohongshu: unavailable
  social-media-analyzer: unavailable
execution_method: degradation_path
```

## 降级执行

由于没有调用社媒专用工具，think-tank 不能声称已经获取小红书样本、评论、互动率或情绪分布。

可执行降级路径：

1. 请求用户提供样本笔记、评论截图、导出文本或关键词列表。
2. 若可使用公开网页或搜索结果，仅输出观察，不输出总体结论。
3. 明确标注样本量、来源和平台偏差。
4. 情绪判断必须使用 `low` 或 `medium` confidence，除非样本充足且可验证。

## 可输出结果

```yaml
platform: xiaohongshu
sample_size: 0
topics: []
sentiment: "unknown"
engagement_summary: "not_available"
representative_quotes: []
risks:
  - 未调用平台专用采集工具
  - 无法确认样本代表性
  - 无法计算互动率
confidence: low
```

## 验证结论

social-listening capability 可以在外部 skills 不可用时正确降级。它只能输出观察或输入需求，不能输出总体舆情结论。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

