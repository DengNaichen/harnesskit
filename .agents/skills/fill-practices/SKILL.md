---
name: fill-practices
description: 从 .harnesskit/facts.md 和已核对的仓库证据填充或刷新 docs/practices/*.md。用于 scan-facts 之后更新 coding、product sense、security、reliability 等判断指导，而不是把每条建议都升级成 RULES.md 规则。
---

# 填充 Practices

使用本 skill 更新 [docs/practices/](../../../docs/practices/)，让它成为 coding、product sense、security 和 reliability 的项目实践层。Practices 解释“这个仓库里通常怎么做、哪些地方需要小心”；[RULES.md](../../../RULES.md) 记录硬约束。

## 工作流

1. 读取 [.harnesskit/facts.md](../../../.harnesskit/facts.md)、[AGENTS.md](../../../AGENTS.md)、[RULES.md](../../../RULES.md)、[ARCHITECTURE.md](../../../ARCHITECTURE.md)，以及 [docs/practices/](../../../docs/practices/) 下的现有文件。
2. 对高影响声明回到 source、tests、templates、scripts、manifests、hooks 和已有 docs 核对。
3. 只更新 practice guidance：项目事实、职责边界、约定形态、风险区域、examples 和少量必要 review questions。
4. 硬约束不要放进 practices，除非它们也已出现在 [RULES.md](../../../RULES.md)，或明确标记为 candidate rules。
5. 如果 practice 暴露了新的稳定硬约束，说明应由 `$fill-rules` 添加或更新对应 `RULE-*.md` details；不要在这里静默升级。
6. 当仓库证据不足时，用 `[NEEDS CLARIFICATION: ...]` 保留不确定性。

## Practice 文件

- `CODING.md`: 从真实代码中提取编码约定，回答“这个项目里代码应该长什么样”。优先写代码组织、模块职责、命名和风格、测试约定、注释和文档边界；不要写成通用“如何写好代码”建议。
- `PRODUCT_SENSE.md`: product north star、CLI UX、模板体验、lint messages 和用户信任。
- `SECURITY.md`: secret handling、文件写入、path safety、依赖和报告/输出泄漏。
- `RELIABILITY.md`: 受保护边界、验证策略、失败处理、兼容性和 drift prevention。

## 填写 `CODING.md`

- 先从 source、tests、templates、examples 和构建清单中提取当前项目已经采用的结构，不要凭偏好补充“应该”。
- 按目录、package、layer、component 或 runtime boundary 写清楚“放什么 / 不放什么”；能用表格说明职责时优先用表格。
- 记录稳定的命名、错误处理、注释、测试和生成输出风格；没有证据的地方保留 `[NEEDS CLARIFICATION: ...]`。
- 如果发现的是“不能破坏”的硬约束，只在这里说明背景，并把规则候选交给 `$fill-rules`。
- 删除泛化内容，例如“保持简单”“避免过度抽象”“写可维护代码”，除非能落到本仓库的具体边界或例子上。

## 边界

- 没有证据和清晰违规形态时，不要把通用建议变成 rules。
- 没核对当前实现前，不要用 roadmap 或 design docs 覆盖产品事实。
- 不要虚构 security policy、CI、support versions、release gates 或 disclosure SLAs。
- 除非用户明确要求同步模板，否则不要更新 generated templates。
