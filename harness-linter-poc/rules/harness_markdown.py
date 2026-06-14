"""Harness Markdown collection, link, marker, and external lint checks."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Iterable

from core.constants import (
    HARNESS_MARKDOWN_GLOBS,
    MARKDOWN_LINK_PATTERN,
    TODO_CHECKLIST_END,
    TODO_CHECKLIST_START,
)
from core.issues import issue
from core.markdown import normalize_markdown_link
from core.models import Issue


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
                        "local markdown link target does not exist",
                        markdown_file,
                        found=raw_target,
                        expected="local Markdown links must point to existing files",
                        suggested_fix=(
                            "Update the stale link to the current file path, or remove it "
                            "if the referenced file is no longer part of the harness documentation."
                        ),
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
