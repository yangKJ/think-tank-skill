# Browser Automation Integration Report

本文记录 think-tank 在 Codex 平台对 `browser-automation` capability 的最小集成测试。

## 验证范围

```yaml
platform: codex
capability: browser-automation
implementation: Codex in-app Browser
test_target: localhost static fixture
network_external: false
status: verified_optional_enhancement
```

## 验证过程

1. 创建本地 HTML fixture。
2. 尝试直接打开 `file://`。
3. Browser 安全策略阻止 `file://` 访问。
4. 改用本地 `localhost` 静态服务。
5. Browser 成功打开页面。
6. 读取页面标题、URL 和 DOM test id。
7. 回收证据并写入示例。

## 验证结果

```yaml
browser_automation:
  local_file_direct_access: blocked_by_policy
  localhost_static_fixture: verified
  dom_snapshot: verified
  testid_locator: verified
  result_recovery: verified
  external_site_validation: verified_partial
```

## 对 think-tank 的意义

这证明 browser-automation 可以作为 Codex 平台的可选增强能力：

- 能打开受支持的本地网页目标。
- 能读取 DOM。
- 能把网页证据带回 think-tank 输出。

但它不能成为最小安装要求。只安装 think-tank 的用户仍然必须能走降级路径。

## 当前能力状态

```yaml
capabilities:
  browser_automation_unavailable_degradation: verified
  browser_automation_codex_localhost_integration: verified_optional
  browser_automation_external_web: verified_partial
  media_processing_external_skill: planned
  social_listening_external_skill: planned
  knowledge_persistence_external_skill: planned
```

## 下一步建议

下一步仍不建议一次安装多个 skills。

可以选择两个方向之一：

1. 准备 Claude Code preflight，验证旧 research agent 和 agent-council 能否作为平台适配素材被吸收。
2. 继续把验证范围从静态外部只读页面推进到登录态、点击交互和复杂动态页面，但仍保持 optional，并避免夸大为通用浏览器能力。
