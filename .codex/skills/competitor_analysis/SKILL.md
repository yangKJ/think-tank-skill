---
name: competitor_analysis
description: |
  竞品分析技能 - iOS 图像编辑 App 竞品分析。
  使用 WebFetch + playwright-cli + obsidian 三技能联动，
  自动从 App Store、掘金等平台获取竞品信息，生成 Markdown 分析报告保存到 Obsidian。
  触发场景：用户说"竞品分析"、"分析一下竞品"、"竞品动态"
---

# 竞品分析技能 ⭐

**研究员 Agent 必须掌握的竞品分析规范**

---

## 一、核心竞品列表

### 🔴 重点竞品（必须深度分析）

| 竞品 | App Store ID | 定位 | 月下载量 | 评分 | 核心新技术 |
|------|-------------|------|----------|------|------------|
| VSCO | id588013825 | 专业滤镜 | 5000万+ | 4.6 | Neural Filter、AI 滤镜策展 |
| Snapseed | id439697863 | 谷歌出品 | 1亿+ | 4.5 | Google AI 增强、样式匹配 |
| Lightroom | id1470781278 | Adobe 专业 | 5000万+ | 4.7 | AI 降噪、Raw AI、镜头模糊 |
| 醒图 | id1618506205 | 国内竞品 | 5000万+ | 4.5 | AI 消除、AI 写真、模板 |
| 美图秀秀 | id415478207 | 国内巨头 | 1亿+ | 4.2 | AI 美颜、AI 绘图、换装 |

### 🟡 新兴竞品（需要关注）

| 竞品 | 定位 | 新技术方向 |
|------|------|-----------|
| 像素蛋糕 | 人像精修 | AI 精修、AI 抠图 |
| 泼辣修图 | 专业功能 | AI 液化、曲线 AI |
| PicsArt | 功能丰富 | AI 艺术生成、对象识别 |
| Afterlight | 简约滤镜 | 胶片模拟、怀旧滤镜 |
| Photoroom | 背景处理 | AI 背景移除、AI 产品图 |
| Fotor | 多平台 | AI 增强、AI 修图 |
| Pixlr | 快速编辑 | AI 头像、AI 拼图 |

### 🎯 重点监控竞品（AI 技术领先）

| 竞品 | AI 技术亮点 | 技术调研优先级 |
|------|-----------|---------------|
| 醒图 | AI 消除、AI 写真、模板工厂 | ⭐⭐⭐ 高 |
| Lightroom | Neural Engine、AI 降噪、Raw 处理 | ⭐⭐⭐ 高 |
| 美图 | AI 绘图、AI 美颜、AI 换装 | ⭐⭐ 高 |
| PicsArt | AI 艺术生成、对象识别 | ⭐⭐ 中 |

---

## 🎯 核心目标：新技术调研（最重要）

🚨 **竞品分析的核心目的不是功能对比，而是新技术调研！**

### 新技术调研优先级

| 优先级 | 技术方向 | 竞品 | 调研深度 |
|--------|----------|------|----------|
| P0 | AI 消除/修复 | 醒图、TouchRetouch | ⭐⭐⭐ 深入调研 |
| P0 | Neural Engine 加速 | Lightroom、Apple Photos | ⭐⭐⭐ 深入调研 |
| P1 | 生成式 AI (Inpainting/Outpainting) | 美图、Photoleap | ⭐⭐ 重点关注 |
| P1 | AI 人像分割 | Prisma、Photomator | ⭐⭐ 重点关注 |
| P2 | Metal GPU 实时处理 | Adobe、全链路 | ⭐ 一般关注 |
| P2 | 胶片模拟/预设 | Filmbox、VSCO | ⭐ 一般关注 |

### 新技术调研输出模板

```markdown
## [新技术名称] 技术调研报告

### 技术概述
- 技术原理：
- 实现难度：低/中/高
- Apple 生态支持：Yes/No

### 竞品应用案例
| 竞品 | 应用场景 | 实现效果 |
|------|----------|----------|
| 醒图 | AI 消除 | 边缘自然、无残影 |
| Lightroom | AI 降噪 | Neural Engine 加速 |

### 技术文档调研
- Apple CoreML 文档：
- Apple Neural Engine 文档：
- 第三方实现方案：

### 对 Awakening 的建议
- 可行性评估：
- 实现路径：
- 优先级建议：
```

### 新技术调研流程

```
1. 发现竞品新技术 → 立即记录到 Obsidian
2. 深挖技术原理 → 搜索 Apple 文档、WWDC 视频
3. 评估实现难度 → 技术栈兼容性、团队能力
4. 输出技术调研报告 → 保存到 /Users/condy/Desktop/Obsidian/技术调研/
5. 同步给开发团队 → 通过 CLAUDE.md 或直接沟通
```

