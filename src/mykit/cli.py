"""Command-line entry point for mykit."""

from __future__ import annotations

from typing import Annotated

import typer
from rich.console import Console

from . import __version__
from .init import InitError, init_project


app = typer.Typer(
    name="mykit",
    help="Minimal project initializer.",
    add_completion=False,
)
console = Console()


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"mykit {__version__}")
        raise typer.Exit()


@app.callback()
def callback(
    version: Annotated[
        bool,
        typer.Option("--version", "-V", callback=_version_callback, is_eager=True, help="Show version and exit."),
    ] = False,
) -> None:
    """Minimal project initializer."""


@app.command("init")
def init_command(
    project: Annotated[
        str | None,
        typer.Argument(help="Project directory, or '.' for the current directory."),
    ] = None,
    here: Annotated[bool, typer.Option("--here", help="Initialize the current directory.")] = False,
    force: Annotated[bool, typer.Option("--force", help="Overwrite existing generated files.")] = False,
) -> None:
    """Create a project from bundled templates."""
    try:
        result = init_project(project, here=here, force=force)
    except InitError as exc:
        console.print(f"[red]error:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(f"Initialized [green]{result.project_path}[/green]")
    if result.created:
        console.print("Created:")
        for path in result.created:
            console.print(f"  {path.relative_to(result.project_path)}")
    if result.skipped:
        console.print("Skipped existing files:")
        for path in result.skipped:
            console.print(f"  {path.relative_to(result.project_path)}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
