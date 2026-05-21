# schemas

`schemas/` 存放 think-tank 输入输出契约的机器可读版本。

这些 schema 是协议辅助，不替代 `protocol/` 的文字规范。

## 文件

- `input.schema.json`：标准输入结构
- `output.schema.json`：标准输出结构
- `claude-dispatch.schema.json`：Claude Code dispatch 输出结构
- `claude-runtime.schema.json`：Claude Code minimal runtime 输出结构，用于检查成功与失败路径样例
- `runtime-provenance.schema.json`：think-tank 风格输出的运行来源披露结构
- `run-record.schema.json`：2.0 可回放运行记录结构
- `provider-invocation-ledger.schema.json`：2.0 provider 调用证据账本结构
- `memory-runtime.schema.json`：2.0 项目记忆运行时结构
- `handoff.schema.json`：2.0 handoff packet 结构
- `guardrail-result.schema.json`：2.0 guardrail 结果结构
- `research-workspace.schema.json`：2.0 Research OS 本地工作区契约
- `eval-case.schema.json`：2.0 回归评测样例结果结构
- `runtime-result.schema.json`：平台无关 runtime pipeline 输出结构
- `codex-orchestrator-result.schema.json`：Codex 自然语言 orchestrator 输出结构
- `evidence-sources.schema.json`：统一证据来源表结构
- `artifact-plan.schema.json`：artifact 写入计划结构
- `strategy-backlog.schema.json`：策略转 backlog 候选结构
- `post-run-curation.schema.json`：研究、策略、审查、内容规划和媒体生产任务的收尾沉淀结构，包含 generated artifacts 候选
- `project-competitive-strategy.schema.json`：项目竞品策略结果结构
- `research-to-video.schema.json`：`research_to_video` 从选题研究、证据、分镜、素材、BGM 到成片质量门禁的结果结构
- `capability-evidence.schema.json`：capability 证据状态结构
- `memory-item.schema.json`、`memory-capture.schema.json`、`memory-promotion.schema.json`：项目记忆候选、捕获和提升决策结构

## 使用原则

- 平台 adapter 可以把用户输入转换成 schema 兼容结构。
- 平台 adapter 可以把最终输出转换成 schema 兼容结构。
- schema 变更必须遵守 `protocol/versioning.md`。

主 agent 领导者系统的 schema 已迁移到外部 sibling 项目：

```text
Desktop/leader-runtime-project/schemas/
```
