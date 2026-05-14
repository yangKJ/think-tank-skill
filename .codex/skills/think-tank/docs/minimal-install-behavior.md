# Minimal Install Behavior

本文定义用户只安装 think-tank、没有安装任何外部 skills 或平台插件时的行为。

## 核心原则

think-tank 必须在最小安装下可用。

最小安装只保证：

- 读取 think-tank 协议
- 选择 mode
- 选择 profiles
- 选择 capabilities
- 根据用户提供材料进行分析
- 输出结构化结论、风险和行动建议
- 明确声明无法验证的边界

最小安装不保证：

- 浏览网页
- 下载视频
- 转录音频
- 抓取社媒
- 写入 Obsidian
- 调用外部 MCP
- 启动真实多 agent runtime

## 能力分级

```yaml
required:
  - protocol execution
  - mode selection
  - profile simulation
  - structured output
  - boundary declaration

optional:
  - browser automation
  - web search/fetch
  - media processing
  - social listening
  - knowledge persistence
  - true multi-agent runtime
```

## 最小安装下的执行方式

```text
用户任务
  -> think-tank 判断 mode
  -> think-tank 选择 profiles
  -> think-tank 选择 capabilities
  -> 如果 capability 无实现，则降级
  -> 基于用户提供材料和当前平台可用能力输出
  -> 标注未验证边界
```

## 示例

用户请求：

```text
帮我分析这个网页上的产品策略。
```

如果没有浏览器能力，think-tank 应回复：

```text
当前环境没有可用浏览器自动化能力。我可以基于你粘贴的网页正文、截图 OCR 内容或摘要进行分析；如果需要验证动态页面、登录态内容或隐藏区域，需要安装或启用 browser-automation capability。
```

## 平台 adapter 责任

平台 adapter 必须区分：

- capability 被选择
- capability 有可用实现
- capability 已真实执行
- capability 只走降级路径

不能因为 capability 文件存在，就声称外部工具已经可用。

