# Product Sense Practices

本文件记录 HarnessKit 的产品判断和体验指导。它解释取舍，不替代 [RULES.md](../../RULES.md) 中的硬约束。

## Product North Star

HarnessKit 的目标是让 agent 更快、更稳地获得仓库上下文、规则和验证入口。它维护 Context Harness，不假装实现 agent runtime、沙箱、调度器或完整项目管理系统。

## Experience Principles

- 少魔法：CLI 和模板输出应让用户看得懂发生了什么。
- 可验证：重要声明应能回到源码、配置、测试、rules、skills 或文档证据。
- 默认保守：默认行为不应覆盖用户文件、夸大支持范围或生成虚假能力。
- 可行动：错误消息、lint issue 和模板 TODO 应告诉用户下一步该做什么。
- 生成内容服务 agent 操作，不写成营销文案或长篇产品介绍。
- 中文团队友好：本仓库 agent-facing 文档优先中文表达，命令、代码标识和必要术语保留英文。

## Surface Guidance

- CLI：默认值要安全，显式参数要清楚，失败输出要短而可修复。
- Templates：占位符要诚实，未确认事实保留 `NEEDS CLARIFICATION`，不要把示例当事实。
- Linter：issue 应指出 found、expected 和 suggested fix，避免只说“不符合规范”。
- Docs：README 讲产品，AGENTS 讲 agent 路由，RULES 讲硬约束，ARCHITECTURE 讲地图，practices 讲判断。

## Review Questions

- 这个改动是否减少 agent 猜测，而不是增加文档噪音？
- 用户会不会误以为某个未实现功能已经可用？
- 生成文件是否能被目标仓库维护者继续编辑和理解？
- 错误或 TODO 是否给出了下一步？
- 这属于产品原则、操作规则，还是实现事实？文件放对了吗？
