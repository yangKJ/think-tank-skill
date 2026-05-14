# Legacy Knowledge Index

本文记录旧 research agent `knowledge/` 目录的迁移处置。

旧目录：

```text
/Users/condy/Desktop/img-company/agents/research/knowledge
```

## 结论

```yaml
knowledge_files: 35
disposition: indexed_as_domain_pack_material
copied_into_core_protocol: false
domain_pack: image-editing
```

这些文件是图像编辑、iOS、Awakening、竞品和技术研究知识。它们不属于 think-tank core，但属于 `image-editing` domain pack 的历史素材。

## 文件索引

| 文件 | 分类 | 处置 |
|------|------|------|
| `AI消除功能技术方案-20260511.md` | AI 修图技术 | technology-radar 素材 |
| `Final_Skills_Report.md` | 旧技能总结 | migration audit 素材 |
| `agency-analysis-report.md` | 竞品/市场分析 | report template 素材 |
| `ai_image_restoration_research.md` | AI 修复 | technology-radar 素材 |
| `ai_models_for_image_editing_latest.md` | AI 模型调研 | technology-radar 素材 |
| `awakening/Awakening项目全景综合报告.md` | Awakening 项目知识 | domain-specific reference |
| `awakening/Awakening项目完整概览.md` | Awakening 项目知识 | domain-specific reference |
| `awakening/README.md` | Awakening 索引 | domain-specific reference |
| `awakening/UI组件与交互深度报告.md` | UI/交互 | domain-specific reference |
| `awakening/前端面板架构深度报告.md` | 前端架构 | domain-specific reference |
| `awakening/多图编辑与导出系统深度报告.md` | 图像编辑工作流 | domain-specific reference |
| `awakening/技术架构深度报告.md` | 技术架构 | domain-specific reference |
| `awakening/数据模型深度报告.md` | 数据模型 | domain-specific reference |
| `awakening/未来功能扩张路线图.md` | 产品路线 | strategy mode 素材 |
| `awakening/测试安全与增长报告.md` | 测试/增长 | review/strategy 素材 |
| `awakening/竞品宣传策略调研报告.md` | 竞品/营销 | competitor report 素材 |
| `awakening/运维发布流程分析.md` | 发布流程 | out-of-core project reference |
| `awakening/配置与扩展模块深度报告.md` | 配置/扩展 | domain-specific reference |
| `awakening_missing_ai_models.md` | AI 模型缺口 | technology-radar 素材 |
| `competitor_analysis_method.md` | 竞品方法论 | report-templates 素材 |
| `ios_automation_research_report_2026-05-04.md` | iOS 自动化 | out-of-core technical reference |
| `ios_automation_xcodebuildmcp_integration.md` | iOS 自动化 | out-of-core technical reference |
| `ios_memory_optimization_report.md` | iOS 性能 | technology-radar 素材 |
| `ios_real_device_automation_technical_report.md` | iOS 自动化 | out-of-core technical reference |
| `metal3_mesh_shader_research.md` | Metal 技术 | technology-radar 素材 |
| `metal_gpu_performance_resources.md` | Metal 性能 | technology-radar 素材 |
| `permissive_license_image_enhancement.md` | 开源许可/图像增强 | source-map 素材 |
| `research_tools.md` | 工具清单 | external skill interop 素材 |
| `tools_guide_summary.md` | 工具总结 | external skill interop 素材 |
| `ui_design_learning_resources.md` | UI 学习资源 | domain-specific reference |
| `xcodebuildmcp-ui-automation.md` | iOS UI 自动化 | out-of-core technical reference |
| `xingtu_pixelcake_ai_comparison.md` | 醒图/像素蛋糕竞品 | competitors 素材 |
| `xor_mask_blending_resources.md` | 图像处理技术 | technology-radar 素材 |
| `xor_mask_technology_research.md` | 图像处理技术 | technology-radar 素材 |
| `zero_dce_ios_feasibility_report.md` | 低光增强/iOS 可行性 | technology-radar 素材 |

## 使用边界

- 可作为 image-editing 领域研究上下文。
- 不作为通用 think-tank 协议依赖。
- 不默认打包旧项目私有知识全文。
- 需要复用时应按具体任务挑选，而不是全量塞进上下文。

