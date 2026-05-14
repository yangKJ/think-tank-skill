# Research Agent Capability Map

本文梳理旧 research agent 中的 skills、subagents 和任务驱动方式，用于判断哪些能力应被吸收到统一 think-tank，哪些应作为 Claude Code 平台适配或可选领域包保留。

旧 research agent 来源：

```text
legacy research workspace
```

## 核心判断

旧 research agent 不是单纯的搜索 agent，而是一个运行在 Claude Code 上的外部情报与研究生产系统。

它把用户任务转成：

```text
任务理解
  -> 研究深度选择
  -> 工具链选择
  -> subagent 分工
  -> 多渠道采集
  -> 证据验证
  -> 报告生成
  -> 知识沉淀
  -> 必要时持续监控
```

在新 think-tank 中，应吸收它的通用研究能力，而不是吸收具体项目的领域绑定。

## 旧系统能力分层

### 1. 用户任务入口层

旧 research agent 支持多种用户意图：

- 快速了解
- 竞品分析
- 深度调研
- 行业分析
- 技术趋势调研
- 舆情分析
- 视频或播客内容提取
- PDF 和报告解读
- 持续监控
- 知识图谱构建

这些不应成为固定命令，而应抽象为 think-tank 的 research mode 子类型。

### 2. 研究深度层

旧 `research-workflow` 中已经有三类研究深度：

| 旧模式 | 新抽象 |
|--------|--------|
| 快速概览 | `quick_scan` |
| 深度研究 | `deep_research` |
| 持续监控 | `continuous_monitoring` |

旧 `omni-research` 还提供自主研究循环：

| 旧能力 | 新抽象 |
|--------|--------|
| research lines | 研究路线 |
| max cycles | 研究预算 |
| research.md | 累积知识库 |
| experiments.tsv | 研究过程日志 |
| steer.md | 中途转向控制 |
| BRIEF.md | 最终摘要 |

这应成为 think-tank research mode 的高级子流程，而不是 Claude Code 专属概念。

### 3. 信息源和工具层

旧 research agent 的技能不是杂乱工具，而是按信息源和任务类型组织的工具链。

| 能力类别 | 旧 skills | 通用抽象 |
|----------|-----------|----------|
| 网页获取 | `web-access`、`playwright-cli`、`google-ai-mode-skill` | web acquisition |
| 内容总结 | `summarize` | content summarization |
| 技术社区 | `juejin-search` | community source |
| 社媒舆情 | `xiaohongshu`、`social-media-analyzer` | social listening |
| 行业热点 | `36kr-hotlist` | news and trend feed |
| 深度自主研究 | `omni-research` | autonomous research loop |
| PDF 报告 | `pdf-extraction` | document extraction |
| 视频播客 | `yt-dlp`、`openai-whisper`、`xiaoyuzhou-transcribe` | media research |
| 知识沉淀 | `obsidian`、`notebooklm` | knowledge persistence |
| 知识结构 | `knowledge-graph-builder` | knowledge graph |
| 任务持续化 | `taskflow` | long-running task state |
| 工具发现 | `mcp-cli` | dynamic tool discovery |

think-tank 应吸收“如何选择信息源和工具链”的策略，而不是依赖这些具体工具存在。

### 4. subagent 分工层

旧 research agent 有一组专业 subagents：

| subagent | 旧职责 | 新 think-tank 抽象 |
|----------|--------|--------------------|
| `Research Sub Researcher` | 外部信息收集、竞品情报、资料搜索 | source collector |
| `Research Sub Trend Researcher` | 趋势识别、市场预测、技术 scouting | trend analyst |
| `Research Sub Xiaohongshu Researcher` | 小红书舆情和社媒反馈 | social listener |
| `Research Sub Feedback Synthesizer` | 多渠道反馈综合、优先级排序 | feedback synthesizer |
| `Research Sub Research Report Architect` | 报告结构化、洞察提炼 | report architect |
| `Research Sub Product Manager` | 产品判断、路线、优先级 | product strategist |
| `Critic` | 质疑、事实核查、风险识别 | skeptic |

这些不是 think-tank 的固定角色名，而是 research mode 的可选专业角色模板。

## 旧 research agent 的任务驱动方式

### 简单任务

```text
用户请求
  -> research agent 自己完成
  -> 直接返回结果
  -> 可选保存到知识库
```

适合：

- 单页资料查询
- 简单搜索
- 快速总结

在新 think-tank 中，这类任务不应强制触发完整多角色流程。

### 复杂研究

```text
用户请求
  -> 判断研究深度
  -> 选择工具链
  -> 派发专业 subagents
  -> 多渠道收集
  -> 交叉验证
  -> 报告架构师整理
  -> 保存知识库
```

适合：

- 深度竞品分析
- 市场和技术趋势
- 多来源证据综合
- 用户反馈研究

在新 think-tank 中，这应成为 `research mode` 的标准深度流程。

### 协作讨论

```text
用户请求
  -> think-tank skill
  -> 多 agent 并行调研
  -> critic 质疑
  -> synthesizer 汇总
  -> 主 agent 决策或执行
```

这部分才是旧 research agent 中的 think-tank 原型。

### 持续监控

```text
监控主题
  -> 定期抓取来源
  -> 检测变化
  -> 生成简报或预警
  -> 知识库沉淀
```

这属于 research mode 的 `continuous_monitoring` 子类型，不应和 council mode 混淆。

## 已抽象进 think-tank 的能力

以下能力应抽象进主仓不同层级：

- `protocol/`：research depth、evidence policy、role planning、output contract、quality gates
- `capabilities/`：source acquisition、media processing、social listening、knowledge persistence、browser automation
- `profiles/`：source collector、trend analyst、social listener、feedback synthesizer、report architect、skeptic、product strategist
- `platforms/claude-code/`：旧 skills 和 subagents 的平台映射
- `domain-packs/`：领域扩展点，具体项目自行维护

## 应进入 research mode 的能力

以下能力应进入 `modes/research.md`：

- 快速概览
- 深度研究
- 持续监控
- 自主研究循环
- 多渠道采集
- 交叉验证
- 报告生成
- 知识沉淀

## 应进入 Claude Code adapter 的能力

以下能力属于 Claude Code 平台实现：

- `.claude/skills/`
- `.claude/agents/`
- frontmatter agent 定义
- `Agent(...)`
- `TeamCreate` / `SendMessage` / `TeamDelete`
- background agent
- `CLAUDE_PLUGIN_DATA`
- CDP web-access proxy
- Obsidian CLI 固定路径
- taskflow 持久化

这些不能进入平台无关协议。

## 应留在具体项目的领域能力

以下能力是私有领域经验，不应进入当前主仓：

- 具体产品背景
- 固定竞品表
- 领域默认技术雷达
- 私有交付路径
- 平台或项目专属舆情关键词

这些应沉淀到具体项目自己的 domain pack 或本地资料目录。

## 对统一 think-tank 的启示

统一 think-tank 应该把 research agent 的能力抽象为：

```text
research mode
├── depth: quick_scan | deep_research | continuous_monitoring | autonomous_research
├── source_strategy: web | official | community | social | media | document | local_knowledge
├── specialist_roles: collector | trend_analyst | social_listener | feedback_synthesizer | report_architect | skeptic
├── evidence_policy: source_quality | freshness | cross_validation | confidence
└── knowledge_output: brief | report | evidence_table | source_queue | knowledge_graph | monitoring_log
```

这样既保留旧 research agent 的强能力，又不会把 think-tank 绑定到某个具体项目或 Claude Code 平台。
