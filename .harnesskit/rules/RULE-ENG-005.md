# RULE-ENG-005

## Rule

发布、部署或托管相关判断必须以仓库配置或团队确认为准，不要把局部 docs 托管配置推断成 package release、CI 或生产部署门槛。

## Details

本规则是 deployment/release 边界，不是发布流程说明。本仓库当前有 package build 配置，也有 `docs/` 下的 Vercel 托管配置；这些事实需要按作用域解读。`docs/` 托管配置只证明文档站点存在相关配置，不能推出 Python package 已配置发布流水线、CI gate、生产部署流程或 release 自动化。

适用范围：

- 修改 package metadata、构建配置、模板打包或发布相关文档。
- 引用 Vercel、CI、release、deployment、production、artifact 或托管状态。
- 在 agent 指南、rules、skills、总结或验证计划里描述发布/部署完成条件。

违反形态：

- 把 `docs/` 的 Vercel 配置写成整个项目的生产部署流程。
- 把没有 runner 证据的 CI、release automation、deployment gate 写成完成条件。
- 影响 package 或模板打包却没有确认 `uv build` 仍可通过。

证据：

- `docs/vercel.json`
- `docs/.vercel/project.json`
- `pyproject.toml`
- `Makefile`
- `AGENTS.md`
- 仓库当前没有已证实的 `.github` CI、package release automation 或生产部署 runner。

验证：

- runner：影响 package、模板打包或构建配置时运行 `uv build` 或 `make verify`。
- review：确认发布、部署、托管和 CI 相关判断都有仓库配置或团队确认支撑。
- 未配置：当前没有证据表明 package release、CI 或生产部署 gate 会自动阻断变更。
