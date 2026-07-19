# Beyond Compare MCP

Local stdio MCP server for Beyond Compare file, folder, multimedia, and developer-workspace tools.

This repository is intentionally scoped for learning and local use:

- Transport: stdio only
- Runtime: Python + FastMCP
- Entry point: `uv run beyondcompare-mcp`
- Tool surface: 13 atomic MCP tools
- Learning extras: MCP prompts and one resource skill

## Quick Start

```powershell
uv sync --extra dev
uv run beyondcompare-mcp
```

For Claude Desktop, add this server to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "beyondcompare-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "D:/OpenSources/beyondcompare-mcp",
        "run",
        "beyondcompare-mcp"
      ]
    }
  }
}
```

## Configuration

Beyond Compare is auto-detected from common install locations. You can override it:

```powershell
$env:BEYOND_COMPARE_PATH = "C:\Program Files\Beyond Compare 5\BCompare.exe"
$env:BC_SCRIPTS_DIR = "D:\Temp\bc_scripts"
$env:LOG_LEVEL = "INFO"
```

## Core Files

- `pyproject.toml` - package metadata, dependencies, and `beyondcompare-mcp` command.
- `src/beyondcompare_mcp/cli.py` - command-line entry point.
- `src/beyondcompare_mcp/server.py` - FastMCP server and 13 tool registrations.
- `src/beyondcompare_mcp/config.py` - environment-backed settings.
- `src/beyondcompare_mcp/exceptions.py` - project exceptions.
- `src/beyondcompare_mcp/prompts.py` - MCP prompt examples.
- `src/beyondcompare_mcp/skills.py` - MCP resource example.
- `src/beyondcompare_mcp/multimedia_scanner.py` - multimedia drive scanning logic.
- `src/beyondcompare_mcp/tools/developer/` - repository backup, analysis, health, and duplicate-code logic.

## Tools

Comparison and sync:

- `compare_files`
- `compare_folders`
- `sync_folders`

Multimedia and drives:

- `multimedia_drive_scanner`
- `find_multimedia_duplicates`
- `detect_usb_drives`

Developer workspace:

- `backup_dev_repositories`
- `analyze_dev_workspace`
- `scan_repo_health`
- `cleanup_dev_artifacts`
- `find_duplicate_code`
- `compare_workspace_snapshots`
- `selective_restore`

## Prompts And Resource

The stdio server also keeps small examples of non-tool MCP capabilities:

- Prompts: `beyondcompare_quick_start`, `beyondcompare_backup_sync`, `beyondcompare_multimedia_inventory`
- Resource: `skill://beyondcompare-mcp/SKILL.md`

## Development

```powershell
uv run python -m pytest tests -q --ignore=tests/test_integration.py
uv run ruff check .
uv run ruff format .
```

## Requirements

- Python 3.12+
- `uv`
- Beyond Compare 4+ or 5
