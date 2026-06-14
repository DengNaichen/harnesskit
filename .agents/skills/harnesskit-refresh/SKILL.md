---
name: "harnesskit-refresh"
description: "刷新或补装 HarnessKit Context Harness 资产，默认使用非覆盖流程。"
---

# harnesskit-refresh

当用户希望补装、刷新或修复当前仓库的 HarnessKit Context Harness 资产时，使用这个 skill。

## 工作方式

<!-- harnesskit:todo-checklist:start -->
调整本节前请确认：
- 命令与当前 CLI 支持的参数和默认 integration 一致。
- 非覆盖和 `--force` 行为描述符合 `harnesskit init` 与 `integration install` 实现。
- 任何会覆盖手写内容的路径都要求用户明确授权。
<!-- harnesskit:todo-checklist:end -->

默认采用安全的非覆盖流程。只有当用户明确要求覆盖已有托管文件时，才使用 `--force`。

1. 先读取：
   - `README.md`
   - `AGENTS.md`
   - `.harnesskit/config.json`
   - `.agents/skills/`
2. 如果当前仓库还没有 `.harnesskit/config.json`，建议运行：
   ```bash
   harnesskit init --here --integration codex
   ```
3. 如果仓库已经初始化，但 Codex skills 缺失或不完整，建议运行：
   ```bash
   harnesskit integration install codex
   ```
4. 只有在用户明确说要覆盖或强制刷新时，才使用：
   ```bash
   harnesskit init --here --integration codex --force
   harnesskit integration install codex --force
   ```

## 输出要求

执行前说明将要运行的命令和是否会覆盖文件。执行后汇报写入、跳过和仍需人工处理的文件。不要在用户未授权时覆盖手写内容。
