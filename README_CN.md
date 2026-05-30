# think-tank-skill

**语言：** [English](README.md) | 中文

**think-tank** 是一个协议优先、跨平台的高阶 AI 协作 Skill，用于研究、审查、讨论决策和策略分析。它当前以 Codex 主路径为默认稳定路径，并用明确的能力边界来说明哪些已经验证、哪些只是可选 provider 生态。

![think-tank 中文主视觉](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/think-tank-hero-cn-image2.png)

主 Skill 位于 [`think-tank/`](think-tank/)。

## 为什么使用 think-tank？

- 一套协议覆盖 research、review、council、strategy 工作流。
- 明确区分编排层和工具层：
  `think-tank = 任务理解 + 角色组织 + 能力路由 + 证据汇总 + 边界声明`。
- 所有能力都用证据状态描述：`verified`、`verified_partial`、`planned`、`blocked`。
- 提供公开 release gate，检查协议完整性、隐私边界、发布包范围和 stable 姿态。

## 快速开始

1. 先选安装方式：

- Codex 安装：

```bash
python3 "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" --repo yangKJ/think-tank-skill --path think-tank
```

- 手动安装：

```text
think-tank/
```

把它复制到你的平台 skill 目录，或者直接 clone 本仓库并引用 `think-tank/`。

2. 安装后重启你的 agent 运行环境。

对 Codex 来说，需要重启 App 或当前会话，新的 skill 才会被识别。

3. 先做首装检查：

```bash
test -f "$HOME/.codex/skills/think-tank/SKILL.md" && echo "think-tank installed"
```

4. 先试用公开模板：

```text
think-tank/examples/usage/research-request.md
think-tank/examples/usage/council-decision.md
think-tank/examples/usage/review-acceptance.md
think-tank/examples/usage/research-to-action.md
think-tank/examples/usage/strategy-backlog.md
```

5. 再阅读 [`think-tank/README.md`](think-tank/README.md) 和 [`think-tank/docs/open-source-quickstart.md`](think-tank/docs/open-source-quickstart.md)，理解协议面和运行边界。

接着走用户操作路径：

- [`think-tank/docs/first-run-guide.md`](think-tank/docs/first-run-guide.md)
- [`think-tank/docs/operator-manual.md`](think-tank/docs/operator-manual.md)
- [`think-tank/docs/cookbook.md`](think-tank/docs/cookbook.md)
- [`think-tank/docs/progression-guide.md`](think-tank/docs/progression-guide.md)

6. 运行公开发布门禁：

```bash
python3 checks/open_source_release_suite.py
```

7. 运行 stable gate：

```bash
python3 checks/stable_release_check.py
```

两条命令都通过，说明当前仓库处在可公开发布的稳定路径上。

## 首装预期

刚安装完 `think-tank`，你立刻能得到：

- protocol-first 的 research、review、council、strategy 工作流
- mode 选择、profile 模拟和结构化输出
- 本地文件分析和用户提供材料分析
- 基于证据状态的边界声明

刚安装完时，不应该默认期待：

- 所有 optional peer skills 自动存在
- browser、社媒、媒体、知识库 provider 已经预授权
- 所有平台都有完整多 agent runtime
- “已经安装” 等于 “已经真实调用并验证通过”

## 平台安装位置

| 平台 | 安装位置 | 安装后动作 |
|---|---|---|
| Codex | `~/.codex/skills/think-tank` | 重启 Codex 或当前会话 |
| Claude Code | `~/.claude/skills/think-tank/` | 重启 Claude Code 会话 |
| 其他 runtime | 对应 runtime 的 skill 目录 | 重建索引或重启 |

## 首装验收

建议按下面最短路径验收：

1. 确认入口文件存在。
2. 重启运行环境。
3. 发一个很小的 research、review 或 strategy 请求。
4. 检查返回是否体现 `think-tank` 的边界感和结构化风格，而不是普通自由回答。

Codex 最小文件检查：

```bash
test -f "$HOME/.codex/skills/think-tank/SKILL.md" && echo "think-tank installed"
```

建议第一条测试 prompt：

```text
Use think-tank to review these notes, separate facts from assumptions, and give me a boundary-aware recommendation.
```

## 首装故障排查

- 如果安装脚本遇到 HTTPS 证书错误，可以改走手动 `git clone` 或下载 zip，再只复制 `think-tank/`。
- 如果目标目录已存在，先删除或改名旧的 `~/.codex/skills/think-tank` 再重装。
- 如果运行环境没有识别到 skill，先重启 App 或会话，再继续深挖。
- 不要把 `.think-tank/`、`.codex/`、`.claude/` 或生成产物目录复制进公开 skill 目录。

## 典型场景

| Research | Council | Review |
|---|---|---|
| ![research scenario](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/research-card-image2.png) | ![council scenario](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/council-card-image2.png) | ![review scenario](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/review-card-image2.png) |

