# Codex Smoke Test

本文定义 think-tank 在 Codex 平台上的第一轮 smoke test。

## 目标

验证 think-tank 协议能否在 Codex 上完成一次完整的单 agent 多 profile 执行。

## 测试任务

```text
研究一个跨平台 Skill 仓库应该如何组织目录结构，要求给出通用建议、风险和下一步行动。
```

## 预期选择

```yaml
mode: research
profiles:
  - source-collector
  - trend-analyst
  - skeptic
  - report-architect
capabilities:
  - source-acquisition
  - knowledge-persistence
```

## 执行步骤

1. 读取当前仓库结构。
2. 读取 `docs/architecture.md`、`protocol/`、`profiles/`、`capabilities/`。
3. 以 `source-collector` 视角整理证据。
4. 以 `trend-analyst` 视角归纳通用结构规律。
5. 以 `skeptic` 视角指出风险和缺口。
6. 以 `report-architect` 视角汇总成结构化输出。
7. 执行 `python3 checks/protocol_check.py`。
8. 写入示例输出到 `examples/codex-smoke-research.md`。

## 验收标准

- 明确 mode、profiles、capabilities。
- 输出包含结论、依据、角色观点、分歧与风险、行动建议、边界。
- 不依赖 Claude Code Agent Team。
- 不声称真实多 agent 执行。
- 协议检查通过。

## 不能证明

- Claude Code Agent Team 可用。
- `.claude/skills` 可被 Codex 直接调用。
- 外部 skills 已集成。
- 真正并行 agent 执行已完成。

