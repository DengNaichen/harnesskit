# Architecture

This file is a coarse repository map for HarnessKit. It helps agents and
contributors find the right part of the codebase before editing. It is not a
workflow spec, API reference, or detailed design document.

<!-- harnesskit:architecture-map:start -->
- path: src/harnesskit/
  coverage: direct-children
- path: src/harnesskit/__init__.py
  coverage: file
- path: src/harnesskit/cli.py
  coverage: file
- path: src/harnesskit/init.py
  coverage: file
- path: templates/
  coverage: directory
- path: tests/
  coverage: directory
- path: harness-linter-poc/
  coverage: direct-children
- path: harness-linter-poc/harness_lint.py
  coverage: file
- path: harness-linter-poc/harness_lint_rules/
  coverage: direct-children
- path: harness-linter-poc/harness_lint_rules/__init__.py
  coverage: file
- path: harness-linter-poc/harness_lint_rules/architecture.py
  coverage: file
- path: harness-linter-poc/harness_lint_rules/config.py
  coverage: file
- path: harness-linter-poc/harness_lint_rules/constants.py
  coverage: file
- path: harness-linter-poc/harness_lint_rules/core.py
  coverage: file
- path: harness-linter-poc/harness_lint_rules/issues.py
  coverage: file
- path: harness-linter-poc/harness_lint_rules/markdown.py
  coverage: file
- path: harness-linter-poc/harness_lint_rules/models.py
  coverage: file
- path: harness-linter-poc/harness_lint_rules/project.py
  coverage: file
- path: harness-linter-poc/harness_lint_rules/skills.py
  coverage: file
- path: harness-linter-poc/harness_lint_rules/tech_stack.py
  coverage: file
- path: harness-linter-poc/harness_lint_rules/verification.py
  coverage: file
- path: harness-linter-poc/test_harness_lint.py
  coverage: file
- path: .agents/skills/
  coverage: directory
- path: docs/
  coverage: directory
- path: pyproject.toml
  coverage: file
- path: AGENTS.md
  coverage: file
- path: README.md
  coverage: file
- path: candidate.md
  coverage: file
<!-- harnesskit:architecture-map:end -->

## Top-Level Map

- [`src/harnesskit/`](src/harnesskit/): Python package and CLI implementation.
- [`templates/`](templates/): Context Harness assets copied or rendered into target repositories.
- [`tests/`](tests/): pytest coverage for initialization and user-visible CLI behavior.
- [`harness-linter-poc/`](harness-linter-poc/): standalone proof of concept for deterministic harness drift checks; [`harness_lint_rules/`](harness-linter-poc/harness_lint_rules/) contains extracted rule modules and shared lint models.
- [`.agents/skills/`](.agents/skills/): repository-local Codex skills used while working on this repository.
- [`docs/`](docs/): product design notes, roadmap, and research references.

## Harness Linter POC Modules

- [`harness_lint.py`](harness-linter-poc/harness_lint.py): CLI entry point, report rendering, and rule orchestration.
- [`harness_lint_rules/config.py`](harness-linter-poc/harness_lint_rules/config.py): `.harnesskit/config.json` checks.
- [`harness_lint_rules/core.py`](harness-linter-poc/harness_lint_rules/core.py): required harness files, Claude pointer, and installed integration assets.
- [`harness_lint_rules/skills.py`](harness-linter-poc/harness_lint_rules/skills.py): skill frontmatter and `$skill-name` reference checks.
- [`harness_lint_rules/markdown.py`](harness-linter-poc/harness_lint_rules/markdown.py): Markdown collection, links, marker blocks, and optional external markdownlint.
- [`harness_lint_rules/architecture.py`](harness-linter-poc/harness_lint_rules/architecture.py): architecture map coverage checks.
- [`harness_lint_rules/tech_stack.py`](harness-linter-poc/harness_lint_rules/tech_stack.py): repository fact detection and tech-stack block checks.
- [`harness_lint_rules/verification.py`](harness-linter-poc/harness_lint_rules/verification.py): verification documentation drift checks.
- [`harness_lint_rules/models.py`](harness-linter-poc/harness_lint_rules/models.py): shared report and block models.
- [`harness_lint_rules/issues.py`](harness-linter-poc/harness_lint_rules/issues.py): issue construction and path display helpers.

## Key Files

- [`src/harnesskit/cli.py`](src/harnesskit/cli.py): Typer command surface for `harnesskit init` and `harnesskit integration ...`.
- [`src/harnesskit/init.py`](src/harnesskit/init.py): project initialization, template copying/rendering, integration installation, and `.harnesskit/config.json` writing.
- [`pyproject.toml`](pyproject.toml): package metadata, dependency groups, build backend, script entry point, and tool configuration.
- [`AGENTS.md`](AGENTS.md): agent operating guide for this repository.
- [`README.md`](README.md): product overview, MVP scope, and CLI usage.
- [`candidate.md`](candidate.md): temporary holding area for observations before they become stable guidance.

## Generated Target-Repository Assets

HarnessKit installs or maintains these kinds of files in target repositories:

- `AGENTS.md`: primary agent guidance entry point.
- `CLAUDE.md`: pointer to `AGENTS.md` for Claude-facing clients.
- `candidate.md`: temporary holding area for project-local observations.
- `.harnesskit/config.json`: minimal HarnessKit installation metadata.
- `.agents/skills/*/SKILL.md`: Codex skills installed by the Codex integration.

## Current Package Shape

The current runtime package is intentionally small:

- `cli.py` owns command parsing, user-visible command names, and terminal output.
- `init.py` owns the initialization behavior behind the CLI commands.
- `__init__.py` exposes package metadata.

As the package grows, this map should stay coarse. Add new modules here when
they change where an agent should look first, not when every helper function
moves.

## Related Documents

- [`README.md`](README.md): explains what HarnessKit is and why it exists.
- [`AGENTS.md`](AGENTS.md): explains how agents should work in this repository.
- [`docs/DESIGN.md`](docs/DESIGN.md): records design discussion and models.
- [`docs/ROADMAP.md`](docs/ROADMAP.md): tracks product direction.
