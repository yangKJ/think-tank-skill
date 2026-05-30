# examples

`examples/` 提供 think-tank 的可复用示例，按板块分类：

- **`usage/`** — 用户使用说明书：如何用 think-tank 做研究、审议、审查、策略
- **`providers/`** — 如何接入外部 provider（web-access、obsidian、小红书等）
- **`workflows/`** — 工作流模式示例
- **`runtime/`** — Runtime 输出格式示例（orchestrator、provenance、dispatch）
- **`schemas/`** — Schema 格式示例（输入输出、evidence、run record）
- **`quality/`** — 质量检查 + capability 降级示例
- **`platforms/`** — 各平台（Codex、Claude Code）验证记录
- **`formats/`** — 版本演进格式示例（v2 Research OS、v3 Skill Experience）

---

## usage/ — 用户使用说明书

| 文件 | 说明 |
|------|------|
| `research-request.md` | 研究模式输入输出示例 |
| `council-request.md` | 委员会讨论模式示例 |
| `end-to-end-research.md` | 端到端 research mode 完整流程 |
| `local-workspace-layout.md` | 本地工作区布局参考 |
| `council-decision.md` | 公开 council 模板，单 agent 多视角 fallback |
| `public-research-request.md` | 公开 research 模板，用户材料路径 + provider 边界 |
| `research-to-action.md` | 调研收口成动作建议 + 观察项 |
| `review-acceptance.md` | 发布验收 + 证据优先输出 |
| `strategy-backlog.md` | readiness、owner 和 backlog 候选结构 |

## providers/ — 如何接入 provider

### patterns/ — 集成模式说明
| 文件 | 说明 |
|------|------|
| `source-acquisition-web-access.md` | 网页抓取 provider 接入模式 |
| `social-listening-xiaohongshu.md` | 社媒监听 provider 接入模式 |
| `media-processing-yt-dlp-whisper.md` | 媒体处理 provider 接入模式 |
| `knowledge-persistence-obsidian.md` | 知识持久化 provider 接入模式 |
| `media-production-research-to-video.md` | 媒体生产 provider 接入模式 |

### ledgers/ — invocation ledger 样例
| 文件 | 说明 |
|------|------|
| `source-acquisition-web-access.json` | 网页抓取调用账本 |
| `social-listening-xiaohongshu.json` | 社媒监听调用账本 |
| `media-processing-yt-dlp-whisper.json` | 媒体处理调用账本 |
| `knowledge-persistence-obsidian.json` | 知识持久化调用账本 |
| `media-production-research-to-video.json` | 媒体生产调用账本 |

### 其他
| 文件 | 说明 |
|------|------|
| `browser-automation-integration.md` | Codex Browser 最小集成测试输出 |

## workflows/ — 工作流模式

| 文件 | 说明 |
|------|------|
| `council-release-decision.md` | 发布决策审议模式 |
| `research-provider-assisted.md` | provider 辅助研究模式 |
| `review-open-source-readiness.md` | 开源 readiness 审查模式 |

## runtime/ — Runtime 输出格式

| 文件 | 说明 |
|------|------|
| `codex-orchestrator-sample.json` | Codex orchestrator 输出样例 |
| `codex-runtime-sample.json` | Codex minimal runtime 成功路径 |
| `codex-runtime-failure-sample.json` | Codex minimal runtime 失败路径 |
| `claude-runtime-sample.json` | Claude Code minimal runtime 成功路径 |
| `claude-runtime-failure-sample.json` | Claude Code minimal runtime 降级路径 |
| `claude-dispatch-sample.json` | Claude Code dispatch 机器样例 |
| `runtime-e2e-fixture.json` | 平台无关端到端 fixture |
| `runtime-provenance-direct-tool.json` | 直接工具调用 provenance |
| `runtime-provenance-full-runtime.json` | 完整 runtime provenance |
| `runtime-provenance-single-agent.json` | 单 agent fallback provenance |
| `specialist-runtime-fixture.json` | specialist subagent runtime fixture |

## schemas/ — Schema 格式示例

