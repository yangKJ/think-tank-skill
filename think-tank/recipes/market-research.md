# Market Research Recipe

```yaml
intent: market_research
default_mode: research
core_question: "目标市场、用户需求、趋势和机会是什么？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `市场调研`
- `行业分析`
- `用户需求`
- `市场规模`
- `目标用户`
- `GTM`
- `定位分析`

## Defaults

```yaml
profiles:
  - source-collector
  - trend-analyst
  - feedback-synthesizer
  - product-strategist
  - skeptic
capabilities:
  - source-acquisition
  - social-listening
  - knowledge-persistence
optional_peer_skills:
  - web-access
  - summarize
  - google-ai-mode-skill
  - 36kr-hotlist
  - xiaohongshu
  - social-media-analyzer
  - obsidian
```

## Required Analysis

1. 市场定义和用户分层。
2. 需求强度和付费/采用信号。
3. 趋势、渠道和竞争格局。
4. 机会窗口和进入风险。
5. 可执行验证路径。

## Output

```text
结论
市场和用户画像
关键证据
机会与风险
验证建议
边界
```
