---
name: scan-stack
description: Scan repository stack and context facts from verified evidence. Use when detecting tech stack, validation entrypoints, architecture maps, local agent skills, when turning those findings into AGENTS.md/RULES.md guidance, or when clarifying rule/tech-stack decisions without inventing unsupported commands or workflows.
---

# Scan Stack

Use this skill to scan repository facts and turn stable findings into practical agent guidance. The default durable output is an updated `AGENTS.md` as the top-level router for agent-facing context; when `RULES.md` exists or the task asks for rules, also complete `RULES.md` from the same evidence. Before writing durable guidance, ask a small MCQ-style checkpoint so the user can choose how rules and tech-stack findings should be applied. A separate scan report is optional and only created when the user asks for one.

## Inputs

Read the smallest useful set of repository-owned evidence:

- Existing guidance: `AGENTS.md`, `CLAUDE.md`, `RULES.md`, `.agents/skills/*/SKILL.md`, architecture notes, and relevant docs.
- Clarification workflow evidence: `.specify/`, SpecKit commands/templates/checklists, planning docs, and existing clarification records.
- Project identity: `README*`, product/design docs, package metadata, and top-level directory names.
- Tech stack facts: manifests, lockfiles, workspace files, source/test layout, tool config, CI/pre-commit config, and documented commands.
- Current state: template placeholders, TODO checklist blocks, missing files, stale paths, or guidance that conflicts with repository files.

Ignore local/generated/vendor noise such as virtual environments, dependency folders, caches, build output, downloaded dependencies, and editor metadata unless the user explicitly asks about them.

## What This Skill Does

1. Build an evidence-backed picture of the repository:
   - what the project is;
   - main languages, runtimes, package managers, frameworks, and important tools;
  - architecture map location and a few high-value entry paths;
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
4. Ask an MCQ-style checkpoint before writing durable guidance:
   - if SpecKit assets exist, read the local clarify/checklist/template instructions and reuse the repository's established question and answer format;
   - always ask at least one lightweight MCQ before updating `AGENTS.md`, `RULES.md`, or related durable guidance, unless the user explicitly requested a non-interactive/defaults-only run;
   - prioritize team decisions that repository evidence cannot settle, such as enabling typecheck, coverage thresholds, single verification wrappers, branch protection expectations, or review-only rules;
   - if no material decision is unresolved, ask the user to choose the update posture, such as apply all evidence-backed defaults, update only high-confidence facts, or keep uncertain items as `NEEDS CLARIFICATION`;
   - keep the checkpoint small, usually 1-5 questions, with a recommended option and the consequence of each choice;
   - do not ask the user to confirm facts already proven by manifests, lockfiles, scripts, CI, hooks, or source layout.
5. Write concise guidance:
   - treat `AGENTS.md` as the top-level router, not the project knowledge base;
   - keep `AGENTS.md` focused on policy, context routing, skill triggers, validation entrypoints, and drift handling;
   - point directory responsibility and module boundaries to `ARCHITECTURE.md` instead of copying a full directory map;
   - when `RULES.md` exists, fill rule status, evidence, agent contract, validation type, validation, and command bindings from the detection model;
   - leave unsupported or unverified rules as `NEEDS CLARIFICATION`, `N/A`, or not configured instead of enabling them from examples;
   - route to skills by trigger and path, not by copying skill bodies;
   - keep product background and long design discussion in README/docs;
   - preserve unresolved uncertainty as short `TODO:` notes or `NEEDS CLARIFICATION` entries.
6. Keep companion guidance aligned:
   - prefer `CLAUDE.md -> AGENTS.md` as a symlink when the repository supports symlinks;
   - otherwise make `CLAUDE.md` a short pointer to `AGENTS.md`.

## Fact Model

Use this internal model while collecting facts. It does not need to be written to disk unless the user asks for a scanner artifact.

- Detection categories: languages, runtimes, package managers, frameworks, build tools, test frameworks, linters, formatters, type checkers, architecture maps, key entry paths, local skills.
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
- Rule candidates: map validation and repository facts to `RULES.md` entries, including single verification entrypoint, tests for new behavior, real test entrypoint, naming style, dependency sync, context drift, lockfiles, typecheck, coverage, lint, format check, build, hook suite, branch protection, and architecture map.
- Clarification candidates: record the checkpoint question, undecidable decision or update posture, evidence gap if any, affected output fields, MCQ options, recommended option, and how each answer changes `AGENTS.md`, `RULES.md`, or related documentation.
- Needs verification: record missing commands, multiple competing lockfiles, README commands without matching scripts, CI commands that differ from local commands, or tools present without a runnable entrypoint.
- AGENTS guidance shape: record only the routing facts that help an agent choose where to look or what to run. Put full directory maps in `ARCHITECTURE.md`, rule details in `RULES.md`, and procedural details in skills.

## Outputs

Produce only the artifacts the task calls for:

- Primary output: updated `AGENTS.md` as a top-level router for context, rules, skills, and verification entrypoints.
- Primary output when present or requested: updated `RULES.md` with evidence-backed rule status, validation type, validation, and project command bindings.
- Primary interaction before durable writes: MCQ-style checkpoint questions; after the user answers, write the selected decisions back into the relevant guidance or leave unanswered items as `NEEDS CLARIFICATION`.
- Optional output: updated `CLAUDE.md` pointer or symlink.
- Optional output: updated `RULES.md` or related documentation for uncertain facts, reusable commands, or follow-up notes.
- Optional output: short final summary listing changed sections, unresolved TODOs, and verification performed or intentionally skipped.

Do not create a separate tech stack report by default. If the user asks for one, keep it temporary or place it where the repository already stores reports.

## Boundaries

- Do not invent commands, tools, URLs, CI, release processes, PR templates, architecture, or compatibility policy.
- Do not turn `AGENTS.md` into a duplicated architecture map, rules catalog, or skill body.
- Do not treat generic template examples as evidence that the target repository supports a tool.
- Do not treat generic SpecKit behavior as evidence; when SpecKit is present, follow the repository's local SpecKit assets.
- Do not ask clarification questions for facts that direct repository evidence already answers.
- Do not skip the MCQ checkpoint when writing durable guidance unless the user explicitly requested a non-interactive/defaults-only run.
- Do not block useful guidance on low-risk uncertainty; record it as `NEEDS CLARIFICATION` or in related documentation.
- Do not turn optional rules into required rules without repository evidence.
- Do not mark a validation as deterministic unless a command, script, hook, CI task, or platform setting provides a clear pass/fail signal.
- Do not record transient dependency versions unless they affect operations or compatibility.
- Do not run runtime test suites for guidance-only edits unless the edit also changes runtime code, templates, build/test config, or generated behavior.
