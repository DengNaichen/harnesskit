# Coding Practices

本文件记录当前仓库的代码判断指导。它不是硬规则索引；必须遵守的约束仍以 [RULES.md](../../RULES.md) 和 `.harnesskit/rules/` 为准。

<!-- harnesskit:todo-checklist:start -->
补全本文件前请确认：
- 从真实代码、测试和 review 习惯中提炼实践，不要从模板示例直接启用。
- 把可执行硬约束抽到 RULES.md；本文件只写判断和指导。
- 未确认内容保留 `[NEEDS CLARIFICATION: ...]`。
<!-- harnesskit:todo-checklist:end -->

## 判断原则

- [NEEDS CLARIFICATION: 本仓库如何处理抽象边界、命名、注释和测试风格。]
- [NEEDS CLARIFICATION: 哪些模块边界需要特别保护。]
- [NEEDS CLARIFICATION: 何时接受重构，何时要求保持小改动。]

## Review Questions

- 这个改动是否保持在正确的模块或 ownership 边界里？
- 新抽象是否降低复杂度，还是只是移动代码？
- 测试是否覆盖用户能观察到的行为变化？
- 是否有无关重排、格式 churn 或顺手重构混入？

## 和 Rules 的关系

违反硬约束时按 [RULES.md](../../RULES.md) 处理；本文件只帮助判断“怎样写得更像这个仓库”。