## Provider 生态模式

`think-tank` 不内置具体工具。它记录 provider 接入模式，并且只在当前平台暴露 provider、当前任务获得授权时，才把 capability slot 路由到可选 peer skills。

![provider ecosystem](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/provider-ecosystem-image2.png)

代表性同级技能模式示例：

| 能力槽 | 典型 peer skills | 状态边界 |
|---|---|---|
| source-acquisition | `web-access`, `agent-reach` | 模式已记录，需要证据 |
| browser-automation | `browser`, `playwright-cli` | 只读路径 `verified_partial` |
| social-listening | `xiaohongshu` | 模式已记录，需要登录和授权 |
| media-processing | `yt-dlp`, `openai-whisper` | 模式已记录，需要媒体权限和授权 |
| knowledge-persistence | `obsidian` | 模式已记录，私有写入必须确认 |
| media-production | `ai-research-to-video-production` | verified_partial，限定生产链路 |

更多说明见 [`think-tank/docs/provider-ecosystem-examples.md`](think-tank/docs/provider-ecosystem-examples.md) 和 [`think-tank/docs/provider-integration-patterns.md`](think-tank/docs/provider-integration-patterns.md)。

## Research OS 与记忆运行层

**Research OS + Memory Runtime** 帮助可重复研究任务产出 run record、memory candidate、provider ledger、handoff、guardrail 和 eval fixture。

![Research OS and Memory Runtime](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/research-os-memory-runtime-image2.png)

- **Run Record：** [`think-tank/protocol/run-record.md`](think-tank/protocol/run-record.md)
- **Project Memory Runtime：** [`think-tank/protocol/project-memory-runtime.md`](think-tank/protocol/project-memory-runtime.md)
- **Provider Invocation Ledger：** [`think-tank/protocol/provider-invocation-ledger.md`](think-tank/protocol/provider-invocation-ledger.md)
- **Handoff Protocol：** [`think-tank/protocol/handoff-protocol.md`](think-tank/protocol/handoff-protocol.md)
- **Guardrails：** [`think-tank/protocol/guardrails.md`](think-tank/protocol/guardrails.md)
- **Research OS：** [`think-tank/protocol/research-os.md`](think-tank/protocol/research-os.md)
- **Eval Pack：** [`think-tank/protocol/eval-pack.md`](think-tank/protocol/eval-pack.md)

## 开源可用性

- **贡献与社区治理：** [`CONTRIBUTING.md`](CONTRIBUTING.md)、[`SECURITY.md`](SECURITY.md)、[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)、[`SUPPORT.md`](SUPPORT.md)、issue templates 和 PR template。
- **Research OS Starter Kit：** [`starter-kits/research-workspace/`](starter-kits/research-workspace/)。
- **Eval Pack Starter：** [`evals/`](evals/)。
- **Provider Test Matrix：** [`think-tank/docs/provider-test-matrix.md`](think-tank/docs/provider-test-matrix.md)。
- **Docs Site：** [`think-tank/docs/index.md`](think-tank/docs/index.md)、concepts、guides、reference 和 release 分区。
- **平台分发：** [`think-tank/docs/platform-publishing.md`](think-tank/docs/platform-publishing.md)、[`think-tank/docs/codex-installation.md`](think-tank/docs/codex-installation.md)、[`think-tank/docs/claude-code-installation.md`](think-tank/docs/claude-code-installation.md)。

## Skill Experience Layer

**Skill Experience Layer** 让 Codex、Claude Code 和其他 agent 更容易判断何时使用 `think-tank`、如何形成 invocation contract、如何渐进加载文档、如何安全组合 optional peer skills，以及如何用 self-test 检查常见边界。

触发词不内置在公开 core 里。触发词、别名和 provider 偏好应放在用户自己的 YAML policy 中；`think-tank` 只提供 intent 类别、路由契约和检查规则。

- **Skill Trigger Intelligence：** [`think-tank/protocol/skill-trigger-intelligence.md`](think-tank/protocol/skill-trigger-intelligence.md)
- **Skill Invocation Contract：** [`think-tank/protocol/skill-invocation-contract.md`](think-tank/protocol/skill-invocation-contract.md)
- **Progressive Disclosure：** [`think-tank/protocol/progressive-disclosure.md`](think-tank/protocol/progressive-disclosure.md)
- **Agent Compatibility Matrix：** [`think-tank/docs/agent-compatibility-matrix.md`](think-tank/docs/agent-compatibility-matrix.md)
- **Skill Composition Guide：** [`think-tank/docs/skill-composition-guide.md`](think-tank/docs/skill-composition-guide.md)
- **Skill Quality Score：** [`think-tank/docs/skill-quality-score.md`](think-tank/docs/skill-quality-score.md)
- **Skill Experience 示例：** [`think-tank/examples/formats/`](think-tank/examples/formats/)
- **Skill Self Tests：** [`self-tests/`](self-tests/)

