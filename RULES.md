# HarnessKit Harness Rules

本文件记录 HarnessKit 仓库当前已经确认或待确认的 Harness Rules。它不是通用模板；通用模板位于 `templates/RULES.md`。本文件只写能从本仓库事实、配置或现有约定中确认的规则，确认不了的内容标记为待确认或未配置。

## 使用方式

- **状态**：写明规则在本仓库中是已确认、部分确认、待确认还是未配置。
- **事实来源**：列出支持这条规则的文件、脚本、配置或人工约定。
- **agent 契约**：用祈使句说明 agent 开发时必须怎么做。
- **Guard 类型**：写明这条规则当前是确定性、部分确定性、人工/agent review 还是未配置。
- **Guard**：写出当前能验证或执行该规则的命令、检查、hook、review 或待补平台配置。

## 基础候选规则

### `RULE-001` 单一验证入口

- **状态**：已确认。本仓库使用 `make verify` 作为单一完整验证入口。
- **Guard 类型**：确定性。
- **事实来源**：`Makefile`、`AGENTS.md`、`.agents/skills/code-change-verification/SKILL.md`、`.pre-commit-config.yaml`。
- **agent 契约**：完成运行时代码、模板、测试、构建配置或测试行为变更时，按 `$code-change-verification` 运行 `make verify`；不要虚构本仓库不存在的 type check、coverage 或 docs build 命令。
- **Guard**：`make verify` 运行 Markdown links、Ruff lint、Ruff format check、pytest、package build 和 pre-commit hooks。

### `RULE-002` 新增行为必须有测试

- **状态**：已确认。
- **Guard 类型**：部分确定性。pytest 能证明测试通过，但“新增行为是否被充分覆盖”仍需要 review 判断。
- **事实来源**：`tests/test_init.py`、`harness-linter-poc/test_*.py`、`AGENTS.md`、`.agents/skills/code-change-verification/SKILL.md`。
- **agent 契约**：修改 CLI 行为、初始化逻辑、配置写入、模板输出、harness lint 行为或其他用户可见行为时，同步更新或新增自动化测试。
- **Guard**：`uv run pytest` 必须通过；`uv run pre-commit run --all-files` 中的 pytest hook 必须通过；review 时检查代码变更和测试变更是否匹配。

### `RULE-003` Test 入口以仓库事实为准

- **状态**：已确认。
- **Guard 类型**：确定性。
- **事实来源**：`pyproject.toml` 中的 dev dependency、`tests/`、`harness-linter-poc/test_*.py`、`.pre-commit-config.yaml`。
- **agent 契约**：使用 pytest 作为测试入口；不要把 unittest 或其他未配置测试框架写进验证计划。
- **Guard**：运行 `uv run pytest`；pre-commit 的 `pytest` hook 也运行同一测试入口。

### `RULE-004` 命名遵守本仓库现有风格

- **状态**：已确认。
- **Guard 类型**：部分确定性。Ruff 覆盖格式和部分代码风格，命名是否符合仓库惯例仍主要靠 review。
- **事实来源**：`src/harnesskit/`、`tests/`、`harness-linter-poc/`、`pyproject.toml` 中的 Ruff 配置。
- **agent 契约**：新增 Python 代码遵守本仓库现有命名风格：函数和变量使用 `snake_case`，类使用 `PascalCase`，项目已有例外以本地代码为准。
- **Guard**：`uv run ruff check .`、`uv run ruff format --check .` 和 review 共同检查命名与风格；当前没有单独 AST/naming guard。

### `RULE-005` import 和依赖必须同步

- **状态**：已确认。
- **Guard 类型**：部分确定性。测试和 build 可暴露部分缺依赖问题，但当前没有专门的 import/dependency guard。
- **事实来源**：`pyproject.toml`、`uv.lock`、`AGENTS.md`。
- **agent 契约**：不要引入未声明依赖；新增第三方 import 时，同步更新 `pyproject.toml` 和 `uv.lock`。
- **Guard**：使用 `uv` 运行仓库命令；`uv run pytest`、`uv build` 和 review 间接检查依赖声明。当前没有专门的 import/dependency guard。

### `RULE-006` 文档和 context harness 不漂移

- **状态**：已确认。
- **Guard 类型**：部分确定性。工具可检查链接、marker、skill 引用和部分 drift；语义是否误导 agent 仍需要 review。
- **事实来源**：`AGENTS.md`、`ARCHITECTURE.md`、`RULES.md`、`.agents/skills/`、`templates/`、`lychee.toml`、`harness-linter-poc/`。
- **agent 契约**：更新 agent-facing context 时，确保 `AGENTS.md`、`ARCHITECTURE.md`、`RULES.md`、skills、verification block、tech stack block 和模板输出不误导 agent。
- **Guard**：运行 `lychee './**/*.md'` 检查 Markdown 链接；运行 `uv run pre-commit run --all-files` 触发 harness lint、Markdown links、pytest、Ruff 和 build。

## 可选规则

### `RULE-101` Branch protection 和 required checks

- **状态**：待确认。仓库内没有 `.github/` 工作流或可验证的 branch protection 配置。
- **Guard 类型**：未配置。
- **事实来源**：当前仓库文件系统未发现 `.github` CI 配置；本地配置不能证明代码托管平台设置。
- **agent 契约**：不要声称本仓库已启用 branch protection、required checks 或 review 要求。需要启用时，先从代码托管平台或团队规则取得证据。
- **Guard**：待补代码托管平台 branch protection / required checks 配置；当前无仓库内 guard。

### `RULE-102` 锁文件一致性

