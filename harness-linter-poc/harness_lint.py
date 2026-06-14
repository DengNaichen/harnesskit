#!/usr/bin/env python3
"""Standalone Context Harness linter POC.

This script is intentionally outside src/harnesskit. It proves the linting shape
without changing the product CLI or package runtime.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from harness_lint_rules.architecture import check_architecture_map
from harness_lint_rules.config import check_config
from harness_lint_rules.core import (
    check_claude_pointer,
    check_core_files,
    check_installed_integrations,
)
from harness_lint_rules.markdown import (
    check_markdown_links,
    check_todo_checklist_markers,
    collect_harness_markdown,
    run_external_markdownlint,
)
from harness_lint_rules.models import Issue, Report
from harness_lint_rules.project import check_project_path
from harness_lint_rules.skills import check_skill_frontmatter, check_skill_references
from harness_lint_rules.tech_stack import check_tech_stack_blocks
from harness_lint_rules.verification import (
    check_declared_tool_documentation,
    check_package_build_documentation,
    check_verification_drift,
)


def lint_project(project_path: Path, *, external_markdownlint: bool = False) -> Report:
    project_path = project_path.expanduser().resolve()
    issues: list[Issue] = []

    project_path_issue = check_project_path(project_path)
    if project_path_issue is not None:
        issues.append(project_path_issue)
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
    check_architecture_map(project_path, issues)
    check_tech_stack_blocks(project_path, markdown_files, issues)
    check_verification_drift(project_path, markdown_files, issues)
    check_declared_tool_documentation(project_path, markdown_files, issues)
    check_package_build_documentation(project_path, markdown_files, issues)

    if external_markdownlint:
        run_external_markdownlint(project_path, markdown_files, issues)

    return Report(str(project_path), issues)


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
    raise SystemExit(main())
