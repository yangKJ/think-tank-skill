# Media Processing

## 目的

处理视频、音频、播客、字幕和转录，提取可用于研究或讨论的内容。

## 适用场景

- 用户提供视频或播客链接
- 研究资料以视频、音频、直播、课程或访谈形式存在
- 需要从媒体内容中提取观点、事实或证据

## 输入

```yaml
media_url: ""
media_type: video | audio | podcast | unknown
desired_output: transcript | summary | evidence | clips
language: auto
```

## 输出

```yaml
transcript_path: ""
summary: ""
key_points: []
evidence: []
timestamps: []
limitations: []
```

## 候选 skills

- `yt-dlp`
- `openai-whisper`
- `xiaoyuzhou-transcribe`
- `summarize`

## 降级策略

- 若不能下载媒体，尝试页面摘要或公开文字稿。
- 若不能转录，提取标题、描述、评论和已有摘要。
- 若媒体平台存在访问限制，标注未覆盖内容。

