# Browser Automation

## 目的

在需要真实浏览器环境、动态页面、登录态、交互或反爬绕过时执行网页任务。

## 适用场景

- 动态渲染页面
- 需要登录态的网页
- 需要点击、滚动、展开、搜索或表单交互
- 静态请求无法获得目标内容

## 输入

```yaml
url: ""
goal: ""
requires_login: false
interaction_needed: false
headless_required: true
```

## 输出

```yaml
content: ""
screenshots: []
extracted_data: []
actions_taken: []
limitations: []
```

## 示例实现

以下为示例，非协议规范。实际 provider 选择由本地 policy 配置决定。

- 通用浏览器自动化 provider
- 可编程浏览器测试 provider

## 降级策略

- 优先使用不打扰用户的后台或无头方式。
- 无法访问登录内容时，向用户说明需要登录或换来源。
- 不应为了浏览器自动化而忽略一手来源优先原则。
- 如果用户环境没有 Browser、Playwright、web-access 或同类能力，必须降级为用户提供材料分析或非浏览器 source-acquisition，并明确未验证动态页面和交互内容。
