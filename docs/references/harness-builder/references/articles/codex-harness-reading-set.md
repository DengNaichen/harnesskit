# Codex Harness Reading Set

> 状态：待阅读 / source audit 进行中。
>
> 本文件记录 Harness Builder 后续研究要优先阅读的 Codex Harness 相关文章集合。标题、日期和重点来自用户提供的信息；已拿到原文或链接的条目会标注 source URL 和核验状态。后续应继续补充摘录、阅读笔记和与 Linear issue 的映射。

## 阅读目标

这组文章用于回答 Harness Builder 的核心产品问题：

- Codex harness 到底包含哪些层：agent loop、运行环境、工具、上下文、反馈、验证、review 和 orchestration。
- Harness Engineer / Harness Engineering 的职责边界是什么。
- 同一套 harness 如何接入 CLI、Cloud、IDE、macOS app 等不同产品表面。
- 多 agent orchestration、任务可读性、scoped context、验证回路和人工 review 如何落到项目级治理资产。
- 这些思想如何映射到本仓库的 Skill-first Harness Builder、TypeScript Engine、facts/evidence、draft/promote 和 Sensor 设计。

## 文章列表

### 1. Unrolling the Codex agent loop

- 日期：2026-01-23
- Source URL: https://openai.com/index/unrolling-the-codex-agent-loop/
- 中文 URL: https://openai.com/zh-Hans-CN/index/unrolling-the-codex-agent-loop/
- Source audit: 已核验为 OpenAI Engineering 文章。
- 本地摘录与总结：
  - 原文摘录：[source.md](openai-unrolling-the-codex-agent-loop/source.md)
  - 总结报告：[summary.md](openai-unrolling-the-codex-agent-loop/summary.md)



### 2. Unlocking the Codex harness: how we built the App Server

- 日期：2026-02-04
- Source URL: https://openai.com/index/unlocking-the-codex-harness/
- Source audit: 已核验为 OpenAI Engineering 文章。
- 主题：Codex App Server 与多产品表面复用同一 harness。
- 关注点：
  - Codex App Server 如何承接统一 Codex harness。
  - web、CLI、IDE extension、macOS app 等不同 surface 如何接入同一底层机制。
  - harness 与产品 UI / 宿主能力之间的边界。
  - thread lifecycle / persistence、config / auth、tool execution / extensions、App Server JSON-RPC protocol。
- 待读取后补充：
  - App Server 的职责边界。
  - surface-agnostic orchestration 的设计原则。
  - 对本仓库纯文本 Skill 入口、host-agnostic task-run 和 Engine contract 的映射。

### 3. Harness engineering: leveraging Codex in an agent-first world

- 日期：2026-02-11
- Source URL: https://openai.com/index/harness-engineering/
- Source audit: 已核验为 OpenAI Engineering 文章。
- 主题：Harness Engineering / Harness Engineer 主文。
- 关注点：
  - 软件工程师角色如何从直接写代码转向设计环境、意图和反馈回路。
  - 如何让 Codex agent 在可控上下文、可执行工具和可验证反馈里可靠工作。
  - Harness Engineer 应如何设计任务入口、约束、检查点、review 和改进回路。
  - repository knowledge as system of record、agent legibility、architecture / taste invariants、evaluation harnesses、background cleanup / garbage collection。
- 本地摘录与总结：
  - 原文链接：[OpenAI - Harness engineering](https://openai.com/index/harness-engineering/)
  - 本地摘录：[source.md](openai-harness-engineering/source.md)
  - 总结报告：[summary.md](openai-harness-engineering/summary.md)



### 4. An open-source spec for Codex orchestration: Symphony

- 日期：2026-04-27
- Source URL: https://openai.com/zh-Hans-CN/index/open-source-codex-orchestration-symphony/
- Source audit: 已核验为 OpenAI 工程文章中文页面。
- 本地摘录与总结：
  - 原文摘录：[source.md](openai-open-source-codex-orchestration-symphony/source.md)
  - 总结报告：[summary.md](openai-open-source-codex-orchestration-symphony/summary.md)
- 主题：Codex orchestration / 多 agent 编排规范。
- 关注点：
  - 如何把 harness engineering 的原则推进到多 agent 编排。
  - Symphony 作为 orchestration spec 解决哪些问题。
  - 多 agent 任务如何表达意图、分配上下文、交接结果、保留审计和验证。
  - issue tracker 作为 control plane、Linear issue 到 agent workspace 的映射、DAG 依赖、WORKFLOW.md、per-issue workspace、orchestrator / runner / status surface。
- 待读取后补充：
  - 是否存在英文 canonical URL。
  - Symphony 的核心对象和流程。
  - orchestration spec 与项目级 `.ai` 资产、workflow runtime / task-run summary 的关系。
  - 对后续 Harness Builder 多 agent / sub agent 支持的启发。

### 5. Building self-improving tax agents with Codex

- 日期：2026-05-27
- Source URL: https://openai.com/zh-Hans-CN/index/building-self-improving-tax-agents-with-codex/
- Source audit: 已核验为 OpenAI 工程文章中文页面。
- 本地摘录与总结：
  - 原文摘录：[source.md](openai-building-self-improving-tax-agents-with-codex/source.md)
  - 总结报告：[summary.md](openai-building-self-improving-tax-agents-with-codex/summary.md)
- 主题：基于 harness engineering 和 Symphony 原则的垂直案例。
- 关注点：
  - 如何让任务对 Codex 可读。
  - 如何提供 scoped context 和工具。
  - 如何保留验证、人工 review 和持续改进机制。
  - 垂直领域 agent 如何通过 harness 逐步自我改进。
  - 从业者反馈、生产追踪、定制评测、Codex 驱动的迭代闭环如何连成可衡量的 self-improvement loop。
- 待读取后补充：
  - 是否存在英文 canonical URL。
  - self-improving loop 的输入、输出和检查点。
  - 税务场景中哪些设计可泛化为项目级 Harness 模式。
  - 对 Harness Builder maturity / evidence / evolution loop 的映射。

## 后续整理格式

拿到原文后，每篇建议按以下格式补充：

```text
Source URL:
Key terms:
Harness definition:
Loop / orchestration model:
Engineering role implications:
Verification / review model:
Mapping to Harness Builder:
Related Linear issues:
Open questions:
```

## 当前注意事项

- 只有标注 `Source audit: 已核验` 的条目可作为已核验公开来源引用。
- 不把文章中的概念直接写入 V2 硬约束；需要先做阅读摘录、Linear 票映射和产品边界讨论。
- 如果文章内容与本仓库已有 `AGENTS.md`、`docs/strategy/` 或 `docs/engineering/` 冲突，应先记录冲突，再决定是否更新稳定文档。
