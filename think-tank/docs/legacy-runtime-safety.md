# Legacy Runtime Safety

本文把旧 think-tank 的安全经验收敛为当前主仓的 runtime 安全要求。

## 来源

旧资产包括：

- `references/safety.md`
- `scripts/safe_filename.py`
- `scripts/prompt_defender.py`
- `scripts/dangerous_cmd_detector.py`
- `scripts/data_sanitizer.py`
- `scripts/cycle_detector.py`

## 当前落点

```text
think-tank/runtime/safety.py
```

该模块只提供平台无关 helper，不执行命令、不写私有目录、不创建 Claude Team。

## 安全要求

### 1. 文件名和路径

任何 adapter 在写入 artifact、checkpoint、result 前必须：

- 拒绝 `..`、绝对路径、反斜杠、空字节。
- 将用户输入转为安全文件名。
- 不把用户输入直接拼接为真实路径。

### 2. 命令风险

think-tank core 不执行 shell 命令。平台 adapter 如果要执行命令，必须先做危险命令检测。

需要阻断的类别：

- 递归删除。
- 提权。
- 修改全局权限。
- 格式化磁盘。
- 原始块设备写入。
- fork bomb。

### 3. 外部内容

进入 evidence、sources、discussion 的外部内容必须：

- 对明显密钥做 redaction。
- 对 prompt injection 模式做标注。
- 在边界里说明外部来源未被信任。

### 4. Claude Code Team 风险

旧 Agent Team 路径的经验保留在 Claude Code adapter 文档中：

- 需要显式清理 Team。
- 需要超时。
- 需要 checkpoint。
- 需要避免把未验证用户输入直接送进 sub-agent。

这些要求不进入 core protocol 的工具调用细节，但进入平台适配的验收边界。

## 状态

```yaml
safety_runtime_helpers: implemented
claude_team_cleanup_runtime: documented_only
dangerous_command_execution: not_in_core
secret_redaction: helper_available
prompt_injection_detection: helper_available
```

