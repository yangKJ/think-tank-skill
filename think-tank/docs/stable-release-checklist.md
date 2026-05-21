# Stable Release Checklist

本文是 stable release 发布与复核清单。

## 文档与边界

- [x] `open-source-packages.yaml` 与实际公开范围一致
- [x] `open-source-release.md` 公开承诺更新为 stable 表述
- [x] `support-matrix.md` 中 blocked/planned 项目已同步
- [x] `README.md` 不再保留 beta-only 提示，或明确说明剩余实验范围

## 证据

- [x] 三条 optional provider invocation 样例存在且带 `dispatch_decision`
- [x] 三条样例都带 `sources[]` / `evidence[]` / `boundaries[]`
- [x] external browser readonly 至少一条成功样例
- [x] multi-agent runtime 至少一条超出 readonly council 的成功样例
- [x] long-running lifecycle 至少一条成功样例

## 检查

- [x] `python3 checks/open_source_release_suite.py`
- [x] `python3 checks/stable_release_check.py`
- [ ] GitHub Actions release gate 通过

## 发布姿态

- [x] 版本号不再停留在纯 beta 心智
- [x] 对外文案不再依赖 `per-provider validation required` 作为默认免责声明
- [ ] 仓库维护者愿意为默认公开路径提供持续支持

## 发布素材

- [x] `docs/v1.0.0-release-notes.md`
- [x] `docs/release-tagging.md`
- [ ] GitHub Release 页面已填充