---

## 🔬 新技术深度调研规范

### 调研技能组合

| 调研类型 | 技能组合 | 输出 |
|---------|---------|------|
| AI 功能调研 | web-access + omni-research + summarize | 技术原理 + 实现方案 |
| Apple 生态调研 | web-access + juejin-search + WWDC 视频 | CoreML/Neural Engine 文档 |
| 竞品技术调研 | competitor_analysis + xiaohongshu + social-media-analyzer | 用户反馈 + 市场验证 |
| 视频技术调研 | yt-dlp + whisper + summarize | WWDC/技术演讲转录 |

### 新技术调研检查清单

```markdown
### [新技术] 深度调研清单

#### 1. 技术原理
- [ ] 技术名称和分类
- [ ] 基本原理（如何实现）
- [ ] Apple 官方文档链接

#### 2. 竞品应用
- [ ] 哪些竞品在使用
- [ ] 具体应用场景
- [ ] 用户评价如何（搜索小红书/知乎）

#### 3. 实现方案
- [ ] Apple 生态实现方式（CoreML? Vision? Metal?）
- [ ] 第三方库/开源方案
- [ ] 实现难度和工期估算

#### 4. 对 Awakening 的价值
- [ ] 与现有功能的整合方案
- [ ] 优先级建议（P0/P1/P2）
- [ ] 潜在风险和挑战

#### 5. 技术文档归档
- [ ] 保存到 /Users/condy/Desktop/Obsidian/技术调研/
- [ ] 标记为已验证/待验证
```

### 可借鉴技术参考（2026-05-10 最新）

| 技术 | 实现难度 | 参考价值 | 优先级 |
|------|----------|---------|--------|
| **AI 消除（Generative Inpaint）** | 中高 | 必备功能，需达到 TouchRetouch 水平 | P0 |
| **Neural Engine 加速推理** | 中 | CoreML 框架支持，需优化 ANE 利用率 | P0 |
| **Metal 实时滤镜渲染** | 中 | Metal Performance Shaders 实现无延迟预览 | P1 |
| **生成式扩展（Outpainting）** | 高 | iOS 27 趋势，需 Stable Diffusion 类模型 | P1 |
| **人像精确分割** | 中 | Portrait Segmentation 是很多功能基础 | P1 |
| **胶片模拟预设系统** | 中 | 可建立自有色彩科学 + 社群分享机制 | P2 |
| **RAW 专业工作流** | 高 | 需 Color Management 深度集成 | P2 |
| **AI 品质增强（超分辨率/降噪）** | 中 | Super Resolution 已成熟，ANE 可加速 | P1 |

---

## 二、四技能联动工作流

```
┌─────────────────────────────────────────────────────────────┐
│                    竞品分析完整工作流                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣ web-access                                             │
│     └── CDP 模式获取 App Store、掘金等页面数据（无头稳定）    │
│                                                             │
│           ↓                                                  │
│                                                             │
│  2️⃣ playwright-cli                                          │
│     └── 仅用于需要 Playwright 特定功能的场景                 │
│                                                             │
│           ↓                                                  │
│                                                             │
│  3️⃣ obsidian                                                │
│     └── 生成分析报告、保存到 Obsidian 仓库                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**优先级原则**：
- 优先使用 web-access（CDP 稳定无头）
- playwright-cli 仅在需要特定 Playwright 功能时使用
- 最终报告 → 保存到 Obsidian

---

## 三、信息获取方式

### web-access CDP（首选 - 稳定无头）

```bash
# 启动 CDP 代理
node "$CLAUDE_SKILL_DIR/scripts/check-deps.mjs"

# 获取 App Store 页面
curl -s "http://localhost:3456/new?url=https://apps.apple.com/cn/app/vsco-photo-video-collage/id588013825"
curl -s "http://localhost:3456/eval?target=ID" -d 'document.body.innerText'

# 搜索掘金
curl -s "http://localhost:3456/new?url=https://juejin.cn/search?query=VSCO滤镜技术"
curl -s "http://localhost:3456/eval?target=ID" -d 'document.body.innerText'

