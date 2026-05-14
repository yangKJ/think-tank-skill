# schemas

`schemas/` 存放 think-tank 输入输出契约的机器可读版本。

这些 schema 是协议辅助，不替代 `protocol/` 的文字规范。

## 文件

- `input.schema.json`：标准输入结构
- `output.schema.json`：标准输出结构
- `claude-dispatch.schema.json`：Claude Code dispatch 输出结构
- `claude-runtime.schema.json`：Claude Code minimal runtime 输出结构，用于检查成功与失败路径样例
- `runtime-result.schema.json`：平台无关 runtime pipeline 输出结构

## 使用原则

- 平台 adapter 可以把用户输入转换成 schema 兼容结构。
- 平台 adapter 可以把最终输出转换成 schema 兼容结构。
- schema 变更必须遵守 `protocol/versioning.md`。
