# think-tank

think-tank 是一个跨平台、可复用的高阶 Skill，用于多角色信息收集、协作分析、讨论审议与结论汇总。

它是本仓库的唯一主品牌、唯一主协议、唯一长期演进对象。research、agent-council、review、strategy 等能力都应收敛为 think-tank 的场景模式或历史实现来源，而不是与 think-tank 平行发展的独立体系。

## 定位

think-tank 不是：

- 某个平台专属脚本壳
- 某个 agent 的附属 prompt
- 某个项目私有实现
- research 的子模块
- agent-council 的改名版本

think-tank 是：

- 一个独立主仓
- 一个统一协议源
- 一个跨平台适配的技能系统
- 一个能被 Claude Code、Codex、其他项目和其他用户复用的能力框架

## 核心能力

- 多渠道信息收集
- 多角色分析
- 协作讨论
- 观点碰撞
- 汇总结论
- 输出行动建议

## 三层结构

```text
think-tank-skill/
├── SKILL.md
├── README.md
├── protocol/
├── capabilities/
├── profiles/
├── platforms/
├── modes/
├── domain-packs/
├── docs/
└── examples/
```

### protocol

协议层是 think-tank 的唯一真相源，必须平台无关。它定义触发条件、输入格式、角色选择、流程阶段、终止条件、输出结构和质量标准。

### platforms

平台适配层负责把同一套协议落到不同运行环境。Claude Code 和 Codex 可以有不同 runtime、subagent 调用方式、目录结构、记忆落点与 hook 方式，但不能改变 think-tank 的核心行为协议。

### capabilities

能力槽层定义 think-tank 如何与工具型 skills 共存。`yt-dlp`、`obsidian`、`playwright-cli`、`xiaohongshu` 等不应被复制进 core，而应通过能力槽由平台适配层调用。

### profiles

角色模板层定义跨平台角色能力。旧 research agent 的 subagents 应被吸收为 profile，而不是原样进入 core。

### modes

场景模式层定义不同使用场景的默认角色、流程强度和输出重点。第一批模式包括：

- `research mode`：承接原 research 体系里的 think-tank 用法
- `council mode`：收编 agent-council 的多角色讨论能力
- `review mode`：用于代码、方案、报告、实现产物审查
- `strategy mode`：用于产品、架构、路线和决策推演

### domain-packs

领域包层承接可选领域知识。图像编辑 App 经验属于 `domain-packs/image-editing/`，不属于 think-tank core。

## 与历史体系的关系

- research 是 think-tank 的一个核心应用场景，主要负责信息收集、证据整理和研究结论输出。
- agent-council 是 think-tank 的历史实现分支或 council mode 来源，主要沉淀多角色讨论、交叉质询和审议机制。
- 旧实现资产应逐步迁入 think-tank 的协议、模式或平台适配目录，不应继续作为新体系中心。

## 第一批建设目标

1. 固化 think-tank 的主仓定位。
2. 建立协议层、平台适配层、模式层的目录边界。
3. 明确 research 与 agent-council 在新体系里的位置。
4. 创建可被 Claude Code 和 Codex 读取的统一 Skill 入口。
5. 为后续吸收旧资产保留清晰迁移路径。

## Codex 验证状态

Codex 当前已完成 foundation 验收：

- `research mode`：verified
- `council mode`：verified
- `review mode`：verified
- `strategy mode`：verified
- capability 降级：verified
- Browser localhost fixture：verified optional
- JSON schema sample：verified

验收命令：

```bash
python3 checks/protocol_check.py
python3 checks/codex_validation_check.py
python3 checks/claude_code_validation_check.py
python3 checks/claude_dispatch_sample_check.py
python3 checks/claude_runtime_sample_check.py
python3 checks/schema_sample_check.py
```

仍未声明完成：

- Claude Code Agent Team
- 真实多 agent 并行执行
- Claude Code adapter 自动 dispatch
- Browser 外部网页 DOM 回收
- `yt-dlp`、`obsidian`、`xiaohongshu` 等外部 skills 集成
