# Session GC Contract

本文定义 think-tank Session 级别的垃圾回收（GC）协议，用于检测和清理 Claude Code 等平台的残留 team 资源。

## 目的

防止 zombie team 长期堆积，影响用户体验和资源管理。Session GC 是跨平台协议，不仅适用于 Claude Code。

## Zombie 检测标准

```yaml
zombie_indicators:
  - condition: "config.json 中 tmuxPaneId 为 'in-process' 且超过 TTL"
    severity: high
  - condition: "config.json 中 state 为 'terminated' 但目录未清理"
    severity: medium
  - condition: "无 config.json 的孤立目录"
    severity: low
  - condition: "agent 超过 3 次 shutdown_approved 但未实际终止"
    severity: high
```

## 分类体系

```yaml
team_classification:
  clean:
    description: "正常终止，可安全删除"
    indicators:
      - "config.json 中 tmuxPaneId 为空或 'terminated'"
      - "所有 agent inbox 无未读消息"
  
  zombie:
    description: "状态卡死，需清理"
    indicators:
      - "tmuxPaneId: 'in-process' 且超过 TTL"
      - "leadSessionId 不匹配当前 session"
  
  orphan:
    description: "无配置文件，可能是部分创建的"
    indicators:
      - "目录存在但无 config.json"
  
  active:
    description: "正在运行，不可触碰"
    indicators:
      - "在过去 5 分钟内有消息活动"
      - "tmuxPaneId 为有效 session ID"
  
  unknown:
    description: "无法判断，需人工确认"
    indicators:
      - "config.json 损坏或不可读"
      - "不符合以上任何分类"
```

## GC 操作模式

```yaml
gc_modes:
  report_only:
    description: "仅输出检测报告，不执行任何清理"
    default: true
    output: "GCReport"
  
  auto_clean:
    description: "自动清理 zombie + clean + orphan"
    requires_confirmation: true
    safety_checks:
      - "min_age_seconds: 600"
      - "require_config_json: true"
      - "不触碰 active 和 unknown 分类"
  
  interactive:
    description: "逐个询问用户确认后清理"
    behavior: "逐个枚举待清理 team，等待用户确认"
```

## 安全约束

```yaml
safety:
  min_age_seconds: 600           # team 目录至少存在 10 分钟
  require_config_json: true      # 必须有 config.json 才判断
  backup_before_delete: false    # 暂不做备份（可配置）
  max_batch_size: 50             # 单次最多清理 50 个
  skip_unknown: true             # 跳过 unknown 分类，只提示
  dry_run_first: true            # auto_clean 前先 report_only

zombie_agent_safety:
  grace_period_seconds: 30       # shutdown_request 发后等待期
  max_shutdown_approvals: 3      # 超过此数视为确认 zombie
  orphan_timeout_seconds: 120    # 无响应超过此时间视为 orphan
```

## GC 报告格式

```yaml
gc_report:
  scan_time: "ISO8601 timestamp"
  team_root: "~/.claude/teams/"
  total_teams: 0
  classifications:
    clean: 0
    zombie: 0
    orphan: 0
    active: 0
    unknown: 0
  actions_taken: []
  manual_cleanup_required: []

team_status:
  team_name: ""
  team_path: ""
  classification: "clean | zombie | orphan | active | unknown"
  member_count: 0
  tmux_pane_states: {}
  last_modified: ""
  evidence: []
```

## Session 启动时默认行为

```yaml
on_session_start:
  policy: "auto_scan"
  mode: "report_only"             # 仅报告，不清理
  action: "输出 GCReport 到主 agent"
  zombie_heads_up: true           # 如有 zombie，提示用户
```

## 相关文档

- `think-tank/protocol/shutdown-contract.md` — 正常 shutdown 流程
- `think-tank/protocol/runtime-contract.md` — 运行时契约
- `think-tank/platforms/claude-code/session-gc.md` — Claude Code 适配

## 状态

```yaml
session_gc_contract: specified
zombie_detection: specified
classification: specified
gc_modes: specified
safety_constraints: specified
implementation: pending
```