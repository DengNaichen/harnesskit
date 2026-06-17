#!/usr/bin/env bash
set -euo pipefail
set +x

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

read -r PACKAGE_NAME PACKAGE_VERSION PACKAGE_STEM < <(
  uv run python - <<'PY'
import re
import tomllib
from pathlib import Path

project = tomllib.loads(Path("pyproject.toml").read_text())["project"]
name = project["name"]
version = project["version"]
stem = re.sub(r"[-_.]+", "_", name)
print(name, version, stem)
PY
)

TOKEN="$(
  uv run python - <<'PY'
import os
import re
from pathlib import Path

token = os.environ.get("UV_PUBLISH_TOKEN")
if token:
    print(token)
    raise SystemExit

env_path = Path(".env")
if not env_path.exists():
    raise SystemExit

text = env_path.read_text()
for raw_line in text.splitlines():
    line = raw_line.strip()
    if not line or line.startswith("#"):
        continue
    if line.startswith("export "):
        line = line[len("export ") :].lstrip()
    if "=" not in line:
        continue
    key, value = line.split("=", 1)
    if key.strip() in {"UV_PUBLISH_TOKEN", "PYPI_TOKEN"}:
        print(value.strip().strip("\"'"))
        raise SystemExit

match = re.search(r"pypi-[A-Za-z0-9_-]+", text)
if match:
    print(match.group(0))
PY
)"

if [ -z "$TOKEN" ]; then
  echo "Missing PyPI token. Set UV_PUBLISH_TOKEN or put a pypi-... token in .env." >&2
  exit 64
fi

echo "Verifying repository before publishing ${PACKAGE_NAME} ${PACKAGE_VERSION}..."
make verify

echo "Building clean distributions..."
rm -rf dist
uv build

shopt -s nullglob
FILES=(
  "dist/${PACKAGE_STEM}-${PACKAGE_VERSION}.tar.gz"
  "dist/${PACKAGE_STEM}-${PACKAGE_VERSION}-"*.whl
)

if [ "${#FILES[@]}" -ne 2 ]; then
  echo "Expected exactly one sdist and one wheel for ${PACKAGE_NAME} ${PACKAGE_VERSION}." >&2
  printf 'Found: %s\n' "${FILES[@]}" >&2
  exit 65
fi

echo "Publishing ${PACKAGE_NAME} ${PACKAGE_VERSION} to PyPI..."
UV_PUBLISH_TOKEN="$TOKEN" uv publish --check-url https://pypi.org/simple/ "${FILES[@]}"
