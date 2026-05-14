---
name: research-workflow
description: |
  研究工作流技能 - 整合多技能的研究员助手。
  当你需要研究任何主题（竞品、市场、技术、趋势）时，智能选择最佳技能组合，
  自动协调 web-access、summarize、yt-dlp、openai-whisper、xiaohongshu、juejin-search、competitor_analysis、omni-research、obsidian 等技能。
  触发场景：用户说"研究一下"、"竞品分析"、"深度调研"、"帮我了解一下"、"全面研究"、"行业分析"
---

# 研究工作流技能 🔬

整合 16 个技能的研究员助手，根据研究深度和场景自动选择最佳工具组合。

## 依赖工具

| 工具 | 安装方式 | 用途 |
|------|----------|------|
| `summarize` | `brew install steipete/tap/summarize` | URL/文件/YouTube 快速总结 |
| `obsidian-cli` | `brew install yakitrak/yakitrak/obsidian-cli` | Obsidian 笔记管理 |
| `web-access` | 内置 CDP 代理 (localhost:3456) | 网页数据获取 |
| `yt-dlp` | `brew install yt-dlp` | 视频下载（YouTube/TikTok等） |
| `whisper` | `brew install openai-whisper` | 音频/视频转文字（本地） |

**注意**：如果工具未安装，技能会降级使用 web-access + 手动处理。

## 一、技能地图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          研究工作流技能地图 v2.0                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📊 快速了解                                                                │
│  web-access + summarize → 快速提炼关键信息                                  │
│                                                                             │
│  🎬 视频研究                                                                │
│  yt-dlp + whisper → 视频内容提取/转录                                      │
│                                                                             │
│  🔍 深度研究                                                                │
│  juejin-search + competitor_analysis → 结构化分析                           │
│                                                                             │
│  📱 社媒舆情                                                                │
│  xiaohongshu → 小红书笔记/评论/舆情                                         │
│                                                                             │
│  📈 数据分析                                                                │
│  social-media-analyzer → 社交媒体 engagement rate、ROI 分析                │
│                                                                             │
│  📄 PDF 研究                                                                │
│  pdf-extraction → 研究报告、白皮书深度解读                                  │
│                                                                             │
│  🕸️ 知识图谱                                                                │
│  knowledge-graph-builder → 竞品关系、趋势追踪、知识沉淀                      │
│                                                                             │
│  🚀 自主探索                                                                │
│  omni-research → 深度研究直到饱和                                          │
│                                                                             │
│  💾 知识沉淀                                                                │
│  obsidian → 保存报告、避免重复研究                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 二、三种研究模式

### 模式 A：快速概览（⚡ 5 分钟）

当用户需要快速了解某事物时使用：
```
web-access + summarize → 提炼要点
```

**触发词**："快速了解一下"、"简单看看"、"先了解一下"、"概况"

**流程**：
```bash
# 1. 获取页面
curl -s "http://localhost:3456/new?url=https://apps.apple.com/cn/app/vsco-photo-video-collage/id588013825"

# 2. 快速总结
summarize "https://apps.apple.com/cn/app/vsco-photo-video-collage/id588013825" --extract-only

# 3. 保存到 Obsidian（可选）
# 写入 /Users/condy/Desktop/Obsidian/快速概览-竞品名-YYYYMMDD.md
```

---

### 模式 B：深度研究（📚 30 分钟）

当用户需要系统性研究时使用：
```
omni-research + juejin-search + competitor_analysis + obsidian
```

**触发词**："深度研究"、"全面研究"、"系统分析"、"好好研究一下"

**流程**：
```
1. [可选] 检查 Obsidian 是否已有相关研究
2. 用 omni-research 启动自主研究循环
3. 或手动：juejin-search → competitor_analysis → obsidian
```

**omni-research 完整流程**：
```bash
# 启动 omni-research（交互式）
/omni-research

# 或带主题（跳过交互）
/omni-research "VSCO 商业模式和用户评价研究"
```

