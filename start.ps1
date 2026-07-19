$env:FASTMCP_LOG_LEVEL = 'WARNING'

Set-Location $PSScriptRoot
uv run beyondcompare-mcp
