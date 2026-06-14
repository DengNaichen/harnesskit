"""Command-line entry point for harnesskit."""

from __future__ import annotations

from typing import Annotated

import typer
from rich.console import Console

from . import __version__
from .init import DEFAULT_INTEGRATION, InitError, available_integrations, init_project, install_integration


app = typer.Typer(
    name="harnesskit",
    help="HarnessKit Context Harness CLI and Codex-facing toolkit.",
    add_completion=False,
)
integration_app = typer.Typer(help="Manage agent integrations.", add_completion=False)
app.add_typer(integration_app, name="integration")
console = Console()


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"harnesskit {__version__}")
        raise typer.Exit()


@app.callback()
def callback(
    version: Annotated[
        bool,
        typer.Option("--version", "-V", callback=_version_callback, is_eager=True, help="Show version and exit."),
    ] = False,
) -> None:
    """HarnessKit Context Harness CLI and Codex-facing toolkit."""


@app.command("init")
def init_command(
    project: Annotated[
        str | None,
        typer.Argument(help="Project directory, or '.' for the current directory."),
    ] = None,
    here: Annotated[bool, typer.Option("--here", help="Initialize the current directory.")] = False,
    force: Annotated[bool, typer.Option("--force", help="Overwrite existing generated files.")] = False,
    integration: Annotated[
        str,
        typer.Option("--integration", help="Agent integration to install. Currently only 'codex' is supported."),
    ] = DEFAULT_INTEGRATION,
) -> None:
    """Initialize a Context Harness from bundled templates."""
    try:
        result = init_project(project, here=here, force=force, integration=integration)
    except InitError as exc:
        console.print(f"[red]error:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(f"Initialized [green]{result.project_path}[/green]")
    _print_result_files(result)


@integration_app.command("list")
def integration_list_command() -> None:
    """List supported agent integrations."""
    console.print("Available integrations:")
    for integration in available_integrations():
        default_label = " [dim](default)[/dim]" if integration == DEFAULT_INTEGRATION else ""
        console.print(f"  [cyan]{integration}[/cyan]{default_label}")


@integration_app.command("install")
def integration_install_command(
    integration: Annotated[str, typer.Argument(help="Integration key to install. Currently only 'codex'.")],
    force: Annotated[bool, typer.Option("--force", help="Overwrite existing integration files.")] = False,
) -> None:
    """Install an agent integration into the current harnesskit project."""
    try:
        result = install_integration(".", integration, force=force)
    except InitError as exc:
        console.print(f"[red]error:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(f"Installed [cyan]{integration}[/cyan] integration in [green]{result.project_path}[/green]")
    _print_result_files(result)


def _print_result_files(result) -> None:
    if result.created:
        console.print("Written:")
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
