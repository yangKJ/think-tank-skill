# platforms

`platforms/` 是 think-tank 的平台适配层。

平台适配层负责把 `protocol/` 的统一协议映射到具体运行环境。它允许存在执行差异，但不允许改变 think-tank 的核心行为。

## 允许不同

- runtime
- subagent 调用方式
- 文件和目录布局
- 中间状态保存方式
- 记忆落点
- hook 方式
- 权限和工具限制

## 不允许不同

- 触发条件
- 核心流程阶段
- mode 语义
- 角色职责
- 输出结构语义
- 质量门禁

## 第一批平台

- `claude-code/`
- `codex/`

每个平台目录至少应包含：

- `README.md`：平台适配概览
- `adapter.md`：该平台如何执行统一 think-tank 协议
