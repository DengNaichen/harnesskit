# HarnessKit Harness Facts

本文件位于 `.harnesskit/facts.md`，是 `scan -> fill` 工作流的事实交接快照。`$scan-facts` 从仓库事实刷新本文件；`$fill-agents`、`$fill-architecture`、`$fill-practices`、`$fill-rules` 和 `$fill-skills` 消费本文件来更新对应 artifact。

本文件不是仓库事实本身的替代品。填充任何 agent-facing 文档前，仍应优先核对真实源码、清单、脚本、锁文件、hook 配置和现有文档。

<!-- harnesskit:todo-checklist:start -->
补全本文件前请确认：
- 每条已确认事实都带有仓库证据路径或团队确认来源。
- 每条事实按 `confirmed`、`candidate`、`absent` 或 `conflict` 标注状态；只有 confirmed facts 才能直接驱动硬规则或用户可见结论。
- 对需要后续填充的事实记录 target hint，例如 AGENTS、ARCHITECTURE、RULES、docs/practices、skills、validation runner 或 facts-only。
- 无法确认的内容保留 `[NEEDS CLARIFICATION: ...]`，不要把模板示例写成事实。
- facts 刷新后，按需运行 `$fill-agents`、`$fill-architecture`、`$fill-practices`、`$fill-rules` 和 `$fill-skills`。
<!-- harnesskit:todo-checklist:end -->

## Project Identity

- **Project name**: HarnessKit
- **Project purpose**: Context Harness CLI/toolkit，用于在目标仓库初始化和维护 agent-facing context assets。
- **Primary audience**: 使用 HarnessKit 初始化目标仓库的开发者和维护 Context Harness 的 agent。
- **Evidence**: `README.md`, `pyproject.toml`, `src/harnesskit/`

## Fact Quality Model

| Status | Meaning | Fill behavior |
| --- | --- | --- |
| confirmed | 源码、配置、脚本、测试、runner 或团队确认支持 | 可进入对应 artifact |
| candidate | 来自文档、惯例或间接线索，尚未核对实现 | 保留为待确认，不升级为硬规则 |
| absent | 已检查合理 evidence，未发现对应能力、runner 或配置 | 可用于说明未配置能力 |
| conflict | evidence source 不一致 | 进入漂移处理，不静默选择 |

| Fact | Status | Evidence | Target hint | Stale risk |
| --- | --- | --- | --- | --- |
| HarnessKit 是 Python 3.11+ Context Harness CLI/toolkit，PyPI 分发名是 `infharness`，console script 是 `harnesskit` | confirmed | `pyproject.toml`, `README.md`, `src/harnesskit/cli.py` | AGENTS, ARCHITECTURE | package metadata、entry point 或 release docs 变化时复核 |
| 完整验证入口是 `make verify` | confirmed | `Makefile`, `.agents/skills/code-change-verification/SKILL.md` | AGENTS, RULES, validation runner | Makefile 或 verification skill 变化时复核 |
| 当前未证实 typecheck、coverage gate、docs build 或 CI 完成条件 | absent | `pyproject.toml`, `Makefile`, `.pre-commit-config.yaml`, `.github/` 缺失 | AGENTS, RULES | 新增 runner、CI 或 docs build 配置时复核 |

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
- `docs/practices/`: guidance for coding, product sense, security, and reliability judgments.
- `.agents/skills/`: local Codex skills used while maintaining this repository.
- `.harnesskit/rules/`: optional historical details/background files; `RULES.md` no longer requires one details file per rule.
- `harness-linter-poc/`: old linter POC/reference implementation, not the product entrypoint.

## Agent-Facing Assets

| Asset | Status | Evidence / notes |
| --- | --- | --- |
| `AGENTS.md` | exists | root agent guide |
| `ARCHITECTURE.md` | exists | repository map |
| `RULES.md` | exists | rules index |
| `docs/practices/` | exists | judgment guidance, not hard rules |
| `.agents/skills/` | exists | local skills |
| `CLAUDE.md` | symlink | companion guide pointing at `AGENTS.md` |

## Rule / Guard Candidates

- Complete verification uses `make verify`.
- User-visible behavior changes require tests.
- Template changes are generated behavior and should be covered by init tests.
- `harnesskit lint` product behavior lives under `src/harnesskit/linter/`.
- Practices guide coding/product/security/reliability judgment; only clear hard constraints should be promoted into `RULES.md`.

## Open Questions

- [NEEDS CLARIFICATION: future release and CI policy]
