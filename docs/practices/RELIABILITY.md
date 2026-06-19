# Reliability Practices

本文件记录 HarnessKit 当前改动风险较高的区域。它回答“在这个项目里，改哪些东西需要格外小心”，不重复通用可靠性建议。硬约束见 [RULES.md](../../RULES.md)。

## 高风险改动区域

按风险从高到低排列：

| 区域 | 影响范围 | 为什么风险高 |
|------|----------|-------------|
| [`src/harnesskit/init.py`](../../src/harnesskit/init.py) | 目标仓库文件写入、默认跳过、`--force` 覆盖、symlink、Jinja 渲染、integration 安装和 `.harnesskit/config.json` | 失败会覆盖用户文件、生成坏 context、写坏状态文件，或让后续 integration/lint 无法判断项目状态 |
| [`templates/`](../../templates/) | `harnesskit init` 复制到目标仓库的 agent-facing 输出，包括 AGENTS/RULES/ARCHITECTURE/practices/skills/Makefile | 模板是用户可见行为；占位符泄漏、路径漂移或未同步测试会把错误扩散到所有新初始化仓库 |
| [`src/harnesskit/linter/`](../../src/harnesskit/linter/) | `harnesskit lint` 的 issue、扫描边界、warning/error 分级、exit code 和 drift 检查 | linter 是 harness 防腐入口；误报会打断用户流程，漏报会让 context 漂移长期存在 |
| [`.harnesskit/config.json`](../../.harnesskit/config.json) 与配置 schema | schema version、默认 integration、installed integrations 和项目状态读取 | 这是安装状态事实源；兼容性变化会影响 `integration install`、linter 和已初始化项目 |
| 验证入口和 hooks | `make verify`、`.pre-commit-config.yaml`、code-change-verification runner、pytest、Ruff、lychee、package build | 这些命令定义完成条件；文档或 runner 漂移会让 agent 报告不存在的 gate 或漏跑真实 gate |

相比之下，纯说明性文档改动风险较低，前提是不改变模板输出、验证入口、CLI 行为、配置语义或当前产品能力声明。

## 当前验证能力

- 完整验证入口是 `make verify`；它通过 code-change-verification runner 编排仓库验证。
- 局部 runner 包括 `uv run pytest`、`uv run ruff check .`、`uv run ruff format --check .`、`uv build`、`lychee './**/*.md'` 和 `uv run pre-commit run --all-files`。
- 模板生成、integration 安装、跳过/覆盖、symlink、配置写入和占位符泄漏主要由 [`tests/test_init.py`](../../tests/test_init.py) 覆盖。
- CLI 参数、交互选择、integration fallback 和 lint exit 行为主要由 [`tests/test_harnesskit_cli.py`](../../tests/test_harnesskit_cli.py) 覆盖。
- `harnesskit lint` 可发现部分 context drift、链接问题、verification drift、skill 引用和 rule details 问题；语义冲突仍需要 review。
- 当前没有已证实的 type checker、coverage gate、docs build 命令或 CI；不要把这些写成完成条件。
- 验证失败后修复问题并重新运行同一验证命令；最终交付只报告最终状态。

## 和 Rules 的关系

完成条件、runner 约束和必须始终成立的硬规则见 [RULES.md](../../RULES.md)。本文件只记录可靠性判断边界：哪里风险高、为什么高、以及当前有什么验证能力覆盖它。
