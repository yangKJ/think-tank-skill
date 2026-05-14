# runtime

`runtime/` 存放 think-tank v0.2 的平台无关最小 runtime library。

这些模块不是 Claude Code adapter，也不是 Codex adapter。它们提供可复用的基础执行模型，平台 adapter 可以调用或复刻其行为。

## Modules

- `planner.py`：从任务和 mode 生成 `runtime_plan`
- `slot_resolver.py`：解析 required / optional capability slot
- `state_model.py`：生成 run/state/result/recovery 数据结构
- `consensus.py`：评估 L1/L2/L3、blocking objection、continue/stop decision

## Boundary

当前 runtime library 已通过检查，但仍不代表：

- Claude Code Team 真并发能力
- 完整 adapter dispatch runtime 能力
- automatic result recovery 能力
- 外部 tools fallback 能力
