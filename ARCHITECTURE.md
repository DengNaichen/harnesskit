# Architecture

This file is a coarse repository map for HarnessKit. It helps agents and
contributors find the right part of the codebase before editing. It is not a
workflow spec, API reference, or detailed design document.

The Markdown links below are the map. A path with
`<!-- harnesskit:coverage=direct-children -->` asks the linter to verify that
its direct children are also represented as links in this document.

## Top-Level Map

- [`src/harnesskit/`](src/harnesskit/) <!-- harnesskit:coverage=direct-children -->: TODO: placeholder responsibility.
  - [`__init__.py`](src/harnesskit/__init__.py): TODO: placeholder responsibility.
  - [`cli.py`](src/harnesskit/cli.py): TODO: placeholder responsibility.
  - [`init.py`](src/harnesskit/init.py): TODO: placeholder responsibility.
- [`templates/`](templates/): TODO: placeholder responsibility.
- [`tests/`](tests/): TODO: placeholder responsibility.
- [`harness-linter-poc/`](harness-linter-poc/) <!-- harnesskit:coverage=direct-children -->: TODO: placeholder responsibility.
  - [`harness_lint.py`](harness-linter-poc/harness_lint.py): TODO: placeholder responsibility.
  - [`core/`](harness-linter-poc/core/) <!-- harnesskit:coverage=direct-children -->: TODO: placeholder responsibility.
    - [`__init__.py`](harness-linter-poc/core/__init__.py): TODO: placeholder responsibility.
    - [`constants.py`](harness-linter-poc/core/constants.py): TODO: placeholder responsibility.
    - [`issues.py`](harness-linter-poc/core/issues.py): TODO: placeholder responsibility.
    - [`markdown.py`](harness-linter-poc/core/markdown.py): TODO: placeholder responsibility.
    - [`models.py`](harness-linter-poc/core/models.py): TODO: placeholder responsibility.
  - [`rules/`](harness-linter-poc/rules/) <!-- harnesskit:coverage=direct-children -->: TODO: placeholder responsibility.
    - [`__init__.py`](harness-linter-poc/rules/__init__.py): TODO: placeholder responsibility.
    - [`architecture.py`](harness-linter-poc/rules/architecture.py): TODO: placeholder responsibility.
    - [`config.py`](harness-linter-poc/rules/config.py): TODO: placeholder responsibility.
    - [`core.py`](harness-linter-poc/rules/core.py): TODO: placeholder responsibility.
    - [`harness_markdown.py`](harness-linter-poc/rules/harness_markdown.py): TODO: placeholder responsibility.
    - [`project.py`](harness-linter-poc/rules/project.py): TODO: placeholder responsibility.
    - [`skills.py`](harness-linter-poc/rules/skills.py): TODO: placeholder responsibility.
    - [`tech_stack.py`](harness-linter-poc/rules/tech_stack.py): TODO: placeholder responsibility.
    - [`verification.py`](harness-linter-poc/rules/verification.py): TODO: placeholder responsibility.
  - [`testing_helpers.py`](harness-linter-poc/testing_helpers.py): TODO: placeholder responsibility.
  - [`test_architecture_rules.py`](harness-linter-poc/test_architecture_rules.py): TODO: placeholder responsibility.
  - [`test_cli.py`](harness-linter-poc/test_cli.py): TODO: placeholder responsibility.
  - [`test_config_rules.py`](harness-linter-poc/test_config_rules.py): TODO: placeholder responsibility.
  - [`test_markdown_rules.py`](harness-linter-poc/test_markdown_rules.py): TODO: placeholder responsibility.
  - [`test_project_rules.py`](harness-linter-poc/test_project_rules.py): TODO: placeholder responsibility.
  - [`test_skill_rules.py`](harness-linter-poc/test_skill_rules.py): TODO: placeholder responsibility.
  - [`test_tech_stack_rules.py`](harness-linter-poc/test_tech_stack_rules.py): TODO: placeholder responsibility.
  - [`test_verification_rules.py`](harness-linter-poc/test_verification_rules.py): TODO: placeholder responsibility.
- [`.agents/skills/`](.agents/skills/): TODO: placeholder responsibility.
- [`docs/`](docs/): TODO: placeholder responsibility.

## Key Files

- [`pyproject.toml`](pyproject.toml): TODO: placeholder responsibility.
- [`AGENTS.md`](AGENTS.md): TODO: placeholder responsibility.
- [`RULES.md`](RULES.md): TODO: placeholder responsibility.
- [`README.md`](README.md): TODO: placeholder responsibility.

## Generated Target-Repository Assets

HarnessKit installs or maintains these kinds of files in target repositories:

- `AGENTS.md`: TODO: placeholder responsibility.
- `RULES.md`: TODO: placeholder responsibility.
- `CLAUDE.md`: TODO: placeholder responsibility.
- `.harnesskit/config.json`: TODO: placeholder responsibility.
- `.agents/skills/*/SKILL.md`: TODO: placeholder responsibility.

## Current Package Shape

The current runtime package is intentionally small:

- `cli.py`: TODO: placeholder responsibility.
- `init.py`: TODO: placeholder responsibility.
- `__init__.py`: TODO: placeholder responsibility.

As the package grows, this map should stay coarse. Add new modules here when
they change where an agent should look first, not when every helper function
moves.

## Related Documents

- [`README.md`](README.md): TODO: placeholder responsibility.
- [`AGENTS.md`](AGENTS.md): TODO: placeholder responsibility.
- [`docs/DESIGN.md`](docs/DESIGN.md): TODO: placeholder responsibility.
- [`docs/ROADMAP.md`](docs/ROADMAP.md): TODO: placeholder responsibility.
