# Coding Practices

本文件记录从当前仓库中提取的编码约定。它回答“在这个项目里，代码应该长什么样”，不重复通用工程建议。硬约束见 [RULES.md](../../RULES.md)。

<!-- harnesskit:todo-checklist:start -->
补全本文件前请确认：
- 从真实源码、测试、构建清单和 review 习惯中提炼约定，不要从模板示例直接启用。
- 只写会影响代码修改判断的项目事实；通用建议不要写进来。
- 可执行硬约束进入 [RULES.md](../../RULES.md)，路径职责进入 [ARCHITECTURE.md](../../ARCHITECTURE.md)。
- 未确认内容保留 `[NEEDS CLARIFICATION: ...]`。
<!-- harnesskit:todo-checklist:end -->

## 代码组织

- [NEEDS CLARIFICATION: 当前仓库的主要代码区域、层级、package/module 边界，以及各自职责。]
- [NEEDS CLARIFICATION: 哪些目录是运行时代码，哪些是测试、示例、模板、生成资产或旧实现。]

## 模块职责

| 区域 | 放什么 | 不放什么 |
|------|--------|----------|
| [NEEDS CLARIFICATION: path] | [NEEDS CLARIFICATION: 该区域负责的代码] | [NEEDS CLARIFICATION: 不应放入该区域的职责] |

## 命名和风格

- [NEEDS CLARIFICATION: 文件、类、函数、变量、命令、配置项或测试命名约定。]
- [NEEDS CLARIFICATION: 错误处理、日志、注释、类型、格式化或语言特定风格。]
- [NEEDS CLARIFICATION: 现有项目偏好的依赖注入、状态管理、数据访问、模板、组件或 API 写法。]

## 测试约定

- [NEEDS CLARIFICATION: 本仓库主要测试入口、测试文件组织和命名方式。]
- [NEEDS CLARIFICATION: 用户可见行为、边界条件、生成输出或回归风险应如何测试。]
- [NEEDS CLARIFICATION: 哪些实现细节不应被测试锁死。]

## 注释和文档

- [NEEDS CLARIFICATION: 代码注释、docstring、Javadoc、README 片段或内联说明的项目风格。]
- [NEEDS CLARIFICATION: 哪些解释应留在代码旁边，哪些应进入 docs、ARCHITECTURE 或 RULES。]

## 和 Rules 的关系

发现“必须始终成立”的稳定约束时，交给 `$fill-rules` 或直接更新 [RULES.md](../../RULES.md)。本文件只帮助判断“这个仓库里的代码通常应该怎么写”。
