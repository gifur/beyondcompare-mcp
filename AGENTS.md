# beyondcompare-mcp - Agent Guide

## Overview

Local stdio MCP server for Beyond Compare file and directory comparison.

## Entry Point

- `uv run beyondcompare-mcp` -> `beyondcompare_mcp.cli:main`

## Scope

- stdio transport only
- FastMCP tool registration in `src/beyondcompare_mcp/server.py`
- 13 atomic tools are the supported MCP surface
- MCP prompts and one resource skill are kept as small learning examples
- No HTTP gateway, web dashboard, native wrapper, MCPB packaging, or agentic sampling layer

## Key Files

- `README.md` - local usage and tool list
- `pyproject.toml` - build config and command entry point
- `src/beyondcompare_mcp/server.py` - MCP server and tool implementations
- `src/beyondcompare_mcp/cli.py` - stdio command entry
- `src/beyondcompare_mcp/prompts.py` - MCP prompt examples
- `src/beyondcompare_mcp/skills.py` - MCP resource example
