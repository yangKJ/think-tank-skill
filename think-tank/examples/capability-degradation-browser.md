# Capability Degradation: Browser Automation

## 测试任务

```text
用户要求打开网页并提取证据；当前用户环境只安装 think-tank，没有 Browser、Playwright、web-access 或其他浏览器自动化能力。
```

## 执行声明

```yaml
platform: codex
mode: research
capability: browser-automation
external_capabilities:
  browser_plugin: unavailable
  playwright: unavailable
  web_access: unavailable
execution_method: degradation_path
```

## 降级执行

当 browser-automation 不可用时，think-tank 不能声称已经打开网页、点击页面、读取 DOM 或完成动态页面验证。

可执行降级路径：

1. 请求用户提供网页正文、截图、导出文本或关键片段。
2. 如果平台仍有基础 web search/fetch 能力，可切换到 `source-acquisition`，但必须说明不是浏览器自动化。
3. 如果没有任何联网或浏览能力，仅基于用户提供材料分析。
4. 动态页面、登录态内容、需点击展开内容必须标注未验证。

## 可输出结果

```yaml
content: ""
screenshots: []
extracted_data: []
actions_taken: []
limitations:
  - 未打开真实浏览器
  - 未执行页面交互
  - 未读取动态渲染内容
  - 只能基于用户提供材料或平台可用的非浏览器来源分析
```

## 验证结论

browser-automation capability 不应作为 think-tank 的默认依赖。只安装 think-tank 的用户仍可使用协议、mode、profiles、capabilities 和结构化输出，但涉及网页交互的任务必须降级或请求用户补充材料。

## Quality Check

```yaml
protocol_complete: true
evidence_boundary_clear: true
actionable: true
```

