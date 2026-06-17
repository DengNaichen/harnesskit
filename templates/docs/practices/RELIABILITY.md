# Reliability Practices

本文件记录当前仓库的可靠性、质量和防漂移判断指导。它不替代 [RULES.md](../../RULES.md) 的验证门槛。

<!-- harnesskit:todo-checklist:start -->
补全本文件前请确认：
- 从真实测试、hook、CI、release、兼容性和运维边界中提炼实践。
- 区分 command、validation 和 runner；不要把未配置检查写成 gate。
- 未确认内容保留 `[NEEDS CLARIFICATION: ...]`。
<!-- harnesskit:todo-checklist:end -->

## Protected Boundaries

- [NEEDS CLARIFICATION: 用户可见 API、CLI、配置、schema、持久数据、生成输出或集成边界。]

## Guidance

- 改动前先判断保护边界；涉及兼容性时明确当前发布或支持边界。
- 测试要覆盖用户可观察结果、回归风险和生成输出差异。
- 失败后修复并重跑同一个验证入口，最终只报告最终状态。
- 没有 runner 证据的检查只能标记为 review、agent 执行或未配置。

## Review Questions

- 这次改动触及了哪个 protected boundary？
- 是否需要局部测试、完整验证，还是只需 review？
- 文档、模板和 rules 是否仍指向真实存在的命令和路径？
