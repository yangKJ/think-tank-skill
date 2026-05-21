# Codex Acceptance

本文定义 think-tank 在 Codex 平台上的验收边界。

它回答一个问题：只在 Codex 里，不切到 Claude Code，think-tank 现在到底能证明什么。

## 必须通过

Codex 侧验收必须同时满足：

```yaml
required:
  protocol_check: pass
  codex_validation_check: pass
  schema_sample_check: pass
  research_mode: verified
  council_mode: verified
  review_mode: verified
  strategy_mode: verified
  capability_degradation: verified
  browser_automation_localhost: verified_optional
  minimal_install_behavior: documented
  codex_operating_guide: documented
  codex_capability_status: documented
  codex_operational_usage: verified
  local_source_markdown_artifact: verified
```

## 已证明能力

```yaml
verified:
  - Codex 可以读取 think-tank 主协议
  - Codex 可以选择 mode
  - Codex 可以选择 profiles
  - Codex 可以选择 capabilities
  - Codex 可以用单 agent 多 profile 模拟完成四个核心 mode
  - Codex 可以基于本地仓库证据输出结构化结论
  - Codex 可以在外部 capability 不可用时降级并声明边界
  - Codex Browser 可以作为 optional capability 读取 localhost fixture
  - Codex 有主平台运行手册、任务模板和 capability 状态矩阵
  - Codex 可以把本地资料研究沉淀为仓库内 Markdown artifact
  - Codex 可以把 research-to-video 任务交给本地长生命周期 adapter，并回收产物
  - Codex 可以派发 specialist subagents 在独立 write scope 中写入并续跑更新结果
```

## 不能声称

```yaml
not_verified:
  - Claude Code Agent Team 已验证
  - 真实多 agent 并行执行已验证
  - 外部网页通用浏览能力
  - yt-dlp 已集成
  - obsidian 已集成
  - xiaohongshu 已集成
  - media transcription 已集成
  - 任意用户只安装 think-tank 后自动拥有 Browser 或 Playwright
```

## 验收命令

在仓库根目录运行：

```bash
python3 checks/protocol_check.py
python3 checks/codex_validation_check.py
python3 checks/claude_code_validation_check.py
python3 checks/claude_dispatch_sample_check.py
python3 checks/claude_runtime_sample_check.py
python3 checks/minimal_runtime_execution_check.py
python3 checks/capability_queue_check.py
python3 checks/schema_sample_check.py
```

前三个命令都通过，才可以说 Codex foundation 和 Claude Code 状态边界没有冲突；八个命令都通过，才可以说当前仓库验证产物完整。

## 通过标准

```yaml
pass:
  - 所有必备文件存在
  - 四个核心 mode 都有 Codex 验证样例
  - 每个样例都有边界声明
  - 每个样例都有 Quality Check
  - minimal install 行为明确
  - optional capability 与 core dependency 明确区分
  - 未验证能力保持 planned 或 not_verified
```

## 失败标准

以下任一情况都不能通过：

- 把单 agent 多 profile 模拟说成真实多 agent。
- 把 Browser 本地 fixture 验证说成通用浏览能力。
- 把 capability 文档存在说成外部 skill 已安装。
- 输出缺少边界声明。
- `checks/protocol_check.py`、`checks/codex_validation_check.py` 或 `checks/claude_code_validation_check.py` 失败。
- `checks/claude_dispatch_sample_check.py` 失败。
- `checks/claude_runtime_sample_check.py` 失败。
- `checks/schema_sample_check.py` 失败。

## 当前结论

Codex 平台当前适合作为 think-tank 的 foundation 验证环境。

当前已经达到 Claude Code preflight 前的 Codex 停止点。

如果继续留在 Codex，只建议做真实用户任务验证，不再扩张 foundation 范围。

下一阶段若推进平台能力，应切到 Claude Code 做：

1. Claude Code skill entrypoint 验证。
2. Claude Code subagent/profile 映射验证。
3. Claude Code skill/capability 映射验证。
4. Claude Code result recovery 验证。

但 Claude Code 的 subagent 和旧 `.claude/skills` 映射仍应留到 Claude Code 平台验证。
