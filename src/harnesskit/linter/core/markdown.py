"""Shared Markdown parsing helpers."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote, urldefrag, urlparse

from .issues import issue
from .models import Issue, MarkedBlock


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


def normalize_markdown_link(raw_target: str) -> Path | None:
    target_without_fragment, _fragment = urldefrag(raw_target)
    if not target_without_fragment:
        return None

    parsed = urlparse(target_without_fragment)
    if parsed.scheme or target_without_fragment.startswith("#"):
        return None

    return Path(unquote(target_without_fragment))
