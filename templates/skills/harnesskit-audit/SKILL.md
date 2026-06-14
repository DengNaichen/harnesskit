---
name: "harnesskit-audit"
description: "审计当前仓库的 HarnessKit Context Harness 状态，默认只读，不修改文件。"
---

# harnesskit-audit

当用户希望检查当前仓库是否已经正确接入 HarnessKit Context Harness，或希望知道缺少哪些 agent-facing 资产时，使用这个 skill。

## 工作方式

<!-- harnesskit:todo-checklist:start -->
调整本节前请确认：
- 最小资产清单与 `harnesskit init` 当前会生成的文件一致。
- integration 名称、skill 路径和配置文件路径都来自本仓库事实。
- 审计仍保持只读，除非用户明确要求修复。
<!-- harnesskit:todo-checklist:end -->

默认只读，不修改文件。除非用户明确要求修复或刷新，否则不要写入、覆盖或删除任何文件。

1. 先确认当前目录是仓库根目录，并读取这些入口：
   - `README.md`
   - `AGENTS.md`
   - `.harnesskit/config.json`
   - `.agents/skills/`
2. 检查 Context Harness 的最小资产是否存在：
   - `AGENTS.md`
   - `.harnesskit/config.json`
   - `.agents/skills/harnesskit-audit/SKILL.md`
   - `.agents/skills/harnesskit-refresh/SKILL.md`
   - `.agents/skills/harnesskit-explain/SKILL.md`
3. 汇总发现：
   - 已安装的 integration
   - 缺失或看起来不完整的文件
   - 可能需要用户补充的项目上下文
   - 推荐的下一步命令

## 输出要求

输出中文报告，保持简洁。先列结论，再列缺失项和建议。不要把 `AGENTS.md` 当作项目说明长文；项目定位应优先来自 `README.md`。
