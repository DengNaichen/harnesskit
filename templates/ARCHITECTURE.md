# [PROJECT_NAME] 架构地图

本文件是当前仓库的粗粒度架构地图。它帮助 agent 和贡献者在修改前找到正确的代码区域。本文件不是工作流规范、API 参考或详细设计文档。

下面的 Markdown 链接就是地图。带有 `<!-- harnesskit:coverage=direct-children -->` 的路径会要求 linter 检查它的直接子项是否也在本文中以链接形式表示。只有在路径和职责已经从仓库事实确认后，才添加 coverage marker。

<!-- harnesskit:todo-checklist:start -->
补全本文件前请确认：
- 从真实目录结构、构建清单、测试文件、脚本和现有文档中确认每条路径说明。
- 只记录对 agent 定位有价值的目录、关键文件和职责边界；不要把本文变成完整文件清单。
- 已确认的路径用 Markdown 链接表示；暂时确认不了的内容保留 `[NEEDS CLARIFICATION: ...]`。
- 完成后同步检查 `AGENTS.md`、`RULES.md`、本地 skills 和验证入口中引用的路径是否一致。
<!-- harnesskit:todo-checklist:end -->

## 顶层地图

- [`AGENTS.md`](AGENTS.md)：agent 操作入口和顶层路由器。
- [`RULES.md`](RULES.md)：工程规则、Guard 绑定和项目命令事实来源。
- `.agents/skills/`：本地 agent skills；具体触发条件应由 `AGENTS.md` 路由，执行细节放在各 skill 的 `SKILL.md`。
- `.harnesskit/config.json`：HarnessKit 状态文件，记录 schema、项目名、默认 integration 和已安装 integration。
- [`.harnesskit/facts.md`](.harnesskit/facts.md)：`$scan-facts` 生成的 scan/fill 事实快照；用于把仓库证据交给 `$fill-agents`、`$fill-architecture`、`$fill-rules` 和 `$fill-skills`，但不能替代真实仓库事实。
- [`Makefile`](Makefile)：HarnessKit 安装的验证入口；具体 checks 必须在 `.agents/skills/code-change-verification/scripts/run_guard.py` 中基于仓库事实补全。
- [`CLAUDE.md`](CLAUDE.md)：companion agent 指南，默认应指向 `AGENTS.md`。
- [NEEDS CLARIFICATION: 主要源码目录，例如 `src/`、`app/`、`packages/` 或其他真实路径]
- [NEEDS CLARIFICATION: 主要测试目录，例如 `tests/`、`test/`、`spec/` 或其他真实路径]
- [NEEDS CLARIFICATION: 主要文档目录，例如 `docs/`、`design/` 或其他真实路径]
- [NEEDS CLARIFICATION: 构建、部署、脚本、模板或生成资产目录]

## 关键文件

- [NEEDS CLARIFICATION: 包管理或构建清单，例如 `pyproject.toml`、`package.json`、`go.mod`、`pom.xml`、`Cargo.toml`]
- [NEEDS CLARIFICATION: 锁文件，例如 `uv.lock`、`package-lock.json`、`pnpm-lock.yaml`、`go.sum` 或 N/A]
- [NEEDS CLARIFICATION: 测试配置、lint 配置、format 配置、CI 配置或 hook 配置]
- [NEEDS CLARIFICATION: 产品说明、README、设计文档或 API 文档]

## 生成资产和外部状态

如果本仓库会生成文件、写入持久配置、发布包或维护外部状态，请在这里记录入口和边界：

- [NEEDS CLARIFICATION: 生成资产路径、生成命令和源模板]
- [NEEDS CLARIFICATION: 持久配置、schema、数据库、缓存或外部状态]
- [NEEDS CLARIFICATION: 发布产物、构建输出、部署目标或集成系统]

## 边界说明

记录容易混淆、需要 agent 特别注意的边界：

- [NEEDS CLARIFICATION: 运行时代码和测试/示例/POC 的边界]
- [NEEDS CLARIFICATION: 当前仓库文档和会生成到其他仓库/环境中的模板输出边界]
- [NEEDS CLARIFICATION: 设计说明和当前实现状态的边界]
- [NEEDS CLARIFICATION: 本地验证 runner、hook、CI 或平台 gate 的边界]

## 更新规则

当主要目录、关键文件、生成输出、验证入口或模块职责发生变化时，同步更新本文件。只有当新模块改变 agent 首先应该查看的位置时，才把它加入这里；不要因为每个 helper 函数移动就更新本地图。
