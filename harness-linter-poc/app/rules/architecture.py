"""Architecture documentation coverage checks."""

from __future__ import annotations

import fnmatch
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from core.constants import MARKDOWN_LINK_PATTERN
from core.issues import issue
from core.markdown import normalize_markdown_link
from core.models import Issue


PLACEHOLDER_TOKEN = "placeholder"
COVERAGE_HINT_TOKEN = "harnesskit:coverage"
COVERAGE_HINT_PATTERN = re.compile(
    r"<!--\s*harnesskit:coverage=(?P<coverage>[a-z-]+)(?P<attrs>.*?)-->"
)
IGNORE_HINT_PATTERN = re.compile(r"\bignore=(?P<value>[^\s>]+)")


@dataclass(frozen=True)
class ArchitectureLink:
    path: str
    line: int
    coverage: str | None
    ignored_paths: tuple[str, ...]


def check_architecture_map(project_path: Path, issues: list[Issue]) -> None:
    architecture_path = project_path / "ARCHITECTURE.md"
    if not architecture_path.is_file():
        return

    text = architecture_path.read_text(encoding="utf-8")
    check_architecture_placeholders(project_path, architecture_path, text, issues)
    check_coverage_hint_syntax(project_path, architecture_path, text, issues)
    architecture_links = collect_architecture_links(
        project_path, architecture_path, text
    )
    if not architecture_links:
        return

    covered_paths = {link.path for link in architecture_links}
    project_files = collect_project_file_paths(project_path)

    for entry in architecture_links:
        if entry.coverage is None:
            continue

        if entry.coverage != "direct-children":
            issues.append(
                issue(
                    "error",
                    "architecture.coverage_invalid",
                    project_path,
                    "architecture coverage hint uses an unsupported mode",
                    architecture_path,
                    line=entry.line,
                    found=entry.coverage,
                    expected="coverage must be direct-children",
                )
            )
            continue

        absolute_path = project_path / entry.path
        if not absolute_path.exists():
            issues.append(
                issue(
                    "error",
                    "architecture.path_missing",
                    project_path,
                    "architecture coverage hint points to a path that does not exist",
                    architecture_path,
                    line=entry.line,
                    found=entry.path,
                    expected="declared architecture paths must exist in the repository",
                    suggested_fix="Update the Markdown link or restore the missing path.",
                )
            )
            continue

        if not absolute_path.is_dir():
            issues.append(
                issue(
                    "error",
                    "architecture.coverage_invalid",
                    project_path,
                    "architecture direct-children coverage hint points to a non-directory path",
                    architecture_path,
                    line=entry.line,
                    found=entry.path,
                    expected="direct-children coverage requires a directory path",
                )
            )
            continue

        ignored_paths = {
            normalize_architecture_path(ignored_path)
            for ignored_path in entry.ignored_paths
        }
        for child_path in sorted(direct_children_under(project_files, entry.path)):
            if architecture_path_ignored(child_path, ignored_paths):
                continue
            if child_path in covered_paths:
                continue
            issues.append(
                issue(
                    "error",
                    "architecture.coverage_missing",
                    project_path,
                    "architecture documentation does not cover a direct child path",
                    architecture_path,
                    line=entry.line,
                    found=child_path,
                    expected=(
                        f"add a Markdown link to `{child_path}` in ARCHITECTURE.md "
                        "or list it in the coverage hint ignore attribute"
                    ),
                    evidence=[
                        f"{entry.path} declares harnesskit:coverage=direct-children",
                        f"{child_path} exists in the repository",
                    ],
                    suggested_fix=(
                        f"Document `{child_path}` as a Markdown link, or add "
                        f"`ignore={child_path}` to the coverage hint if it should stay "
                        "out of the map."
                    ),
                )
            )


def check_architecture_placeholders(
    project_path: Path, architecture_path: Path, text: str, issues: list[Issue]
) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if PLACEHOLDER_TOKEN not in line.lower():
            continue
        issues.append(
            issue(
                "warning",
                "architecture.placeholder_description",
                project_path,
                "ARCHITECTURE.md contains placeholder responsibility text",
                architecture_path,
                line=line_number,
                found=line.strip(),
                expected="replace placeholder text with a concrete responsibility description",
                suggested_fix=(
                    "Replace the placeholder with a concise description of what this "
                    "path owns or why it exists."
                ),
            )
        )


