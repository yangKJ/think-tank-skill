# Templates

`templates/` 存放从旧 think-tank 迁移并重写后的跨平台输出模板。

这些模板不是平台 adapter，也不是旧 Claude Code Agent Team 文档。它们只定义 think-tank 输出应该如何组织。

## Templates

- `deep-research.md`：research mode 的深度研究报告。
- `expert-meeting.md`：council mode 的专家会议纪要。
- `task-kickoff.md`：strategy/review/research 任务启动前的执行规划。
- `research-to-video-brief.md`：`research_to_video` 的选题、来源、证据、素材和 BGM 输入 brief。
- `video-storyboard.md`：`research-to-video` 的镜头级分镜、素材表和音频时间线。
- `media-run-record.md`：`research-to-video` 的 provider 调用、生成产物、质量门禁和升级路径记录。

## Required Fields

模板必须包含：

- mode
- profiles
- capabilities
- runtime_provenance
- sources/evidence 或 discussion inputs
- disagreements
- risks
- boundaries
- action recommendations
- quality_check

## Boundary

模板可以被 Claude Code、Codex 或其他平台填充，但不得要求某个平台的私有工具。
