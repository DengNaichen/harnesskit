"""Project initialization logic."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, StrictUndefined, TemplateError


JINJA_TEMPLATE_SUFFIX = ".j2"
JINJA_ENV = Environment(
    autoescape=False,
    keep_trailing_newline=True,
    undefined=StrictUndefined,
)


class InitError(Exception):
    """Raised when project initialization cannot continue."""


@dataclass(frozen=True)
class InitResult:
    project_path: Path
    created: list[Path]
    skipped: list[Path]


def init_project(project: str | None, *, here: bool = False, force: bool = False) -> InitResult:
    project_path = _resolve_project_path(project, here=here)
    template_root = _locate_templates()

    if project_path.exists() and not project_path.is_dir():
        raise InitError(f"{project_path} exists but is not a directory")

    project_path.mkdir(parents=True, exist_ok=True)

    created: list[Path] = []
    skipped: list[Path] = []
    context = {"PROJECT_NAME": project_path.name}

    for source in sorted(template_root.rglob("*")):
        if source.is_dir():
            continue

        relative_path = source.relative_to(template_root)
        relative_path = _template_output_path(relative_path)
        destination = project_path / relative_path

        if destination.exists() and not force:
            skipped.append(destination)
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        _copy_template(source, destination, context)
        created.append(destination)

    return InitResult(project_path=project_path, created=created, skipped=skipped)


def _resolve_project_path(project: str | None, *, here: bool) -> Path:
    if project == ".":
        here = True
        project = None

    if here and project:
        raise InitError("pass either a project name or --here, not both")

    if here:
        return Path.cwd()

    if not project:
        raise InitError("missing project name; pass a name, '.', or --here")

    return Path(project).expanduser().resolve()


def _locate_templates() -> Path:
    package_templates = Path(__file__).parent / "templates"
    if package_templates.is_dir():
        return package_templates

    source_templates = Path(__file__).resolve().parents[2] / "templates"
    if source_templates.is_dir():
        return source_templates

    raise InitError("bundled templates were not found")


def _template_output_path(path: Path) -> Path:
    if path.name.endswith(JINJA_TEMPLATE_SUFFIX):
        return path.with_name(path.name[: -len(JINJA_TEMPLATE_SUFFIX)])
    return path


def _copy_template(source: Path, destination: Path, context: dict[str, str]) -> None:
    if source.name.endswith(JINJA_TEMPLATE_SUFFIX):
        text = source.read_text(encoding="utf-8")
        try:
            rendered = JINJA_ENV.from_string(text).render(context)
        except TemplateError as exc:
            raise InitError(f"failed to render template {source}: {exc}") from exc
        destination.write_text(rendered, encoding="utf-8")
        return

    shutil.copy2(source, destination)
