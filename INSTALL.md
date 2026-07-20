# Install

## Prerequisites

- Python 3.10+
- `uv`
- Beyond Compare 4+ or 5

## Install Dependencies

```powershell
uv sync --extra dev
```

## Run Locally

```powershell
uv run beyondcompare-mcp
```

The server uses stdio, so it normally runs under an MCP client such as Claude Desktop.

## Claude Desktop Config

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

## Optional Environment Variables

```powershell
$env:BEYOND_COMPARE_PATH = "C:\Program Files\Beyond Compare 5\BCompare.exe"
$env:BC_SCRIPTS_DIR = "D:\Temp\bc_scripts"
$env:LOG_LEVEL = "INFO"
```
