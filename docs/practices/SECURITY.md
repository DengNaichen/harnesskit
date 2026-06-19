# Security Practices

本文件记录 HarnessKit 当前实际存在的安全配置面和风险边界。它回答“在这个项目里，哪些地方改了会影响安全”，不重复通用安全建议。硬约束见 [RULES.md](../../RULES.md)。

## 安全配置面

### 认证、授权与访问控制

- 当前运行时代码是本地 CLI/toolkit，没有登录、会话、RBAC、HTTP middleware、管理后台或在线权限模型。
- 当前会使用 token 的入口是 [`scripts/publish_pypi.sh`](../../scripts/publish_pypi.sh)：发布 PyPI 时从 `UV_PUBLISH_TOKEN` 或被 git 忽略的本地 `.env` 读取 token，再通过环境变量传给 `uv publish`。
- 不要在文档、模板、facts、rules、receipts、测试 fixture 或生成输出中写入真实 token、私有 URL、用户名、机器特定路径或客户数据。
- 安全政策、漏洞披露渠道、支持版本和响应 SLA 当前没有仓库配置证据；需要时只能写成未配置或待确认。

### 数据、文件写入与输出

- 主要数据面是目标仓库里的 context 资产：`AGENTS.md`、`ARCHITECTURE.md`、`RULES.md`、`docs/practices/`、`.agents/skills/`、`.harnesskit/config.json`、`.harnesskit/facts.md` 和 receipts。
- 文件写入集中在 [`src/harnesskit/init.py`](../../src/harnesskit/init.py)：模板复制、Jinja 渲染、symlink、integration 安装和 `.harnesskit/config.json` 写入。
- 默认行为必须跳过已有文件；只有显式 `--force` 才覆盖。改 `_copy_template_tree()`、`_copy_template_paths()` 或 symlink 写入时要重新检查覆盖语义。
- 目标路径、模板路径和生成路径应保持在目标项目内；任何路径拼接、symlink 或 future `--fix` 行为都要避免路径逃逸和误删用户内容。
- linter 报告应优先输出相对路径；`relative_path()` 无法相对化时才会回退到绝对路径，新增诊断输出不要无必要暴露本机路径。

### 外部系统与依赖

- 当前没有数据库、对象存储、消息队列、支付、通知或认证服务连接。
- 外部命令边界包括 `uv`、`git`、可选 `markdownlint`、`lychee`、pre-commit、pytest/Ruff 和 `uv publish`。
- 新增依赖必须同步 [pyproject.toml](../../pyproject.toml) 与 [uv.lock](../../uv.lock)，并确认它不会把 secret、网络访问或系统命令执行引入未说明的信任边界。
- [`scripts/publish_pypi.sh`](../../scripts/publish_pypi.sh) 使用 `set +x` 避免 shell trace 泄露 token；不要在发布脚本、日志或错误输出中打印 token。
- [.gitignore](../../.gitignore) 忽略 `.env`、`.env.*` 和 `.harnesskit/receipts/`；不要把这些本地状态或 receipt 内容改成默认可提交资产。

## 当前安全检查能力

- 当前没有已证实的 secret scan、dependency scan、SAST、CI security gate、安全披露流程或支持版本政策。
- `uv run pytest` 覆盖默认跳过、`--force` 覆盖、symlink、配置写入和 integration 安装等关键写文件行为。
- `uv run harnesskit lint .` 和 Markdown link check 可发现部分 context drift、坏链接、verification drift 和引用问题，但不等于安全扫描。
- 发布入口 `make publish` 会通过 [`scripts/publish_pypi.sh`](../../scripts/publish_pypi.sh) 先运行 `make verify`、清理并重建 `dist/`，再调用 `uv publish`。
- 仍需人工 review 的安全边界包括：输出是否泄露敏感信息、路径是否可能逃逸、模板是否诱导提交 secret、新依赖或外部命令是否扩大信任边界。

## 和 Rules 的关系

- 稳定、可执行、必须遵守的安全约束应沉淀到 [RULES.md](../../RULES.md)，复杂背景保留在本文。
- 可自动检查的安全要求应绑定到测试、lint、pre-commit、CI 或其他 runner；没有 runner 证据时，只能写成 review 或待确认。
- 不要把本文中的待确认或 review 项改写成硬规则，除非已经用仓库事实或团队确认支撑。
