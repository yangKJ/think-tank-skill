# Claude Code Session GC

本文定义 Claude Code 平台如何使用 Session GC 检测和清理 zombie team。

## 集成方式

```yaml
claude_code_session_gc:
  integration_points:
    startup_hook:
      description: "主 agent 启动时自动运行 scan_teams(report_only)"
      trigger: "AGENTS.md 加载后、首次用户交互前"
      output: "GCReport 显示给用户"
    
    pre_council_hook:
      description: "council 模式启动前检查上次残留"
      trigger: "TeamCreate 被调用前"
      action: "如检测到 zombie，提示用户先清理"
    
    manual_trigger:
      description: "用户主动触发清理"
      triggers:
        - "清理 zombie team"
        - "gc team"
        - "session cleanup"
      action: "run_gc(mode='auto_clean')"
```

## Claude Code 特定检测

```yaml
claude_code_indicators:
  config_json_locations:
    - "~/.claude/teams/{team_name}/config.json"
  
  zombie_patterns:
    - pattern: "tmuxPaneId: 'in-process' + agent 无响应 > 10min"
      action: "mark_as_zombie"
    - pattern: "inbox 中有未读 shutdown_request，但无对应 shutdown_approved"
      action: "mark_as_potential_zombie"
    - pattern: "config.json 中 leadSessionId 不匹配当前 session"
      action: "mark_as_clean (old session)"
  
  active_patterns:
    - pattern: "agent inbox 在过去 5 分钟内有消息活动"
      action: "mark_as_active"
    - pattern: "tmuxPaneId 为有效 tmux session ID"
      action: "mark_as_active"
```

## 与 AGENTS.md 协作

```yaml
agents_md_integration:
  on_startup:
    - 执行 scan_teams()
    - 输出 GCReport 摘要
    - 如有 zombie，提示清理命令
  
  artifact:
    path: ".think-tank/artifacts/zombie-teams/"
    format: "{timestamp}-{team_name}.json"
    content: "TeamStatus + GCReport"
```

## 使用示例

```bash
# 扫描报告
python -c "
import sys
sys.path.insert(0, 'think-tank')
from runtime.session_gc import run_gc
report = run_gc(mode='report_only')
print(report.format_summary())
"

# 自动清理（需确认）
python -c "
import sys
sys.path.insert(0, 'think-tank')
from runtime.session_gc import run_gc
report = run_gc(mode='auto_clean', dry_run=False)
print(report.format_summary())
"
```

## 安全提醒

- 默认 `report_only` 模式，绝不自动删除
- `auto_clean` 需要显式指定 + `dry_run=False`
- 最小年龄 10 分钟，避免误杀新建 team
- 不触碰无 config.json 的目录

## 相关文档

- `think-tank/protocol/session-gc-contract.md` — GC 协议
- `think-tank/runtime/session_gc.py` — Python 实现
- `think-tank/platforms/claude-code/teamless-collaboration.md` — 无 Team 协作（事前规避）
