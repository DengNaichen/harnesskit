# HarnessKit Harness Facts

本文件位于 `.harnesskit/facts.md`，是 `scan -> fill` 工作流的事实交接快照。`$scan-facts` 从仓库事实刷新本文件；`$fill-agents`、`$fill-architecture`、`$fill-rules` 和 `$fill-skills` 消费本文件来更新对应 artifact。

本文件不是仓库事实本身的替代品。填充任何 agent-facing 文档前，仍应优先核对真实源码、清单、脚本、锁文件、hook 配置和现有文档。

<!-- harnesskit:todo-checklist:start -->
补全本文件前请确认：
- 每条已确认事实都带有仓库证据路径或团队确认来源。
- 无法确认的内容保留 `[NEEDS CLARIFICATION: ...]`，不要把模板示例写成事实。
- facts 刷新后，按需运行 `$fill-agents`、`$fill-architecture`、`$fill-rules` 和 `$fill-skills`。
<!-- harnesskit:todo-checklist:end -->

## Project Identity

- **Project name**: HarnessKit
- **Project purpose**: Context Harness CLI/toolkit，用于在目标仓库初始化和维护 agent-facing context assets。
- **Primary audience**: 使用 HarnessKit 初始化目标仓库的开发者和维护 Context Harness 的 agent。
- **Evidence**: `README.md`, `pyproject.toml`, `src/harnesskit/`

## Tech Stack

| Category | Detected fact | Evidence | Confidence |
| --- | --- | --- | --- |
| Languages / runtimes | Python 3.11+ | `pyproject.toml` | high |
| Package managers | uv | `uv.lock`, `README.md`, `Makefile` | high |
| Frameworks / libraries | Typer, Rich, Jinja2 | `pyproject.toml`, `src/harnesskit/cli.py`, `src/harnesskit/init.py` | high |
| Build tools | Hatchling | `pyproject.toml` | high |

## Validation Entrypoints

| Kind | Command | Runner / binding | Evidence |
| --- | --- | --- | --- |
| Full verify | `make verify` | Makefile, agent verification skill | `Makefile`, `.agents/skills/code-change-verification/SKILL.md` |
| Test | `uv run pytest` | pre-commit, `make verify` | `.pre-commit-config.yaml`, `.agents/skills/code-change-verification/SKILL.md` |
| Lint | `uv run ruff check .` | pre-commit, `make verify` | `.pre-commit-config.yaml`, `.agents/skills/code-change-verification/SKILL.md` |
| Format check | `uv run ruff format --check .` | pre-commit, `make verify` | `.pre-commit-config.yaml`, `.agents/skills/code-change-verification/SKILL.md` |
| Build | `uv build` | pre-commit, `make verify` | `.pre-commit-config.yaml`, `.agents/skills/code-change-verification/SKILL.md` |
| Markdown links | `lychee './**/*.md'` | pre-commit, `make verify` | `.pre-commit-config.yaml`, `lychee.toml` |

## Repository Map Candidates

- `src/harnesskit/`: packaged CLI/runtime and linter.
- `templates/`: generated Context Harness assets copied into target repositories.
- `tests/`: pytest coverage for CLI/init behavior.
- `.agents/skills/`: local Codex skills used while maintaining this repository.
- `.harnesskit/rules/`: details files for rules listed in `RULES.md`.
- `harness-linter-poc/`: old linter POC/reference implementation, not the product entrypoint.

## Agent-Facing Assets

| Asset | Status | Evidence / notes |
| --- | --- | --- |
| `AGENTS.md` | exists | root agent guide |
| `ARCHITECTURE.md` | exists | repository map |
| `RULES.md` | exists | rules index |
| `.agents/skills/` | exists | local skills |
| `CLAUDE.md` | symlink | companion guide pointing at `AGENTS.md` |

## Rule / Guard Candidates

- Complete verification uses `make verify`.
- User-visible behavior changes require tests.
- Template changes are generated behavior and should be covered by init tests.
- `harnesskit lint` product behavior lives under `src/harnesskit/linter/`.

## Open Questions

- [NEEDS CLARIFICATION: future release and CI policy]
