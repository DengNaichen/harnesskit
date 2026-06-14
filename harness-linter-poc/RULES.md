# Harness Linter POC Rules

This file describes the first rule set for the standalone Harness Linter POC.

## Rule Groups

### Config

- `config.missing`: `.harnesskit/config.json` must exist.
- `config.invalid_json`: `.harnesskit/config.json` must parse as JSON.
- `config.not_object`: config must be a JSON object.
- `config.schema_version`: `schema_version` must match the supported schema.
- `config.default_integration`: `default_integration` must be supported.
- `config.installed_integrations`: `installed_integrations` must be a list of strings.
- `config.installed_integration.unsupported`: every installed integration must be supported.

### Core Files

- `core.missing`: required harness files must exist.
- `core.empty`: required harness files must not be empty.
- `claude.pointer`: `CLAUDE.md` should point readers to `AGENTS.md`.
- `claude.broken_symlink`: `CLAUDE.md` symlink targets must exist.

### Codex Integration

- `codex.skill.missing`: installed Codex harness skills must exist.
- `codex.skill.empty`: installed Codex harness skills must not be empty.

### Skills

- `skill.frontmatter.missing`: every skill `SKILL.md` must start with frontmatter.
- `skill.frontmatter.name`: skill frontmatter must include `name`.
- `skill.frontmatter.description`: skill frontmatter must include `description`.
- `skill.reference.missing`: `$skill-name` references in `AGENTS.md` must point to an installed `.agents/skills/<skill-name>/SKILL.md`.

### Markdown

- `markdown.link.missing`: local Markdown link targets inside harness files must exist.
- `markdown.todo_checklist.unpaired`: `harnesskit:todo-checklist` start and end markers must be paired and ordered.
- `markdown.tech_stack.unpaired`: `harnesskit:tech-stack` start and end markers must be paired and ordered.
- `markdown.verification.unpaired`: `harnesskit:verification` start and end markers must be paired and ordered.
- `external.markdownlint`: optional external markdownlint run failed.
- `external.markdownlint.missing`: optional external markdownlint was requested but no supported binary was installed.

### Tech Stack

- `tech_stack.mismatch`: values declared inside a `harnesskit:tech-stack` block must match repository facts detected from configuration, lock files, and tests.

### Verification

- `verification.block_missing`: verification docs must use a `harnesskit:verification` block when repository facts expose declared verification tools.
- `verification.tool_not_documented`: tool dependencies such as Ruff must be documented inside each `harnesskit:verification` block as active verification gates or explicitly inactive.

## Non-Goals

- No application source linting.
- No application source formatting.
- No automatic fixes in this POC.
- No LLM-based judgment.
