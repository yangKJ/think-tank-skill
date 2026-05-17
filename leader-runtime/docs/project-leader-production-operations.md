# Project Leader Production Operations

这份手册定义 leader 化能力的实战验证、稳定性观察与放量策略。目标是验证控制面闭环是否稳定、主控边界是否可信、主机接入是否可持续。

## 实战原则

1. 不允许把 `planned_uninvoked`、`ready_uninvoked`、`ready_for_host_dispatch` 直接当作真实调用成功。
2. 只在 host 返回 `invoked: true` 的 evidence 上才允许升级 `invocation` 状态。
3. 任何回归都先回到“selection only”模式，保留基础研究与决策能力。

## 阶段 0：预热（1-2 天）

- 执行本地闭环样本，确认环境和输出字段完整。
- 建议每个项目只做一次：

```bash
python3 leader-runtime/runtime/project_leader_pilot.py \
  leader-runtime/examples/project-leader-pilot.sample.yaml
```

关注字段：

- `selection_result.selected_count`
- `review_report.promoted_count`
- `project_team_activation.candidate_agents`
- `project_candidate_invocation_gate.decision_status`
- `project_candidate_host_dispatch_bundle.dispatch_status`
- `project_candidate_invocation_evidence.successful_invocations`

通过标准：

- 关键字段都存在；
- `project_candidate_host_dispatch_bundle.dispatch_status == ready_for_host_dispatch`；
- 若无真实 host 回灌，`project_candidate_invocation_evidence` 允许为空；
- 说明文本位于 `boundaries` 中，含有“非真实调用”边界提示。

## 阶段 1：真实 Host 灰度（1-2 周）

每个任务执行后保留 host request 与 host result 两份文件，以便 `project_candidate_invocation_evidence` 回灌。

1. 先走 selection + review + activation：

```bash
python3 leader-runtime/runtime/project_leader_pilot.py leader-runtime/examples/project-leader-pilot.sample.yaml
```

2. 将 `project_candidate_host_dispatch_bundle` 发给 host（若无真实 host，可先用本地 runner 仿真）：

```bash
python3 leader-runtime/runtime/project_candidate_host_runner.py \
  --bundle-json /tmp/host_dispatch_bundle.json \
  --output-json /tmp/host_results.json \
  --host-provider ${HOST_PROVIDER:-codex-host-adapter} \
  --run-id ${RUN_ID}
```

3. 真实 host 场景可直接替换为你的 host adapter，接收 `host_results.json` 后回灌：

```bash
python3 leader-runtime/runtime/project_leader_pilot.py \
  leader-runtime/examples/project-leader-pilot.sample.yaml
```

4. 若你有 host 回执文件（`results.json`），在 pilot spec 中填 `candidate_host_results`，让一次命令直接回灌 evidence。

- 第一次必须是“显式 allow + verified partial”：

```yaml
allow_candidate_invocation: true
candidate_runtime_support: verified_partial
```

验收标准：

- host 回执中包含 `task_id + candidate_agent_id + invocation_status + result_ref + summary`；
- `project_candidate_invocation_evidence.results` 中命中的结果 `invoked` 与 host 回执一致；
- 失败场景下 `project_candidate_invocation_gate` 与 `boundaries` 能明确失败边界（如 blocked/disabled/missing).

## 阶段 2：稳定性监控（3-7 天）

- 每日固定时段跑 5-15 次 pilot 或真实任务。
- 记录时间窗口内指标：
  - 成功率（包括 evidence 成功）；
  - `blocked/ready_uninvoked/ready_for_host_dispatch` 分布；
  - host 回灌失败率；
  - 平均决策耗时；
  - 需要手工降级恢复的比例。
- 建议阈值：
  - 关键链路成功率（含 evidence）≥ 95%；
  - 无 `invoked` 误报；
  - host 回执失败可恢复率 ≥ 99%；
  - 无边界缺失（每个运行都应有边界声明）。

## 生产放量步骤

1. 周期内只允许 1 个 pilot 项目并发 1-2 条任务流。
2. 第 1 周可接受 `selection only` 与 `host-disabled fallback` 同时存在。
3. 第 2 周开始允许 `ready_for_host_dispatch` 任务 30% 进入 host。
4. 第 3 周开始按任务优先级放量，保持人工复核节奏不降。

## 运行日志与追踪模板

把每次运行记录在一个独立文件，建议字段如下：

```yaml
run_id:
project_id:
timestamp:
request:
selection_count:
promoted_count:
activated_candidate_count:
dispatch_status:
invocation_gate_status:
bundle_status:
successful_invocations:
failed_invocations:
boundary_violations:
host_error:
manual_fallback_count:
operator_notes:
```

可直接落到：

- `leader-runtime/observations/<run_id>-pilot-run.yml`

## 一周验收清单（你最后验收时看这 6 项）

1. 所有 `invoked: true` 都来自 host evidence 文件。
2. `boundaries` 明确说明 `ready_*` 与 `invoked` 的差异。
3. `project_team_activation` 只包含已 promote 的 candidate。
4. Host 回灌失败不会导致伪造成功，也不会吞掉运行痕迹。
5. 降级策略（blocked/not_applicable/retry）始终可回放。
6. 指标变化有可观察趋势，能指导是否加速放量。
