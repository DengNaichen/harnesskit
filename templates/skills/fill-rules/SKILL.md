---
name: fill-rules
description: 从 .harnesskit/facts.md 和已核对的仓库证据填充或刷新 RULES.md 短规则索引。用于 scan-facts 之后更新可执行规则；validation、guardrail 和 runner bindings 应进入对应 guardrail 或 verification artifact。
---

# 填充 Rules

使用本 skill 更新 [RULES.md](../../../RULES.md) 作为短约束索引。Rules 只回答“这个仓库里什么必须始终成立”：包括绝对不能做什么、必须遵守什么，以及哪些项目特定不变量不能被破坏；背景、判断指导和可执行检查分别进入 [ARCHITECTURE.md](../../../ARCHITECTURE.md)、[docs/practices/](../../../docs/practices/) 和 [.harnesskit/guardrails/](../../../.harnesskit/guardrails/) / verification runner。

Rules 必须满足：

1. **仓库特异**：非通用工程常识，来自当前仓库事实或团队明确采纳。
2. **硬性约束**：能判断遵守或违反，不是偏好、流程或建议。
3. **高防踩坑**：用于防止 agent 因旧教程、默认配置、跨项目先验或过度发挥而破坏项目不变量。

## 工作流

1. 读取 [.harnesskit/facts.md](../../../.harnesskit/facts.md)、当前 [RULES.md](../../../RULES.md)、validation scripts、guardrails、manifests、hook/CI config 和 agent guidance。
2. 只有当事项是仓库本地约束或已明确采纳、跨任务稳定、有清晰违规形态，并且有证据支撑时，才升级为 Rule。
3. 写入 [RULES.md](../../../RULES.md) 前，把 candidate rule changes 作为 single-choice MCQ 展示给用户。如果当前 Codex surface 支持 native single-choice UI，就使用它；否则把选项渲染成文本并等待用户字母或修正。
   - A. 确认所有 candidate rule changes 并写入。
   - B. 写入前先修正一个或多个 candidate rules。
   - C. 暂时跳过 rule changes 写入。
   - D. 只写入 high-confidence repository rules，其余保留为 `[NEEDS CLARIFICATION: ...]`。
   如果用户修正规则、分类、guardrail coverage 或 runner status，把该修正视为 user-confirmed evidence，并记录到适当 artifact。
4. category headings 只用于组织；不要把 general engineering、AI coding、stack、architecture 或 domain 等分类本身当成启用规则的证据。
5. [RULES.md](../../../RULES.md) 中每条 rule 保持为一句短约束，不要求也不默认创建 `RULE-*.md` details。
6. 将 rationale、evidence、caveats 和 examples 放入 architecture 或 practices；将 validation context、runner bindings 和可执行检查放入 guardrails 或 verification skill。
7. 对 unsupported 或 unverified rules 标记为 `[NEEDS CLARIFICATION: ...]`、`N/A`、`未配置` 或 `不适用`，不要从示例直接启用。
8. 区分 rule、guardrail/check 和 runner；没有 runner 证据时，不要声称某个检查会阻断变更。
9. 除非用户明确要求迁移，否则保留已有客户手写 rules 和结构。

## 用户确认协议

使用类似下面的简短 MCQ 确认提示：

```text
我找到这些候选 Rule 变更。写入 `RULES.md` 前请确认。

1. 新增 / 更新 rule: RULE-...
   约束: ...
   分类: ...
   证据: ...
   Guardrail / validation coverage: ...
   Runner / binding: ...

2. 保留未解决事项: ...
   原因: ...

请选择：
A. 确认所有 candidate rule changes 并写入。
B. 写入前先修正一个或多个 candidate rules。
C. 暂时跳过 rule changes 写入。
D. 只写入 high-confidence repository rules，其余保留为 `[NEEDS CLARIFICATION: ...]`。
```

如果当前 Codex surface 有 native single-choice UI，用该 UI 展示四个选项；否则使用上方文本 MCQ。然后暂停等待用户回复。没有用户确认时，不要把 facts、通用工程建议、template examples 或 inferred commands 静默升级成 durable Rules。

## 输出

只更新 [RULES.md](../../../RULES.md)。如果 [AGENTS.md](../../../AGENTS.md)、[ARCHITECTURE.md](../../../ARCHITECTURE.md)、[docs/practices/](../../../docs/practices/)、guardrails 或 skills 需要匹配变更，调用对应 fill skill 或直接更新对应 artifact。

## 边界

- 不要虚构 commands、CI、branch protection、coverage thresholds、typecheck、docs build 或 PR requirements。
- 不要把通用工程建议、任务步骤、工具教程、临时计划或未验证猜测变成 Rules。
- workflows 放进 skills 或 [AGENTS.md](../../../AGENTS.md)；目录地图放进 [ARCHITECTURE.md](../../../ARCHITECTURE.md)；产品背景放进 README 或 docs。
- 不要把局部 review judgment 标记为确定性 validation coverage。
- [.harnesskit/facts.md](../../../.harnesskit/facts.md) 是本 skill 的输入源（中间产物），不是核对 runner config 的替代品；高影响判断必须回到真实仓库文件。
- 除非用户明确要求迁移，否则不要重构现有非模板 [RULES.md](../../../RULES.md)。
