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
5. 如果 practice 暴露了新的稳定硬约束，说明应由 `$fill-rules` 判断是否进入 [RULES.md](../../../RULES.md)；不要在这里静默升级。
6. 当仓库证据不足时，用 `[NEEDS CLARIFICATION: ...]` 保留不确定性。

## Practice 文件

- `CODING.md`: 从真实代码中提取编码约定，回答“这个项目里代码应该长什么样”。优先写代码组织、模块职责、命名和风格、测试约定、注释和文档边界；不要写成通用“如何写好代码”建议。
- `PRODUCT_SENSE.md`: 从真实 README、docs、产品 surface、CLI/API/UI、templates、config、generated output 和用户反馈中提取产品定位、surface、配置/生成输出/文档职责和风险边界，回答“这个项目里，什么算产品体验”；不要写成通用产品设计建议。
- `SECURITY.md`: 从真实源码、配置、脚本、依赖和发布入口中提取安全配置面，优先写认证/授权、数据/文件写入/输出、外部系统/依赖、当前安全检查能力和 Rules 关系；不要虚构 security policy、secret scan、dependency scan、SAST、CI security gate、支持版本或响应 SLA。
- `RELIABILITY.md`: 从测试、hook、runner、生成输出、持久配置和发布边界中提取高风险改动区域、当前验证能力和 Rules 关系；按影响范围和失败代价排序，不要写成泛化质量 checklist。

## 填写 `CODING.md`

- 先从 source、tests、templates、examples 和构建清单中提取当前项目已经采用的结构，不要凭偏好补充“应该”。
- 按目录、package、layer、component 或 runtime boundary 写清楚“放什么 / 不放什么”；能用表格说明职责时优先用表格。
- 记录稳定的命名、错误处理、注释、测试和生成输出风格；没有证据的地方保留 `[NEEDS CLARIFICATION: ...]`。
- 如果发现的是“不能破坏”的硬约束，只在这里说明背景，并把规则候选交给 `$fill-rules`。
- 删除泛化内容，例如“保持简单”“避免过度抽象”“写可维护代码”，除非能落到本仓库的具体边界或例子上。

## 填写 `PRODUCT_SENSE.md`

- 先从 README、docs、真实用户入口、CLI/API/UI、runtime behavior、templates、config、generated output、integrations 和用户反馈中提取当前产品事实，不要凭愿景补充“应该”。
- 写清楚产品定位、目标用户、主要使用场景、当前支持的 product surface，以及哪些能力不是当前默认体验。
- 对配置、默认值、模板、生成输出、导入/导出、报告、lint messages 或文档站等用户可见 surface，说明它们的职责边界和容易误导用户的风险。
- 区分已支持能力、可选配置、演示内容、路线图、上游背景和待确认信息；没有证据的地方保留 `[NEEDS CLARIFICATION: ...]`。
- 删除泛化内容，例如“提升可用性”“保持一致体验”“增强用户信任”，除非能落到本仓库的具体入口、输出、配置或文档职责。

## 填写 `SECURITY.md`

- 先确认项目是否存在登录、会话、token、API key、权限模型、管理后台、外部服务或发布凭据；没有证据时明确写成未配置或 N/A。
- 对文件写入、路径拼接、生成输出、日志、报告、缓存、诊断信息和发布脚本，说明哪些改动可能造成 secret 泄露、路径逃逸、覆盖用户内容或扩大信任边界。
- 记录当前真实安全检查能力：secret scan、dependency scan、SAST、安全相关测试、pre-commit、CI security gate 或人工 review；没有 runner 证据时不要写成 gate。

## 填写 `RELIABILITY.md`

- 先从测试、hooks、CI、release、持久数据、生成输出和外部集成中识别高风险区域，并按影响范围和失败代价排序。
- 写清楚每个高风险区域影响什么、为什么风险高，以及当前由哪些测试、lint、build、link check、pre-commit、CI 或人工 review 覆盖。
- 区分 command、validation 和 runner；不要把未配置的 typecheck、coverage、docs build、CI 或 release gate 写成完成条件。

## 边界

- 没有证据和清晰违规形态时，不要把通用建议变成 rules。
- 没核对当前实现前，不要用 roadmap 或 design docs 覆盖产品事实。
- 不要虚构 security policy、CI、support versions、release gates、disclosure SLAs 或 verification gates。
- 除非用户明确要求同步模板，否则不要更新 generated templates。
