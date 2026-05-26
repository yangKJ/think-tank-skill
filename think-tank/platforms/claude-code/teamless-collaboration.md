# Claude Code Teamless Collaboration

本文定义如何在 Claude Code 平台使用 Filesystem Message Bus 替代 Team API 进行多 agent 协作。

## 核心思路

绕过 `TeamCreate/TeamDelete/SendMessage` API，直接通过文件系统传递消息：

```
主 agent 创建 bus 目录 → Agent tool spawn subagent → subagent 读写文件 → 主 agent 收集结果 → 清理 bus
```

## 执行流程

### Step 1: 创建消息总线

```python
import sys; sys.path.insert(0, 'think-tank')
from runtime.filesystem_bus import create_bus

bus = create_bus(
    run_id="council-20260524",
    profiles=["collector", "domain-expert", "skeptic"],
    base_dir=".think-tank/runs"
)
```

产生目录结构：
```
.think-tank/runs/council-20260524/bus/
├── dispatch/          # 任务文件
├── results/           # 结果文件
├── signals/           # shutdown/ack 信号
└── state/state.json   # 共享状态
```

### Step 2: 派发任务

```python
from runtime.filesystem_bus import dispatch_tasks

tasks = [
    {"profile": "collector", "objective": "收集 think-tank 核心能力"},
    {"profile": "domain-expert", "objective": "分析技术架构"},
    {"profile": "skeptic", "objective": "提出质疑和改进"},
]

dispatch_tasks(bus, tasks)
```

### Step 3: Spawn Subagent（不使用 team_name）

```
Agent(
    description="collector - 收集信息",
    name="collector",
    prompt="
        你是 think-tank collector 角色。

        任务在文件系统中：
        - 任务文件: .think-tank/runs/council-20260524/bus/dispatch/*collector*.json
        - 结果文件: .think-tank/runs/council-20260524/bus/results/collector-result.json

        步骤：
        1. 读取 dispatch 目录中找到你的任务文件
        2. 使用 Read 工具读取任务定义
        3. 执行任务
        4. 将 RoleResult 写入 results/ 目录
        5. 检查 signals/ 中是否有 shutdown_request
        6. 如有，写入 shutdown_approved 信号并退出

        不要: 使用 SendMessage（我们不在 Team 模式中）
    ",
    subagent_type="Software Architect",
    run_in_background=true
    # 注意: 不传递 team_name 参数！
)
```

### Step 4: 收集结果

```python
from runtime.filesystem_bus import collect_results

results = collect_results(bus, timeout_seconds=60)
# → {"collector": {...}, "domain-expert": {...}, "skeptic": {...}}
```

### Step 5: Shutdown

```python
from runtime.filesystem_bus import send_shutdown

approved = send_shutdown(bus)
# → {"collector": True, "domain-expert": True, "skeptic": False}
```

### Step 6: 清理

```python
from runtime.filesystem_bus import cleanup_bus

cleanup_bus(bus)
```

## Subagent Prompt 模板

```
你是 think-tank 的 {profile} 角色。

你的任务定义在文件系统中：
- 任务文件: .think-tank/runs/{run_id}/bus/dispatch/{profile}-*.json
- 结果文件: .think-tank/runs/{run_id}/bus/results/{profile}-result.json
- 信号目录: .think-tank/runs/{run_id}/bus/signals/

执行步骤：
1. 读取任务文件，理解你的 objective
2. 执行你的 profile 职责（使用 Read、WebSearch 等工具）
3. 将结构化 RoleResult 写入结果文件
4. 检查 signals/ 中是否有 shutdown_request.json
5. 如收到 shutdown_request，写入 shutdown_approved 信号

禁止：
- 不要调用 SendMessage（我们不在 Team 模式中）
- 不要尝试 TeamCreate 或 TeamDelete
- 结果必须写入指定文件路径，不要写错

输出格式 (写入结果文件):
{
  "message_id": "uuid",
  "from": "{profile}",
  "to": "facilitator",
  "type": "result",
  "timestamp": "ISO8601",
  "payload": {
    "role_result": {
      "profile": "{profile}",
      "execution_method": "specialist_subagent",
      "claim": "你的主要结论",
      "evidence": [...],
      "risks": [...],
      "objections": [...],
      "recommendations": [...],
      "boundaries": [...]
    }
  }
}
```

## 与 Team API 模式对比

| 维度 | Team API 模式 | Teamless 模式 |
|------|-------------|--------------|
| 通信 | 实时推送 (SendMessage) | 文件轮询 (1s 间隔) |
| 可靠性 | 有 shutdown_deadlock bug | 高 (原子写入) |
| 清理 | TeamDelete 可能失败 | 直接 rm -rf bus 目录 |
| Setup | TeamCreate | create_bus() |
| 消息持久化 | inbox 文件 | JSON 文件（可审计） |
| 并发安全 | 系统保证 | 原子写入保证 |

## 降级策略

```yaml
degradation:
  primary: "Team API 模式（正常情况）"
  fallback: "Teamless 模式（本方案）"
  final_fallback: "single_agent_multi_profile_fallback"
  
  trigger_conditions:
    - "TeamDelete 连续失败 2 次"
    - "shutdown_approved 后 30s agent 未终止"
    - "用户要求 '用文件模式'"
```

## 相关文档

- `think-tank/protocol/filesystem-message-bus.md` — 总线协议
- `think-tank/runtime/filesystem_bus.py` — Python 实现
- `think-tank/platforms/claude-code/session-gc.md` — Zombie 清理（事后修复）
