---
name: juejin-search
description: |
  掘金网站帖子搜索技能。支持三种模式：
  1. 关键词搜索 - 使用 web-access (CDP无头浏览器) 搜索任意关键词
  2. 热门排行 - 直接调用掘金 API，获取分类热门文章排行
  3. 内容提取 - 使用 jina-reader 提取完整文章内容转 Markdown

  适用于：竞品调研、技术文章收集、行业动态追踪、热门趋势监控。
  触发场景：用户说"帮我搜一下掘金的xxx帖子"、"去掘金找找xxx相关内容"、"搜索掘金xxx"、"掘金热门文章"、"掘金排行榜"、"看看前端最新文章"
---

# 掘金帖子搜索技能

支持三种工作模式，根据需求选择最佳方式。

## 三模式架构

```
┌─────────────────────────────────────────────────────────────┐
│                    掘金搜索三模式                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🔍 模式 1：关键词搜索（灵活）                               │
│  web-access CDP → 搜索任意关键词                            │
│  适用于：竞品名、技术栈、特定话题                             │
│                                                             │
│           ↓                                                  │
│                                                             │
│  📊 模式 2：热门排行（快速）                                 │
│  juejin-trends.js → 直接 API + UA 轮换                      │
│  适用于：了解行业趋势、发现热门文章                           │
│                                                             │
│           ↓                                                  │
│                                                             │
│  📄 模式 3：内容提取（深入）                                 │
│  jina read <url> → 转 Markdown                              │
│  适用于：深度阅读文章、保存到笔记                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 模式 1：关键词搜索（web-access CDP）

### 工作流程

```
1. [可选] obsidian-cli 搜索是否已有研究
2. web-access CDP 打开搜索页
3. 获取文章链接
4. 生成 Markdown 笔记
5. [可选] obsidian-cli 保存到 Obsidian
```

### 操作步骤

```bash
# Step 1: 打开搜索
curl -s "http://localhost:3456/new?url=https://juejin.cn/search?query=VSCO滤镜"

# Step 2: 获取文章链接
curl -s "http://localhost:3456/eval?target=ID" -d 'JSON.stringify([...document.querySelectorAll("a")].filter(a => a.href.includes("/post/")).slice(0, 20).map(a => ({title: a.textContent?.trim().substring(0, 80), url: a.href})))'

# Step 3: 获取页面文本
curl -s "http://localhost:3456/eval?target=ID" -d 'document.body.innerText'
```

---

## 模式 2：热门排行（直接 API）

### 获取分类列表

```bash
node .codex/skills/juejin-search/scripts/juejin-trends.js categories
```

返回：
```json
[
  { "id": "6809637769959178254", "name": "前端" },
  { "id": "6809637769959178255", "name": "后端" },
  { "id": "6809637769959178257", "name": "iOS" },
  { "id": "6809637769959178258", "name": "人工智能" }
]
```

### 获取热门文章

```bash
# 获取前端热门文章（前 20 篇）
node .codex/skills/juejin-search/scripts/juejin-trends.js articles 6809637769959178254 hot 20

# 获取 iOS 最新文章
node .codex/skills/juejin-search/scripts/juejin-trends.js articles 6809637769959178257 new 10

# 获取 AI 热门文章
node .codex/skills/juejin-search/scripts/juejin-trends.js articles 6809637769959178258 hot 20
```

返回数据包含：
- title、author、articleId
- viewCount、likeCount、collectCount、commentCount
- url、tags

---

## 模式 3：内容提取（jina-reader）

需要安装 jina-reader：
```bash
npx skills add dwsy/agent@jina-reader -g -y
```

```bash
# 读取文章转 Markdown
jina read "https://juejin.cn/post/xxx" --format markdown

# 只提取内容（不用 AI 总结）
jina read "https://juejin.cn/post/xxx" --extract-only

# 指定输出格式
jina read "https://juejin.cn/post/xxx" --format text
```

---

## Obsidian 集成

### 检查已有研究

```bash
obsidian-cli search-content "VSCO"
obsidian-cli list
```

### 保存笔记

```bash
# 保存到 Obsidian
obsidian-cli create "Research/juejin-VSCO-20260510" --content "$(cat markdown-content.md)" --open
```

---

## 完整操作示例

### 示例 1：搜索 VSCO 相关文章

```bash
# 关键词搜索
curl -s "http://localhost:3456/new?url=https://juejin.cn/search?query=VSCO滤镜"
curl -s "http://localhost:3456/eval?target=ID" -d 'document.body.innerText'

# 生成 Markdown 保存到 Obsidian
```

### 示例 2：查看前端热门排行

```bash
# 查看分类
node .codex/skills/juejin-search/scripts/juejin-trends.js categories

# 获取前端热门
node .codex/skills/juejin-search/scripts/juejin-trends.js articles 6809637769959178254 hot 10

# 结果自动格式化输出
```

### 示例 3：深度阅读某篇文章

```bash
# 提取文章内容
jina read "https://juejin.cn/post/7636583332298948623" --format markdown

# 保存到 Obsidian
```

---

## 分类 ID 参考

| 分类 | ID |
|------|-----|
| 后端 | 6809637769959178254 |
| 前端 | 6809637767543259144 |
| Android | 6809635626879549454 |
| iOS | 6809635626661445640 |
| 人工智能 | 6809637773935378440 |
| 开发工具 | 6809637771511070734 |
| 代码人生 | 6809637776263217160 |
| 阅读 | 6809637772874219534 |

---

## 模式选择指南

| 需求 | 推荐模式 | 命令 |
|------|----------|------|
| "搜索 VSCO 相关文章" | 🔍关键词搜索 | web-access CDP |
| "看看前端热门文章" | 📊热门排行 | juejin-trends.js |
| "这篇深度文章讲什么" | 📄内容提取 | jina read |
| "调研 AI 领域最新动态" | 📊热门排行 | juejin-trends.js |
| "收集竞品技术文章" | 🔍关键词搜索 | web-access CDP |

---

## 注意事项

| 工具 | 用途 | 注意 |
|------|------|------|
| web-access CDP | 关键词搜索 | 稳定无头，不打扰用户 |
| juejin-trends.js | 热门排行 | 直接 API，UA 轮换防封 |
| jina-reader | 内容提取 | 需单独安装 |
| obsidian-cli | 笔记管理 | 先设置默认 vault |

---

*版本: v2.0.0 | 更新日期: 2026-05-10 | 新增：热门排行模式、内容提取模式*
