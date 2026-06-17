# Security Practices

本文件记录当前仓库的安全判断指导。安全硬约束仍应抽到 [RULES.md](../../RULES.md) 和 `.harnesskit/rules/`，并尽可能绑定测试、lint 或 review。

<!-- harnesskit:todo-checklist:start -->
补全本文件前请确认：
- 从真实威胁模型、文件写入、数据处理、依赖和部署方式中提炼实践。
- 不要虚构安全披露渠道、支持版本或响应 SLA。
- 未确认内容保留 `[NEEDS CLARIFICATION: ...]`。
<!-- harnesskit:todo-checklist:end -->

## Scope

- [NEEDS CLARIFICATION: 本仓库最重要的安全边界，例如 secrets、用户数据、文件写入、网络、权限、依赖或部署。]

## Guidance

- 不要把 secret、token、私有凭据、真实用户数据或机器特定敏感信息写入模板、facts、rules、报告或生成产物。
- 文件写入、路径处理、外部命令和依赖变更必须回到仓库事实核对。
- [NEEDS CLARIFICATION: 本仓库的安全报告入口、支持范围和不适用范围。]

## Review Questions

- 输出里是否可能包含真实 secret、token、私有 URL、用户名或机器路径？
- 文件写入是否可能覆盖用户手写内容或写到项目外？
- 安全声明是否有仓库证据，还是只是通用最佳实践？
