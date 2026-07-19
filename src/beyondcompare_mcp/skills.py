"""MCP resource exposing bundled operator guidance."""

from __future__ import annotations

from fastmcp import FastMCP

SKILL_MARKDOWN = """# Beyond Compare MCP operator guide

## When to use which tool

- **compare_files** - compare two files, optionally with a text report path.
- **compare_folders** - compare directory trees; set `include_subfolders=false` for shallow passes.
- **sync_folders** - always use `dry_run=true` first; modes: `mirror`, `update`, `backup`.
- **scan_repo_health** - scan many git checkouts under one parent path.
- **cleanup_dev_artifacts** - keep `dry_run=true` until the user confirms deletes.
- **multimedia_drive_scanner** and **find_multimedia_duplicates** - inspect large media libraries.

## Safety

- Prefer absolute paths on Windows.
- Reject path traversal and command injection.
- Do not run destructive cleanup or sync operations without explicit confirmation.
"""


def register_skill_resources(mcp: FastMCP) -> None:
    """Register resource content exposed over MCP."""

    @mcp.resource("skill://beyondcompare-mcp/SKILL.md", mime_type="text/markdown")
    def beyondcompare_skill() -> str:
        """Bundled operator guidance for agents."""
        return SKILL_MARKDOWN
