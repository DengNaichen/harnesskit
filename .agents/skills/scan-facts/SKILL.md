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

## 证据路由

扫描前先按事实类型选择默认 evidence，不要无差别深扫源码：

- CLI/runtime facts：优先核对 package manifest、`src/` 入口、CLI/runtime tests 和用户可见命令文档。
- Template/generated-output facts：优先核对 `templates/`、template render context、init tests 和生成输出断言。
- Validation facts：优先核对 Makefile、scripts、pre-commit/CI 配置、verification skill 和最近的 runner receipt。
- Release/deploy facts：优先核对 release scripts、package metadata、publish docs 和部署配置；没有 runner 或配置证据时标为 absent/candidate。
- Context assets facts：优先核对 AGENTS、RULES、ARCHITECTURE、docs/practices、skills 和 `.harnesskit/` 文件。
- Product/docs facts：优先核对 README、docs、design notes；如果没有源码/配置支持，标为 candidate，不升级成硬约束。

## 事实准入和状态

只记录会影响 agent 操作、用户可见输出、验证/发布、安全边界、模板渲染或漂移处理的事实。普通实现细节、可从源码自然读出的局部代码结构、一次性草稿和头脑风暴不要写入 durable facts。

每条事实应能标注以下状态之一：

- `confirmed`：由源码、配置、脚本、测试、runner 或团队确认支持。
- `candidate`：来自文档、惯例或间接线索，尚未核对实现。
- `absent`：已检查合理 evidence，未发现对应能力、runner 或配置。
- `conflict`：两个或多个 evidence source 不一致，需要漂移处理。

需要时为事实补充 `target hint`，说明它后续应进入 AGENTS、ARCHITECTURE、RULES、docs/practices、skills、validation runner，还是只留在 facts。

## 扫描深度

- 默认使用 quick scan：清单、锁文件、脚本、配置、模板、测试入口、现有 context 文件和顶层文档。
- 只有高价值事实不确定、出现 conflict，或事实会影响规则/模板/验证结论时，才 targeted 读取相关源码或测试。
- 不做 exhaustive 项目文档扫描；不为 facts 生成 API contracts、data models、component inventory 或 deep-dive 文档。

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
- Fact quality：status、evidence path、target hint 和 stale-risk notes。
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
