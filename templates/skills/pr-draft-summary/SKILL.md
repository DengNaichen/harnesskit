---
name: pr-draft-summary
description: Create the required PR-ready summary block, branch suggestion, title, and draft description. Use in the final handoff after moderate-or-larger changes to runtime code, tests, examples, build/test configuration, or docs with behavior impact; skip only for trivial or conversation-only tasks, repo-meta/doc-only tasks without behavior impact, or when the user explicitly says not to include the PR draft block.
---

# PR Draft Summary

## Purpose
Produce the PR-ready summary required in this repository after substantive code work is complete: a concise summary plus a PR-ready title and draft description that begins with "This pull request <verb> ...". The block should be ready to paste into a PR.

## When to Trigger

<!-- harnesskit:todo-checklist:start -->
Before adjusting this section:
- Match trigger rules to the repository's real review and release expectations.
- Keep skip cases explicit for docs-only, metadata-only, or conversation-only work.
- Do not require a PR block for workflows the repository does not use.
<!-- harnesskit:todo-checklist:end -->

- The task for this repo is finished (or ready for review) and it touched runtime code, tests, examples, docs with behavior impact, or build/test configuration.
- Treat this as the default final handoff step for substantive code work. Run it after any required verification or changeset work and before sending the "work complete" response.
- Skip only for trivial or conversation-only tasks, repo-meta/doc-only tasks without behavior impact, or when the user explicitly says not to include the PR draft block.

## Inputs to Collect Automatically (do not ask the user)

<!-- harnesskit:todo-checklist:start -->
Before adjusting this section:
- Verify branch, release tag, base reference, and hosting assumptions from repository evidence.
- Replace generic category signals with this repository's actual runtime, test, template, docs, and config paths.
- Remove commands that cannot run in the repository's normal environment.
<!-- harnesskit:todo-checklist:end -->

- Current branch: `git rev-parse --abbrev-ref HEAD`.
- Working tree: `git status -sb`.
- Untracked files: `git ls-files --others --exclude-standard`.
- Changed files: `git diff --name-only` (unstaged) and `git diff --name-only --cached` (staged); sizes via `git diff --stat` and `git diff --stat --cached`.
- Latest release tag, when available: `LATEST_RELEASE_TAG=$(git describe --tags --abbrev=0 2>/dev/null || true)`.
- Base reference:
  - Prefer the branch upstream: `BASE_REF=$(git rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>/dev/null || true)`.
  - If there is no upstream, try the remote default branch: `BASE_REF=${BASE_REF:-$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null || true)}`.
  - If a base reference exists, compute the base commit: `BASE_COMMIT=$(git merge-base --fork-point "$BASE_REF" HEAD 2>/dev/null || git merge-base "$BASE_REF" HEAD 2>/dev/null || true)`.
- Commits ahead of the base fork point, when available: `test -n "$BASE_COMMIT" && git log --oneline --no-merges ${BASE_COMMIT}..HEAD`.
- Category signals for a typical repository; adjust from local evidence instead of assuming every path exists:
  - Runtime or product behavior: `src/**`, `app/**`, `lib/**`, `packages/**`, `cmd/**`, `internal/**`, `server/**`, `client/**`.
  - Tests: `test/**`, `tests/**`, `spec/**`, `__tests__/**`.
  - User-facing examples, fixtures, templates, or generated assets: `examples/**`, `fixtures/**`, `templates/**`.
  - Build, packaging, dependency, or CI configuration: package/build manifests, lockfiles, workflow files, Dockerfiles, Makefiles, and tool config files.
  - Documentation with behavior impact: `README*`, `CHANGELOG*`, `docs/**`, migration guides, API docs.
  - Agent or repository policy metadata: `AGENTS.md`, `.agents/**`, other local agent guidance files.

## Workflow
1) Run the commands above without asking the user. If `BASE_REF`, `BASE_COMMIT`, or `LATEST_RELEASE_TAG` cannot be discovered, keep going and state the uncertainty only when it affects the PR summary.
2) If there are no staged/unstaged/untracked changes and either no `BASE_COMMIT` or no commits ahead of `${BASE_COMMIT}`, reply briefly that no code changes were detected and skip emitting the PR block.
3) Infer change type from touched paths and diff content; classify as feature, fix, refactor, or docs-with-impact. Flag backward-compatibility risk only when the diff changes released public APIs, external config, persisted data, serialized state, or wire protocols. Judge that risk against `LATEST_RELEASE_TAG` when available, or against documented compatibility policy when no tag exists.
4) Summarize changes in 1–3 short sentences using the key paths (top 5) and `git diff --stat` output; explicitly call out untracked files because `--stat` does not include them. If the working tree is clean but there are commits ahead of `${BASE_COMMIT}`, summarize using those commit messages.
5) Choose the lead verb for the description: feature → `adds`, bug fix → `fixes`, refactor/perf → `improves` or `updates`, docs-only → `updates`.
6) Suggest a branch name. If already off the default branch, keep it; otherwise propose `feat/<slug>`, `fix/<slug>`, or `docs/<slug>` based on the primary area. If the default branch cannot be discovered, avoid pretending it is known.
7) If the current branch matches `issue-<number>` (digits only), keep that branch suggestion. Include an auto-closing line such as `This pull request resolves #<number>.` only when the repository hosting platform is known to support that syntax; otherwise mention the issue reference without claiming auto-close behavior.
8) Draft the PR title and description using the template below.
9) Output only the block in "Output Format".

## Output Format
When closing out a task, add this concise Markdown block after any brief status note unless the task falls under the documented skip cases or the user says they do not want it.

```
# Pull Request Draft

## Branch name suggestion

git checkout -b <kebab-case suggestion, e.g., feat/add-login-flow>

## Title

<single-line imperative title; conventional commit prefix like feat:, fix:, chore: preferred>

## Description

<start with "This pull request adds/fixes/improves ..."; explain the background and what changed; use bullets for detail if needed>
```

Keep it tight—no redundant prose around the block, and avoid repeating details between changes and the description. Tests do not need to be listed unless specifically requested.
