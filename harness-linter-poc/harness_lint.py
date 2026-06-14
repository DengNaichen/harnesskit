#!/usr/bin/env python3
"""Standalone Context Harness linter POC.

This script is intentionally outside src/harnesskit. It proves the linting shape
without changing the product CLI or package runtime.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Literal
from urllib.parse import unquote, urldefrag, urlparse


Severity = Literal["error", "warning"]

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
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
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


@dataclass(frozen=True)
class Issue:
    severity: Severity
    code: str
    path: str
    message: str
    line: int | None = None
    found: str | None = None
    expected: str | None = None
    evidence: list[str] | None = None
    suggested_fix: str | None = None
    verify_command: str | None = None


@dataclass(frozen=True)
class Report:
    project_path: str
    issues: list[Issue]

    @property
    def errors(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.severity == "warning"]

    @property
    def passed(self) -> bool:
        return not self.errors


@dataclass(frozen=True)
class MarkedBlock:
    start_line: int
    content: str


def lint_project(project_path: Path, *, external_markdownlint: bool = False) -> Report:
    project_path = project_path.expanduser().resolve()
    issues: list[Issue] = []

    if not project_path.is_dir():
        issues.append(
            issue(
                "error",
                "project.not_directory",
                project_path,
                "project path is not a directory",
                project_path,
            )
        )
        return Report(str(project_path), issues)

    config = check_config(project_path, issues)
    check_core_files(project_path, issues)
    check_claude_pointer(project_path, issues)
    check_installed_integrations(project_path, config, issues)
    check_skill_frontmatter(project_path, issues)
    check_skill_references(project_path, issues)
    markdown_files = collect_harness_markdown(project_path)
    check_markdown_links(project_path, markdown_files, issues)
    check_todo_checklist_markers(project_path, markdown_files, issues)
    check_tech_stack_blocks(project_path, markdown_files, issues)
    check_verification_drift(project_path, markdown_files, issues)
    check_declared_tool_documentation(project_path, markdown_files, issues)
    check_package_build_documentation(project_path, markdown_files, issues)

    if external_markdownlint:
        run_external_markdownlint(project_path, markdown_files, issues)

    return Report(str(project_path), issues)


def check_config(project_path: Path, issues: list[Issue]) -> dict[str, object] | None:
    config_path = project_path / ".harnesskit" / "config.json"
    if not config_path.is_file():
        issues.append(
            issue(
                "error",
                "config.missing",
                project_path,
                "missing .harnesskit/config.json",
                config_path,
            )
        )
        return None

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issues.append(
            issue(
                "error",
                "config.invalid_json",
                project_path,
                f"invalid JSON: {exc}",
                config_path,
            )
        )
        return None

    if not isinstance(config, dict):
        issues.append(
            issue(
                "error",
                "config.not_object",
                project_path,
                "config must be a JSON object",
                config_path,
            )
        )
        return None

    if config.get("schema_version") != CONFIG_SCHEMA_VERSION:
        issues.append(
            issue(
                "error",
                "config.schema_version",
                project_path,
                f"schema_version must be {CONFIG_SCHEMA_VERSION}",
                config_path,
            )
        )

    default_integration = config.get("default_integration")
    if default_integration not in SUPPORTED_INTEGRATIONS:
        issues.append(
            issue(
                "error",
                "config.default_integration",
                project_path,
                f"unsupported default_integration: {default_integration!r}",
                config_path,
            )
        )

    installed = config.get("installed_integrations")
    if not isinstance(installed, list) or not all(
        isinstance(item, str) for item in installed
    ):
        issues.append(
            issue(
                "error",
                "config.installed_integrations",
                project_path,
                "installed_integrations must be a list of strings",
                config_path,
            )
        )
        return config

    for integration in installed:
        if integration not in SUPPORTED_INTEGRATIONS:
            issues.append(
                issue(
                    "error",
                    "config.installed_integration.unsupported",
                    project_path,
                    f"unsupported installed integration: {integration!r}",
                    config_path,
                )
            )

    return config


def check_core_files(project_path: Path, issues: list[Issue]) -> None:
    for relative_path in ("AGENTS.md", "CLAUDE.md"):
        path = project_path / relative_path
        if not path.exists():
            issues.append(
                issue(
                    "error",
                    "core.missing",
                    project_path,
                    "required harness file is missing",
                    path,
                )
            )
        elif path.is_file() and path.stat().st_size == 0:
            issues.append(
                issue(
                    "error",
                    "core.empty",
                    project_path,
                    "required harness file is empty",
                    path,
                )
            )


def check_claude_pointer(project_path: Path, issues: list[Issue]) -> None:
    claude_path = project_path / "CLAUDE.md"
    agents_path = project_path / "AGENTS.md"
    if not claude_path.exists() or not agents_path.exists():
        return

    if claude_path.is_symlink():
        try:
            if claude_path.resolve(strict=True) != agents_path.resolve(strict=True):
                issues.append(
                    issue(
                        "warning",
                        "claude.pointer",
                        project_path,
                        "CLAUDE.md symlink should point to AGENTS.md",
                        claude_path,
                    )
                )
        except FileNotFoundError:
            issues.append(
                issue(
                    "error",
                    "claude.broken_symlink",
                    project_path,
                    "CLAUDE.md symlink target is missing",
                    claude_path,
                )
            )
        return

    if claude_path.is_file() and "AGENTS.md" not in claude_path.read_text(
        encoding="utf-8"
    ):
        issues.append(
            issue(
                "warning",
                "claude.pointer",
                project_path,
                "CLAUDE.md should point readers to AGENTS.md",
                claude_path,
            )
        )


def check_installed_integrations(
    project_path: Path, config: dict[str, object] | None, issues: list[Issue]
) -> None:
    installed = config.get("installed_integrations", []) if config else []
    if not isinstance(installed, list):
        return

    if "codex" in installed:
        for relative_path in CODEX_SKILLS:
            path = project_path / relative_path
            if not path.is_file():
                issues.append(
                    issue(
                        "error",
                        "codex.skill.missing",
                        project_path,
                        "required Codex skill is missing",
                        path,
                    )
                )
            elif path.stat().st_size == 0:
                issues.append(
                    issue(
                        "error",
                        "codex.skill.empty",
                        project_path,
                        "required Codex skill is empty",
                        path,
                    )
                )


def check_skill_frontmatter(project_path: Path, issues: list[Issue]) -> None:
    for skill_path in sorted((project_path / ".agents" / "skills").glob("*/SKILL.md")):
        text = skill_path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        if frontmatter is None:
            issues.append(
                issue(
                    "error",
                    "skill.frontmatter.missing",
                    project_path,
                    "SKILL.md must start with frontmatter",
                    skill_path,
                )
            )
            continue

        for required_key in ("name", "description"):
            if not frontmatter.get(required_key):
                issues.append(
                    issue(
                        "error",
                        f"skill.frontmatter.{required_key}",
                        project_path,
                        f"frontmatter must include {required_key}",
                        skill_path,
                    )
                )


def check_skill_references(project_path: Path, issues: list[Issue]) -> None:
    agents_path = project_path / "AGENTS.md"
    if not agents_path.is_file():
        return

    text = agents_path.read_text(encoding="utf-8")
    for skill_name in sorted(set(SKILL_REFERENCE_PATTERN.findall(text))):
        skill_path = project_path / ".agents" / "skills" / skill_name / "SKILL.md"
        if not skill_path.is_file():
            issues.append(
                issue(
                    "error",
                    "skill.reference.missing",
                    project_path,
                    f"AGENTS.md references ${skill_name}, but .agents/skills/{skill_name}/SKILL.md does not exist",
                    agents_path,
                )
            )


def parse_frontmatter(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return values
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("\"'")

    return None


def collect_harness_markdown(project_path: Path) -> list[Path]:
    files_by_real_path: dict[Path, Path] = {}
    for pattern in HARNESS_MARKDOWN_GLOBS:
        for path in project_path.glob(pattern):
            if path.is_file():
                files_by_real_path.setdefault(path.resolve(), path)
    return sorted(files_by_real_path.values())


def check_markdown_links(
    project_path: Path, markdown_files: Iterable[Path], issues: list[Issue]
) -> None:
    for markdown_file in markdown_files:
        text = markdown_file.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_PATTERN.finditer(text):
            raw_target = match.group(1).strip()
            target = normalize_markdown_link(raw_target)
            if target is None:
                continue

            if target.is_absolute():
                resolved = (project_path / str(target).lstrip("/")).resolve()
            else:
                resolved = (markdown_file.parent / target).resolve()
            if not resolved.exists():
                issues.append(
                    issue(
                        "error",
                        "markdown.link.missing",
                        project_path,
                        f"local markdown link target does not exist: {raw_target}",
                        markdown_file,
                    )
                )


def check_todo_checklist_markers(
    project_path: Path, markdown_files: Iterable[Path], issues: list[Issue]
) -> None:
    for markdown_file in markdown_files:
        open_count = 0
        for line in markdown_file.read_text(encoding="utf-8").splitlines():
            if TODO_CHECKLIST_START in line:
                open_count += 1
            if TODO_CHECKLIST_END in line:
                if open_count == 0:
                    issues.append(
                        issue(
                            "error",
                            "markdown.todo_checklist.unpaired",
                            project_path,
                            "todo checklist end marker appears before a start marker",
                            markdown_file,
                        )
                    )
                    return
                open_count -= 1

        if open_count:
            issues.append(
                issue(
                    "error",
                    "markdown.todo_checklist.unpaired",
                    project_path,
                    "todo checklist start marker is missing a matching end marker",
                    markdown_file,
                )
            )


def check_tech_stack_blocks(
    project_path: Path, markdown_files: Iterable[Path], issues: list[Issue]
) -> None:
    facts = detect_tech_stack_facts(project_path)
    for markdown_file in markdown_files:
        text = markdown_file.read_text(encoding="utf-8")
        for block in extract_marked_blocks(
            project_path,
            markdown_file,
            text,
            TECH_STACK_START,
            TECH_STACK_END,
            "markdown.tech_stack.unpaired",
            issues,
        ):
            for key, declared_value in parse_tech_stack_entries(block).items():
                expected_value = facts.get(key)
                if expected_value is None:
                    continue
                if not tech_stack_value_matches(declared_value, expected_value):
                    issues.append(
                        issue(
                            "error",
                            "tech_stack.mismatch",
                            project_path,
                            f"{key!r} declares {declared_value!r}, but repository facts indicate {expected_value!r}",
                            markdown_file,
                        )
                    )


def check_verification_drift(
    project_path: Path, markdown_files: Iterable[Path], issues: list[Issue]
) -> None:
    facts = detect_tech_stack_facts(project_path)
    tests = facts.get("tests")
    if tests != "pytest":
        return

    stale_patterns = (
        r"\bpython\s+-m\s+unittest\b",
        r"\bunittest\s+discover\b",
        r"`unittest`",
    )
    stale_references = [
        re.compile(pattern, re.IGNORECASE) for pattern in stale_patterns
    ]
    for markdown_file in markdown_files:
        text = markdown_file.read_text(encoding="utf-8")
        match = find_first_line_match(text, stale_references)
        if match is not None:
            line_number, found = match
            issues.append(
                issue(
                    "error",
                    "verification.stale_test_framework",
                    project_path,
                    "repository facts indicate pytest, but harness markdown still references unittest",
                    markdown_file,
                    line=line_number,
                    found=found,
                    expected="uv run pytest",
                    evidence=verification_evidence(project_path),
                    suggested_fix=(
                        "Replace stale unittest verification guidance with the pytest command. "
                        "Update every harness file that describes the full verification stack."
                    ),
                    verify_command="uv run pytest",
                )
            )


def check_declared_tool_documentation(
    project_path: Path, markdown_files: Iterable[Path], issues: list[Issue]
) -> None:
    declared_tools = declared_python_tools(project_path)
    if "ruff" not in declared_tools:
        return

    documentation_targets = verification_documentation_targets(
        project_path, markdown_files
    )
    for markdown_file in documentation_targets:
        text = markdown_file.read_text(encoding="utf-8")
        verification_blocks = extract_marked_blocks_with_lines(
            project_path,
            markdown_file,
            text,
            VERIFICATION_START,
            VERIFICATION_END,
            "markdown.verification.unpaired",
            issues,
        )
        if not verification_blocks:
            if VERIFICATION_START in text or VERIFICATION_END in text:
                continue

            line_match = find_verification_context_line(text)
            line_number = line_match[0] if line_match else None
            found = (
                line_match[1]
                if line_match
                else f"{relative_path(project_path, markdown_file)} has no verification block"
            )
            issues.append(
                issue(
                    "error",
                    "verification.block_missing",
                    project_path,
                    "verification documentation must use a harnesskit:verification block",
                    markdown_file,
                    line=line_number,
                    found=found,
                    expected=f"add {VERIFICATION_START} / {VERIFICATION_END} with verification commands",
                    evidence=[
                        "pyproject.toml declares ruff",
                        f"{relative_path(project_path, markdown_file)} is a verification doc",
                    ],
                    suggested_fix=verification_block_suggestion(),
                    verify_command=RUFF_CHECK_COMMAND,
                )
            )
            continue

        check_ruff_lint_documented(
            project_path, markdown_file, verification_blocks, issues
        )
        check_ruff_format_documented(
            project_path, markdown_file, verification_blocks, issues
        )


def check_ruff_lint_documented(
    project_path: Path,
    markdown_file: Path,
    verification_blocks: list[MarkedBlock],
    issues: list[Issue],
) -> None:
    if marked_blocks_document_tool(verification_blocks, "ruff"):
        return

    first_block = verification_blocks[0]
    issues.append(
        issue(
            "error",
            "verification.tool_not_documented",
            project_path,
            "harnesskit:verification block omits declared tool Ruff",
            markdown_file,
            line=first_block.start_line,
            found="harnesskit:verification block does not mention Ruff",
            expected="add Ruff to the verification block as an active gate or explicitly inactive",
            evidence=[
                "pyproject.toml declares ruff",
                f"{relative_path(project_path, markdown_file)} verification block does not mention ruff",
            ],
            suggested_fix=verification_block_suggestion(),
            verify_command=RUFF_CHECK_COMMAND,
        )
    )


def check_ruff_format_documented(
    project_path: Path,
    markdown_file: Path,
    verification_blocks: list[MarkedBlock],
    issues: list[Issue],
) -> None:
    if not ruff_formatter_configured(project_path):
        return

    mutating_command = find_ruff_format_line(verification_blocks, require_check=False)
    if mutating_command is not None:
        block, found = mutating_command
        issues.append(
            issue(
                "error",
                "verification.format_command_mutates",
                project_path,
                "Ruff formatter verification command must be check-only",
                markdown_file,
                line=block.start_line,
                found=found,
                expected=RUFF_FORMAT_CHECK_COMMAND,
                evidence=[
                    "pyproject.toml configures [tool.ruff.format]",
                    f"{relative_path(project_path, markdown_file)} verification block uses a mutating Ruff format command",
                ],
                suggested_fix=f"Replace the mutating format command with `{RUFF_FORMAT_CHECK_COMMAND}`.",
                verify_command=RUFF_FORMAT_CHECK_COMMAND,
            )
        )
        return

    if marked_blocks_document_ruff_format(verification_blocks):
        return

    first_block = verification_blocks[0]
    issues.append(
        issue(
            "error",
            "verification.format_not_documented",
            project_path,
            "harnesskit:verification block omits configured Ruff formatter",
            markdown_file,
            line=first_block.start_line,
            found="harnesskit:verification block does not mention Ruff format",
            expected=f"add `{RUFF_FORMAT_CHECK_COMMAND}` as a format gate or explicitly mark Ruff format inactive",
            evidence=[
                "pyproject.toml configures [tool.ruff.format]",
                f"{relative_path(project_path, markdown_file)} verification block does not mention ruff format",
            ],
            suggested_fix=(
                f"Add `- Python format: {RUFF_FORMAT_CHECK_COMMAND}` to the verification block, "
                "or document `- Python format: Ruff format inactive`."
            ),
            verify_command=RUFF_FORMAT_CHECK_COMMAND,
        )
    )


def check_package_build_documentation(
    project_path: Path, markdown_files: Iterable[Path], issues: list[Issue]
) -> None:
    if not package_build_configured(project_path):
        return

    documentation_targets = verification_documentation_targets(
        project_path, markdown_files
    )
    for markdown_file in documentation_targets:
        text = markdown_file.read_text(encoding="utf-8")
        verification_blocks = extract_marked_blocks_with_lines(
            project_path,
            markdown_file,
            text,
            VERIFICATION_START,
            VERIFICATION_END,
            "markdown.verification.unpaired",
            issues,
        )
        if not verification_blocks:
            if VERIFICATION_START in text or VERIFICATION_END in text:
                continue

            line_match = find_verification_context_line(text)
            line_number = line_match[0] if line_match else None
            found = (
                line_match[1]
                if line_match
                else f"{relative_path(project_path, markdown_file)} has no verification block"
            )
            issues.append(
                issue(
                    "error",
                    "verification.block_missing",
                    project_path,
                    "verification documentation must use a harnesskit:verification block",
                    markdown_file,
                    line=line_number,
                    found=found,
                    expected=f"add {VERIFICATION_START} / {VERIFICATION_END} with package build verification",
                    evidence=[
                        "pyproject.toml configures [build-system]",
                        f"{relative_path(project_path, markdown_file)} is a verification doc",
                    ],
                    suggested_fix=package_build_suggestion(),
                    verify_command=PACKAGE_BUILD_COMMAND,
                )
            )
            continue

        if marked_blocks_document_package_build(verification_blocks):
            continue

        first_block = verification_blocks[0]
        issues.append(
            issue(
                "error",
                "verification.build_not_documented",
                project_path,
                "harnesskit:verification block omits configured package build",
                markdown_file,
                line=first_block.start_line,
                found="harnesskit:verification block does not mention package build",
                expected=f"add `{PACKAGE_BUILD_COMMAND}` as a package build gate or explicitly mark package build inactive",
                evidence=[
                    "pyproject.toml configures [build-system]",
                    f"{relative_path(project_path, markdown_file)} verification block does not mention package build",
                ],
                suggested_fix=package_build_suggestion(),
                verify_command=PACKAGE_BUILD_COMMAND,
            )
        )


def verification_documentation_targets(
    project_path: Path, markdown_files: Iterable[Path]
) -> list[Path]:
    markdown_by_relative_path = {
        relative_path(project_path, path): path for path in markdown_files
    }
    targets = [
        markdown_by_relative_path[relative]
        for relative in VERIFICATION_DOC_PATHS
        if relative in markdown_by_relative_path
    ]
    if targets:
        return targets
    return list(markdown_files)


def find_verification_context_line(text: str) -> tuple[int, str] | None:
    command_patterns = [
        re.compile(pattern, re.IGNORECASE)
        for pattern in VERIFICATION_COMMAND_CONTEXT_PATTERNS
    ]
    command_match = find_first_line_match(text, command_patterns)
    if command_match is not None:
        return command_match

    text_patterns = [
        re.compile(pattern, re.IGNORECASE)
        for pattern in VERIFICATION_TEXT_CONTEXT_PATTERNS
    ]
    return find_first_line_match(text, text_patterns)


def marked_blocks_document_tool(blocks: Iterable[MarkedBlock], tool_name: str) -> bool:
    pattern = re.compile(rf"\b{re.escape(tool_name)}\b", re.IGNORECASE)
    return any(pattern.search(block.content) for block in blocks)


def marked_blocks_document_ruff_format(blocks: Iterable[MarkedBlock]) -> bool:
    return find_ruff_format_line(blocks, require_check=True) is not None or any(
        re.search(r"\bruff\b", block.content, re.IGNORECASE)
        and re.search(r"\bformat(?:ter)?\b", block.content, re.IGNORECASE)
        and re.search(r"\binactive\b", block.content, re.IGNORECASE)
        for block in blocks
    )


def find_ruff_format_line(
    blocks: Iterable[MarkedBlock], *, require_check: bool
) -> tuple[MarkedBlock, str] | None:
    for block in blocks:
        for line in block.content.splitlines():
            if not re.search(r"\bruff\s+format\b", line, re.IGNORECASE):
                continue
            if re.search(r"\binactive\b", line, re.IGNORECASE):
                continue
            has_check = "--check" in line
            if has_check == require_check:
                return block, line.strip()
    return None


def marked_blocks_document_package_build(blocks: Iterable[MarkedBlock]) -> bool:
    return any(
        re.search(r"\buv\s+build\b", block.content, re.IGNORECASE)
        or (
            re.search(r"\bpackage\s+build\b", block.content, re.IGNORECASE)
            and re.search(r"\binactive\b", block.content, re.IGNORECASE)
        )
        for block in blocks
    )


def ruff_formatter_configured(project_path: Path) -> bool:
    pyproject_path = project_path / "pyproject.toml"
    if not pyproject_path.is_file():
        return False

    text = pyproject_path.read_text(encoding="utf-8")
    return bool(toml_section(text, "tool.ruff.format"))


def package_build_configured(project_path: Path) -> bool:
    pyproject_path = project_path / "pyproject.toml"
    if not pyproject_path.is_file():
        return False

    text = pyproject_path.read_text(encoding="utf-8")
    return bool(toml_section(text, "project")) and bool(
        toml_section(text, "build-system")
    )


def verification_block_suggestion() -> str:
    return (
        f"Add a block like `{VERIFICATION_START}` with entries such as "
        f"`- Python lint: {RUFF_CHECK_COMMAND}`, or `- Python lint: Ruff installed, inactive`, "
        f"then close it with `{VERIFICATION_END}`."
    )


def package_build_suggestion() -> str:
    return (
        f"Add `- Package build: {PACKAGE_BUILD_COMMAND}` to the verification block, "
        "or document `- Package build: inactive`."
    )


def find_first_line_match(
    text: str, patterns: Iterable[re.Pattern[str]]
) -> tuple[int, str] | None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern in patterns:
            match = pattern.search(line)
            if match:
                found = line.strip() or match.group(0)
                return line_number, found
    return None


def verification_evidence(project_path: Path) -> list[str]:
    evidence: list[str] = []
    pyproject = project_path / "pyproject.toml"
    if pyproject.is_file():
        evidence.append("pyproject.toml declares pytest in dev dependencies")

    tests_dir = project_path / "tests"
    pytest_tests = []
    if tests_dir.is_dir():
        for test_file in sorted(tests_dir.glob("**/*.py")):
            text = test_file.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"(?m)^\s*(import pytest|from pytest\b)", text):
                pytest_tests.append(test_file)
    if pytest_tests:
        first = pytest_tests[0].relative_to(project_path)
        evidence.append(f"{first} imports pytest")

    if not evidence:
        evidence.append("repository test facts indicate pytest")
    return evidence


def detect_tech_stack_facts(project_path: Path) -> dict[str, str]:
    facts: dict[str, str] = {}
    pyproject_path = project_path / "pyproject.toml"
    if pyproject_path.is_file():
        text = pyproject_path.read_text(encoding="utf-8")
        project_section = toml_section(text, "project")
        build_section = toml_section(text, "build-system")
        dependencies = {
            dependency_name(item)
            for item in toml_array_strings(project_section, "dependencies")
        }

        if project_section:
            facts["language"] = "Python"
        if "typer" in dependencies:
            facts["cli"] = "Typer"
        if "rich" in dependencies:
            facts["terminal output"] = "Rich"
        if "jinja2" in dependencies:
            facts["templates"] = "Jinja2"
        if "hatchling" in {
            dependency_name(item)
            for item in toml_array_strings(build_section, "requires")
        }:
            facts["build backend"] = "Hatchling"
        elif "hatchling" in toml_string(build_section, "build-backend").lower():
            facts["build backend"] = "Hatchling"

    package_json_path = project_path / "package.json"
    if package_json_path.is_file():
        facts.setdefault("language", "JavaScript")
        if (project_path / "pnpm-lock.yaml").is_file():
            facts["package manager"] = "pnpm"
        elif (project_path / "yarn.lock").is_file():
            facts["package manager"] = "yarn"
        elif (project_path / "package-lock.json").is_file():
            facts["package manager"] = "npm"

    if (project_path / "uv.lock").is_file():
        facts["package manager"] = "uv"

    detected_tests = detect_python_test_framework(project_path)
    if detected_tests:
        facts["tests"] = detected_tests

    return facts


def declared_python_tools(project_path: Path) -> set[str]:
    pyproject_path = project_path / "pyproject.toml"
    if not pyproject_path.is_file():
        return set()

    text = pyproject_path.read_text(encoding="utf-8")
    return {dependency_name(item) for item in re.findall(r'"([^"]+)"', text)}


def detect_python_test_framework(project_path: Path) -> str | None:
    test_files = list((project_path / "tests").glob("**/*.py"))
    for test_file in test_files:
        text = test_file.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"(?m)^\s*(import unittest|from unittest\b)", text):
            return "unittest"

    if (project_path / "pytest.ini").is_file() or (
        project_path / "conftest.py"
    ).is_file():
        return "pytest"
    for test_file in test_files:
        text = test_file.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"(?m)^\s*(import pytest|from pytest\b)", text):
            return "pytest"
    return None


def extract_marked_blocks(
    project_path: Path,
    markdown_file: Path,
    text: str,
    start_marker: str,
    end_marker: str,
    issue_code: str,
    issues: list[Issue],
) -> list[str]:
    return [
        block.content
        for block in extract_marked_blocks_with_lines(
            project_path,
            markdown_file,
            text,
            start_marker,
            end_marker,
            issue_code,
            issues,
        )
    ]


def extract_marked_blocks_with_lines(
    project_path: Path,
    markdown_file: Path,
    text: str,
    start_marker: str,
    end_marker: str,
    issue_code: str,
    issues: list[Issue],
) -> list[MarkedBlock]:
    blocks: list[MarkedBlock] = []
    current: list[str] | None = None
    current_start_line: int | None = None

    for line_number, line in enumerate(text.splitlines(), start=1):
        if start_marker in line:
            if current is not None:
                issues.append(
                    issue(
                        "error",
                        issue_code,
                        project_path,
                        "nested marker block is not allowed",
                        markdown_file,
                    )
                )
                return blocks
            current = []
            current_start_line = line_number
            continue
        if end_marker in line:
            if current is None:
                issues.append(
                    issue(
                        "error",
                        issue_code,
                        project_path,
                        "end marker appears before a start marker",
                        markdown_file,
                    )
                )
                return blocks
            blocks.append(
                MarkedBlock(
                    start_line=current_start_line or line_number,
                    content="\n".join(current),
                )
            )
            current = None
            current_start_line = None
            continue
        if current is not None:
            current.append(line)

    if current is not None:
        issues.append(
            issue(
                "error",
                issue_code,
                project_path,
                "start marker is missing a matching end marker",
                markdown_file,
            )
        )

    return blocks


def parse_tech_stack_entries(block: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in block.splitlines():
        match = TECH_STACK_ENTRY_PATTERN.match(line)
        if not match:
            continue
        key = normalize_tech_stack_key(match.group(1))
        value = match.group(2).strip().strip("`")
        entries[key] = value
    return entries


def normalize_tech_stack_key(key: str) -> str:
    return re.sub(r"\s+", " ", key.strip().lower().replace("-", " "))


def tech_stack_value_matches(declared_value: str, expected_value: str) -> bool:
    declared = normalize_tech_stack_value(declared_value)
    expected = normalize_tech_stack_value(expected_value)
    return expected in declared or declared in expected


def normalize_tech_stack_value(value: str) -> str:
    return re.sub(r"[^a-z0-9+#.]+", " ", value.lower()).strip()


def toml_section(text: str, section_name: str) -> str:
    pattern = re.compile(rf"(?ms)^\[{re.escape(section_name)}\]\s*(.*?)(?=^\[|\Z)")
    match = pattern.search(text)
    return match.group(1) if match else ""


def toml_string(section_text: str, key: str) -> str:
    match = re.search(rf'(?m)^{re.escape(key)}\s*=\s*"([^"]*)"', section_text)
    return match.group(1) if match else ""


def toml_array_strings(section_text: str, key: str) -> list[str]:
    match = re.search(rf"(?ms)^{re.escape(key)}\s*=\s*\[(.*?)\]", section_text)
    if not match:
        return []
    return re.findall(r'"([^"]+)"', match.group(1))


def dependency_name(requirement: str) -> str:
    name = re.split(r"[\s<>=!~;\[]", requirement.strip(), maxsplit=1)[0]
    return name.lower().replace("_", "-")


def normalize_markdown_link(raw_target: str) -> Path | None:
    target_without_fragment, _fragment = urldefrag(raw_target)
    if not target_without_fragment:
        return None

    parsed = urlparse(target_without_fragment)
    if parsed.scheme or target_without_fragment.startswith("#"):
        return None

    return Path(unquote(target_without_fragment))


def run_external_markdownlint(
    project_path: Path, markdown_files: list[Path], issues: list[Issue]
) -> None:
    if not markdown_files:
        return

    command = find_markdownlint()
    if command is None:
        issues.append(
            issue(
                "warning",
                "external.markdownlint.missing",
                project_path,
                "markdownlint-cli2 or markdownlint is not installed",
                project_path,
            )
        )
        return

    result = subprocess.run(
        [*command, *[str(path.relative_to(project_path)) for path in markdown_files]],
        cwd=project_path,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        output = result.stdout.strip() or "markdownlint failed"
        issues.append(
            issue("error", "external.markdownlint", project_path, output, project_path)
        )


def find_markdownlint() -> list[str] | None:
    if shutil.which("markdownlint-cli2"):
        return ["markdownlint-cli2"]
    if shutil.which("markdownlint"):
        return ["markdownlint"]
    return None


def issue(
    severity: Severity,
    code: str,
    project_path: Path,
    message: str,
    path: Path,
    *,
    line: int | None = None,
    found: str | None = None,
    expected: str | None = None,
    evidence: list[str] | None = None,
    suggested_fix: str | None = None,
    verify_command: str | None = None,
) -> Issue:
    display_path = relative_path(project_path, path)
    return Issue(
        severity=severity,
        code=code,
        path=display_path,
        message=message,
        line=line,
        found=found,
        expected=expected,
        evidence=evidence,
        suggested_fix=suggested_fix,
        verify_command=verify_command,
    )


def relative_path(project_path: Path, path: Path) -> str:
    try:
        relative = path.resolve().relative_to(project_path.resolve())
        return str(relative)
    except ValueError:
        return str(path)


def print_text_report(report: Report) -> None:
    status = "passed" if report.passed else "failed"
    print(f"Harness lint {status}: {report.project_path}")
    if not report.issues:
        return

    for item in report.issues:
        location = f"{item.path}:{item.line}" if item.line is not None else item.path
        print(f"{item.severity.upper()} {item.code} {location}: {item.message}")
        if item.found:
            print(f"  Found: {item.found}")
        if item.expected:
            print(f"  Expected: {item.expected}")
        if item.evidence:
            print("  Evidence:")
            for entry in item.evidence:
                print(f"    - {entry}")
        if item.suggested_fix:
            print(f"  Suggested fix: {item.suggested_fix}")
        if item.verify_command:
            print(f"  Verify: {item.verify_command}")


def print_json_report(report: Report) -> None:
    payload = {
        "project_path": report.project_path,
        "passed": report.passed,
        "issue_count": len(report.issues),
        "error_count": len(report.errors),
        "warning_count": len(report.warnings),
        "issues": [asdict(item) for item in report.issues],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Standalone Context Harness linter POC."
    )
    parser.add_argument(
        "project", nargs="?", default=".", help="Project directory to lint."
    )
    parser.add_argument(
        "--json", action="store_true", help="Print a machine-readable JSON report."
    )
    parser.add_argument(
        "--external-markdownlint",
        action="store_true",
        help="Run markdownlint-cli2 or markdownlint when installed.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    report = lint_project(
        Path(args.project), external_markdownlint=args.external_markdownlint
    )
    if args.json:
        print_json_report(report)
    else:
        print_text_report(report)

    return 0 if report.passed else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(2)
