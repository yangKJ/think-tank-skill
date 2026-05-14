# External Capability Testing Strategy

本文定义 think-tank 何时以及如何测试外部 skills 或平台插件。

## 基本判断

外部 capability 集成是增强能力，不是 think-tank 的最低运行要求。

只安装 think-tank 的用户仍应能执行：

- 协议判断
- mode 选择
- profile 模拟
- 基于用户提供材料的分析
- 结构化输出
- 边界声明

## 测试顺序

```text
1. core protocol validation
2. mode validation
3. capability degradation validation
4. single optional capability integration
5. multi-capability workflow
6. platform-specific multi-agent runtime
```

## 当前状态

```yaml
core_protocol_validation: verified
codex_mode_validation:
  research: verified
  council: verified
  review: verified
  strategy: verified
capability_degradation:
  media_processing_unavailable: verified
  social_listening_unavailable: verified
  knowledge_persistence_local_markdown_only: verified
  browser_automation_unavailable: verified
external_capability_integration:
  browser_automation_codex_localhost: verified_optional
  other_capabilities: planned
```

## 第一个可选集成候选

```yaml
candidate: browser-automation
status: verified_optional_for_codex_localhost_fixture
reason:
  - 与 Codex 环境相对接近
  - 不涉及私有知识库写入
  - 不涉及社媒登录和反爬
  - 不涉及视频下载和转录依赖
```

验证记录：

```text
think-tank/docs/browser-automation-integration-report.md
```

## 集成测试规则

测试外部 capability 时必须记录：

```yaml
capability: ""
implementation: ""
platform: ""
installed_or_available: true
executed: true
result_recovered: true
fallback_available: true
status: verified | failed | skipped
boundary: []
```

## 不能做的事

- 不把某个外部 skill 当成 think-tank 默认依赖。
- 不因为当前环境有 Browser/Playwright，就假设其他用户也有。
- 不一次接入多个外部 skills。
- 不在未验证结果回收前标记为 verified。
- 不默认写用户私有目录。
