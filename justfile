set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]

# Show available commands
default:
    @just --list

# ── Quality ───────────────────────────────────────────────────────────────────

# Execute Ruff SOTA v13.1 linting
lint:
    Set-Location '{{justfile_directory()}}'
    uv run ruff check .

# Execute Ruff SOTA v13.1 fix and formatting
fix:
    Set-Location '{{justfile_directory()}}'
    uv run ruff check . --fix --unsafe-fixes
    uv run ruff format .

# ── Tests ─────────────────────────────────────────────────────────────────────

# Run pytest (excludes heavy integration suite)
test:
    Set-Location '{{justfile_directory()}}'
    uv sync --extra dev
    uv run python -m pytest tests -q --ignore=tests/test_integration.py
