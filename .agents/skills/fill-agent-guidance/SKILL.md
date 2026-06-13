---
name: fill-agent-guidance
description: Create or update repository agent guidance files. Use when initializing or revising AGENTS.md, removing template placeholders, routing repo-local skills, keeping CLAUDE.md aligned with AGENTS.md, or turning discovered repository facts into concise agent policy.
---

# Fill Agent Guidance

## Purpose

Update `AGENTS.md` from repository facts, not from generic templates. Keep the file short, policy-oriented, and useful to future coding agents.

## Workflow

1. Inspect the repository before writing:
   - Read root build manifests such as `pom.xml`, `package.json`, `pyproject.toml`, `go.mod`, or equivalents.
   - List top-level modules and important source/test/resource directories.
   - Inspect existing `.agents/skills/*/SKILL.md` files and any current `AGENTS.md`, `CLAUDE.md`, or architecture notes.
2. Write `AGENTS.md` as repository policy and routing:
   - State what the project is, its main technology stack, and its important modules.
   - Route to repo-local skills by saying when to use them and where to read full instructions.
   - Do not copy full skill bodies into `AGENTS.md`.
   - Do not invent commands, tools, URLs, release process, CI, or architecture details that are not present in the repository.
3. Handle placeholders deliberately:
   - Replace placeholders only when the value is supported by repository evidence.
   - Keep unresolved values as concise `TODO:` notes or explicitly scoped placeholders.
   - Report remaining placeholders in the final handoff.
4. Keep `CLAUDE.md` aligned:
   - Prefer `CLAUDE.md -> AGENTS.md` as a symlink when the repository supports symlinks.
   - If symlinks are not appropriate, make `CLAUDE.md` a short pointer to `AGENTS.md` instead of duplicating content.
5. Preserve separation of concerns:
   - `AGENTS.md` defines project policy, triggering conditions, and navigation.
   - Skill files define execution details.
   - Architecture documents define module boundaries and data flow.

## Output Expectations

- Summarize the sections changed in `AGENTS.md`.
- Call out any unresolved TODOs or placeholders.
- Mention whether `CLAUDE.md` is a symlink, pointer file, or duplicated file.
- Do not run runtime test suites unless the guidance update also changes code, build files, or generated artifacts.