版本更新记录统一放在 [`CHANGELOG.md`](CHANGELOG.md)。

## 用户操作路径

- **首次运行指南：** [`think-tank/docs/first-run-guide.md`](think-tank/docs/first-run-guide.md)
- **操作手册：** [`think-tank/docs/operator-manual.md`](think-tank/docs/operator-manual.md)
- **专属定制：** [`think-tank/docs/cookbook.md`](think-tank/docs/cookbook.md)
- **进阶教程：** [`think-tank/docs/progression-guide.md`](think-tank/docs/progression-guide.md)

| 首次运行指南 |进阶教程 |
|:---:|:---:|
| [![First Run Guide](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/first-run-guide-image2.png)](think-tank/docs/first-run-guide.md) | [![Progression Guide](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/progression-guide-image2.png)](think-tank/docs/progression-guide.md) |
| 专属定制 | 操作手册 |
| [![Cookbook](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/cookbook-image2.png)](think-tank/docs/cookbook.md) | [![Operator Manual](https://raw.githubusercontent.com/yangKJ/think-tank-skill/master/think-tank/assets/brand/operator-manual-image2.png)](think-tank/docs/operator-manual.md) |

## 仓库结构

```text
think-tank-skill/
├── README.md
├── README_CN.md
├── LICENSE
├── .gitignore
├── think-tank/
│   ├── SKILL.md
│   ├── README.md
│   ├── protocol/
│   ├── capabilities/
│   ├── profiles/
│   ├── platforms/
│   ├── modes/
│   ├── templates/
│   ├── runtime/
│   ├── docs/
│   └── examples/
├── starter-kits/
│   └── research-workspace/
├── evals/
└── self-tests/
```

## Stable 是什么含义？

Stable 表示：

- `think-tank/` 协议面稳定。
- Codex-first 默认路径稳定。
- 公开 release gate 稳定。
- 能力声明基于证据状态。

Stable 不表示：

- 所有 optional provider 默认可用。
- 所有平台 runtime 都已完成。
- 登录、社媒抓取、私有知识库写入是默认能力。
- 安装同级 skill 就等于已经被真实调用和回收结果。

## 证据概览

| 范围 | 状态 | 来源 |
|---|---|---|
| Codex foundation | verified | [`think-tank/docs/codex-readiness-matrix.md`](think-tank/docs/codex-readiness-matrix.md) |
| Provider invocation proofs | 4 public proofs | [`think-tank/examples/quality/stable-release-readiness.yaml`](think-tank/examples/quality/stable-release-readiness.yaml) |
| 外部浏览器只读 | verified_partial | [`think-tank/examples/platforms/codex/codex-browser-external-readonly.md`](think-tank/examples/platforms/codex/codex-browser-external-readonly.md) |
| subagent runtime | verified_partial | [`think-tank/examples/platforms/codex/codex-subagent-lifecycle-validation.md`](think-tank/examples/platforms/codex/codex-subagent-lifecycle-validation.md) |
| Claude Code runtime | deferred | [`think-tank/docs/support-matrix.md`](think-tank/docs/support-matrix.md) |

## 推荐阅读

- [`think-tank/README.md`](think-tank/README.md)
- [`think-tank/docs/open-source-quickstart.md`](think-tank/docs/open-source-quickstart.md)
- [`think-tank/docs/support-matrix.md`](think-tank/docs/support-matrix.md)
- [`think-tank/docs/validation-tiers.md`](think-tank/docs/validation-tiers.md)
- [`think-tank/docs/provider-ecosystem-examples.md`](think-tank/docs/provider-ecosystem-examples.md)
- [`think-tank/docs/provider-integration-patterns.md`](think-tank/docs/provider-integration-patterns.md)
- [`think-tank/docs/codex-installation.md`](think-tank/docs/codex-installation.md)
- [`think-tank/docs/claude-code-installation.md`](think-tank/docs/claude-code-installation.md)
- [`think-tank/docs/platform-publishing.md`](think-tank/docs/platform-publishing.md)
- [`think-tank/docs/index.md`](think-tank/docs/index.md)
- [`think-tank/docs/faq.md`](think-tank/docs/faq.md)
- [`think-tank/docs/troubleshooting.md`](think-tank/docs/troubleshooting.md)
- [`think-tank/docs/provider-test-matrix.md`](think-tank/docs/provider-test-matrix.md)
- [`think-tank/docs/open-source-release.md`](think-tank/docs/open-source-release.md)

## 验证

公开 release gate：

```bash
python3 checks/open_source_release_suite.py
```

stable gate：

```bash
python3 checks/stable_release_check.py
```

生成平台分发产物：

```bash
python3 scripts/package_agent_distributions.py
```

## 设计边界

协议层定义 think-tank 是什么。平台 adapter 定义它如何在具体环境运行。mode 定义场景默认策略。

平台特有行为不能反向改写 core protocol。
