---
name: scan-facts
description: 从已核对证据扫描仓库事实并写入 .harnesskit/facts.md。用于填充 AGENTS.md、ARCHITECTURE.md、RULES.md 或项目特定 skill section 前，启动或刷新 Context Harness facts。
---

# 扫描 Facts

使用本 skill 从仓库证据刷新 [.harnesskit/facts.md](../../../.harnesskit/facts.md)。本 skill 是唯一应该创建或刷新 facts artifact 的 generated skill。

## 输入

读取最小但足够有用的 repository-owned evidence：

- Existing guidance：[AGENTS.md](../../../AGENTS.md)、[CLAUDE.md](../../../CLAUDE.md)、[RULES.md](../../../RULES.md)、[.agents/skills/](../../skills/) skill files、architecture notes 和相关 docs。
- Project identity：`README*`、product/design docs、package metadata 和顶层目录名。
- Tech stack facts：manifests、lockfiles、workspace files、source/test layout、tool config、CI/pre-commit config 和 documented commands。
- Current state：`[NEEDS CLARIFICATION: ...]` placeholders、todo-checklist marker blocks、missing files、stale paths，或与仓库文件冲突的 guidance。

忽略 local/generated/vendor 噪音，例如 virtual environments、dependency folders、caches、build output、downloaded dependencies 和 editor metadata，除非用户明确询问。

## 工作流

1. 在提问前先检查仓库事实。
2. 只把 evidence-backed facts 记录到 [.harnesskit/facts.md](../../../.harnesskit/facts.md)。
3. 对不确定事项保留 `[NEEDS CLARIFICATION: ...]`，并简短说明缺少什么证据。
4. 不要从本 skill 更新 [AGENTS.md](../../../AGENTS.md)、[ARCHITECTURE.md](../../../ARCHITECTURE.md)、[RULES.md](../../../RULES.md) 或其他 skills。
5. 如果 [.harnesskit/facts.md](../../../.harnesskit/facts.md) 缺失，使用 generated template 的相同 sections 重建。

## 事实模型

记录：

- Project identity 和 audience。
- Languages、runtimes、package managers、frameworks、build tools、test frameworks、linters、formatters 和 type checkers。
- Validation entrypoints：setup、full verify、test、lint、format check、typecheck、coverage、build、docs、link check、hook suite 和 CI/platform gates。
- Repository map candidates：重要 source、test、docs、config、generated-output 和 tooling paths。
- Agent-facing assets 和 installed local skills。
- 带 runner evidence 的 Rule 与 Validation candidates。
- 仓库事实无法确定的 open questions。

## 边界

- 不要虚构 commands、tools、URLs、CI、release processes、PR templates、architecture 或 compatibility policy。
- 不要把 generic template examples 当成目标仓库支持某工具的证据。
- 除非 command、script、hook、CI task 或 platform setting 提供明确 pass/fail 证据，否则不要把 Validation 标记为 deterministic。
- guidance-only refresh 不要运行 runtime test suites，除非 refresh 也改变运行时代码、模板、构建/测试配置或生成行为。
