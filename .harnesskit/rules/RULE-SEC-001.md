# RULE-SEC-001

## Rule

不要把 secret、token、私有凭据或机器特定敏感信息写入模板、facts、rules、报告或生成产物。

## Details

本规则保护 agent-facing context 不泄漏敏感信息。安全判断参考 [docs/practices/SECURITY.md](../../docs/practices/SECURITY.md)。HarnessKit 会生成模板、facts、report 和 validation receipts；这些文件可能被提交、复制到目标仓库或展示给 agent，因此不应包含真实凭据、私有 token、真实用户数据或无必要的机器特定敏感信息。

违反形态：

- 把真实 token、API key、cookie、secret、私有凭据写入 docs、facts、rules、report 或模板。
- 在示例中使用看起来像真实凭据的值，而不是占位符。
- 无必要记录完整本机路径、用户名或私有 URL。

证据：

- [docs/practices/SECURITY.md](../../docs/practices/SECURITY.md)
- [templates/](../../templates/)
- [.harnesskit/facts.md](../facts.md)
- [docs/report.md](../../docs/report.md)

验证：

- review：检查新增文档、模板、报告和生成产物是否包含敏感信息。
- runner：Markdown/link/lint 不能完整证明无 secret；必要时应补专门扫描工具后再写成 deterministic gate。
