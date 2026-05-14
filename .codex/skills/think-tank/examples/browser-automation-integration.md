# Browser Automation Integration

本文件记录 think-tank 在 Codex 平台的 optional browser-automation 最小集成测试。

## 测试任务

```text
验证 think-tank 是否能通过 browser-automation capability 打开一个网页目标，读取 DOM，并回收证据。
```

## 执行声明

```yaml
platform: codex
capability: browser-automation
implementation: Codex in-app Browser
status: verified_optional_enhancement
minimum_install_requirement: false
```

## 测试目标

本次使用本仓库内的静态 HTML fixture：

```text
think-tank/examples/browser-automation-fixture.html
```

通过本机静态服务访问：

```text
http://127.0.0.1:8765/think-tank/examples/browser-automation-fixture.html
```

## 执行结果

浏览器成功打开页面，并回收 DOM 证据：

```yaml
title: think-tank browser automation fixture
url: http://127.0.0.1:8765/think-tank/examples/browser-automation-fixture.html
root_count: 1
mode_text: "mode: research"
capability_text: "capability: browser-automation"
claim_text: "browser automation is optional, not a core dependency."
```

## 重要边界

直接访问 `file://` 本地文件被 Browser 安全策略阻止。本次没有绕过策略，而是改用 Browser 支持的 `localhost` 本地目标。

该结果证明：

- 当前 Codex 环境可以通过 Browser 执行 browser-automation capability。
- browser-automation 可以回收网页 DOM 证据。
- browser-automation 是 optional enhancement，不是 think-tank 最小安装依赖。

该结果不证明：

- 所有用户的 Codex 都安装了 Browser。
- Playwright 插件在所有环境可用。
- 外部网站、登录态页面或动态网页都能稳定访问。
- Claude Code 的 web-access 或 playwright-cli 已集成。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

