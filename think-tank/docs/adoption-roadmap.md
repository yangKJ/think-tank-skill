# Adoption Roadmap

## Phase 1: 主仓骨架

- 建立 README、SKILL、protocol、platforms、modes、docs、examples
- 固化 think-tank 的主品牌和三层结构
- 明确 research 与 agent-council 的新定位

## Phase 2: 协议细化

- 补全输入输出 schema
- 固化质量门禁
- 定义 mode 选择规则
- 定义角色组合策略

## Phase 3: 旧资产吸收

- 从旧 research think-tank 中迁移可复用研究流程
- 从 agent-council 中迁移多角色讨论机制
- 标注 mock、tracking、verified、planned 能力边界
- 建立 `docs/legacy-assets-inventory.md`
- 建立 research 与 agent-council 的迁移说明

## Phase 4: 平台适配

- 完成 Claude Code adapter
- 完成 Codex adapter
- 定义真实执行、结果回收和失败恢复契约
- 完成 Codex 四个核心 mode 的内部验证
- 完成 Codex Browser 本地 fixture optional capability 验证
- 准备 Claude Code preflight，避免旧实现反向污染主协议

## Phase 5: 可复用发布

- 增加示例
- 增加测试或协议检查脚本
- 增加贡献和版本演进规则

## Phase 6: Minimal Runtime

- 实现 Claude Code minimal runtime
- 只覆盖 `source-acquisition`
- 只覆盖公开静态网页只读读取
- 输出 `dispatch_request`、`dispatch_decision`、`invocation`、`recovery`、`sources[]`、`evidence[]`
- 增加成功和失败路径样例
- 不接入高风险外部 skills

## Phase 7: Optional Capability Expansion

- 按 `docs/capability-validation-roadmap.md` 逐个验证 capability
- 优先 `browser-automation` 只读 DOM
- 再验证仓库内 knowledge persistence
- 最后才考虑 media/social/private-write 能力

## 当前 Codex 收敛状态

```yaml
codex_foundation:
  protocol_check: pass
  codex_validation_check: pass
  schema_sample_check: pass
  core_modes: verified
  capability_degradation: verified
  browser_localhost_optional: verified_optional
  local_source_markdown_artifact: verified
  external_source_readonly: verified
  browser_external_readonly: blocked
  claude_capability_auto_mapping: verified_partial_pre_invocation_decision
  claude_minimal_runtime_contract: implemented_as_repeatable_contract
  ready_for_claude_code_preflight: true
```
