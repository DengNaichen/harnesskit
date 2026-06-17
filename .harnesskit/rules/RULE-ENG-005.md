# RULE-ENG-005

## Rule

发布、部署或托管相关判断必须以仓库配置或团队确认为准，不要把局部 docs 托管配置推断成 package release、CI 或生产部署门槛。

## Details

本规则是 deployment/release 边界，不是发布流程说明。本仓库当前有 package build 配置、手动 PyPI 发布入口，也有 [docs/](../../docs/) 下的 GitHub Pages 静态站点资产；这些事实需要按作用域解读。[docs/](../../docs/) 静态站点资产只证明文档站点可由 GitHub Pages 托管，不能推出 Python package 已配置 CI gate、生产部署流程或自动 release gate。

适用范围：

- 修改 package metadata、构建配置、模板打包或发布相关文档。
- 引用 GitHub Pages、CI、release、deployment、production、artifact 或托管状态。
- 在 agent 指南、rules、skills、总结或验证计划里描述发布/部署完成条件。

违反形态：

- 把 [docs/](../../docs/) 的 GitHub Pages 静态站点写成整个项目的生产部署流程。
- 把没有 runner 证据的 CI、release automation、deployment gate 写成完成条件。
- 影响 package 或模板打包却没有确认 `uv build` 仍可通过。

证据：

- [docs/index.html](../../docs/index.html)
- [docs/.nojekyll](../../docs/.nojekyll)
- [pyproject.toml](../../pyproject.toml)
- [Makefile](../../Makefile)
- [scripts/publish_pypi.sh](../../scripts/publish_pypi.sh)
- [AGENTS.md](../../AGENTS.md)
- 仓库当前有 `make publish` 手动 PyPI 发布入口；文档站点改用 GitHub Pages 静态托管；没有已证实的 `.github` CI、自动 release gate 或生产部署 runner。

验证：

- runner：影响 package、模板打包或构建配置时运行 `uv build` 或 `make verify`。
- runner：手动发布 PyPI 包时使用 `make publish`；它要求 PyPI token 来自环境变量或被忽略的本地 `.env`。
- review：确认发布、部署、托管和 CI 相关判断都有仓库配置或团队确认支撑。
- 未配置：当前没有证据表明 package release、CI 或生产部署 gate 会自动阻断变更。
