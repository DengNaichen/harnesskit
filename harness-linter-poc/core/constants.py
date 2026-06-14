"""Shared constants for Harness Linter rule modules."""

from __future__ import annotations

import re


CONFIG_SCHEMA_VERSION = 1
SUPPORTED_INTEGRATIONS = {"codex"}
CODEX_SKILLS = (
    ".agents/skills/harnesskit-audit/SKILL.md",
    ".agents/skills/harnesskit-refresh/SKILL.md",
    ".agents/skills/harnesskit-explain/SKILL.md",
)
HARNESS_MARKDOWN_GLOBS = (
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "ARCHITECTURE.md",
    ".agents/skills/*/SKILL.md",
)
VERIFICATION_DOC_PATHS = (
    "AGENTS.md",
    ".agents/skills/code-change-verification/SKILL.md",
)
VERIFICATION_COMMAND_CONTEXT_PATTERNS = (
    r"\bpytest\b",
    r"\blychee\b",
    r"\bunittest\b",
    r"\buv\s+run\b",
)
VERIFICATION_TEXT_CONTEXT_PATTERNS = (
    r"\bverification\b",
    r"验证",
)
MARKDOWN_LINK_PATTERN = re.compile(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
SKILL_REFERENCE_PATTERN = re.compile(r"(?<![\w`])\$([A-Za-z][A-Za-z0-9_-]*)")
TODO_CHECKLIST_START = "<!-- harnesskit:todo-checklist:start -->"
TODO_CHECKLIST_END = "<!-- harnesskit:todo-checklist:end -->"
TECH_STACK_START = "<!-- harnesskit:tech-stack:start -->"
TECH_STACK_END = "<!-- harnesskit:tech-stack:end -->"
VERIFICATION_START = "<!-- harnesskit:verification:start -->"
VERIFICATION_END = "<!-- harnesskit:verification:end -->"
TECH_STACK_ENTRY_PATTERN = re.compile(r"^\s*[-*]\s*([^:]+):\s*(.+?)\s*$")
RUFF_CHECK_COMMAND = "uv run ruff check ."
RUFF_FORMAT_CHECK_COMMAND = "uv run ruff format --check ."
PACKAGE_BUILD_COMMAND = "uv build"
PRE_COMMIT_COMMAND = "uv run pre-commit run --all-files"
