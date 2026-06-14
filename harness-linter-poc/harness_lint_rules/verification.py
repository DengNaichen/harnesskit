"""Verification documentation drift checks."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from .constants import (
    PACKAGE_BUILD_COMMAND,
    RUFF_CHECK_COMMAND,
    RUFF_FORMAT_CHECK_COMMAND,
    VERIFICATION_COMMAND_CONTEXT_PATTERNS,
    VERIFICATION_DOC_PATHS,
    VERIFICATION_END,
    VERIFICATION_START,
    VERIFICATION_TEXT_CONTEXT_PATTERNS,
)
from .issues import issue, relative_path
from .markdown import extract_marked_blocks_with_lines
from .models import Issue, MarkedBlock
from .tech_stack import declared_python_tools, detect_tech_stack_facts, toml_section


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