**手动深度研究**：
```bash
# 1. 搜索掘金社区讨论
curl -s "http://localhost:3456/new?url=https://juejin.cn/search?query=VSCO滤镜"
curl -s "http://localhost:3456/eval?target=ID" -d 'document.body.innerText'

# 2. 结构化竞品分析
# 参考 competitor_analysis 技能文档

# 3. 保存报告
# 写入 /Users/condy/Desktop/Obsidian/竞品分析-VSCO-YYYYMMDD.md
```

---

### 模式 C：持续监控（📅 长期）

当用户需要定期追踪某事物时使用：
```
taskflow + web-access + obsidian
```

**触发词**："持续监控"、"定期追踪"、"关注"、"监控"

**流程**：
```bash
# 1. 创建监控任务（参考 taskflow 技能）
# 使用 taskflow 创建持续监控流

# 2. 定期获取数据
curl -s "http://localhost:3456/new?url=https://apps.apple.com/cn/app/vsco-photo-video-collage/id588013825"
curl -s "http://localhost:3456/eval?target=ID" -d 'document.body.innerText'

# 3. 检测更新，有变化则记录
# 写入 /Users/condy/Desktop/Obsidian/竞品动态-YYYYMMDD.md
```

---

## 三、智能选择指南

| 需求 | 推荐模式 | 技能组合 |
|------|----------|----------|
| "VSCO 是什么？" | ⚡快速概览 | web-access + summarize |
| "VSCO 商业模式分析" | 📚深度研究 | competitor_analysis + obsidian |
| "调研图像编辑行业趋势" | 🚀自主探索 | omni-research（替代 google-ai-mode） |
| "最近有什么新动态？" | 🚀自主探索 | omni-research |
| "每周监控竞品更新" | 📅持续监控 | taskflow + web-access + obsidian |
| "全面了解醒图" | 📚深度研究 | omni-research + competitor_analysis |
| "小红书上的用户评价" | 📱社媒舆情 | xiaohongshu + obsidian |
| "分析醒图的舆情" | 📱社媒舆情 | xiaohongshu + summarize |
| "这个视频讲了什么？" | 🎬视频研究 | yt-dlp + whisper |
| "提取播客内容" | 🎬视频研究 | whisper + summarize |
| "分析竞品社交媒体表现" | 📈数据分析 | social-media-analyzer + web-access |
| "解读行业白皮书" | 📄PDF研究 | pdf-extraction + summarize |
| "构建竞品知识图谱" | 🕸️知识图谱 | knowledge-graph-builder + web-access + obsidian |

---

## 四、竞品研究标准流程

### 快速竞品概览
```bash
# 1. 获取 App Store 信息
TARGET=$(curl -s "http://localhost:3456/new?url=https://apps.apple.com/cn/app/vsco-photo-video-collage/id588013825" | grep -o '"id":"[^"]*"' | head -1)
curl -s "http://localhost:3456/eval?target=${TARGET#*\"}" -d 'document.body.innerText' | head -100

# 2. 快速总结
summarize "https://apps.apple.com/cn/app/vsco-photo-video-collage/id588013825" --extract-only

# 3. 搜索社区讨论
curl -s "http://localhost:3456/new?url=https://juejin.cn/search?query=VSCO滤镜效果"
```

### 深度竞品分析
```bash
# 1. 用 omni-research 启动
/omni-research "醒图 App 竞品分析 - 功能、定位、用户评价"

# 2. 或手动分步
# juejin-search → 搜索社区讨论
# competitor_analysis → 结构化分析
# obsidian → 生成报告
```

### 小红书舆情研究
```bash
# 1. 启动 xiaohongshu MCP 服务
cd .codex/skills/xiaohongshu/scripts/
./start-mcp.sh

# 2. 搜索相关笔记
mcp-call.sh search_feeds "关键词=VSCO滤镜"

# 3. 获取笔记详情
mcp-call.sh get_note_detail "feed_id=xxx&xsec_token=xxx"

# 4. 分析评论情感
# 参考 xiaohongshu 技能文档

# 5. 生成舆情报告保存到 Obsidian
```

---

## 五、研究交付规范

### 快速概览（< 10 分钟）
- 直接返回关键发现
- 可选保存到 Obsidian

