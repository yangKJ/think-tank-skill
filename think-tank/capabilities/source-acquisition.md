# Source Acquisition

## 目的

获取外部或本地来源中的事实、资料、数据、文档和上下文。

## 适用场景

- 研究问题需要证据
- 需要当前信息
- 需要官方文档、报告、社区讨论或新闻来源
- 需要对多个来源进行交叉验证

## 输入

```yaml
query: ""
source_types:
  - official
  - documentation
  - web
  - community
  - news
  - report
  - local_knowledge
constraints: []
freshness_required: true
citations_required: true
```

## 输出

```yaml
sources:
  - title: ""
    url: ""
    source_type: ""
    summary: ""
    reliability: low | medium | high
    freshness: ""
    extracted_at: ""
gaps: []
```

## 示例实现

以下为示例，非协议规范。实际 provider 选择由本地 policy 配置决定。

- 通用网页搜索与抓取 provider
- AI 增强搜索 provider
- 技术社区搜索 provider
- 行业热榜 provider
- PDF 提取 provider
- 命令行资料获取 provider

## 降级策略

- 首选一手来源。
- 找不到一手来源时，可使用权威二手来源，并标注边界。
- 当前信息无法获取时，必须说明未验证。
- 工具不可用时，可使用用户提供资料或本地知识库。

