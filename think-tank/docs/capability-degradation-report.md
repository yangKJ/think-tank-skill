# Capability Degradation Report

本文记录 think-tank 在 Codex 平台的 capability 降级测试。

## 验证范围

```yaml
platform: codex
external_skills_invoked: false
purpose: 验证外部 skill 不可用时是否能正确降级和声明边界
```

## 验证结果

```yaml
capability_degradation:
  media_processing_unavailable: verified
  social_listening_unavailable: verified
  knowledge_persistence_local_markdown_only: verified
  browser_automation_unavailable: verified
  browser_automation_codex_localhost_integration: verified_optional
  browser_automation_external_web: verified_partial
  source_acquisition_external_readonly: verified
```

## 验证产物

| capability | 文件 | 状态 |
|------------|------|------|
| media-processing | `examples/quality/capability-degradation-media.md` | verified |
| social-listening | `examples/quality/capability-degradation-social.md` | verified |
| knowledge-persistence | `examples/quality/capability-degradation-knowledge.md` | verified |
| browser-automation unavailable | `examples/quality/capability-degradation-browser.md` | verified |

## 结论

think-tank 在外部 skills 或插件不可用时可以正确降级：

- 不伪装成已下载、转录或处理媒体。
- 不伪装成已抓取社媒样本或计算互动率。
- 不默认写入用户私有知识库。
- 不伪装成已打开浏览器、点击页面或读取 DOM。
- 可以把结果沉淀为当前仓库内的 Markdown artifact。

## 下一阶段判断

现在可以进入单一外部能力最小集成测试，但必须把该测试标记为“可选增强路径”，不能作为 think-tank 的最低可用要求。

建议选择：

```yaml
first_external_capability_candidate: browser-automation
reason:
  - 相比 xiaohongshu，登录和反爬风险更低
  - 相比 obsidian，不涉及用户私有知识库写入
  - 相比 yt-dlp，不涉及下载媒体和转录依赖
  - 与 Codex 当前环境能力最接近
```

## 仍不建议

暂时不建议一次性安装或接入：

- `xiaohongshu`
- `obsidian`
- `yt-dlp`
- `openai-whisper`
- 全量旧 research `.claude/skills`

这些应在 browser-automation 最小集成通过后逐个验证。
