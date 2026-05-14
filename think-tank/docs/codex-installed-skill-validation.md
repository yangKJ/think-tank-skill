# Codex Installed Skill Validation

本文记录 think-tank 在当前 Codex 本机环境中的安装验证。

## 安装方式

```yaml
install_method: repository_relative_symlink
source: <repo>/think-tank
target: <repo>/.codex/skills/think-tank
symlink_target: ../../think-tank
status: installed
```

使用仓库内软链接的原因：

- `think-tank/` 是唯一主 Skill 源。
- Codex 实际读取 `.codex/skills/think-tank` 时，读到的就是同一份主 Skill。
- 不需要 rsync 同步，避免双真相源。
- 软链接目标在当前仓库内，不依赖旧 research agent 目录。

## 已验证

```yaml
skill_entrypoint_readable: true
entrypoint: <repo>/.codex/skills/think-tank/SKILL.md
repository_relative_symlink: true
symlink_resolves_to_source: true
subagent_runtime_check: passing
role_result_schema_check: passing
```

## 当前边界

```yaml
project_codex_skill_files_installed: verified
codex_can_read_skill_entrypoint: verified
current_thread_skill_list_refresh: requires_new_session_or_loader_refresh
true_parallel_subagent_runtime: not_verified
single_agent_multi_profile_fallback: supported
```

当前线程启动时的 Codex skill 列表不会自动重新加载新安装 skill。因此本次验证证明的是：

- 项目内文件系统安装路径正确。
- 项目内 Codex skills 目录可读取 think-tank。
- 主仓 runtime/schema checks 通过。

要验证 Codex UI/loader 是否把 `think-tank` 作为可触发 skill 列入，需要新开 Codex 线程或刷新 skill loader 后发送真实触发 prompt。

## 真实触发 Prompt

新 Codex 线程中使用：

```text
用 think-tank council mode 讨论：
在 Codex 平台没有已验证真实 subagent runtime 的情况下，think-tank 应如何执行专业角色协作？

要求：
1. 明确 selected_mode、selected_profiles、execution_method。
2. 如果没有独立 subagent runtime，必须标记 single_agent_multi_profile_fallback。
3. 每个 profile 输出 role-result 结构。
4. 最终输出结论、依据、分歧、风险、行动建议、边界。
5. 不得声称 true_parallel_runtime_verified。
```

验收标准：

```yaml
skill_loaded: true
execution_method_labeled: true
role_result_shape_present: true
fallback_not_overclaimed: true
quality_check_present: true
```