- **状态**：部分确认。仓库使用 `uv.lock` 锁定依赖，但完整验证栈当前没有单独的 locked install gate。
- **Guard 类型**：部分确定性。
- **事实来源**：`pyproject.toml`、`uv.lock`、`AGENTS.md`、`.agents/skills/code-change-verification/SKILL.md`。
- **agent 契约**：首次配置或依赖变更后运行 `uv sync`；依赖变更必须同步 `pyproject.toml` 和 `uv.lock`。不要只改依赖清单而不更新锁文件。
- **Guard**：`uv run pytest`、`uv build` 和 review 间接检查依赖一致性；是否加入 `uv sync --locked` 作为 CI gate 仍待确认。

### `RULE-103` Type check

- **状态**：未配置。
- **Guard 类型**：未配置。
- **事实来源**：`pyproject.toml` 未声明 mypy、pyright 或同类 type checker；`AGENTS.md` 明确当前没有 type checker 配置。
- **agent 契约**：不要把 type check 写成本仓库完成条件；如果未来新增 type checker，同步更新本文件、`AGENTS.md` 和 `$code-change-verification`。
- **Guard**：当前无 type check guard。

### `RULE-109` 测试覆盖率 gate

- **状态**：未配置。
- **Guard 类型**：未配置。
- **事实来源**：`pyproject.toml` 未声明 coverage、pytest-cov 或同类覆盖率工具；`AGENTS.md` 和 `$code-change-verification` 当前完整验证栈没有 coverage 命令。
- **agent 契约**：不要把 coverage 写成本仓库完成条件；新增 coverage 工具或覆盖率阈值后，同步更新本文件、`AGENTS.md` 和 `$code-change-verification`。即使未来启用 coverage，也不能用覆盖率阈值替代新增行为的自动化测试。
- **Guard**：当前无 coverage guard。

### `RULE-104` Linter

- **状态**：已确认。
- **Guard 类型**：确定性。
- **事实来源**：`pyproject.toml` dev dependencies、`.pre-commit-config.yaml`、`.agents/skills/code-change-verification/SKILL.md`。
- **agent 契约**：把 Ruff lint 作为 Python 代码和测试变更的完成门槛。
- **Guard**：运行 `uv run ruff check .`；pre-commit 的 `ruff check` hook 运行同一检查。

### `RULE-105` Formatter check-only gate

- **状态**：已确认。
- **Guard 类型**：确定性。
- **事实来源**：`pyproject.toml` 中的 Ruff formatter 配置、`.pre-commit-config.yaml`、`.agents/skills/code-change-verification/SKILL.md`。
- **agent 契约**：完成检查使用 `uv run ruff format --check .`；不要把会改文件的 `ruff format .` 写成完成门槛。
- **Guard**：运行 `uv run ruff format --check .`；pre-commit 的 `ruff format --check` hook 运行同一检查。

### `RULE-106` Build 进入验证入口

- **状态**：已确认。
- **Guard 类型**：确定性。
- **事实来源**：`pyproject.toml` 的 `[project]`、`[build-system]` 和 Hatchling 配置；`.pre-commit-config.yaml`；`.agents/skills/code-change-verification/SKILL.md`。
- **agent 契约**：影响 package、模板打包或构建配置时，运行 `uv build` 并确认包能构建成功。
- **Guard**：运行 `uv build`；pre-commit 的 `package build` hook 运行 `uv build && rm -rf dist`。

### `RULE-107` Pre-commit 或 hook suite

- **状态**：已确认。
- **Guard 类型**：确定性。
- **事实来源**：`.pre-commit-config.yaml`。
- **agent 契约**：把 pre-commit 视为验证 suite，而不是唯一 Guard；完成实质性代码或模板变更时仍按 `make verify` 收敛。
- **Guard**：运行 `uv run pre-commit run --all-files`，触发 Ruff、harness lint、pytest、Markdown links 和 package build。

### `RULE-108` Architecture Map

- **状态**：已确认，但当前 `ARCHITECTURE.md` 仍有 placeholder 职责描述。
- **Guard 类型**：部分确定性。harness lint 可检查路径、coverage hint 和 placeholder；职责描述是否准确仍需要 review。
- **事实来源**：`ARCHITECTURE.md`、`harness-linter-poc/rules/architecture.py`、`.pre-commit-config.yaml`。
- **agent 契约**：修改重要模块、目录职责或生成资产时，先参考 `ARCHITECTURE.md`；新增重要模块或职责变化时同步更新架构地图。
- **Guard**：harness lint 检查路径存在性、coverage hint 和 placeholder；当前 placeholder 会作为 warning 暴露。

## 项目命令绑定

| 检查项 | 当前命令 | 事实来源 |
| --- | --- | --- |
| 完整验证入口 | `make verify` | `Makefile`、`AGENTS.md`、`.agents/skills/code-change-verification/SKILL.md` |
| 依赖安装 | `uv sync` | `AGENTS.md`、`.agents/skills/code-change-verification/SKILL.md` |
| Markdown links | `lychee './**/*.md'` | `AGENTS.md`、`lychee.toml` |
| Lint | `uv run ruff check .` | `pyproject.toml`、`.pre-commit-config.yaml` |
| Format check | `uv run ruff format --check .` | `pyproject.toml`、`.pre-commit-config.yaml` |
| Test | `uv run pytest` | `pyproject.toml`、`tests/`、`harness-linter-poc/test_*.py` |
| Type check | N/A，当前未配置 | `AGENTS.md`、`pyproject.toml` |
| Coverage | N/A，当前未配置 | `pyproject.toml`、`AGENTS.md`、`.agents/skills/code-change-verification/SKILL.md` |
| Build | `uv build` | `pyproject.toml`、`.agents/skills/code-change-verification/SKILL.md` |
| Hook suite | `uv run pre-commit run --all-files` | `.pre-commit-config.yaml` |
