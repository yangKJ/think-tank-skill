# Media Production

## 目的

从研究材料、来源证据、脚本、素材和平台 provider 组合中生产可验收的媒体成品。

`media-production` 负责“产出媒体 artifact”的通用能力槽；`media-processing` 负责“读取、转录、摘要或分析已有媒体”。两者可以组合，但不能互相替代。

## 适用场景

- 用户要求生成资讯视频、产品介绍视频、研究转视频、音频简报或可播放演示。
- 任务需要从来源研究进入脚本、口播、字幕、素材、合成和最终文件交付。
- 成品质量依赖真实素材、来源清单、渲染检查、音轨检查或关键帧验收。
- 需要把一次媒体制作沉淀为 run record、runbook、样例或后续可复用模板。

不适用：

- 只需要摘要已有视频、播客或音频时，使用 `media-processing`。
- 只需要收集网页、图片或报告来源时，使用 `source-acquisition`。
- 只需要写文案而不生成媒体 artifact 时，可使用 research、strategy 或 content planning 流程，不必声明媒体生产已完成。

## 输入

```yaml
media_request:
  output_type: video | audio | web_presentation | image_sequence | other
  topic: ""
  audience: ""
  aspect_ratio: "16:9 | 9:16 | 1:1 | other"
  duration_target_seconds: 0
  language: auto
  required_sources: []
  required_assets: []
  narration_required: true | false
  subtitles_required: true | false
  bgm_required: true | false
  optional_user_supplied_assets:
    bgm:
      required_for: final_polish
      accepted_formats: [mp3, wav, m4a]
      preferred_destination: assets/audio/bgm.mp3
      can_be_provided_at:
        - before_generation
        - after_draft_render
      missing_behavior: produce_draft_without_bgm
      upgrade_action: attach_bgm_and_rerender
  rights_boundary: personal_review | internal_review | publish_candidate | commercial_release
  quality_gates:
    - source_manifest
    - asset_presence
    - narration_subtitle_alignment
    - render_probe
    - keyframe_review
```

## 输出

```yaml
media_production_result:
  artifact_paths: []
  source_manifest_path: ""
  asset_manifest_path: ""
  script_path: ""
  narration_paths: []
  subtitle_tracks: []
  render_outputs: []
  verification:
    commands_run: []
    keyframes_checked: []
    audio_probe: {}
    video_probe: {}
    quality_gate_status:
      source_manifest: pass | fail | partial | not_applicable
      asset_presence: pass | fail | partial | not_applicable
      narration_subtitle_alignment: pass | fail | partial | not_applicable
      render_probe: pass | fail | partial | not_applicable
      keyframe_review: pass | fail | partial | not_applicable
  known_gaps: []
  upgrade_path: ""
  output_status: draft_without_bgm | review_candidate | final_with_bgm | blocked
  rights_boundary: personal_review | internal_review | publish_candidate | commercial_release
  verification_status: verified | verified_partial | failed | blocked
```

## 候选 skills

候选实现由平台 adapter 或项目本地 registry 声明，think-tank core 只要求能力契约，不写死具体 provider。

可能的 provider 类型：

- source acquisition provider：获取公开来源、官方公告、网页、图片或引用。
- browser automation provider：生成页面截图、检查动态网页或本地预览。
- image or visual provider：生成辅助视觉、处理素材或导出图像序列。
- TTS provider：生成口播音频。
- subtitle provider：生成、对齐或检查字幕。
- render provider：合成 HTML/video/audio 并导出成品。
- probe provider：检查分辨率、时长、音轨、关键帧和文件存在性。

具体 skill 名只可出现在 `platforms/<platform>/`、本地 provider registry 或用户显式上下文中。

## 降级策略

- 来源不足：降级为脚本草案或研究 brief，不声称生成合格媒体成品。
- 真实素材不足：替换选题、请求用户素材，或输出 `blocked`；不得用假截图、假界面或纯抽象图冒充证据素材。
- 口播 provider 不可用：生成文本脚本和字幕草案，标记 `narration_missing`。
- BGM provider 或本地 BGM 缺失：先输出 `draft_without_bgm` 或 `review_candidate`，保留主体视频；最终交付必须说明用户可在生成前或生成后提供 BGM，并给出 `attach_bgm_and_rerender` 升级路径。
- 浏览器或截图 provider 不可用：使用静态来源图、官方 OG 图或用户提供截图，并说明动态页面未验证。
- 渲染 provider 不可用：输出项目源文件、脚本和素材包，标记 `render_blocked`。
- 质量门禁失败：停止升级为 `verified`，最多标记 `verified_partial`，并列出失败门禁和下一步。

## 媒体生产门禁

媒体生产任务在最终输出前应接入：

```text
protocol/artifact-quality-gates.md
protocol/post-run-curation.md
```

最低要求：

- 每个外部 claim 至少有来源候选或明确的缺失边界。
- 每个新闻、产品或事实卡片至少有一个可追溯素材或明确标记为未完成。
- 每段口播若进入最终成品，必须有对应字幕或明确说明无字幕的原因。
- 最终媒体文件必须通过基本 probe：存在、非空、时长、分辨率或音轨符合预期。
- 至少抽查关键帧，确认没有空白、重叠、串屏、遮挡核心素材或字幕越界。
- 用户可后补素材必须写清楚：接受格式、推荐路径、可提供时机、缺失时的输出状态和升级动作。
