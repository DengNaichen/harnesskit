# Coding Practices

本文件记录从 HarnessKit 当前源码、测试和配置中提取的编码约定。它回答“这个仓库里的代码应该长什么样”，不重复通用工程建议。硬约束见 [RULES.md](../../RULES.md)。

## 代码组织

- [`src/harnesskit/`](../../src/harnesskit/) 是打包后的运行时代码；CLI、初始化、integration 安装、模板渲染和 linter 产品行为都应落在这里。
- [`templates/`](../../templates/) 是 `harnesskit init` 的用户可见输出；改模板要按生成行为处理，不要把模板占位符当成本仓库事实。
- [`tests/`](../../tests/) 覆盖 CLI/init/generated harness/lint 行为；模板输出变化优先同步 [`tests/test_init.py`](../../tests/test_init.py)，命令面变化优先同步 [`tests/test_harnesskit_cli.py`](../../tests/test_harnesskit_cli.py)。
- [`harness-linter-poc/`](../../harness-linter-poc/) 是旧参考实现；新增产品 lint 行为不要放回 POC。

## 模块职责

| 区域 | 放什么 | 不放什么 |
|------|--------|----------|
| [`src/harnesskit/cli.py`](../../src/harnesskit/cli.py) | Typer 命令定义、参数解析、交互选择、CLI 输出和 exit 行为 | 模板复制细节、配置写入细节、linter rule 实现 |
| [`src/harnesskit/init.py`](../../src/harnesskit/init.py) | 项目路径解析、模板复制/渲染、symlink、integration 安装、`.harnesskit/config.json` 写入 | Typer 展示逻辑、linter drift 检查 |
| [`src/harnesskit/linter/core/`](../../src/harnesskit/linter/core/) | linter 共享模型、常量、issue 构造和 Markdown helper | 具体产品规则分支 |
| [`src/harnesskit/linter/rules/`](../../src/harnesskit/linter/rules/) | 按主题拆分的 harness lint 检查 | CLI 命令定义、init 写文件行为 |
| [`tests/`](../../tests/) | 面向用户可观察行为的 pytest 覆盖 | 只锁死内部 helper 排列的脆弱测试 |

## 命名和风格

- Python 代码使用 `from __future__ import annotations`、`Path`、类型标注和小型纯 helper；优先延续现有函数式拆分，而不是引入类层级。
- CLI 参数使用 `typing.Annotated` 配合 Typer；用户可见错误通过 `InitError` 转成 CLI exit，不在 CLI 层散落底层异常细节。
- init 相关常量集中在 [`src/harnesskit/init.py`](../../src/harnesskit/init.py) 顶部；linter 共享常量集中在 [`src/harnesskit/linter/core/constants.py`](../../src/harnesskit/linter/core/constants.py)。
- linter issue 统一通过 `issue(...)` 构造，包含明确的 `code`、`found`、`expected`、必要证据和修复提示；不要在规则里手写不一致的报告结构。
- 注释和 docstring 只解释模块职责或不明显边界；避免重复代码已经表达的操作。

## 测试约定

- 测试入口是 `uv run pytest`；完整验证入口是 `make verify`。
- CLI 行为使用 Typer `CliRunner`，交互依赖用 `monkeypatch` 和小型 fake 对象替换，不依赖真实 TTY。
- init/template 测试应断言生成文件、配置字段、symlink、跳过/覆盖行为和占位符泄漏；不要只断言函数被调用。
- linter 测试应通过生成项目或修改 harness 文件来验证用户能看到的 lint 输出和 exit code。
- 测试应覆盖行为边界和回归风险；只有当 helper 本身承载稳定契约时才直接测试 helper。

## 注释和文档

- 运行时代码旁边只保留解释边界、错误语义或兼容性风险的短注释。
- 路径职责、生成资产和旧/新入口边界写入 [`ARCHITECTURE.md`](../../ARCHITECTURE.md)，不要散落到代码注释里。
- 硬性约束写入 [`RULES.md`](../../RULES.md)；背景、取舍和判断问题写入 `docs/practices/`。
- 修改 HarnessKit 自身 context 文档时，先直接按目标态更新 root/template/skill/tests/linter 中确有职责关联的部分，不用 fill skill 代替人工判断。

## 和 Rules 的关系

违反现有模块边界、测试约束或验证入口时，按对应 Rule 处理；本文件只帮助判断“怎样写得更像这个仓库”。
