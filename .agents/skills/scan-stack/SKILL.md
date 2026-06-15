---
name: scan-stack
description: Scan repository stack and context facts from verified evidence. Use when detecting tech stack, validation entrypoints, key directories, local agent skills, or when turning those findings into AGENTS.md guidance without inventing unsupported commands or workflows.
---

# Scan Stack

Use this skill to scan repository facts and turn stable findings into practical agent guidance. The default durable output is an updated `AGENTS.md`; a separate scan report is optional and only created when the user asks for one.

## Inputs

Read the smallest useful set of repository-owned evidence:

- Existing guidance: `AGENTS.md`, `CLAUDE.md`, `.agents/skills/*/SKILL.md`, architecture notes, and relevant docs.
- Project identity: `README*`, product/design docs, package metadata, and top-level directory names.
- Tech stack facts: manifests, lockfiles, workspace files, source/test layout, tool config, CI/pre-commit config, and documented commands.
- Current state: template placeholders, TODO checklist blocks, missing files, stale paths, or guidance that conflicts with repository files.

Ignore local/generated/vendor noise such as virtual environments, dependency folders, caches, build output, downloaded dependencies, and editor metadata unless the user explicitly asks about them.

## What This Skill Does

1. Build an evidence-backed picture of the repository:
   - what the project is;
   - main languages, runtimes, package managers, frameworks, and important tools;
   - important source, test, template, docs, and config paths;
   - available validation commands and where they are configured;
   - local skills and when agents should use them.
2. Record facts in a lightweight detection model before writing:
   - detections: category, name, status, confidence, and evidence;
   - validation entrypoints: kind, command, source, status, and evidence;
   - needs verification: missing, conflicting, stale, or indirect evidence.
3. Filter and rank facts:
   - high confidence: manifest/config/source layout/commands agree;
   - medium confidence: one strong source exists but entrypoints or commands are not confirmed;
   - low confidence: docs-only, example-only, or extension-only signal;
   - reject: evidence comes only from ignored, generated, local, vendored, or downloaded content.
4. Write concise guidance:
   - keep `AGENTS.md` focused on policy, routing, commands, and navigation;
   - route to skills by trigger and path, not by copying skill bodies;
   - keep product background and long design discussion in README/docs;
   - preserve unresolved uncertainty as short `TODO:` notes or `candidate.md` entries.
5. Keep companion guidance aligned:
   - prefer `CLAUDE.md -> AGENTS.md` as a symlink when the repository supports symlinks;
   - otherwise make `CLAUDE.md` a short pointer to `AGENTS.md`.

## Fact Model

Use this internal model while collecting facts. It does not need to be written to disk unless the user asks for a scanner artifact.

- Detection categories: languages, runtimes, package managers, frameworks, build tools, test frameworks, linters, formatters, type checkers, key directories, local skills.
- Detection statuses:
  - `detected`: direct repository evidence exists.
  - `inferred`: evidence is nearby and plausible, but the exact command or behavior was not verified.
  - `needs verification`: evidence is incomplete, conflicting, stale, or indirect.
- Confidence:
  - `high`: manifest, lockfile, tool config, source layout, and/or configured commands agree.
  - `medium`: one strong source exists, such as a dependency, script, or CI command.
  - `low`: README mention, docs snippet, example file, or extension-only signal.
- Evidence format: record the path and the reason, for example `pyproject.toml: [tool.ruff] present` or `.pre-commit-config.yaml: hook entry runs pytest`.
- Validation entrypoints: record `kind` such as setup, lint, format, typecheck, test, build, docs, link-check, or full verification; include the exact command only when supported by repository evidence.
- Needs verification: record missing commands, multiple competing lockfiles, README commands without matching scripts, CI commands that differ from local commands, or tools present without a runnable entrypoint.

## Outputs

Produce only the artifacts the task calls for:

- Primary output: updated `AGENTS.md`.
- Optional output: updated `CLAUDE.md` pointer or symlink.
- Optional output: updated `candidate.md` for uncertain facts, reusable commands, or follow-up notes.
- Optional output: short final summary listing changed sections, unresolved TODOs, and verification performed or intentionally skipped.

Do not create a separate tech stack report by default. If the user asks for one, keep it temporary or place it where the repository already stores reports.

## Boundaries

- Do not invent commands, tools, URLs, CI, release processes, PR templates, architecture, or compatibility policy.
- Do not treat generic template examples as evidence that the target repository supports a tool.
- Do not record transient dependency versions unless they affect operations or compatibility.
- Do not run runtime test suites for guidance-only edits unless the edit also changes runtime code, templates, build/test config, or generated behavior.
