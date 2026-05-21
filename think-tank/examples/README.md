# examples

`examples/` 存放 think-tank 的可复用示例。

示例必须体现主协议，而不是某个平台的临时脚本。

视觉说明和 Image2 提示词见：

```text
../assets/
../assets/prompts/
```

## 第一批示例

- `public/research-request.md`：公开 research 模板，展示用户材料路径和 provider 边界。
- `public/council-decision.md`：公开 council 模板，展示单 agent 多视角 fallback 的声明方式。
- `public/review-acceptance.md`：公开 review 模板，展示发布验收和证据优先输出。
- `provider-patterns/`：v1.1 provider 接入模式示例，只说明可能接法，不承诺 provider 已安装或已调用。
- `provider-ledgers/`：v2.4 provider ledger 样例，与 provider test matrix 对齐。
- `workflow-patterns/`：v1.1 工作流模式示例，展示用户可参考的组织方式，不替用户完成具体 provider 功能。
- `v2/`：2.0 Research OS + Memory Runtime fixture，覆盖 run record、provider ledger、handoff、guardrail、eval 和本地 workspace contract。
- `v3/`：3.0 Skill Experience fixture，覆盖 skill route decision、invocation contract、progressive disclosure、self-test result 和 quality score。
- `research-request.md`：研究模式输入输出示例
- `council-request.md`：委员会讨论模式输入输出示例
- `end-to-end-research.md`：端到端 research mode 示例
- `codex-smoke-research.md`：Codex 平台 smoke test 输出
- `codex-council-validation.md`：Codex council mode 验证输出
- `codex-review-validation.md`：Codex review mode 验证输出
- `codex-strategy-validation.md`：Codex strategy mode 验证输出
- `codex-minimal-install-validation.md`：Codex 最小安装行为验证输出
- `codex-operational-request.md`：Codex 主平台日常请求示例
- `codex-operational-validation.md`：Codex 主平台日常使用验证输出
- `codex-local-source-artifact.md`：Codex 本地资料研究 Markdown artifact
- `codex-local-source-validation.md`：Codex 本地 source-acquisition 与 artifact 验证
- `codex-external-source-validation.md`：Codex 外部只读 source-acquisition 验证
- `codex-browser-external-readonly.md`：Codex Browser 外部只读验证成功记录
- `codex-long-running-adapter-runtime.md`：Codex 长生命周期 adapter runtime 验证记录
- `codex-long-running-adapter-runtime.json`：Codex 长生命周期 adapter runtime 机器样例
- `codex-runtime-sample.json`：Codex minimal runtime 成功路径样例
- `codex-runtime-failure-sample.json`：Codex minimal runtime 失败路径样例
- `claude-code-research-validation.md`：Claude Code research mode preflight 验证记录
- `claude-code-council-validation.md`：Claude Code council mode preflight 验证记录
- `claude-code-capability-discovery.md`：Claude Code capability 到 skill 发现和映射验证记录
- `claude-code-external-source-readonly.md`：Claude Code WebFetch 外部只读 source-acquisition 片段验证
- `claude-code-adapter-dispatch-attempt.md`：Claude Code adapter dispatch 尝试但未发生的验证记录
- `claude-code-dispatch-contract-sample.md`：Claude Code adapter dispatch 目标输出样例
- `claude-code-dispatch-contract-validation.md`：Claude Code dispatch contract 验证记录，当前为 order gap partial
- `claude-code-dispatch-pre-invocation-validation.md`：Claude Code dispatch decision 调用前形成的验证记录
- `claude-code-final-validation.md`：Claude Code final low-flow validation 记录，当前为 partial
- `claude-dispatch-sample.json`：Claude Code dispatch 机器可检查样例
- `claude-runtime-sample.json`：Claude Code minimal runtime 成功路径机器可检查样例
- `claude-runtime-failure-sample.json`：Claude Code minimal runtime 失败/降级路径机器可检查样例
- `capability-degradation-media.md`：media-processing 降级测试
- `capability-degradation-social.md`：social-listening 降级测试
- `capability-degradation-knowledge.md`：knowledge-persistence 降级测试
- `capability-degradation-browser.md`：browser-automation 缺失时的降级测试
- `browser-automation-fixture.html`：browser-automation 本地测试页面
- `browser-automation-integration.md`：Codex Browser 最小集成测试输出
- `schema-sample-input.json`：输入 schema 样例
- `schema-sample-output.json`：输出 schema 样例
- `runtime-e2e-fixture.json`：平台无关 runtime pipeline 端到端 fixture
- `project-competitive-strategy-local-image-editor.json`：项目竞品策略 golden sample，基于本地创意工具项目实战调研抽象而来，保留结构不保留私有实现。
- `post-run-curation-example.json`：post-run curation 通用收尾沉淀样例，不包含私有项目知识。
- `media-production-run-record.json`：媒体生产链路 run record 样例，覆盖来源、素材、口播、字幕、渲染、关键帧和 known gaps。
