# Harness Builder Research Summary

> 状态：research 分支阶段性收口。本文只记录本轮已整理材料的短摘要，后续产品化结论仍需进入正式 spec / plan。

## 本轮整理

- 已建立 OpenAI / Anthropic harness 相关 reading set，并完成基础 source audit。
- 已将 OpenAI 文章材料按单篇目录归档：`source.md`、`summary.md` 和可选 `pics/`。
- 已整理四篇 OpenAI 资料：Codex agent loop、Harness Engineering、Symphony、self-improving tax agents。

## 初步结论

- Harness Builder 不应实现宿主 agent loop，而应生成项目级 context、规则、验证契约和 evidence 入口。
- `AGENTS.md` 更适合作为地图，而不是巨型手册；详细约束应通过渐进式加载进入 `docs/`。
- Sensors / evals / task-run evidence 是 Harness 的关键差异点：它们把自然语言规则变成可执行反馈闭环。
- 后续 feature 起点应保持很小：先让终端 `init` 命令写入最小 Harness 模板，再逐步接入真实 proposal、CodeGraph 和 promote 闭环。

## Harness 分类与 MVP 边界

本轮 research 暂时把 harness 分成三类：

- **Context Harness**：给 agent 使用的项目级上下文，包括架构地图、规则、约束、验证入口、handoff、evidence 说明和渐进式加载索引。约束也属于 context，因为不同项目、技术栈、基础设施和风险偏好会产生不同约束；只有把约束表达成 agent-friendly 的项目资产，agent 才能稳定消费。
- **Agent Runtime Harness**：宿主产品内置的运行边界和能力，例如 agent loop、tool registry、sandbox、权限审批、shell / browser / git 执行、模型调用和工具结果回填。这一层属于 Codex、Claude Code 等宿主 runtime，不属于 Harness Builder MVP。
- **Controller / Orchestration Harness**：运行在 runtime 之上的调度控制层，例如 Symphony 将 Linear issue 转成 agent 工作队列、管理 workspace、并发、重试和状态对齐。这一层可以作为未来集成方向，但不属于当前 MVP。

因此，Harness Builder MVP 只负责 **Context Harness**：初始化并维护目标项目中 agent-friendly 的 context、规则、约束、验证契约和 evidence 入口；不实现 Agent Runtime，也不实现 Controller / Orchestration。

## 命名假设

当前 `Harness Builder` 名称容易被理解为“构建所有 harness 层”。为了表达 MVP 的真实边界，后续产品和工程命名可以逐步收敛到 `context_harness_builder`：

- `context_harness`：项目级 context、规则、约束、验证契约和 evidence 入口。
- `context_harness_builder`：生成和维护 `context_harness` 的工具。

这个命名不要求立即重命名仓库或目录；当前先作为 research 阶段的定位假设，后续进入正式 spec / plan 后再决定是否同步到包名、命令名、Linear 标签和文档标题。

## OpenAI / Anthropic 路线假设

本轮 research 的暂时判断是：Harness Builder MVP 应更多参考 OpenAI 的 Context Harness 路线，而不是优先复制 Anthropic 的厚 runtime 路线。

- OpenAI 材料更强调把 repository knowledge、rules、evals、workflow 和 evidence 做成项目内、agent-friendly、可验证的上下文框架，让 agent 在框架内自主发挥。这与 Harness Builder 的 Context Harness 边界高度一致。
- Anthropic 材料尚未完成单篇细读；但从当前印象看，它更强调把 long-running agent 所需的规划、恢复、进度管理、多 agent 协作和执行约束内化进 Claude Code / agent 产品本身。这更接近 Agent Runtime Harness 或 runtime 内置 workflow，不适合作为当前 MVP 的直接实现边界。
- 一个待验证假设是：不同模型和产品的指令遵循、工具使用与自主性风格，会影响 harness 更适合放在 context 层还是 runtime 层。这个判断需要后续阅读 Anthropic 原文后再校正。

因此，当前产品取向是：以 OpenAI 的 Context Harness 实践作为 MVP 主参考；Anthropic 的 long-running agent harness 经验先作为未来 runtime 集成、controller 设计和长期任务治理的参考材料。

## 后续待补

- App Server 文章仍需按同样目录模式补齐。
- self-improving tax agents 的 summary 仍是粗稿，后续需要补强对 Harness Builder evolution loop 的映射。
- Anthropic 三篇材料还需要进入单篇摘录和总结。
