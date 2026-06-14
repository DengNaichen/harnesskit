"""Architecture map coverage checks."""

from __future__ import annotations

import fnmatch
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .constants import (
    ARCHITECTURE_MAP_END,
    ARCHITECTURE_MAP_START,
    MARKDOWN_LINK_PATTERN,
)
from .issues import issue
from .markdown import extract_marked_blocks_with_lines, normalize_markdown_link
from .models import Issue, MarkedBlock


@dataclass(frozen=True)
class ArchitectureMapEntry:
    path: str
    coverage: str
    ignored_paths: tuple[str, ...]


def check_architecture_map(project_path: Path, issues: list[Issue]) -> None:
    architecture_path = project_path / "ARCHITECTURE.md"
    if not architecture_path.is_file():
        return

    text = architecture_path.read_text(encoding="utf-8")
    blocks = extract_marked_blocks_with_lines(
        project_path,
        architecture_path,
        text,
        ARCHITECTURE_MAP_START,
        ARCHITECTURE_MAP_END,
        "markdown.architecture_map.unpaired",
        issues,
    )
    if not blocks:
        if ARCHITECTURE_MAP_START in text or ARCHITECTURE_MAP_END in text:
            return
        issues.append(
            issue(
                "error",
                "architecture.map_missing",
                project_path,
                "ARCHITECTURE.md must include a harnesskit:architecture-map block",
                architecture_path,
                expected=f"add {ARCHITECTURE_MAP_START} / {ARCHITECTURE_MAP_END}",
                suggested_fix=architecture_map_suggestion(),
            )
        )
        return

    declared_entries: list[ArchitectureMapEntry] = []
    for block in blocks:
        declared_entries.extend(
            parse_architecture_map_entries(
                project_path, architecture_path, block, issues
            )
        )

    if not declared_entries:
        return

    declared_paths = {
        normalize_architecture_path(entry.path) for entry in declared_entries
    }
    markdown_paths = architecture_markdown_paths(project_path, architecture_path)
    covered_paths = declared_paths | markdown_paths
    project_files = collect_project_file_paths(project_path)

    for entry in declared_entries:
        normalized_path = normalize_architecture_path(entry.path)
        absolute_path = project_path / normalized_path
        if not absolute_path.exists():
            issues.append(
                issue(
                    "error",
                    "architecture.path_missing",
                    project_path,
                    "architecture map declares a path that does not exist",
                    architecture_path,
                    found=entry.path,
                    expected="declared architecture paths must exist in the repository",
                    suggested_fix="Update the architecture map path or restore the missing file.",
                )
            )
            continue

        if entry.coverage == "directory" and not absolute_path.is_dir():
            issues.append(
                issue(
                    "error",
                    "architecture.coverage_invalid",
                    project_path,
                    "architecture map declares directory coverage for a non-directory path",
                    architecture_path,
                    found=entry.path,
                    expected="use coverage: file for files",
                )
            )
            continue

        if entry.coverage == "file" and not absolute_path.is_file():
            issues.append(
                issue(
                    "error",
                    "architecture.coverage_invalid",
                    project_path,
                    "architecture map declares file coverage for a non-file path",
                    architecture_path,
                    found=entry.path,
                    expected="use coverage: directory or coverage: direct-children for directories",
                )
            )
            continue

        if entry.coverage != "direct-children":
            continue

        if not absolute_path.is_dir():
            issues.append(
                issue(
                    "error",
                    "architecture.coverage_invalid",
                    project_path,
                    "architecture map declares direct-children coverage for a non-directory path",
                    architecture_path,
                    found=entry.path,
                    expected="direct-children coverage requires a directory path",
                )
            )
            continue

        ignored_paths = {
            normalize_architecture_path(ignored_path)
            for ignored_path in entry.ignored_paths
        }
        for child_path in sorted(direct_children_under(project_files, normalized_path)):
            if architecture_path_ignored(child_path, ignored_paths):
                continue
            if child_path in covered_paths:
                continue
            issues.append(
                issue(
                    "error",
                    "architecture.coverage_missing",
                    project_path,
                    "architecture map does not cover a direct child path",
                    architecture_path,
                    found=child_path,
                    expected=f"add `- path: {child_path}` to the architecture map or list it under ignore",
                    evidence=[
                        f"{entry.path} declares coverage: direct-children",
                        f"{child_path} exists in the repository",
                    ],
                    suggested_fix=(
                        f"Document `{child_path}` in ARCHITECTURE.md, or add it to "
                        f"`ignore` under `{entry.path}` if it should stay out of the map."
                    ),
                )
            )


def parse_architecture_map_entries(
    project_path: Path,
    architecture_path: Path,
    block: MarkedBlock,
    issues: list[Issue],
) -> list[ArchitectureMapEntry]:
    entries: list[ArchitectureMapEntry] = []
    current_path: str | None = None
    current_coverage = "directory"
    current_ignored_paths: list[str] = []
    in_ignore_list = False

    def finish_current_entry() -> None:
        nonlocal current_path, current_coverage, current_ignored_paths
        if current_path is None:
            return
        if current_coverage not in {"directory", "direct-children", "file"}:
            issues.append(
                issue(
                    "error",
                    "architecture.coverage_invalid",
                    project_path,
                    "architecture map entry uses an unsupported coverage mode",
                    architecture_path,
                    line=block.start_line,
                    found=f"{current_path}: {current_coverage}",
                    expected="coverage must be directory, direct-children, or file",
                )
            )
        else:
            entries.append(
                ArchitectureMapEntry(
                    path=current_path,
                    coverage=current_coverage,
                    ignored_paths=tuple(current_ignored_paths),
                )
            )
        current_path = None
        current_coverage = "directory"
        current_ignored_paths = []

    for line in block.content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- path:"):
            finish_current_entry()
            current_path = clean_architecture_value(stripped.removeprefix("- path:"))
            current_coverage = "directory"
            current_ignored_paths = []
            in_ignore_list = False
            continue
        if current_path is None:
            continue
        if stripped.startswith("coverage:"):
            current_coverage = clean_architecture_value(
                stripped.removeprefix("coverage:")
            )
            in_ignore_list = False
            continue
        if stripped == "ignore:":
            in_ignore_list = True
            continue
        if in_ignore_list and stripped.startswith("- "):
            current_ignored_paths.append(clean_architecture_value(stripped[2:]))

    finish_current_entry()
    return entries


def architecture_markdown_paths(
    project_path: Path, architecture_path: Path
) -> set[str]:
    paths: set[str] = set()
    text = architecture_path.read_text(encoding="utf-8")
    for match in MARKDOWN_LINK_PATTERN.finditer(text):
        target = normalize_markdown_link(match.group(1).strip())
        if target is None:
            continue
        if target.is_absolute():
            resolved = project_path / str(target).lstrip("/")
        else:
            resolved = architecture_path.parent / target
        try:
            relative = resolved.resolve().relative_to(project_path.resolve())
        except ValueError:
            continue
        paths.add(normalize_architecture_path(str(relative)))
    return paths


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


def clean_architecture_value(value: str) -> str:
    return value.strip().strip("`").strip("\"'")


def normalize_architecture_path(path: str) -> str:
    return path.strip().strip("`").strip("\"'").rstrip("/")


def architecture_map_suggestion() -> str:
    return (
        "Add an architecture map block with entries like "
        f"`{ARCHITECTURE_MAP_START}`, `- path: src/harnesskit/`, "
        "`coverage: direct-children`, then close it with "
        f"`{ARCHITECTURE_MAP_END}`."
    )