### 深度研究（> 30 分钟）
- 生成完整报告
- 保存到 `/Users/condy/Desktop/Obsidian/`
- 命名格式：`[类型]-[主题]-YYYYMMDD.md`

### 持续监控
- 创建 taskflow 跟踪进度
- 每次更新保存到 Obsidian
- 重大变化立即通知

---

## 六、Obsidian 检查（避免重复）

研究开始前，先检查是否已有相关笔记：

```bash
obsidian-cli search-content "VSCO"
obsidian-cli list
```

---

*版本: v1.4.0 | 更新日期: 2026-05-10 | 整合: web-access + summarize + juejin-search + competitor_analysis + omni-research + google-ai-mode + obsidian + xiaohongshu + yt-dlp + whisper + pdf-extraction + social-media-analyzer + knowledge-graph-builder + 36kr-hotlist + xiaoyuzhou-transcribe*

---

## 四、技能联动实战

### 联动 1：竞品深度调研（30分钟）

```
┌──────────────────────────────────────────────────────────────────┐
│  omni-research + competitor_analysis + obsidian                  │
│  → 完整竞品分析报告                                              │
└──────────────────────────────────────────────────────────────────┘

步骤：
1. omni-research "VSCO 商业模式、用户评价、竞争格局"
2. competitor_analysis 整理结构化分析
3. obsidian 保存报告到 /Users/condy/Desktop/Obsidian/竞品分析-VSCO-YYYYMMDD.md
```

### 联动 2：舆情分析（20分钟）

```
┌──────────────────────────────────────────────────────────────────┐
│  xiaohongshu + social-media-analyzer + summarize                │
│  → 醒图舆情分析报告                                              │
└──────────────────────────────────────────────────────────────────┘

步骤：
1. xiaohongshu → 搜索"醒图 App"相关笔记（热度排序）
2. 获取 Top 10 笔记详情和评论
3. social-media-analyzer → 计算点赞率、互动率
4. summarize → 提炼用户反馈要点
5. obsidian → 保存舆情报告
```

### 联动 3：行业研究（60分钟）

```
┌──────────────────────────────────────────────────────────────────┐
│  pdf-extraction + knowledge-graph-builder + web-access          │
│  → AI 图像编辑行业知识图谱                                        │
└──────────────────────────────────────────────────────────────────┘

步骤：
1. pdf-extraction → 提取行业白皮书关键数据
2. web-access → 获取 App Store 竞品数据、掘金技术文章
3. knowledge-graph-builder → 构建实体关系图谱
   - 竞品（VSCO、醒图、美图）
   - 功能（滤镜、蒙版、AI 消除）
   - 用户群体
   - 技术栈（Metal、Core Image）
4. obsidian → 保存图谱快照

输出示例：
┌─────────────────────────┐
│      Awakening          │
│    (产品 - 图像编辑)     │
│         ↑               │
│    竞争关系 → VSCO      │
│    技术相似 → Snapseed  │
│    用户重叠 → 醒图      │
│    功能借鉴 → Lightroom │
└─────────────────────────┘
```

### 联动 4：视频内容研究（15分钟）

```
┌──────────────────────────────────────────────────────────────────┐
│  yt-dlp + whisper + summarize                                    │
│  → 提取 B 站/YouTube 视频精华                                    │
└──────────────────────────────────────────────────────────────────┘

步骤：
1. yt-dlp "视频URL" → 下载视频
2. whisper "视频文件" → 转文字
3. summarize --extract-only → 提炼关键内容
4. 存 obsidian 或直接返回
```

---

## 五、工具链组合公式

| 场景 | 工具链 | 输出 |
|------|--------|------|
| 快速了解竞品 | web-access + summarize | 3 句话总结 |
| 深度技术分析 | juejin-search + pdf-extraction | 结构化报告 |
| 舆情监控 | xiaohongshu + social-media-analyzer | 数据仪表盘 |
| 知识沉淀 | web-access + knowledge-graph-builder + obsidian | 可查询知识图谱 |
| 视频研究 | yt-dlp + whisper + summarize | 文字摘要 + 要点 |
| 竞品动态 | taskflow + web-access + competitor_analysis | 定期推送 |
