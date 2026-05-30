profile: product-strategist
execution_method: specialist_subagent
status: completed
phase: initial

## Claim

新增 `browser` 和 `adapter` 证据后，`think-tank` 距离 stable release 的判断已经更清楚：外部只读 browser-automation 不再是 blocker，long-running 能力也不应再被笼统表述为“完全缺失”。但 stable release 仍然不能成立，因为当前还缺三类关键闭环：公开发布姿态升级、超出 readonly council 的真实多 agent runtime 证据、以及 long-running subagent lifecycle 证据。

从产品视角看，这次新增证据的价值不在于“已经稳定”，而在于把 stable gap 从模糊的不确定性，收敛成可以逐项验收的明确缺口列表。

## Evidence

1. `think-tank/docs/stable-readiness-matrix.md` 已明确当前 `stable_release_ready: false`，并把 blocker 收敛到三项：
   - `public release posture` 仍是 `public_beta`
   - `multi-agent beyond readonly council` 仍是 `not_verified`
   - `long-running subagent lifecycle` 仍是 `not_verified`

2. `think-tank/examples/platforms/codex/codex-browser-external-readonly.md` 证明外部只读 browser 路径已经形成真实 invocation 证据：
   - `playwright-cli` 已被真实调用
   - `external_dom_read` 和 `external_page_result_recovery` 已发生
   - 状态已经达到 `verified_partial`
   这意味着 browser external readonly 应从 stable blocker 列表里移除，后续只需保持边界说明，不必继续把它当成核心发布障碍。

3. `think-tank/examples/platforms/codex/codex-long-running-adapter-runtime.md` 证明已经存在一条真实 long-running adapter runtime：
   - 有真实 provider invocation
   - 有多步 lifecycle continuation
   - 有 artifact recovery 和 delivery report
   - 状态为 `verified_partial`
   这说明仓库不能再把 long-running 能力整体描述为“没有证据”；准确说法应是：adapter runtime 有证据，但 subagent lifecycle 还没有证据。

4. `think-tank/examples/platforms/codex/codex-true-council-runtime.md` 证明 Codex 已经具备 readonly council 级别的真实 subagent 派发与 role result 回收：
   - `subagents_spawned: true`
   - `role_results_recovered: true`
   - `status: verified_partial`
   但该证据同时明确边界：它只覆盖 readonly repo analysis，不覆盖更高权限、长生命周期、可恢复的多 agent runtime。因此它不能解除 stable 对 “multi-agent beyond readonly council” 的 blocker。

## Risks

1. 最大产品风险是证据升级后出现叙事偷换：把 `browser verified_partial` 误说成“浏览器自动化已稳定”，或把 `long-running adapter runtime` 误说成“subagent lifecycle 已稳定”。

2. 如果继续把 readonly council 当作多 agent runtime 的总代表，stable 发布会在能力边界上失真。用户会以为系统已经验证了长期运行、失败恢复、权限升级和多阶段协作，但当前证据并没有覆盖这些点。

3. 如果发布姿态仍停留在 `public_beta`，即使技术证据继续增加，stable 叙事也会缺少产品层的统一信号。这个问题不是文档修辞，而是发布承诺与真实证据是否同步的问题。

## Recommendations

1. 把 stable 缺口统一改写成三个明确 gate，而不是泛泛说“还需要更多验证”：
   - 发布姿态升级到 `stable_candidate_or_stronger`
   - 新增一条超出 readonly council 的真实多 agent runtime 样例
   - 新增一条真实 long-running subagent lifecycle 样例

2. 对外表述采用分层承诺：
   - browser external readonly: `verified_partial`
   - long-running adapter runtime: `verified_partial`
   - true council readonly runtime: `verified_partial`
   - multi-agent beyond readonly council: `not_verified`
   - long-running subagent lifecycle: `not_verified`
   这样可以保证 stable 之前的产品信息可解释、可回归、不过度承诺。

3. 下一条最高优先级证据不应继续补 browser，也不应重复证明 adapter 已能长跑，而应专门设计一个 `specialist_subagent` 长生命周期样例，覆盖：
   - dispatch decision
   - subagent invocation
   - intermediate artifact recovery
   - failure / retry boundary
   - final role result recovery

4. 在 stable gate 文档或检查脚本中显式区分：
   - adapter runtime evidence
   - subagent runtime evidence
   - readonly council evidence
   避免未来再次把三者混写为单一的 “multi-agent ready”。

## Boundaries

1. 本结论只基于当前四份仓库内证据文件，不代表外部 provider、登录态 browser、Claude Code runtime 或其他平台已经同步完成验证。

2. 本结论讨论的是 stable release 还缺什么，不是重新定义 `think-tank` core 或 `leader-runtime` 的架构归属。

3. 本结果不能把 adapter 证据外推为 subagent 证据，也不能把 readonly council 外推为 full multi-agent runtime 证据。

## Lifecycle Update

```yaml
phase: resumed_after_peer_results
peer_results_reviewed: 2
delta_recommendation: >
  看过 skeptic 和 report-architect 两份 peer 结果后，我没有改变 stable release 的主优先级判断，
  但我会把优先级表达收得更明确：最先要补的已经不是 browser external readonly，也不是重复证明
  adapter long-running，而是按顺序补齐 beyond-readonly 的真实多 agent runtime 证据与
  long-running specialist subagent lifecycle 证据；发布姿态升级仍然重要，但应跟随这两类
  runtime blocker 的补齐同步推进，而不是单独前置成“先改文案就能接近 stable”。
```

peer 结果强化了我原来的判断，没有改变 stable release 仍被三项缺口卡住的结论。

具体调整不在“换优先级”，而在“压实排序”：

1. `skeptic.md` 强化了术语边界，进一步证明不能把 adapter long-running 样例拿来替代 subagent lifecycle。
2. `report-architect.md` 强化了公开叙述结构，说明现在最需要的是把已验证层和 blocked 层并排讲清，而不是继续堆新的模糊表述。

因此，我对 stable release 的优先级判断调整为：

1. 第一优先级：补一条 beyond-readonly 的真实多 agent runtime 样例。
2. 第二优先级：补一条真实 long-running specialist subagent lifecycle 样例。
3. 第三优先级：在前两条证据到位后，再把 `public_beta` 升级到 `stable_candidate_or_stronger`。

这意味着我比 initial 阶段更明确地认为：`stable release posture` 仍然是 blocker，但它不是当前最先应该单独处理的 blocker。当前真正决定 stable 能否成立的，是 runtime 证据缺口，而不是发布措辞缺口。
