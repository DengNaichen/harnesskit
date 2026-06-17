---
name: scan-facts
description: Scan repository facts into .harnesskit/facts.md from verified evidence. Use when bootstrapping or refreshing Context Harness facts before filling AGENTS.md, ARCHITECTURE.md, RULES.md, or project-specific skill sections.
---

# Scan Facts

Use this skill to refresh [.harnesskit/facts.md](../../../.harnesskit/facts.md) from repository evidence. This skill is the only generated skill that should create or refresh the facts artifact.

## Inputs

Read the smallest useful set of repository-owned evidence:

- Existing guidance: [AGENTS.md](../../../AGENTS.md), [CLAUDE.md](../../../CLAUDE.md), [RULES.md](../../../RULES.md), [.agents/skills/](../../skills/) skill files, architecture notes, and relevant docs.
- Project identity: `README*`, product/design docs, package metadata, and top-level directory names.
- Tech stack facts: manifests, lockfiles, workspace files, source/test layout, tool config, CI/pre-commit config, and documented commands.
- Current state: `[NEEDS CLARIFICATION: ...]` placeholders, todo-checklist marker blocks, missing files, stale paths, or guidance that conflicts with repository files.

Ignore local/generated/vendor noise such as virtual environments, dependency folders, caches, build output, downloaded dependencies, and editor metadata unless the user explicitly asks about them.

## Workflow

1. Inspect repository facts before asking questions.
2. Prepare a short "candidate facts" confirmation message for the user before writing durable facts. Include:
   - project name;
   - project purpose;
   - primary audience when evident;
   - language/runtime/platform and key frameworks;
   - package/build/test/lint/format entrypoints;
   - important source, test, docs, specs, scripts, and config directories;
   - any high-impact uncertainty that needs human choice.
3. Ask the user to confirm or correct the candidate facts using a single-choice MCQ. If the current Codex surface supports a native single-choice UI, use it; otherwise, render the choices as text and wait for the user's letter or correction.
   - A. Confirm all candidate facts and write them.
   - B. Correct one or more facts before writing.
   - C. Skip writing durable facts for now.
   - D. Write only high-confidence repository facts and keep human-owned items as `[NEEDS CLARIFICATION: ...]`.
   If the user corrects a fact, treat the correction as user-confirmed evidence and record it as such.
4. Only after confirmation, record evidence-backed or user-confirmed facts in [.harnesskit/facts.md](../../../.harnesskit/facts.md).
5. Keep unresolved items as `[NEEDS CLARIFICATION: ...]` with a short note about what evidence is missing.
6. Do not update [AGENTS.md](../../../AGENTS.md), [ARCHITECTURE.md](../../../ARCHITECTURE.md), [RULES.md](../../../RULES.md), or other skills from this skill.
7. If [.harnesskit/facts.md](../../../.harnesskit/facts.md) is missing, recreate it using the same sections as the generated template.

## User Confirmation Protocol

Use a concise MCQ confirmation prompt like:

```text
I detected these candidate Harness facts. Please confirm before I write `.harnesskit/facts.md`.

1. Project name: ...
   Evidence: ...

2. Project purpose: ...
   Evidence: ...

3. Tech stack: ...
   Evidence: ...

4. Validation entrypoints: ...
   Evidence: ...

5. Important directories: ...
   Evidence: ...

Choose one:
A. Confirm all candidate facts and write them.
B. Correct one or more facts before writing.
C. Skip writing durable facts for now.
D. Write only high-confidence repository facts and keep human-owned items as `[NEEDS CLARIFICATION: ...]`.
```

If a native single-choice UI is available in the current Codex surface, present the four choices with that UI. If not, use the textual MCQ above. Then pause for the user's response. Do not silently write durable facts when the scan includes user-facing project identity, purpose, stack, validation commands, or important boundaries that a human can confirm.

If the user has explicitly asked for a non-interactive scan, or the current environment does not allow follow-up interaction, write high-confidence repository facts and keep all uncertain or human-owned facts as `[NEEDS CLARIFICATION: ...]`.

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
