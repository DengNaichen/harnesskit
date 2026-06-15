# 架构地图

本文件是 HarnessKit 的粗粒度仓库地图。它帮助 agent 和贡献者在修改前找到正确的代码区域。本文件不是工作流规范、API 参考或详细设计文档。

下面的 Markdown 链接就是地图。带有 `<!-- harnesskit:coverage=direct-children -->` 的路径会要求 linter 检查它的直接子项是否也在本文中以链接形式表示。

## 顶层地图

- [`src/harnesskit/`](src/harnesskit/) <!-- harnesskit:coverage=direct-children -->：打包后的 HarnessKit 运行时代码。修改 CLI、初始化行为、integration 安装、模板渲染或 `.harnesskit/config.json` 写入时看这里。
  - [`__init__.py`](src/harnesskit/__init__.py)：包元数据入口；当前暴露 `__version__`。
  - [`cli.py`](src/harnesskit/cli.py)：Typer 命令面，定义 `harnesskit init`、`harnesskit integration list`、`harnesskit integration install`、`--force`、`--here`、`--integration` 和 `--version`。
  - [`init.py`](src/harnesskit/init.py)：初始化引擎，负责解析项目路径、复制内置模板、用 `StrictUndefined` 渲染 Jinja 模板、写入符号链接、安装 Codex skills、校验 integration，并写入 `.harnesskit/config.json`。
- [`templates/`](templates/)：`harnesskit init` 复制到目标仓库的内置资产。这里的改动会影响生成的 harness 输出，应视为用户可见的模板行为。
- [`tests/`](tests/)：打包 CLI/init 行为的 pytest 测试，覆盖生成文件、配置写入、integration 安装、跳过/强制覆盖行为、未补全模板标记和 shared skill 输出。
- [`harness-linter-poc/`](harness-linter-poc/) <!-- harnesskit:coverage=direct-children -->：独立的 Context Harness linter POC。它有意放在打包运行时 `src/harnesskit` 之外，并由 pre-commit 用来校验 harness 文件。
  - [`app/`](harness-linter-poc/app/) <!-- harnesskit:coverage=direct-children -->：linter 实现和命令行入口。
    - [`harness_lint.py`](harness-linter-poc/app/harness_lint.py)：独立 CLI 和编排层，运行所有 lint 规则组，并输出文本或 JSON 报告。
    - [`core/`](harness-linter-poc/app/core/) <!-- harnesskit:coverage=direct-children -->：linter 规则共享的基础组件。
      - [`__init__.py`](harness-linter-poc/app/core/__init__.py)：标记 core helper package。
      - [`constants.py`](harness-linter-poc/app/core/constants.py)：共享 linter 常量、支持的 integration、必需 Codex skill 路径、marker 字符串、命令字符串和正则模式。
      - [`issues.py`](harness-linter-poc/app/core/issues.py)：构造标准化 lint issue 的 helper，并把路径规范化为仓库相对路径。
      - [`markdown.py`](harness-linter-poc/app/core/markdown.py)：Markdown marker 和链接解析 helper，供多个规则模块复用。
      - [`models.py`](harness-linter-poc/app/core/models.py)：lint issue、report、severity 和 marked Markdown block 的 dataclass 模型。
    - [`rules/`](harness-linter-poc/app/rules/) <!-- harnesskit:coverage=direct-children -->：相互独立的 lint 规则组。
      - [`__init__.py`](harness-linter-poc/app/rules/__init__.py)：标记 rule package。
      - [`architecture.py`](harness-linter-poc/app/rules/architecture.py)：检查 `ARCHITECTURE.md` 的未完成职责描述、coverage hint、链接路径是否存在，以及 direct-child coverage。
      - [`config.py`](harness-linter-poc/app/rules/config.py)：检查 `.harnesskit/config.json` 的结构、schema version、默认 integration 和 installed integration 列表。
      - [`core.py`](harness-linter-poc/app/rules/core.py)：检查必需 harness 文件、`CLAUDE.md` 指针行为和已安装的 Codex integration 资产。
      - [`harness_markdown.py`](harness-linter-poc/app/rules/harness_markdown.py)：收集 harness Markdown 文件，并检查本地链接、TODO checklist marker 配对和可选外部 Markdown lint。
      - [`project.py`](harness-linter-poc/app/rules/project.py)：检查请求 lint 的目标是否为目录。
      - [`rule_details.py`](harness-linter-poc/app/rules/rule_details.py)：检查 `RULES.md` 中的短规则是否有对应 `.harnesskit/rules/RULE-*.md` details 文件，并暴露 orphan/过长规则摘要。
      - [`skills.py`](harness-linter-poc/app/rules/skills.py)：检查 skill frontmatter，以及 `AGENTS.md` 中的 `$skill-name` 引用是否存在对应 skill。
      - [`tech_stack.py`](harness-linter-poc/app/rules/tech_stack.py)：从 manifest 检测仓库技术栈事实，并检查已声明的 tech-stack block 是否漂移。
      - [`verification.py`](harness-linter-poc/app/rules/verification.py)：检查验证文档中的过期测试框架引用，以及 lint、format、build、pre-commit 命令是否被正确记录。
  - [`tests/`](harness-linter-poc/tests/) <!-- harnesskit:coverage=direct-children -->：独立 linter POC 的 pytest 覆盖。
    - [`conftest.py`](harness-linter-poc/tests/conftest.py)：测试路径设置，让 POC app 模块可以被导入。
    - [`testing_helpers.py`](harness-linter-poc/tests/testing_helpers.py)：临时 harness 项目的 fixture 构造器和断言 helper。
    - [`test_architecture_rules.py`](harness-linter-poc/tests/test_architecture_rules.py)：测试架构地图未完成文本、链接、coverage hint 和 direct-child 检查。
    - [`test_cli.py`](harness-linter-poc/tests/test_cli.py)：测试 linter CLI/report 行为。
    - [`test_config_rules.py`](harness-linter-poc/tests/test_config_rules.py)：测试 `.harnesskit/config.json` 校验。
    - [`test_markdown_rules.py`](harness-linter-poc/tests/test_markdown_rules.py)：测试 harness Markdown 链接和 marker 检查。
    - [`test_project_rules.py`](harness-linter-poc/tests/test_project_rules.py)：测试项目路径校验。
    - [`test_rule_detail_rules.py`](harness-linter-poc/tests/test_rule_detail_rules.py)：测试短规则和 details 文件的联动、必需章节、orphan details 和过长规则摘要检查。
    - [`test_skill_rules.py`](harness-linter-poc/tests/test_skill_rules.py)：测试 skill frontmatter 和 `$skill` 引用检查。
    - [`test_tech_stack_rules.py`](harness-linter-poc/tests/test_tech_stack_rules.py)：测试技术栈事实检测和漂移检查。
    - [`test_verification_rules.py`](harness-linter-poc/tests/test_verification_rules.py)：测试验证漂移和命令文档检查。
