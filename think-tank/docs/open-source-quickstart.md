# Open Source Quickstart

本文给第一次使用公开 `think-tank` 仓库的用户一个最短上手路径。

## 适合谁

适合：

- 想把复杂研究、审议、review、strategy 任务收口到一个高阶 Skill 协议中的用户
- 愿意接受 `verified`、`verified_partial`、`planned`、`blocked` 这些显式状态边界的用户
- 主要在 Codex 环境中工作，并接受最小安装先跑通 core protocol 的用户

不适合：

- 希望安装后自动获得全套外部 provider 的用户
- 希望默认拥有稳定跨平台多 agent runtime 的用户
- 不愿意处理权限、登录态、网络和 provider 单独验收的用户

## 最小安装预期

只安装 `think-tank` 时，默认保证：

- protocol execution
- mode selection
- profile simulation
- local file analysis
- user-provided material analysis
- structured output
- boundary declaration

只安装 `think-tank` 时，默认不保证：

- external browser automation
- social media scraping
- video download
- audio transcription
- private knowledge-base write
- full multi-agent runtime

## 推荐阅读顺序

```text
README.md
  -> think-tank/README.md
  -> think-tank/examples/usage/
  -> think-tank/platforms/codex/operating-guide.md
  -> think-tank/docs/support-matrix.md
  -> think-tank/docs/validation-tiers.md
  -> think-tank/docs/provider-ecosystem-examples.md
  -> think-tank/docs/open-source-release.md
```

## 两种使用方式

```text
clone as repo
  -> run release checks from repository root

copy as skill
  -> copy think-tank/ into your platform skill directory
  -> keep .think-tank/ as project-local runtime data, not as public skill source
```

## 最小验证命令

在仓库根目录运行：

```bash
python3 checks/open_source_release_suite.py
python3 checks/protocol_check.py
python3 checks/codex_validation_check.py
python3 checks/schema_sample_check.py
python3 checks/minimal_runtime_execution_check.py
python3 checks/release_privacy_check.py
python3 checks/open_source_release_check.py
```

如果这 6 条都通过，可以确认：

- 公开协议骨架完整
- Codex foundation 路径没有明显回归
- 样例和最小 runtime 仍可执行
- 公开仓库没有明显本地私有路径泄漏
- 对外发布文案仍保持保守边界

## 第一次实际使用

推荐先从以下任务开始：

- research mode
- review mode
- strategy mode

先用本地文件或用户提供材料验证，再考虑外部 provider。

可直接复制的模板：

```text
think-tank/examples/usage/research-request.md
think-tank/examples/usage/council-decision.md
think-tank/examples/usage/review-acceptance.md
```

## 升级路径

```text
minimal install
  -> local/user-provided analysis
  -> one optional provider
  -> provider-specific invocation evidence
  -> multi-capability workflow
  -> verified_partial multi-agent runtime
  -> wider public beta confidence
```

## 硬边界

- route selection 不等于 provider invocation
- provider installed 不等于 capability verified
- single-agent multi-profile 不等于 true multi-agent runtime
- localhost browser fixture 不等于 external browser automation
