# beyondcompare-mcp - Claude Code Guide

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
- `AGENTS.md` - OpenAI Codex agent context
