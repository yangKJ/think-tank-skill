# domain-packs

`domain-packs/` 存放可选领域包。

领域包不是 think-tank core。它们只为特定领域提供默认背景、术语、信息源、竞品表、报告模板和监控关键词。

## 设计原则

- core 保持跨领域。
- domain pack 可插拔。
- domain pack 不能改变协议。
- domain pack 可以扩展 source strategy、profile prompt 和报告模板。

## 第一批领域包

当前主仓不内置任何领域包。

如果某个项目需要领域知识，应在该项目中自行添加 domain pack，或通过本地、不上传的配置和资料目录接入。
