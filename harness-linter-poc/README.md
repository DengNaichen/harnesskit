# Harness Linter POC

This folder is a standalone proof of concept for a HarnessKit Harness Linter.
It does not modify `src/harnesskit/`, does not register a CLI command, and does not change existing tests.

## Scope

The linter only checks Context Harness assets created or maintained by HarnessKit.
It does not lint or format the target project's application code.

Current checks:

- `.harnesskit/config.json` exists, is valid JSON, and uses `schema_version: 1`.
- `AGENTS.md` and `CLAUDE.md` exist and are not empty.
- `CLAUDE.md` points to `AGENTS.md`, either as a symlink or by referencing it.
- Installed Codex harness skills exist:
  - `.agents/skills/harnesskit-audit/SKILL.md`
  - `.agents/skills/harnesskit-refresh/SKILL.md`
  - `.agents/skills/harnesskit-explain/SKILL.md`
- Every `.agents/skills/*/SKILL.md` has minimal frontmatter with `name` and `description`.
- `$skill-name` references in `AGENTS.md` point to installed local skills.
- Local Markdown links inside harness files point to existing files.
- `harnesskit:todo-checklist` start/end markers are paired.
- Optional `harnesskit:tech-stack` blocks match repository facts from config, lock files, and tests.
- Verification docs use `harnesskit:verification` blocks for machine-readable completion gates.
- Declared tool dependencies such as Ruff are documented inside each verification block as active verification gates or explicitly inactive.

Example tech stack block:

```markdown
<!-- harnesskit:tech-stack:start -->
- Language: Python 3.11+
- Package manager: uv
- CLI: Typer
- Terminal output: Rich
- Templates: Jinja2
- Build backend: Hatchling
- Tests: pytest
<!-- harnesskit:tech-stack:end -->
```

Example verification block:

```markdown
<!-- harnesskit:verification:start -->
- Markdown links: lychee './**/*.md'
- Tests: uv run pytest
- Python lint: uv run ruff check .
<!-- harnesskit:verification:end -->
```

If an installed tool is intentionally not part of the completion gate, declare it explicitly:

```markdown
<!-- harnesskit:verification:start -->
- Tests: uv run pytest
- Python lint: Ruff installed, inactive
<!-- harnesskit:verification:end -->
```

Optional integration:

- `--external-markdownlint` will call `markdownlint-cli2` or `markdownlint` when either tool is installed.

## Usage

```bash
python harness-linter-poc/harness_lint.py /path/to/project
python harness-linter-poc/harness_lint.py /path/to/project --json
uv run pytest harness-linter-poc/test_harness_lint.py
```

Demo fixture:

```bash
python harness-linter-poc/harness_lint.py harness-linter-poc/fixtures/valid
python harness-linter-poc/harness_lint.py harness-linter-poc/fixtures/valid --json
```

Exit codes:

- `0`: no errors
- `1`: one or more lint errors
- `2`: invalid invocation or unexpected crash

## Product Notes

This POC is intentionally conservative. It is a Harness Preservation tool, not a Harness Evolution system.
It should help keep an installed harness present, readable, and internally consistent without taking over the target repository's code style.
