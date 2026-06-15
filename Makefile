.PHONY: verify verify-core links lint format test build hooks

verify:
	uv run python .agents/skills/code-change-verification/scripts/run_validation.py

verify-core: links lint format test build

links:
	lychee './**/*.md'

lint:
	uv run ruff check .

format:
	uv run ruff format --check .

test:
	uv run pytest

build:
	uv build
	rm -rf dist

hooks:
	uv run pre-commit run --all-files
