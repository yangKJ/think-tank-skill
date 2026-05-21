# Stable Release Checklist

本文是准备从 `public_beta` 升级到 stable release 前的执行清单。

## 文档与边界

- [ ] `open-source-packages.yaml` 与实际公开范围一致
- [ ] `open-source-release.md` 公开承诺更新为 stable 候选表述
- [ ] `support-matrix.md` 中 blocked/planned 项目已同步
- [ ] `README.md` 不再保留 beta-only 提示，或明确说明剩余实验范围

## 证据

- [ ] 三条 optional provider invocation 样例存在且带 `dispatch_decision`
- [ ] 三条样例都带 `sources[]` / `evidence[]` / `boundaries[]`
- [ ] external browser readonly 至少一条成功样例
- [ ] multi-agent runtime 至少一条超出 readonly council 的成功样例
- [ ] long-running lifecycle 至少一条成功样例

## 检查

- [ ] `python3 checks/open_source_release_suite.py`
- [ ] `python3 checks/stable_release_check.py`
- [ ] GitHub Actions release gate 通过

## 发布姿态

- [ ] 版本号不再停留在纯 beta 心智
- [ ] 对外文案不再依赖 `per-provider validation required` 作为默认免责声明
- [ ] 仓库维护者愿意为默认公开路径提供持续支持
