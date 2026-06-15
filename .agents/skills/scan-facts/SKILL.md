---
name: scan-facts
description: Scan repository facts into .harnesskit/facts.md from verified evidence. Use when bootstrapping or refreshing Context Harness facts before filling AGENTS.md, ARCHITECTURE.md, RULES.md, or project-specific skill sections.
---

# Scan Facts

Use this skill to refresh `.harnesskit/facts.md` from repository evidence. This skill is the only generated skill that should create or refresh the facts artifact.

## Inputs

Read the smallest useful set of repository-owned evidence:

- Existing guidance: `AGENTS.md`, `CLAUDE.md`, `RULES.md`, `.agents/skills/*/SKILL.md`, architecture notes, and relevant docs.
- Project identity: `README*`, product/design docs, package metadata, and top-level directory names.
- Tech stack facts: manifests, lockfiles, workspace files, source/test layout, tool config, CI/pre-commit config, and documented commands.
- Current state: `[NEEDS CLARIFICATION: ...]` placeholders, todo-checklist marker blocks, missing files, stale paths, or guidance that conflicts with repository files.

Ignore local/generated/vendor noise such as virtual environments, dependency folders, caches, build output, downloaded dependencies, and editor metadata unless the user explicitly asks about them.

## Workflow

1. Inspect repository facts before asking questions.
2. Record only evidence-backed facts in `.harnesskit/facts.md`.
3. Keep uncertain items as `[NEEDS CLARIFICATION: ...]` with a short note about what evidence is missing.
4. Do not update `AGENTS.md`, `ARCHITECTURE.md`, `RULES.md`, or other skills from this skill.
5. If `.harnesskit/facts.md` is missing, recreate it using the same sections as the generated template.

## Fact Model

Capture:

- Project identity and audience.
- Languages, runtimes, package managers, frameworks, build tools, test frameworks, linters, formatters, and type checkers.
- Validation entrypoints: setup, full verify, test, lint, format check, typecheck, coverage, build, docs, link check, hook suite, and CI/platform gates.
- Repository map candidates: important source, test, docs, config, generated-output, and tooling paths.
- Agent-facing assets and installed local skills.
- Rule and Validation candidates with runner evidence.
- Open questions that repository facts cannot settle.

## Boundaries

- Do not invent commands, tools, URLs, CI, release processes, PR templates, architecture, or compatibility policy.
- Do not treat generic template examples as evidence that the target repository supports a tool.
- Do not mark a Validation as deterministic unless a command, script, hook, CI task, or platform setting provides clear pass/fail evidence.
- Do not run runtime test suites for guidance-only refreshes unless the refresh also changes runtime code, templates, build/test config, or generated behavior.
