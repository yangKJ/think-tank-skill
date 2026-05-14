# Media Research Recipe

```yaml
intent: media_research
default_mode: research
core_question: "视频、播客、音频或长内容中有哪些可用信息和结论？"
optional_peer_skills_are_dependencies: false
```

## Triggers

- `这个视频讲了什么`
- `总结这个播客`
- `转录`
- `提取视频内容`
- `音频分析`
- `长内容摘要`

## Defaults

```yaml
profiles:
  - source-collector
  - report-architect
  - skeptic
capabilities:
  - media-processing
  - source-acquisition
optional_peer_skills:
  - yt-dlp
  - openai-whisper
  - xiaoyuzhou-transcribe
  - summarize
fallback_inputs:
  - user_provided_transcript
  - user_provided_summary
  - local_media_metadata
```

## Required Analysis

1. 内容来源和处理方式。
2. 核心观点和证据。
3. 可引用片段或时间点。
4. 对用户任务的行动建议。
5. 未转录、不可访问或版权边界。

## Output

```text
结论
内容摘要
关键证据
可行动洞察
风险和边界
```