def check_coverage_hint_syntax(
    project_path: Path, architecture_path: Path, text: str, issues: list[Issue]
) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if COVERAGE_HINT_TOKEN not in line:
            continue
        if COVERAGE_HINT_PATTERN.search(line):
            continue
        issues.append(
            issue(
                "error",
                "architecture.coverage_hint_invalid",
                project_path,
                "architecture coverage hint is malformed",
                architecture_path,
                line=line_number,
                found=line.strip(),
                expected=(
                    "<!-- harnesskit:coverage=direct-children --> or "
                    "<!-- harnesskit:coverage=direct-children ignore=path -->"
                ),
                suggested_fix=(
                    "Use a complete HTML comment coverage hint on the same line "
                    "as the Markdown link."
                ),
            )
        )


def collect_architecture_links(
    project_path: Path, architecture_path: Path, text: str
) -> list[ArchitectureLink]:
    links: list[ArchitectureLink] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        coverage, ignored_paths = parse_coverage_hint(line)
        for match in MARKDOWN_LINK_PATTERN.finditer(line):
            target = normalize_markdown_link(match.group(1).strip())
            if target is None:
                continue
            path = architecture_link_path(project_path, architecture_path, target)
            if path is None:
                continue
            links.append(
                ArchitectureLink(
                    path=path,
                    line=line_number,
                    coverage=coverage,
                    ignored_paths=ignored_paths,
                )
            )

    return links


def parse_coverage_hint(line: str) -> tuple[str | None, tuple[str, ...]]:
    match = COVERAGE_HINT_PATTERN.search(line)
    if match is None:
        return None, ()

    coverage = match.group("coverage").strip()
    attrs = match.group("attrs")
    ignored_paths: list[str] = []
    ignore_match = IGNORE_HINT_PATTERN.search(attrs)
    if ignore_match is not None:
        ignored_paths = [
            normalize_architecture_path(value)
            for value in ignore_match.group("value").strip("\"'").split(",")
            if value.strip()
        ]

    return coverage, tuple(ignored_paths)


def architecture_link_path(
    project_path: Path, architecture_path: Path, target: Path
) -> str | None:
    if target.is_absolute():
        resolved = project_path / str(target).lstrip("/")
    else:
        resolved = architecture_path.parent / target

    try:
        relative = resolved.resolve().relative_to(project_path.resolve())
    except ValueError:
        return None

    return normalize_architecture_path(str(relative))


def collect_project_file_paths(project_path: Path) -> set[str]:
    git_files = collect_git_file_paths(project_path)
    if git_files is not None:
        return git_files

    ignored_dirs = {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "node_modules",
    }
    files: set[str] = set()
    for path in project_path.rglob("*"):
        relative_parts = path.relative_to(project_path).parts
        if any(part in ignored_dirs for part in relative_parts):
            continue
        if path.is_file():
            files.add(normalize_architecture_path(str(path.relative_to(project_path))))
    return files


def collect_git_file_paths(project_path: Path) -> set[str] | None:
    if not (project_path / ".git").exists() or not shutil.which("git"):
        return None

    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=project_path,
        text=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        return None

    return {
        normalize_architecture_path(raw_path.decode("utf-8"))
        for raw_path in result.stdout.split(b"\0")
        if raw_path
    }


def direct_children_under(project_files: set[str], directory_path: str) -> set[str]:
    directory_prefix = directory_path.rstrip("/") + "/"
    children: set[str] = set()
    for file_path in project_files:
        if not file_path.startswith(directory_prefix):
            continue
        remaining = file_path[len(directory_prefix) :]
        first_part = remaining.split("/", 1)[0]
        children.add(directory_prefix + first_part)
    return children


def architecture_path_ignored(path: str, ignored_paths: set[str]) -> bool:
    return any(
        path == ignored or fnmatch.fnmatch(path, ignored) for ignored in ignored_paths
    )


def normalize_architecture_path(path: str) -> str:
    return path.strip().strip("`").strip("\"'").rstrip("/")
