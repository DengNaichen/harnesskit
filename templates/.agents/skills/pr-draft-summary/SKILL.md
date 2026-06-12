---
name: pr-draft-summary
description: Create the required PR-ready summary block, branch suggestion, title, and draft description. Use in the final handoff after moderate-or-larger changes to runtime code, tests, examples, build/test configuration, or docs with behavior impact; skip only for trivial or conversation-only tasks, repo-meta/doc-only tasks without behavior impact, or when the user explicitly says not to include the PR draft block.
---

# PR Draft Summary

## Purpose
Produce the PR-ready summary required in this repository after substantive code work is complete: a concise summary plus a PR-ready title and draft description that begins with "This pull request <verb> ...". The block should be ready to paste into a PR.

## When to Trigger
- The task for this repo is finished (or ready for review) and it touched runtime code, tests, examples, docs with behavior impact, or build/test configuration.
- Treat this as the default final handoff step for substantive code work. Run it after any required verification or changeset work and before sending the "work complete" response.
- Skip only for trivial or conversation-only tasks, repo-meta/doc-only tasks without behavior impact, or when the user explicitly says not to include the PR draft block.

## Inputs to Collect Automatically (do not ask the user)
- Current branch: `git rev-parse --abbrev-ref HEAD`.
- Working tree: `git status -sb`.
- Untracked files: `git ls-files --others --exclude-standard`.
- Changed files: `git diff --name-only` (unstaged) and `git diff --name-only --cached` (staged); sizes via `git diff --stat` and `git diff --stat --cached`.
- Latest release tag: `LATEST_RELEASE_TAG=$(git tag -l 'v*' --sort=-v:refname | head -n1)`.
- Base reference (use the branch's upstream, fallback to `origin/main`):
  - `BASE_REF=$(git rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>/dev/null || echo origin/main)`.
  - `BASE_COMMIT=$(git merge-base --fork-point "$BASE_REF" HEAD || git merge-base "$BASE_REF" HEAD || echo "$BASE_REF")`.
- Commits ahead of the base fork point: `git log --oneline --no-merges ${BASE_COMMIT}..HEAD`.
- Category signals for this repo:
{{CATEGORY_SIGNALS}}

## Workflow
1) Run the commands above without asking the user; compute `BASE_REF`/`BASE_COMMIT` first so later commands reuse them.
2) If there are no staged/unstaged/untracked changes and no commits ahead of `${BASE_COMMIT}`, reply briefly that no code changes were detected and skip emitting the PR block.
3) Infer change type from the touched paths listed under "Category signals"; classify as feature, fix, refactor, or docs-with-impact, and flag backward-compatibility risk only when the diff changes released public APIs, external config, persisted data, serialized state, or wire protocols. Judge that risk against `LATEST_RELEASE_TAG`, not unreleased branch-only churn.
4) Summarize changes in 1–3 short sentences using the key paths (top 5) and `git diff --stat` output; explicitly call out untracked files because `--stat` does not include them. If the working tree is clean but there are commits ahead of `${BASE_COMMIT}`, summarize using those commit messages.
5) Choose the lead verb for the description: feature → `adds`, bug fix → `fixes`, refactor/perf → `improves` or `updates`, docs-only → `updates`.
6) Suggest a branch name. If already off main, keep it; otherwise propose `feat/<slug>`, `fix/<slug>`, or `docs/<slug>` based on the primary area.
7) If the current branch matches `issue-<number>` (digits only), keep that branch suggestion. When an issue number is present, reference `{{GITHUB_REPO_URL}}/issues/<number>` and include an auto-closing line such as `This pull request resolves #<number>.`
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
