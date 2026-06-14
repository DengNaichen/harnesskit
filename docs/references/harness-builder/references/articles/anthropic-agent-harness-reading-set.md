# Anthropic Harness Reading Set

> 状态：待阅读 / source audit 已完成。
>
> 本文件记录 Harness Builder 后续研究要优先阅读的 Anthropic harness 相关材料。标题来自用户提供的信息；已拿到原文或链接的条目会标注 source URL 和核验状态。后续应继续补充摘录、阅读笔记和与 Linear issue 的映射。

## 阅读目标

这组材料用于和 OpenAI Codex Harness 阅读集对照：

- long-running agent 为什么需要模型外层 harness，而不是只依赖裸模型能力。
- 面向长期应用开发任务的 harness 如何管理目标、上下文、工具、权限、状态、恢复、验证和人工审查。
- managed agents 如何拆分 reasoning / planning 与 execution / tools。
- 这些思想如何映射到 Harness Builder 的 Skill / LLM 与 TypeScript Engine 分工、task-run、progress-summary、Sensor、draft/promote 和 completion audit。

## 文章 / 文档列表

### 1. Effective harnesses for long-running agents

- 日期：2025-11-26
- Source URL: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Source audit: 已核验为 Anthropic Engineering 文章。
- 主题：long-running agents 的有效 harness 设计。
- 关注点：
  - long-running agent 为什么需要模型外层 harness，而不是只依赖裸模型能力。
  - harness 如何管理目标、上下文、工具、权限、持久状态、恢复、验证和人工审查。
  - 长任务中的 drift、context rot、tool failure、partial progress、checkpoint、handoff 和 stop condition。
  - 对 Claude Code / Cowork / 多 agent 工作流的通用启发。
  - initializer agent / coding agent 分工、feature list、progress file、git history、init.sh、end-to-end testing。
- 待读取后补充：
  - long-running agent harness 的核心组件。
  - 与 OpenAI Codex App Server、Symphony 和 self-improving tax agents 的对照。
  - 对 Harness Builder task-run、progress-summary、completion audit、Sensor 和 evolution loop 的映射。

### 2. Harness design for long-running application development

- 日期：2026-03-24
- Source URL: https://www.anthropic.com/engineering/harness-design-long-running-apps
- Source audit: 已核验为 Anthropic Engineering 文章。
- 主题：面向长期应用开发任务的 harness design。
- 关注点：
  - long-running application development 与一次性 coding task 的差异。
  - harness 如何支撑跨多轮、多文件、多 PR、多验证阶段的应用开发。
  - 如何管理项目知识、计划、环境、执行状态、错误恢复、代码审查、测试回归和交付证据。
  - agent 在长期应用开发中何时自主推进，何时需要 human judgment / product judgment。
  - planner / generator / evaluator 三 agent 架构、sprint contract、context reset vs compaction、Playwright MCP、load-bearing harness component。
- 待读取后补充：
  - application development harness 的核心组件。
  - 与 OpenAI `Harness engineering`、`Symphony`、`Building self-improving tax agents with Codex` 的对照。
  - 对 Harness Builder Guides、Sensors、Workflow Runtime、task-run evidence 和 evolution loop 的映射。

### 3. Scaling Managed Agents: Decoupling the brain from the hands

- 日期：2026-04-08
- Source URL: https://www.anthropic.com/engineering/managed-agents
- Source audit: 已核验为 Anthropic Engineering 文章。
- 主题：managed agents 的扩展架构，以及 reasoning / planning 与 execution / tools 的职责拆分。
- 关注点：
  - `brain` 与 `hands` 分别指什么：模型推理 / 计划 / 判断 vs 工具执行 / 环境操作 / 外部副作用。
  - 为什么 managed agents 需要把决策层、执行层、权限层、状态层和观测层解耦。
  - 如何在长期任务中管理 agent 的目标、上下文、工具调用、执行隔离、重试、审计和人工接管。
  - decoupling 如何帮助多 surface、多执行环境、多 agent 并发和安全策略演进。
  - Managed Agents 作为 meta-harness：session、harness、sandbox 三个可替换接口，以及 `execute(name, input) -> string`、`provision({resources})`、`wake(sessionId)`、`emitEvent(id, event)` 等接口思想。
- 待读取后补充：
  - managed agents 的架构图或核心组件。
  - `brain / hands` 分离与 OpenAI Codex App Server、Codex core、tool execution / extensions 的对照。
  - 对 Harness Builder Skill / LLM 与 TypeScript Engine 分工、CodeGraph adapter、Sensor Bootstrap、draft/promote 和 task-run orchestration 的映射。

## 后续整理格式

拿到原文细读后，每篇建议按以下格式补充：

```text
Source URL:
Key terms:
Agent / harness definition:
Loop / orchestration model:
Tool / ACI design:
Context / session model:
Verification / review model:
Mapping to Harness Builder:
Related Linear issues:
Open questions:
```

## 当前注意事项

- 只有标注 `Source audit: 已核验` 的条目可作为已核验公开来源引用。
- Anthropic 的术语未必等同于 OpenAI 的 `harness engineering`，后续映射时应先记录原文概念，再做产品解释。
- 不把文章中的概念直接写入 V2 硬约束；需要先做阅读摘录、Linear 票映射和产品边界讨论。
