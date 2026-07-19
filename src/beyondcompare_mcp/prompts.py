"""Native FastMCP prompts for Beyond Compare MCP."""

from __future__ import annotations

from fastmcp import FastMCP


def register_prompts(mcp: FastMCP) -> None:
    """Register prompts exposed over MCP."""

    @mcp.prompt()
    def beyondcompare_quick_start(workspace_root: str = "D:/Dev/repos") -> str:
        """How to compare folders and run repo health with this MCP server."""
        return f"""You are helping a developer use Beyond Compare MCP.

1. Ensure Beyond Compare 4+ is installed. Optional: set BEYOND_COMPARE_PATH to BCompare.exe.
2. For a quick folder diff: call compare_folders(left_path, right_path, include_subfolders=true).
3. For repo hygiene across clones: call scan_repo_health(repos_path='{workspace_root}').
4. For sync operations: always call sync_folders(..., dry_run=true) before making changes."""

    @mcp.prompt()
    def beyondcompare_backup_sync() -> str:
        """Plan backup and sync using BC-backed tools."""
        return """Plan a safe backup or sync:

1. Optionally analyze_dev_workspace(workspace_path) for size and languages.
2. For directory sync, use sync_folders with dry_run=true first.
3. For full-tree backups, backup_dev_repositories with dry_run=true first.
4. Never delete data without explicit user confirmation; prefer dry_run and reports."""

    @mcp.prompt()
    def beyondcompare_multimedia_inventory() -> str:
        """Drive scan and duplicate workflow for multimedia tools."""
        return """Multimedia workflow:

1. Run multimedia_drive_scanner() to refresh inventory.
2. Run find_multimedia_duplicates(use_content_hash=false) for a fast pass.
3. Use use_content_hash=true only when accuracy matters more than speed.
4. Use detect_usb_drives before copying large sets to removable media."""