# 截图
curl -s "http://localhost:3456/screenshot?target=ID&file=/tmp/screenshot.png"
```

### 工具选择

| 场景 | 工具 | 说明 |
|------|------|------|
| App Store 页面 | web-access CDP | 稳定无头，不打扰用户 |
| 掘金搜索 | web-access CDP | 可获取完整搜索结果 |
| 需要 Playwright 特定功能 | playwright-cli | 备用选项 |
| 最终报告 | Write → Obsidian | 保存到 Obsidian 仓库 |

---

## 四、分析维度

### 1. 功能对比

| 功能 | Awakening | VSCO | Snapseed | Lightroom |
|------|-----------|------|----------|-----------|
| 滤镜 | ✅ | ✅ | ✅ | ✅ |
| 蒙版 | ✅ | ❌ | ❌ | ✅ |
| 撤销/重做 | ✅ | ✅ | ✅ | ✅ |
| 多图编辑 | ✅ | ❌ | ❌ | ✅ |

### 2. 商业化对比

| 竞品 | 定价 | 订阅模式 |
|------|------|----------|
| VSCO | ¥68/年 | 高级滤镜 |
| Lightroom | ¥148/月 | 全功能 |
| PicsArt | 免费+订阅 | 解锁功能 |

---

## 五、完整操作流程

### Step 1: 获取 App Store 数据（web-access CDP）

```bash
# 获取竞品基本信息（稳定无头）
curl -s "http://localhost:3456/new?url=https://apps.apple.com/cn/app/vsco-photo-video-collage/id588013825"
curl -s "http://localhost:3456/eval?target=ID" -d 'document.body.innerText'

# 提取：版本号、评分、更新时间、描述
```

### Step 2: 搜索掘金相关讨论（web-access CDP）

```bash
# 使用 CDP 无头浏览（稳定快速）
curl -s "http://localhost:3456/new?url=https://juejin.cn/search?query=VSCO滤镜技术"
curl -s "http://localhost:3456/eval?target=ID" -d 'document.body.innerText'

# 仅在需要截图或复杂交互时使用 playwright-cli
# playwright-cli open "https://juejin.cn/search?query=VSCO滤镜技术" --browser=chromium
```

### Step 3: 保存到 Obsidian（Write 工具）

报告保存路径：
```
/Users/condy/Desktop/Obsidian/竞品分析-竞品名-YYYYMMDD.md
```

---

## 六、分析报告模板

```markdown
# [竞品名] 竞品分析报告

> 分析日期：[YYYY-MM-DD]
> 数据来源：App Store / 掘金

## 基本信息

| 项目 | 内容 |
|------|------|
| App Store | [链接] |
| 版本 | [版本号] |
| 更新日期 | [日期] |
| 评分 | [X.X 分] |
| 下载量 | [数量] |

## 核心功能
1. 功能1
2. 功能2
3. 功能3

## 差异化亮点
- 亮点1
- 亮点2

## 社区讨论
[来自掘金/小红书/知乎的用户讨论摘要]

## SWOT 分析
- **优势 (S)**：
- **劣势 (W)**：
- **机会 (O)**：
- **威胁 (T)**：

## 结论
- **借鉴**：我们可以学习的地方
- **超越**：我们可以做得更好的地方

---

> 💡 由 competitor_analysis + web-access + obsidian 技能生成
```

---

## 七、竞品关键词搜索表

### App Store 链接模板

```
https://apps.apple.com/cn/app/[竞品名]/id[AppID]
```

### 掘金搜索关键词

| 竞品 | 搜索关键词 |
|------|-----------|
| VSCO | "VSCO 滤镜" / "VSCO 调色技巧" |
| Snapseed | "Snapseed 使用教程" |
| Lightroom | "Lightroom Mobile 技巧" |
| 醒图 | "醒图 App 功能" / "醒图 AI 消除" |

---

## 八、输出规范

| 输出 | 频率 | 保存位置 |
|------|------|----------|
| 竞品动态快报 | 发现重大更新时 | `/Users/condy/Desktop/Obsidian/` |
| 竞品分析报告 | 每季度 | `/Users/condy/Desktop/Obsidian/竞品分析-竞品名-YYYYMMDD.md` |
| 月度竞品总结 | 每月1日 | `/Users/condy/Desktop/Obsidian/月度竞品动态-YYYYMM.md` |

---

## 九、注意事项

### WebFetch 适用场景
- App Store 页面（静态内容）
- 官网介绍（静态页面）
- 评测文章（静态页面）

### playwright-cli 适用场景
- 需要登录才能查看的内容
- 需要点击/滚动加载更多内容
- 动态渲染的页面

### 性能优化
- 优先使用 web-access CDP 获取静态数据（App Store、掘金）
- 避免用 playwright-cli 打开内容过多的页面
- 需要交互时再切换 playwright-cli

---

*版本: v1.2.0 | 更新日期: 2026-05-10 | 联动: web-access + playwright-cli + obsidian*