- [`.agents/skills/`](.agents/skills/)：本仓库工作时使用的 Codex 本地技能。这里应与根目录 `AGENTS.md`、`RULES.md`、模板和验证 runner 保持一致。
- [`docs/`](docs/)：产品、设计、路线图和进展文档。设计类文档位于 [`docs/design/`](docs/design/)。

## 关键文件

- [`pyproject.toml`](pyproject.toml)：Python 包元数据、运行时依赖、console script 入口、Hatchling 构建配置和 dev dependency group。
- [`AGENTS.md`](AGENTS.md)：本仓库的顶层 agent 路由指南，指向规则、skills、架构地图和验证入口。
- [`RULES.md`](RULES.md)：本仓库基于证据沉淀的工程规则、Guard 绑定和命令事实。
- [`README.md`](README.md)：产品定位、MVP 范围、CLI 使用方式和 Context Harness 总览。

## 生成到目标仓库的资产

HarnessKit 会在目标仓库中安装或维护这些文件：

- `AGENTS.md`：目标仓库的 agent 路由指南，由 [`templates/AGENTS.md`](templates/AGENTS.md) 生成。
- `RULES.md`：目标仓库的规则模板，由 [`templates/RULES.md`](templates/RULES.md) 生成。
- `CLAUDE.md`：指向 `AGENTS.md` 的 companion 文件；本仓库当前把它生成为符号链接。
- `.harnesskit/config.json`：HarnessKit 状态文件，包含 `schema_version`、`project_name`、`default_integration` 和 `installed_integrations`。
- `.agents/skills/*/SKILL.md`：从 [`templates/skills/`](templates/skills/) 安装的 Codex skill 说明。

## 当前包形状

当前运行时包刻意保持很小：

- `cli.py`：用户可见的 Typer 命令声明和 Rich 输出。
- `init.py`：初始化、integration 安装、模板渲染、符号链接和配置写入的文件系统行为。
- `__init__.py`：包版本元数据。

随着包增长，这份地图仍应保持粗粒度。只有当新模块改变 agent 首先应该查看的位置时，才把它加入这里；不要因为每个 helper 函数移动就更新本地图。

## 相关文档

- [`README.md`](README.md)：产品概览、MVP 边界和 CLI 使用方式。
- [`AGENTS.md`](AGENTS.md)：本仓库的 agent 操作指南。
- [`docs/design/`](docs/design/)：AGENTS、RULES、Guard 和 Harness Builder 模型的设计笔记。
- [`docs/design/ARCHITECTURE.md`](docs/design/ARCHITECTURE.md)：`ARCHITECTURE.md` 的设计说明，解释架构地图如何保持粗粒度、可验证和不漂移。
- [`docs/design/DESIGN.md`](docs/design/DESIGN.md)：Scan -> Rule -> Guard 产品设计模型。
- [`docs/ROADMAP.md`](docs/ROADMAP.md)：面向未来的产品和实现路线图。
