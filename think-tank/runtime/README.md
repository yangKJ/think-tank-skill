# runtime

`runtime/` 存放 think-tank v0.2 的平台无关最小 runtime library。

这些模块不是 Claude Code adapter，也不是 Codex adapter。它们提供可复用的基础执行模型，平台 adapter 可以调用或复刻其行为。

## Modules

- `planner.py`：从任务和 mode 生成 `runtime_plan`
- `slot_resolver.py`：解析 required / optional capability slot
- `state_model.py`：生成 run/state/result/recovery 数据结构
- `consensus.py`：评估 L1/L2/L3、blocking objection、continue/stop decision
- `safety.py`：迁移旧 think-tank 的安全文件名、危险命令、密钥清理、prompt injection 和循环检测 helper
- `council.py`：迁移旧 agent-council 的 collect/discuss/conclude/complete 状态 helper
- `subagent.py`：v0.5 专业 subagent 派发计划、profile prompt 和 role-result 聚合 helper

## Boundary

当前 runtime library 已通过检查，但仍不代表：

- Claude Code Team 真并发能力
- 完整 adapter dispatch runtime 能力
- automatic result recovery 能力
- 外部 tools fallback 能力

`safety.py` 只提供检测和清理原语，不执行 shell 命令，不写私有目录，也不创建 Claude Code Team。

`council.py` 只提供平台无关状态判断和 synthesis payload，不实现旧 agent-council 的 HMAC manifest、文件锁、Team 调度或 ios-automation-mcp 项目路径。

`subagent.py` 不创建真实子进程或外部 agent。它定义专业 subagent runtime 的平台无关任务包、结果包和 fallback 标签，由具体平台 adapter 负责真实派发。
