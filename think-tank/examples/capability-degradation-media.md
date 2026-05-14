# Capability Degradation: Media Processing

## 测试任务

```text
用户提供一个视频链接，要求提取关键观点；当前不调用 yt-dlp、Whisper 或 summarize。
```

## 执行声明

```yaml
platform: codex
mode: research
capability: media-processing
external_skills:
  yt-dlp: unavailable
  openai-whisper: unavailable
  summarize: unavailable
execution_method: degradation_path
```

## 降级执行

由于没有调用媒体处理工具，think-tank 不能声称已经下载、转录或完整观看视频。

可执行降级路径：

1. 请求用户提供视频标题、描述、摘要或转录文本。
2. 如果页面公开信息可访问，可只基于标题、描述、评论或已有文字稿分析。
3. 如果没有任何文本材料，输出无法完成媒体内容提取的边界。

## 可输出结果

```yaml
summary: ""
key_points: []
evidence: []
limitations:
  - 未下载视频
  - 未转录音频
  - 未验证视频完整内容
  - 只能基于用户提供文本或公开页面信息分析
```

## 验证结论

media-processing capability 可以在外部 skills 不可用时正确降级。它不会伪装成已处理媒体，而是要求替代输入或明确边界。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

