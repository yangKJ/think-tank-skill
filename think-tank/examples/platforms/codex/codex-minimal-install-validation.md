# Codex Minimal Install Validation

本文件记录 Codex 平台对 minimal install 行为的验证。

## 测试任务

```text
用户只安装 think-tank，没有 Browser、Playwright、yt-dlp、obsidian、xiaohongshu 等外部技能。请分析一段用户提供的材料，并说明哪些能力可用、哪些能力不可用。
```

## 执行声明

```yaml
platform: codex
execution_method: single_agent_profile_simulation
mode: research
external_skills_invoked: false
network_required: false
profiles:
  - source-collector
  - skeptic
  - report-architect
capabilities:
  selected:
    - source-acquisition
    - browser-automation
    - media-processing
    - social-listening
    - knowledge-persistence
  available:
    - local_repository_collection
    - structured_markdown_output
  unavailable:
    - browser-automation
    - media-processing
    - social-listening
    - external_knowledge_persistence
```

## 结论

只安装 think-tank 时，系统仍然可用，但可用范围是协议执行、角色模拟、基于用户提供材料的分析、结构化输出和边界声明。

它不能自动获得浏览器、视频下载、社媒抓取、音频转录或 Obsidian 写入能力。

## 依据

- `docs/minimal-install-behavior.md` 明确区分最小安装保证和不保证的能力。
- `capabilities/*` 为能力槽，不是工具安装清单。
- `platforms/codex/capability-mapping.md` 将 Browser、media、social、knowledge persistence 标为环境依赖或 planned。

## 角色观点

```yaml
source_collector:
  claim: 最小安装可以处理用户粘贴的文本、截图 OCR 文本、仓库文件和本地 Markdown。
  confidence: high

skeptic:
  claim: 如果用户要求验证网页、抓社媒或处理视频，必须降级并要求补充材料或启用对应 capability。
  confidence: high

report_architect:
  claim: 输出必须把可用能力、不可用能力和下一步补充材料写清楚。
  confidence: high
```

## 分歧与风险

- 分歧：是否应默认把 Browser 视为 Codex 可用能力。
- 判断：不能默认。Browser 是 optional capability，只有真实调用并回收证据后才能标为 verified。
- 风险：用户可能把 think-tank 理解成包含所有旧 research skills 的大包。
- 缓解：所有外部能力保持 capability 槽位表达，并写明降级策略。

## 行动建议

1. 在 Codex 上默认以 minimal install 能力运行。
2. 只有用户任务确实需要外部能力时，才选择对应 capability。
3. capability 不可用时，不伪装执行，转为用户材料驱动分析。
4. 任何 optional capability 验证都必须写入 examples 和 docs。

## 边界

本次没有调用外部 skill，没有访问网络，没有打开 Browser，也没有写入用户私有知识库。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```
