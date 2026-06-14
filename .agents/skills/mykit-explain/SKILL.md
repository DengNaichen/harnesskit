---
name: "mykit-explain"
description: "解释当前仓库中的 mykit Context Harness 资产和使用方式。"
---

# mykit-explain

当用户询问 `mykit` 是什么、当前仓库为什么有这些 harness 文件，或这些文件分别给谁使用时，使用这个 skill。

## 工作方式

1. 优先读取 `README.md` 理解项目定位。
2. 读取 `.mykit/config.json` 判断当前安装状态。
3. 读取 `AGENTS.md` 理解 agent 操作规则。
4. 查看 `.agents/skills/` 说明当前 Codex 可用的 mykit skills。

## 解释重点

<!-- mykit:todo-checklist:start -->
调整本节前请确认：
- 文件职责说明与当前模板输出和 `.mykit/config.json` 内容一致。
- 不把 `AGENTS.md` 当作产品说明来源，项目定位优先来自 `README.md`。
- 新增或移除 harness 资产后同步更新这里。
<!-- mykit:todo-checklist:end -->

- `mykit` 是 Context Harness CLI 与 Codex-facing toolkit。
- CLI 负责把 harness 资产写入仓库。
- `.agents/skills/` 里的 skills 负责让 Codex 在对话里继续审计、刷新和解释这些资产。
- `README.md` 讲项目是什么和为什么存在。
- `AGENTS.md` 讲 agent 在仓库里应该如何工作。
- `.mykit/config.json` 记录 mykit 管理的最小元数据。

## 输出要求

使用中文回答。先解释当前仓库状态，再解释各文件职责，最后给出用户下一步可以怎么用。
