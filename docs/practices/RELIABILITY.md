# Reliability Practices

本文件记录 HarnessKit 的可靠性、质量和防漂移判断指导。它不替代 [RULES.md](../../RULES.md) 的验证门槛。

## Protected Boundaries

优先保护这些外部可观察边界：

- Typer CLI 命令、参数、错误消息和退出行为。
- `.harnesskit/config.json` schema 和写入语义。
- `templates/` 生成到目标仓库的文件和占位内容。
- `harnesskit lint` issue、扫描边界和退出码。
- agent-facing context 文件之间的职责分层和链接可用性。

## Guidance

- 改动前先判断保护边界；涉及兼容性时使用 `$implementation-strategy`。
- 测试要覆盖用户可观察结果、回归风险和模板输出差异。
- 失败后修复并重跑同一个验证入口，最终只报告最终状态。
- 没有 runner 证据的检查只能标记为 review、agent 执行或未配置。
- 可靠性文档应说明 command、runner 和例外，不要只写“保持质量”。
- 遇到漂移时先回到仓库事实，再同步 AGENTS、RULES、ARCHITECTURE、skills、facts 或模板。

## Review Questions

- 这次改动触及了哪个 protected boundary？
- 是否需要局部测试、完整 `make verify`，还是只需 review？
- 测试失败是否是新行为暴露的问题，而不是测试本身可忽略？
- 文档、模板和 rules 是否仍指向真实存在的命令和路径？
- 是否把未配置的 CI、typecheck、coverage 或 docs build 写成完成条件？