| 文件 | 说明 |
|------|------|
| `schema-sample-input.json` | 输入 schema 样例 |
| `schema-sample-output.json` | 输出 schema 样例 |
| `capability-evidence-sample.json` | capability evidence 样例 |
| `media-production-run-record.json` | 媒体生产链路 run record |
| `memory-promotion-sample.json` | memory promotion 样例 |
| `post-run-curation-example.json` | post-run curation 通用收尾样例 |
| `project-memory-capture-sample.json` | 项目记忆捕捉样例 |
| `project-memory-capture-report.md` | 项目记忆捕捉报告 |
| `project-competitive-strategy-local-image-editor.json` | 竞品策略 golden sample |

## quality/ — 质量检查 + 降级

| 文件 | 说明 |
|------|------|
| `stable-release-readiness.yaml` | 稳定版本 readiness 检查表 |
| `capability-degradation-browser.md` | browser-automation 缺失降级 |
| `capability-degradation-knowledge.md` | knowledge-persistence 缺失降级 |
| `capability-degradation-media.md` | media-processing 缺失降级 |
| `capability-degradation-social.md` | social-listening 缺失降级 |

## platforms/ — 平台验证记录

### codex/ — Codex 平台验证
| 文件 | 说明 |
|------|------|
| `codex-smoke-research.md` | research mode smoke test |
| `codex-council-validation.md` | council mode 验证 |
| `codex-review-validation.md` | review mode 验证 |
| `codex-strategy-validation.md` | strategy mode 验证 |
| `codex-true-council-runtime.md` | true council runtime 验证 |
| `codex-operational-request.md` | 日常请求示例 |
| `codex-operational-validation.md` | 日常使用验证 |
| `codex-minimal-install-validation.md` | 最小安装行为验证 |
| `codex-local-source-validation.md` | 本地 source-acquisition 验证 |
| `codex-local-source-artifact.md` | 本地资料 Markdown artifact |
| `codex-external-source-validation.md` | 外部只读 source-acquisition 验证 |
| `codex-browser-external-readonly.md` | Browser 外部只读验证 |
| `codex-browser-external-blocked.md` | Browser 外部阻断验证 |
| `codex-long-running-adapter-runtime.md` | 长生命周期 adapter runtime 验证 |
| `codex-long-running-adapter-runtime.json` | 长生命周期 adapter runtime 机器样例 |
| `codex-provider-invocation-matrix.json` | provider invocation 矩阵 |
| `codex-subagent-lifecycle-validation.md` | subagent 生命周期验证 |
| `codex-subagent-lifecycle-validation.json` | subagent 生命周期机器样例 |
| `subagent-lifecycle-validation/role-results/` | subagent 角色执行结果 |

### claude-code/ — Claude Code 平台验证
| 文件 | 说明 |
|------|------|
| `claude-code-research-validation.md` | research mode preflight 验证 |
| `claude-code-council-validation.md` | council mode preflight 验证 |
| `claude-code-final-validation.md` | final low-flow validation |
| `claude-code-capability-discovery.md` | capability → skill 发现映射 |
| `claude-code-external-source-readonly.md` | WebFetch 外部 source 验证 |
| `claude-code-adapter-dispatch-attempt.md` | adapter dispatch 尝试验证 |
| `claude-code-dispatch-contract-sample.md` | dispatch contract 输出样例 |
| `claude-code-dispatch-contract-validation.md` | dispatch contract 验证 |
| `claude-code-dispatch-pre-invocation-validation.md` | dispatch decision 调用前验证 |

## formats/ — 输出格式参考

| 文件 | 说明 |
|------|------|
| `handoff-guardrail-eval.json` | handoff guardrail eval |
| `provider-invocation-ledger.json` | provider invocation ledger |
| `research-os-run-record.json` | Research OS run record |
| `research-workspace-contract.json` | research workspace contract |
| `progressive-disclosure-plan.json` | progressive disclosure plan |
| `skill-invocation-contract.json` | skill invocation contract |
| `skill-quality-score.json` | skill quality score |
| `skill-route-decision.json` | skill route decision |
| `skill-self-test-result.json` | skill self-test result |

---

## 其他文件

| 文件 | 说明 |
|------|------|
| `browser-automation-fixture.html` | browser-automation 本地测试页面 |
