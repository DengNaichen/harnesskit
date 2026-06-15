"""Run the repository guard suite and write a lightweight receipt."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from shlex import join as shell_join
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
RECEIPTS_DIR = REPO_ROOT / ".harnesskit" / "receipts"
RUNS_DIR = RECEIPTS_DIR / "runs"


@dataclass(frozen=True)
class Check:
    name: str
    command: tuple[str, ...]


CHECKS = (
    Check("markdown links", ("lychee", "./**/*.md")),
    Check("python lint", ("uv", "run", "ruff", "check", ".")),
    Check("python format", ("uv", "run", "ruff", "format", "--check", ".")),
    Check("tests", ("uv", "run", "pytest")),
    Check("package build", ("uv", "build")),
    Check("pre-commit hooks", ("uv", "run", "pre-commit", "run", "--all-files")),
)


def run_text(command: tuple[str, ...]) -> str | None:
    try:
        result = subprocess.run(
            command,
            cwd=REPO_ROOT,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except FileNotFoundError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def git_info() -> dict[str, Any]:
    commit = run_text(("git", "rev-parse", "--short", "HEAD"))
    status = run_text(("git", "status", "--porcelain"))
    return {
        "commit": commit,
        "dirty": bool(status),
    }


def safe_run_id(started_at: datetime) -> str:
    return started_at.isoformat(timespec="seconds").replace(":", "-")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    tmp_path.replace(path)


def cleanup_build_artifacts() -> None:
    shutil.rmtree(REPO_ROOT / "dist", ignore_errors=True)


def run_check(check: Check) -> dict[str, Any]:
    print(f"\n==> {check.name}: {shell_join(check.command)}", flush=True)
    started = time.monotonic()
    try:
        result = subprocess.run(check.command, cwd=REPO_ROOT, check=False)
        exit_code = result.returncode
    except FileNotFoundError as error:
        print(f"Command not found: {error.filename}", file=sys.stderr, flush=True)
        exit_code = 127
    duration = round(time.monotonic() - started, 3)

    if check.name == "package build":
        cleanup_build_artifacts()

    return {
        "name": check.name,
        "command": shell_join(check.command),
        "status": "passed" if exit_code == 0 else "failed",
        "exit_code": exit_code,
        "duration_seconds": duration,
    }


def main() -> int:
    started_at = datetime.now().astimezone()
    run_id = safe_run_id(started_at)
    checks: list[dict[str, Any]] = []
    status = "passed"

    for check in CHECKS:
        check_result = run_check(check)
        checks.append(check_result)
        if check_result["exit_code"] != 0:
            status = "failed"
            break

    finished_at = datetime.now().astimezone()
    receipt = {
        "schema_version": 1,
        "type": "guard",
        "run_id": run_id,
        "started_at": started_at.isoformat(timespec="seconds"),
        "finished_at": finished_at.isoformat(timespec="seconds"),
        "entrypoint": "make verify",
        "status": status,
        "git": git_info(),
        "checks": checks,
    }

    run_path = RUNS_DIR / f"{run_id}.json"
    latest_path = RECEIPTS_DIR / "latest.json"
    write_json(run_path, receipt)
    write_json(latest_path, receipt)

    print(f"\nGuard receipt: {run_path.relative_to(REPO_ROOT)}", flush=True)
    print(f"Guard status: {status}", flush=True)
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
