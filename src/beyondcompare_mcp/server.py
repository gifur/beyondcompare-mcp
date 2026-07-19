"""
Beyond Compare MCP Server

A Model Context Protocol (MCP) server that provides file and directory comparison
capabilities using Beyond Compare. Built with modern MCP 2.11+ standards.
"""

# CRITICAL: Set stdio to binary mode on Windows for Antigravity IDE compatibility
# MUST be done BEFORE any imports that might use stdout
# Antigravity IDE is strict about JSON-RPC protocol and interprets trailing \r as "invalid trailing data"
# Binary mode prevents Python from automatically converting line endings
import sys
import os
import warnings

if os.name == "nt":  # Windows
    try:
        import msvcrt

        # Set stdin/stdout to binary mode to prevent line ending conversion
        # This fixes "invalid trailing data" errors with Antigravity IDE
        # Use try/except to handle cases where fileno() doesn't exist or isn't callable
        try:
            msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        except (OSError, AttributeError):
            pass  # stdin might not be a real file descriptor or already patched
        try:
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        except (OSError, AttributeError):
            pass  # stdout might not be a real file descriptor or already patched
    except (ImportError, OSError, AttributeError):
        pass  # If msvcrt is not available, continue anyway

# Detect if we're running in stdio mode (MCP server)
_is_stdio_mode = (
    not sys.stdout.isatty()
    or os.getenv("MCP_STDIO_MODE", "").lower() == "true"
    or "stdio" in sys.argv
    or __name__ == "__main__"
)

if _is_stdio_mode:
    # CRITICAL: Patch stdout to prevent ANY writes during initialization
    # This catches print statements, Rich console, FastMCP banners, etc.
    if not hasattr(sys, "_original_stdout"):

        class DevNullStdout:
            """A file-like object that discards all writes (like /dev/null)."""

            def write(self, s: str) -> int:
                # Discard all writes to stdout - they would break JSON-RPC
                return len(s)

            def flush(self) -> None:
                pass

            def isatty(self) -> bool:
                return False

            def readable(self) -> bool:
                return False

            def writable(self) -> bool:
                return True

            def seekable(self) -> bool:
                return False

            @property
            def buffer(self):
                import io

                if not hasattr(self, "_bytes"):
                    self._bytes = io.BytesIO()
                return self._bytes

            @property
            def encoding(self) -> str:
                return "utf-8"

            @property
            def errors(self) -> str:
                return "strict"

        # Store original stdout and replace with null device
        # This will be restored before FastMCP.run()
        sys._original_stdout = sys.stdout
        sys.stdout = DevNullStdout()

    # Suppress deprecation warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # Configure Python's logging module to prevent stdout pollution
    # FastMCP uses Python's logging module internally
    import logging

    logging.basicConfig(
        level=logging.CRITICAL,  # Only show CRITICAL (suppress everything else)
        format="%(message)s",
        stream=sys.stderr,  # Send to stderr, not stdout
        force=True,  # Override any existing configuration
    )

    # Suppress ALL loggers to prevent any output
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.CRITICAL)
    root_logger.handlers = []

    # Suppress FastMCP and other noisy loggers completely
    for logger_name in [
        "fastmcp",
        "mcp",
        "asyncio",
    ]:
        log = logging.getLogger(logger_name)
        log.setLevel(logging.CRITICAL)
        log.handlers = []
        log.propagate = False
else:
    import logging

import asyncio
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from fastmcp import FastMCP

from .config import settings
from .exceptions import (
    BeyondCompareNotInstalledError,
    BeyondCompareCommandError,
    BeyondCompareTimeoutError,
    BeyondCompareScriptError,
)
from .multimedia_scanner import MultimediaDriveScanner
from .prompts import register_prompts
from .skills import register_skill_resources
from .tools.developer import (
    DevRepositoryBackup,
    WorkspaceAnalyzer,
    RepositoryHealthChecker,
    CodeDuplicateDetector,
)

logger = logging.getLogger(__name__)


class BeyondCompareMCP:
    """Beyond Compare MCP server implementation for local stdio clients."""

    def __init__(
        self,
        bc_path: Optional[str] = None,
        scripts_dir: Optional[str] = None,
        mcp: Optional[FastMCP] = None,
    ):
        """Initialize the Beyond Compare MCP server.

        Args:
            bc_path: Path to Beyond Compare executable
            scripts_dir: Directory for temporary script files
            mcp: Optional FastMCP instance; if omitted, a standalone instance is created
        """
        self.bc_path = self._find_bc_executable(bc_path)
        self.scripts_dir = Path(scripts_dir or settings.BC_SCRIPTS_DIR)
        self.scripts_dir.mkdir(parents=True, exist_ok=True)

        # Initialize multimedia scanner
        self.multimedia_scanner = MultimediaDriveScanner()

        # Initialize developer tools
        self.dev_backup = DevRepositoryBackup(self.bc_path)
        self.workspace_analyzer = WorkspaceAnalyzer(self.bc_path)
        self.health_checker = RepositoryHealthChecker(self.bc_path)
        self.duplicate_detector = CodeDuplicateDetector(self.bc_path)

        self.mcp = mcp if mcp is not None else FastMCP(name="Beyond Compare MCP")

        # Register MCP tools
        self._register_tools()
        register_prompts(self.mcp)
        register_skill_resources(self.mcp)

    def _find_bc_executable(self, bc_path: Optional[str] = None) -> Path:
        """Find the Beyond Compare executable."""
        # If a full path is provided (not just the executable name), verify it exists
        if bc_path and (
            Path(bc_path).is_absolute() or "/" in bc_path or "\\" in bc_path
        ):
            path = Path(bc_path).expanduser().resolve()
            if path.exists():
                return path
            raise BeyondCompareNotInstalledError(str(path))

        # Check common installation paths first
        if platform.system() == "Windows":
            program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
            common_paths = [
                Path(program_files) / "Beyond Compare 5" / "BCompare.exe",
                Path(program_files) / "Beyond Compare 4" / "BCompare.exe",
                Path(program_files) / "Beyond Compare 3" / "BCompare.exe",
                Path(program_files) / "Beyond Compare" / "BCompare.exe",
                Path("C:\\Program Files (x86)\\Beyond Compare 5\\BCompare.exe"),
                Path("C:\\Program Files (x86)\\Beyond Compare 4\\BCompare.exe"),
                Path("C:\\Program Files (x86)\\Beyond Compare 3\\BCompare.exe"),
            ]

            for path in common_paths:
                if path.exists():
                    return path

        # Check PATH for the executable name (provided or default)
        bc_exe = (
            bc_path
            if bc_path
            else ("BCompare.exe" if platform.system() == "Windows" else "bcompare")
        )
        which_bc = shutil.which(bc_exe)
        if which_bc:
            return Path(which_bc)

        # If we still haven't found it and a specific executable name was provided, also try the default
        if bc_path and bc_path != (
            "BCompare.exe" if platform.system() == "Windows" else "bcompare"
        ):
            default_exe = (
                "BCompare.exe" if platform.system() == "Windows" else "bcompare"
            )
            which_default = shutil.which(default_exe)
            if which_default:
                return Path(which_default)

        raise BeyondCompareNotInstalledError(
            f"Beyond Compare not found. Searched for: {bc_exe if bc_path else 'BCompare.exe'}"
        )

    def _register_tools(self) -> None:
        """Register MCP tools with FastMCP."""

        @self.mcp.tool()
        def compare_files(
            left_path: str,
            right_path: str,
            output_report: Optional[str] = None,
        ) -> Dict[str, Any]:
            """Compare two files using Beyond Compare.

            Performs a side-by-side comparison of two files using Beyond Compare's
            powerful comparison engine. Supports text, binary, and image files with
            automatic format detection. The comparison uses quick compare mode (size
            and timestamp) for fast results, but can generate detailed reports when
            requested.

            Prerequisites:
                - Beyond Compare must be installed and accessible
                - Both file paths must be valid and accessible
                - Files must exist (will return error if missing)

            Parameters:
                left_path: Path to the left file for comparison
                    - Required: Yes
                    - Can be absolute or relative path
                    - Supports Windows, macOS, and Linux path formats
                    - Example: 'C:/folder/file1.txt' or './file1.txt'

                right_path: Path to the right file for comparison
                    - Required: Yes
                    - Can be absolute or relative path
                    - Must be same file type as left_path for meaningful comparison
                    - Example: 'C:/folder/file2.txt' or './file2.txt'

                output_report: Optional path to save detailed comparison report (default: None)
                    - Optional: Yes
                    - If provided, generates text report with differences
                    - Parent directory will be created if it doesn't exist
                    - Example: 'C:/reports/comparison.txt'

            Returns:
                Dictionary containing:
                    - success: Boolean indicating if comparison completed successfully
                    - left_path: Resolved absolute path to left file
                    - right_path: Resolved absolute path to right file
                    - identical: Boolean indicating if files are identical (True if no differences)
                    - differences_found: Boolean indicating if differences were detected
                    - output_report: Path to report file if generated (None otherwise)
                    - message: Human-readable status message
                    - error: Error message string (only present if success is False)

            Usage:
                Use this tool to compare two files and determine if they are identical
                or identify differences between them. Ideal for verifying file integrity,
                checking if backups are current, or validating that files match expected
                versions. The quick compare mode uses file size and modification time
                for fast comparison, making it suitable for large files.

                Common scenarios:
                - Verify backup files match originals
                - Check if configuration files have changed
                - Compare different versions of the same file
                - Validate file integrity after transfer
                - Generate difference reports for documentation

                Best practices:
                - Use absolute paths for reliability
                - Generate reports for important comparisons
                - Check success field before using results
                - Use compare_folders for directory-level comparisons

            Examples:
                Basic file comparison:
                    result = compare_files(
                        left_path='C:/source/config.txt',
                        right_path='C:/backup/config.txt'
                    )
                    # Returns: {
                    #     'success': True,
                    #     'identical': False,
                    #     'differences_found': True,
                    #     'message': 'Differences found between files'
                    # }

                Compare with report generation:
                    result = compare_files(
                        left_path='C:/docs/manual_v1.txt',
                        right_path='C:/docs/manual_v2.txt',
                        output_report='C:/reports/manual_diff.txt'
                    )
                    # Returns: {
                    #     'success': True,
                    #     'identical': False,
                    #     'output_report': 'C:/reports/manual_diff.txt',
                    #     'message': 'Differences found between files'
                    # }

                Error handling - missing file:
                    result = compare_files(
                        left_path='C:/missing.txt',
                        right_path='C:/exists.txt'
                    )
                    # Returns: {
                    #     'success': False,
                    #     'error': 'Left file not found: C:/missing.txt'
                    # }

            Notes:
                - Comparison uses Beyond Compare's quick compare mode (/qc) for speed
                - Large files may take longer to compare
                - Binary files are compared byte-by-byte
                - Text files support encoding detection
                - Report generation adds overhead but provides detailed differences
                - Paths are validated and resolved before comparison
                - Command injection protection is applied to all paths

            See Also:
                - compare_folders: For comparing entire directory structures
                - sync_folders: For synchronizing folders based on differences
            """
            return self._compare_files(left_path, right_path, output_report)

        @self.mcp.tool()
        def compare_folders(
            left_path: str,
            right_path: str,
            output_report: Optional[str] = None,
            include_subfolders: bool = True,
        ) -> Dict[str, Any]:
            """Compare two folders using Beyond Compare.

            Performs a comprehensive comparison of two directory structures, identifying
            files that exist in one folder but not the other, files that differ between
            folders, and files that are identical. Supports recursive subfolder comparison
            and can generate detailed reports showing all differences. This is ideal for
            verifying backups, checking synchronization status, or identifying changes
            between directory versions.

            Prerequisites:
                - Beyond Compare must be installed and accessible
                - Both folder paths must be valid and accessible
                - Folders must exist (will return error if missing)
                - Sufficient permissions to read both directories

            Parameters:
                left_path: Path to the left folder for comparison
                    - Required: Yes
                    - Can be absolute or relative path
                    - Supports Windows, macOS, and Linux path formats
                    - Example: 'C:/source/project' or './project'

                right_path: Path to the right folder for comparison
                    - Required: Yes
                    - Can be absolute or relative path
                    - Should be similar structure to left_path for meaningful comparison
                    - Example: 'C:/backup/project' or './project_backup'

                output_report: Optional path to save detailed comparison report (default: None)
                    - Optional: Yes
                    - If provided, generates summary report with all differences
                    - Report includes file counts, size differences, and mismatch details
                    - Parent directory will be created if it doesn't exist
                    - Example: 'C:/reports/folder_comparison.txt'

                include_subfolders: Whether to recursively compare subfolders (default: True)
                    - Optional: Yes (default: True)
                    - True: Compares all nested directories recursively
                    - False: Only compares files in the top-level directory
                    - Set to False for faster comparison of shallow directory structures

            Returns:
                Dictionary containing:
                    - success: Boolean indicating if comparison completed successfully
                    - left_path: Resolved absolute path to left folder
                    - right_path: Resolved absolute path to right folder
                    - include_subfolders: Whether subfolders were included in comparison
                    - differences_found: Boolean indicating if any differences were detected
                    - output_report: Path to report file if generated (None otherwise)
                    - message: Human-readable status message
                    - error: Error message string (only present if success is False)

            Usage:
                Use this tool to compare two directory structures and identify differences
                between them. Perfect for verifying that backups are complete, checking
                synchronization status, identifying missing or changed files, or preparing
                for folder synchronization operations. The recursive comparison option
                allows you to control whether nested directories are included.

                Common scenarios:
                - Verify backup completeness and accuracy
                - Check if folders are synchronized
                - Identify files that have changed between versions
                - Find files that exist in one location but not another
                - Generate reports for documentation or auditing
                - Prepare for folder synchronization operations

                Best practices:
                - Use absolute paths for reliability
                - Generate reports for important comparisons
                - Set include_subfolders=False for shallow directories to save time
                - Review report before performing synchronization
                - Use compare_files for single file comparisons

            Examples:
                Basic folder comparison:
                    result = compare_folders(
                        left_path='C:/source/project',
                        right_path='C:/backup/project'
                    )
                    # Returns: {
                    #     'success': True,
                    #     'differences_found': True,
                    #     'include_subfolders': True,
                    #     'message': 'Differences found between folders'
                    # }

                Compare top-level only (faster):
                    result = compare_folders(
                        left_path='C:/docs',
                        right_path='D:/docs_backup',
                        include_subfolders=False
                    )
                    # Returns: {
                    #     'success': True,
                    #     'differences_found': False,
                    #     'include_subfolders': False,
                    #     'message': 'Folders are identical'
                    # }

                Compare with detailed report:
                    result = compare_folders(
                        left_path='C:/project_v1',
                        right_path='C:/project_v2',
                        output_report='C:/reports/version_diff.txt'
                    )
                    # Returns: {
                    #     'success': True,
                    #     'differences_found': True,
                    #     'output_report': 'C:/reports/version_diff.txt',
                    #     'message': 'Differences found between folders'
                    # }

                Error handling - missing folder:
                    result = compare_folders(
                        left_path='C:/nonexistent',
                        right_path='C:/exists'
                    )
                    # Returns: {
                    #     'success': False,
                    #     'error': 'Left folder not found: C:/nonexistent'
                    # }

            Notes:
                - Comparison uses Beyond Compare's folder comparison engine
                - Large directories may take significant time to compare
                - Recursive comparison (include_subfolders=True) processes all nested folders
                - Report generation includes summary statistics and file-level differences
                - Paths are validated and resolved before comparison
                - Command injection protection is applied to all paths
                - Comparison results are based on file size and modification time by default

            See Also:
                - compare_files: For comparing individual files
                - sync_folders: For synchronizing folders based on comparison results
            """
            return self._compare_folders(
                left_path, right_path, output_report, include_subfolders
            )

        @self.mcp.tool()
        def sync_folders(
            source_path: str,
            target_path: str,
            sync_mode: str = "mirror",
            dry_run: bool = True,
        ) -> Dict[str, Any]:
            """Synchronize folders using Beyond Compare.

            Synchronizes two folders using Beyond Compare's powerful synchronization
            engine. Supports three synchronization modes: mirror (exact copy), update
            (one-way sync), and backup (preserve existing). Includes a dry-run mode
            to preview changes before executing, making it safe to test synchronization
            operations. This tool is ideal for maintaining backups, keeping folders
            in sync, or preparing for deployment.

            Prerequisites:
                - Beyond Compare must be installed and accessible
                - Source folder must exist and be readable
                - Target folder will be created if it doesn't exist
                - Sufficient permissions to read source and write to target
                - Always use dry_run=True first to preview changes

            Parameters:
                source_path: Source directory path (left side, source of truth)
                    - Required: Yes
                    - Can be absolute or relative path
                    - This is the folder that will be copied FROM
                    - Example: 'C:/source/project' or './project'

                target_path: Target directory path (right side, destination)
                    - Required: Yes
                    - Can be absolute or relative path
                    - This is the folder that will be synchronized TO
                    - Will be created if it doesn't exist
                    - Example: 'C:/backup/project' or './project_backup'

                sync_mode: Synchronization mode (default: 'mirror')
                    - Optional: Yes (default: 'mirror')
                    - Valid values: 'mirror', 'update', 'backup'
                    - 'mirror': Exact copy - target matches source exactly (deletes extra files)
                    - 'update': One-way sync - copies new/changed files, preserves target-only files
                    - 'backup': Preserve existing - only copies files that don't exist in target
                    - Example: 'mirror' for exact backups, 'update' for incremental sync

                dry_run: Preview mode - show what would be done without executing (default: True)
                    - Optional: Yes (default: True)
                    - True: Preview changes only, no files are modified
                    - False: Actually perform the synchronization
                    - ALWAYS use True first to review changes before executing
                    - Example: Set to False only after reviewing dry_run results

            Returns:
                Dictionary containing:
                    - success: Boolean indicating if synchronization completed successfully
                    - source_path: Resolved absolute path to source folder
                    - target_path: Resolved absolute path to target folder
                    - sync_mode: The synchronization mode used
                    - dry_run: Whether this was a preview (True) or actual sync (False)
                    - changes_detected: Boolean indicating if any differences were found
                    - message: Human-readable status message
                    - error: Error message string (only present if success is False)

            Usage:
                Use this tool to synchronize two folders, keeping them in sync or
                creating backups. The dry-run mode allows you to preview all changes
                before executing, making it safe to test synchronization operations.
                Choose the appropriate sync mode based on your needs: mirror for exact
                copies, update for incremental sync, or backup for preserving existing files.

                Common scenarios:
                - Create exact backups of important folders (mirror mode)
                - Keep development and production folders synchronized (update mode)
                - Incrementally backup files without overwriting (backup mode)
                - Preview synchronization changes before executing
                - Maintain multiple copies of the same folder structure
                - Prepare folders for deployment or distribution

                Best practices:
                - ALWAYS use dry_run=True first to preview changes
                - Review dry_run results carefully before executing
                - Use mirror mode for exact backups where target should match source
                - Use update mode when you want to preserve files that only exist in target
                - Use backup mode to avoid overwriting existing files
                - Verify source_path is correct before synchronizing
                - Keep backups of important data before synchronizing

            Examples:
                Preview synchronization (dry run):
                    result = sync_folders(
                        source_path='C:/source/project',
                        target_path='C:/backup/project',
                        sync_mode='mirror',
                        dry_run=True
                    )
                    # Returns: {
                    #     'success': True,
                    #     'dry_run': True,
                    #     'changes_detected': True,
                    #     'message': 'Synchronization preview completed successfully'
                    # }

                Execute mirror synchronization:
                    result = sync_folders(
                        source_path='C:/source/project',
                        target_path='C:/backup/project',
                        sync_mode='mirror',
                        dry_run=False
                    )
                    # Returns: {
                    #     'success': True,
                    #     'dry_run': False,
                    #     'changes_detected': True,
                    #     'message': 'Synchronization completed successfully'
                    # }

                Update mode (preserve target-only files):
                    result = sync_folders(
                        source_path='C:/dev/project',
                        target_path='C:/prod/project',
                        sync_mode='update',
                        dry_run=True
                    )
                    # Returns: Preview of update synchronization

                Error handling - missing source:
                    result = sync_folders(
                        source_path='C:/nonexistent',
                        target_path='C:/backup'
                    )
                    # Returns: {
                    #     'success': False,
                    #     'error': 'Source folder not found: C:/nonexistent'
                    # }

            Notes:
                - Synchronization uses Beyond Compare's sync engine for reliability
                - Mirror mode will DELETE files in target that don't exist in source
                - Update mode preserves files that only exist in target
                - Backup mode never overwrites existing files in target
                - Dry-run mode is safe and recommended before actual synchronization
                - Large folders may take significant time to synchronize
                - Paths are validated and resolved before synchronization
                - Command injection protection is applied to all paths
                - Target folder is created automatically if it doesn't exist

            See Also:
                - compare_folders: For comparing folders without synchronizing
                - compare_files: For comparing individual files
            """
            return self._sync_folders(source_path, target_path, sync_mode, dry_run)

        # Multimedia Drive Scanner Tools

        @self.mcp.tool()
        def multimedia_drive_scanner(
            drives: Optional[List[str]] = None,
            recent_days: Optional[int] = None,
            file_types: Optional[List[str]] = None,
        ) -> Dict[str, Any]:
            """Scan multimedia drives for complete inventory of media files.

            Scans specified multimedia drives (E:, F:, K:, L:) to create a comprehensive
            inventory of all media files including videos, audio, images, and documents.
            Provides detailed statistics, file counts, sizes, and organization information.
            Supports filtering by file type and modification date to focus on specific
            subsets of the collection. Results are cached for use with duplicate detection.

            Prerequisites:
                - Multimedia drives must be accessible (E:, F:, K:, L:)
                - Drives must contain 'multimedia files' folder structure
                - Sufficient permissions to read drive contents
                - Drives must be mounted and available

            Parameters:
                drives: Specific drives to scan (default: None - scans all available)
                    - Optional: Yes (default: None - all available drives)
                    - List of drive letters to scan (e.g., ['E:', 'F:'])
                    - If None, automatically detects and scans all available drives
                    - Only scans drives that contain 'multimedia files' folder
                    - Example: ['E:', 'F:'] to scan only E: and F: drives

                recent_days: Only include files modified in last N days (default: None)
                    - Optional: Yes (default: None - all files)
                    - Integer number of days to look back
                    - Filters files by modification date
                    - Useful for finding recently added or changed files
                    - Example: 30 to find files modified in last 30 days

                file_types: Filter by media types (default: None - all types)
                    - Optional: Yes (default: None - all media types)
                    - List of media type strings: 'video', 'audio', 'images', 'documents'
                    - Filters scan results to only specified types
                    - Can specify multiple types: ['video', 'audio']
                    - Example: ['video'] to scan only video files

            Returns:
                Dictionary containing:
                    - success: Boolean indicating if scan completed successfully
                    - scan_time_seconds: Time taken to complete scan
                    - drives_scanned: List of drive letters that were scanned
                    - total_files: Total number of files found across all drives
                    - total_size_gb: Total size of all files in gigabytes
                    - results: Dictionary with per-drive scan results
                        - Each drive contains: files, file_count, total_size_gb, media_stats
                    - scan_filters: Dictionary showing filters applied
                    - summary: Summary statistics including media distribution
                    - error: Error message string (only present if success is False)

            Usage:
                Use this tool to inventory multimedia files across multiple drives,
                providing a comprehensive view of your media collection. Ideal for
                understanding collection size, organization, and identifying files
                for management or cleanup. Results are cached for use with duplicate
                detection tools.

                Common scenarios:
                - Get complete inventory of multimedia collection
                - Find recently added files (use recent_days filter)
                - Analyze collection by media type (use file_types filter)
                - Prepare for duplicate detection (scan results are cached)
                - Monitor drive space usage and organization
                - Generate reports on media collection statistics

                Best scenarios:
                - Scan all drives first to get complete picture
                - Use file_types filter to focus on specific media types
                - Use recent_days to find recently added content
                - Review summary statistics for collection overview
                - Use cached results with find_multimedia_duplicates

            Examples:
                Scan all available drives:
                    result = multimedia_drive_scanner()
                    # Returns: {
                    #     'success': True,
                    #     'total_files': 15234,
                    #     'total_size_gb': 1234.56,
                    #     'drives_scanned': ['E:', 'F:', 'K:', 'L:']
                    # }

                Scan specific drives for videos only:
                    result = multimedia_drive_scanner(
                        drives=['E:', 'F:'],
                        file_types=['video']
                    )
                    # Returns: Video files from E: and F: drives only

                Find recently added files:
                    result = multimedia_drive_scanner(
                        recent_days=7,
                        file_types=['video', 'audio']
                    )
                    # Returns: Video and audio files modified in last 7 days

                Error handling - no drives found:
                    result = multimedia_drive_scanner()
                    # Returns: {
                    #     'success': False,
                    #     'error': 'No multimedia drives found'
                    # }

            Notes:
                - Scan results are cached for use with duplicate detection
                - Only scans drives containing 'multimedia files' folder
                - Large collections may take several minutes to scan
                - File size minimum is 1KB (tiny files are excluded)
                - Media types are determined by file extension
                - Scan time increases with number of files and drives
                - Results include detailed per-drive statistics

            See Also:
                - find_multimedia_duplicates: For finding duplicate files (uses scan cache)
                - detect_usb_drives: For detecting USB drives for sync operations
            """
            return self.multimedia_scanner.scan_multimedia_drives(
                drives=drives, recent_days=recent_days, file_types=file_types
            )

        @self.mcp.tool()
        def find_multimedia_duplicates(
            drives: Optional[List[str]] = None,
            min_size_mb: float = 0.1,
            file_types: Optional[List[str]] = None,
            use_content_hash: bool = True,
        ) -> Dict[str, Any]:
            """Find duplicate multimedia files across drives.

            Identifies duplicate multimedia files across specified drives using either
            content hash (accurate but slower) or name/size matching (faster but less
            accurate). Groups duplicates together and provides recommendations for which
            files to keep and which to remove, along with potential space savings.
            Uses cached scan results from multimedia_drive_scanner when available.

            Prerequisites:
                - Multimedia drives must be accessible
                - Should run multimedia_drive_scanner first for best results
                - Sufficient disk space for hash calculation (if use_content_hash=True)
                - Files must be readable for hash calculation

            Parameters:
                drives: Specific drives to check (default: None - uses last scan results)
                    - Optional: Yes (default: None - uses cached scan results)
                    - List of drive letters to check (e.g., ['E:', 'F:'])
                    - If None, uses results from last multimedia_drive_scanner call
                    - If specified, performs new scan before duplicate detection
                    - Example: ['E:', 'F:'] to check only E: and F: drives

                min_size_mb: Minimum file size in MB to check for duplicates (default: 0.1)
                    - Optional: Yes (default: 0.1 MB)
                    - Files smaller than this are excluded from duplicate detection
                    - Reduces processing time by skipping tiny files
                    - Recommended: 1.0 MB or higher for faster processing
                    - Example: 10.0 to only check files larger than 10 MB

                file_types: Filter by media types (default: None - all types)
                    - Optional: Yes (default: None - all media types)
                    - List of media type strings: 'video', 'audio', 'images', 'documents'
                    - Filters duplicate detection to only specified types
                    - Can specify multiple types: ['video', 'audio']
                    - Example: ['video'] to find only duplicate video files

                use_content_hash: Use content hash for accurate detection (default: True)
                    - Optional: Yes (default: True)
                    - True: Uses SHA-256 hash of file content (accurate, slower)
                    - False: Uses filename and size matching (faster, less accurate)
                    - Recommended: True for accurate results, False for quick scan
                    - Hash calculation can be slow for large files
                    - Example: Set to False for initial quick scan, True for final check

            Returns:
                Dictionary containing:
                    - success: Boolean indicating if duplicate detection completed successfully
                    - scan_time_seconds: Time taken to complete duplicate detection
                    - detection_method: Method used ('content_hash' or 'name_and_size')
                    - total_files_checked: Total number of files analyzed
                    - duplicate_groups: List of duplicate file groups
                        - Each group contains: files, duplicate_count, potential_savings_mb
                    - total_duplicate_groups: Number of duplicate groups found
                    - total_duplicate_files: Total number of duplicate files (excluding originals)
                    - total_savings_gb: Total potential space savings in gigabytes
                    - recommendations: List of cleanup recommendations
                    - error: Error message string (only present if success is False)

            Usage:
                Use this tool to identify duplicate files across your multimedia collection,
                helping you reclaim disk space by removing unnecessary duplicates. The tool
                groups duplicates together and provides recommendations for which files to
                keep (based on drive priority) and which to remove. Use content hash for
                accurate detection or name/size for faster scanning.

                Common scenarios:
                - Find and remove duplicate files to free up disk space
                - Identify files that exist on multiple drives
                - Get recommendations for which duplicates to keep
                - Calculate potential space savings from cleanup
                - Verify backup completeness (should have duplicates)
                - Organize multimedia collection by removing duplicates

                Best practices:
                - Run multimedia_drive_scanner first to cache results
                - Start with use_content_hash=False for quick initial scan
                - Use use_content_hash=True for final accurate detection
                - Set min_size_mb to 1.0 or higher to skip tiny files
                - Review recommendations before deleting files
                - Start with largest duplicates for maximum space savings

            Examples:
                Find duplicates using cached scan results:
                    result = find_multimedia_duplicates()
                    # Returns: {
                    #     'success': True,
                    #     'total_duplicate_groups': 42,
                    #     'total_savings_gb': 15.3,
                    #     'duplicate_groups': [...]
                    # }

                Quick scan with name/size matching:
                    result = find_multimedia_duplicates(
                        min_size_mb=10.0,
                        use_content_hash=False
                    )
                    # Returns: Fast duplicate detection using filename and size

                Accurate detection for video files only:
                    result = find_multimedia_duplicates(
                        file_types=['video'],
                        min_size_mb=100.0,
                        use_content_hash=True
                    )
                    # Returns: Accurate duplicate detection for large video files

                Check specific drives:
                    result = find_multimedia_duplicates(
                        drives=['E:', 'F:'],
                        min_size_mb=1.0
                    )
                    # Returns: Duplicates between E: and F: drives

            Notes:
                - Uses cached scan results from multimedia_drive_scanner when available
                - Content hash calculation can be slow for large files
                - Name/size matching is faster but may miss some duplicates
                - Duplicate groups are sorted by potential savings (largest first)
                - Recommendations prioritize keeping files on lower drive letters (E: < F: < K: < L:)
                - Total savings represents space that could be freed by removing duplicates
                - Large collections may take significant time to process

            See Also:
                - multimedia_drive_scanner: For scanning drives before duplicate detection
                - detect_usb_drives: For detecting USB drives for sync operations
            """
            return self.multimedia_scanner.find_multimedia_duplicates(
                drives=drives,
                min_size_mb=min_size_mb,
                file_types=file_types,
                use_content_hash=use_content_hash,
            )

        @self.mcp.tool()
        def detect_usb_drives() -> Dict[str, Any]:
            """Detect connected USB drives for sync operations.

            Scans the system for connected USB drives and returns information about
            each drive including drive letter, label, available space, and whether
            it contains a multimedia files folder. Useful for identifying removable
            storage devices that can be used for backup or synchronization operations.
            Automatically excludes the fixed multimedia drives (E:, F:, K:, L:).

            Prerequisites:
                - System must support USB drive detection
                - USB drives must be mounted and accessible
                - On Windows, win32api provides better detection (optional dependency)
                - Drives must be recognized by the operating system

            Parameters:
                None: This tool takes no parameters

            Returns:
                Dictionary containing:
                    - success: Boolean indicating if detection completed successfully
                    - usb_drives: List of USB drive information dictionaries
                        - Each drive contains:
                            - drive_letter: Drive letter (e.g., 'G:')
                            - label: Volume label or 'Unknown Label'
                            - space_info: Dictionary with total_gb, used_gb, free_gb, used_percent
                            - multimedia_folder_exists: Boolean indicating if 'multimedia files' folder exists
                            - detection_method: 'win32api' or 'fallback' (optional)
                    - count: Number of USB drives detected
                    - message: Human-readable status message
                    - error: Error message string (only present if success is False)

            Usage:
                Use this tool to identify connected USB drives that can be used for
                backup or synchronization operations. The tool automatically excludes
                the fixed multimedia drives and focuses on removable storage devices.
                Check the multimedia_folder_exists flag to see if drives are ready
                for multimedia sync operations.

                Common scenarios:
                - Find USB drives for backup operations
                - Identify removable storage for synchronization
                - Check available space on USB drives
                - Verify USB drives are ready for multimedia sync
                - Prepare for backup to external storage
                - Monitor connected removable storage devices

                Best practices:
                - Check space_info before starting large sync operations
                - Verify multimedia_folder_exists if using for multimedia sync
                - Use drive label to identify specific USB drives
                - Check free_gb to ensure sufficient space
                - Use with sync_folders for backup operations

            Examples:
                Detect all USB drives:
                    result = detect_usb_drives()
                    # Returns: {
                    #     'success': True,
                    #     'count': 2,
                    #     'usb_drives': [
                    #         {
                    #             'drive_letter': 'G:',
                    #             'label': 'BACKUP_DRIVE',
                    #             'space_info': {'free_gb': 500.0, 'total_gb': 1000.0},
                    #             'multimedia_folder_exists': True
                    #         }
                    #     ]
                    # }

                Check USB drive space:
                    result = detect_usb_drives()
                    if result['success']:
                        for drive in result['usb_drives']:
                            print(f"{drive['drive_letter']}: {drive['space_info']['free_gb']} GB free")
                    # Output: G: 500.0 GB free

                Error handling - detection failed:
                    result = detect_usb_drives()
                    # Returns: {
                    #     'success': False,
                    #     'error': 'USB drive detection failed - may require win32api dependency'
                    # }

            Notes:
                - Automatically excludes fixed multimedia drives (E:, F:, K:, L:)
                - Uses win32api on Windows for accurate detection (optional dependency)
                - Falls back to directory scanning if win32api not available
                - Only detects drives that are mounted and accessible
                - Drive labels may show as 'Unknown Label' if win32api unavailable
                - Detection method is indicated in drive information when available
                - USB drives must be recognized by operating system

            See Also:
                - multimedia_drive_scanner: For scanning multimedia drives
                - sync_folders: For synchronizing folders to USB drives
                - find_multimedia_duplicates: For finding duplicate files
            """
            try:
                usb_drives = self.multimedia_scanner.get_usb_drives()
                return {
                    "success": True,
                    "usb_drives": usb_drives,
                    "count": len(usb_drives),
                    "message": f"Found {len(usb_drives)} USB drive(s)",
                }
            except Exception as e:
                logger.error(f"USB drive detection failed: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e),
                    "message": "USB drive detection failed - may require win32api dependency",
                }

        # Developer Backup and Repository Management Tools
        @self.mcp.tool()
        def backup_dev_repositories(
            source_path: str,
            backup_path: str,
            exclude_patterns: Optional[List[str]] = None,
            include_git_essentials: bool = True,
            compress: bool = True,
            incremental: bool = True,
            dry_run: bool = False,
        ) -> Dict[str, Any]:
            """Smart backup of development repositories with intelligent filtering."""
            return self.dev_backup.backup_repositories(
                source_path,
                backup_path,
                exclude_patterns,
                include_git_essentials,
                compress,
                incremental,
                dry_run,
            )

        @self.mcp.tool()
        def analyze_dev_workspace(
            workspace_path: str,
            report_path: Optional[str] = None,
            include_git_stats: bool = True,
            include_dependencies: bool = True,
            include_size_analysis: bool = True,
        ) -> Dict[str, Any]:
            """Analyze development workspace for insights and optimization opportunities."""
            return self.workspace_analyzer.analyze_workspace(
                workspace_path,
                report_path,
                include_git_stats,
                include_dependencies,
                include_size_analysis,
            )

        @self.mcp.tool()
        def scan_repo_health(
            repos_path: str,
            checks: Optional[List[str]] = None,
            report_path: Optional[str] = None,
            fix_issues: bool = False,
        ) -> Dict[str, Any]:
            """Scan repository health and identify potential issues."""
            return self.health_checker.scan_repository_health(
                repos_path, checks, report_path, fix_issues
            )

        @self.mcp.tool()
        def cleanup_dev_artifacts(
            repos_path: str,
            targets: Optional[List[str]] = None,
            size_threshold_mb: float = 100,
            dry_run: bool = True,
        ) -> Dict[str, Any]:
            """Clean up build artifacts and temporary files across repositories."""
            return self.health_checker.cleanup_development_artifacts(
                repos_path, targets, size_threshold_mb, dry_run
            )

        @self.mcp.tool()
        def find_duplicate_code(
            repos_path: str,
            file_types: Optional[List[str]] = None,
            min_lines: int = 10,
            similarity_threshold: float = 0.8,
            report_path: Optional[str] = None,
        ) -> Dict[str, Any]:
            """Find duplicate code across repositories."""
            return self.duplicate_detector.find_duplicate_code(
                repos_path, file_types, min_lines, similarity_threshold, report_path
            )

        @self.mcp.tool()
        def compare_workspace_snapshots(
            snapshot1_path: str,
            snapshot2_path: str,
            report_path: Optional[str] = None,
            show_changes: Optional[List[str]] = None,
        ) -> Dict[str, Any]:
            """Compare workspace snapshots to identify changes over time."""
            return self.duplicate_detector.compare_workspace_snapshots(
                snapshot1_path, snapshot2_path, report_path, show_changes
            )

        @self.mcp.tool()
        def selective_restore(
            backup_path: str,
            restore_items: List[str],
            target_path: str,
            preserve_structure: bool = True,
            overwrite_existing: bool = False,
        ) -> Dict[str, Any]:
            """Selectively restore specific projects or files from backup."""
            return self.duplicate_detector.selective_restore(
                backup_path,
                restore_items,
                target_path,
                preserve_structure,
                overwrite_existing,
            )

    def _run_bc_command(
        self,
        args: List[Union[str, Path]],
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Run a Beyond Compare command with proper input validation.

        Args:
            args: List of command-line arguments (validated)
            timeout: Command timeout in seconds

        Returns:
            Dictionary with command results

        Raises:
            BeyondCompareCommandError: If command fails
            BeyondCompareTimeoutError: If command times out
        """
        if not self.bc_path:
            self.bc_path = self._find_bc_executable()

        # Input validation - only allow safe arguments
        safe_args = []
        for arg in args:
            if arg is None:
                continue
            arg_str = str(arg)
            # Basic path validation to prevent command injection
            if not self._is_safe_argument(arg_str):
                raise BeyondCompareCommandError(
                    command=f"Invalid argument: {arg_str}",
                    returncode=-1,
                    stderr="Invalid or unsafe argument detected",
                )
            safe_args.append(arg_str)

        cmd = [str(self.bc_path)] + safe_args

        try:
            logger.debug(f"Executing: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout or settings.COMMAND_TIMEOUT,
                creationflags=subprocess.CREATE_NO_WINDOW
                if platform.system() == "Windows"
                else 0,
            )

            # Beyond Compare returns:
            # 0 = success, no differences
            # 1 = success, differences found
            # 2+ = error
            if result.returncode >= 2:
                raise BeyondCompareCommandError(
                    command=" ".join(cmd),
                    returncode=result.returncode,
                    stderr=result.stderr,
                )

            return {
                "success": True,
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "has_differences": result.returncode == 1,
            }

        except subprocess.TimeoutExpired as e:
            raise BeyondCompareTimeoutError(
                command=" ".join(cmd),
                timeout=timeout or settings.COMMAND_TIMEOUT,
            ) from e

        except Exception as e:
            raise BeyondCompareCommandError(
                command=" ".join(cmd),
                returncode=getattr(e, "returncode", -1),
                stderr=str(e),
            ) from e

    def _is_safe_argument(self, arg: str) -> bool:
        """Validate that an argument is safe to pass to subprocess.

        Args:
            arg: Argument to validate

        Returns:
            True if argument is safe, False otherwise
        """
        # Block common command injection patterns
        dangerous_chars = [";", "|", "&", ">", "<", "`", "$", "(", ")"]
        for char in dangerous_chars:
            if char in arg:
                return False

        # Allow normal paths and Beyond Compare arguments
        return True

    def _validate_path(self, path_str: str) -> Path:
        """Validate and resolve a path safely.

        Args:
            path_str: Path string to validate

        Returns:
            Validated Path object

        Raises:
            ValueError: If path is invalid or unsafe
        """
        try:
            path = Path(path_str).expanduser().resolve()

            # Prevent path traversal attacks
            if ".." in path_str:
                raise ValueError("Path traversal detected")

            return path
        except Exception as e:
            raise ValueError(f"Invalid path: {path_str}") from e

    def _create_script(self, commands: List[str], script_name: str) -> Path:
        """Create a temporary Beyond Compare script file.

        Args:
            commands: List of Beyond Compare script commands
            script_name: Base name for the script file

        Returns:
            Path to the created script file

        Raises:
            BeyondCompareScriptError: If script creation fails
        """
        try:
            self.scripts_dir.mkdir(parents=True, exist_ok=True)

            # Create a unique script filename using tempfile for security
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".bcscript",
                dir=self.scripts_dir,
                delete=False,
                encoding="utf-8",
            ) as script_file:
                # Write the script with proper line endings
                script_content = "\r\n".join(commands) + "\r\n"
                script_file.write(script_content)
                script_path = Path(script_file.name)

            return script_path

        except Exception as e:
            raise BeyondCompareScriptError(
                script_path="unknown",
                error=str(e),
            ) from e

    def _compare_files(
        self,
        left_path: str,
        right_path: str,
        output_report: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Compare two files using Beyond Compare."""
        try:
            # Validate and resolve paths
            left = self._validate_path(left_path)
            right = self._validate_path(right_path)

            if not left.exists():
                return {
                    "success": False,
                    "error": f"Left file not found: {left_path}",
                    "left_path": left_path,
                    "right_path": right_path,
                }
            if not right.exists():
                return {
                    "success": False,
                    "error": f"Right file not found: {right_path}",
                    "left_path": left_path,
                    "right_path": right_path,
                }

            # Build command arguments for silent comparison
            # Beyond Compare 5 requires /qc (Quick Compare) for command-line operation
            args = ["/silent", "/qc", str(left), str(right)]

            # Add report generation if requested
            if output_report:
                report_path = self._validate_path(output_report)
                report_path.parent.mkdir(parents=True, exist_ok=True)
                args.extend(["/qc=text-conflicts", f"/o={report_path}"])

            # Run the comparison
            result = self._run_bc_command(args)

            return {
                "success": True,
                "left_path": str(left),
                "right_path": str(right),
                "identical": not result["has_differences"],
                "differences_found": result["has_differences"],
                "output_report": output_report,
                "message": (
                    "Files are identical"
                    if not result["has_differences"]
                    else "Differences found between files"
                ),
            }

        except Exception as e:
            logger.error(f"File comparison failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "left_path": left_path,
                "right_path": right_path,
                "message": f"Comparison failed: {e}",
            }

    def _compare_folders(
        self,
        left_path: str,
        right_path: str,
        output_report: Optional[str] = None,
        include_subfolders: bool = True,
    ) -> Dict[str, Any]:
        """Compare two folders using Beyond Compare."""
        try:
            # Validate and resolve paths
            left = self._validate_path(left_path)
            right = self._validate_path(right_path)

            if not left.exists():
                return {
                    "success": False,
                    "error": f"Left folder not found: {left_path}",
                    "left_path": left_path,
                    "right_path": right_path,
                }
            if not right.exists():
                return {
                    "success": False,
                    "error": f"Right folder not found: {right_path}",
                    "left_path": left_path,
                    "right_path": right_path,
                }

            # Create script for folder comparison
            script_commands = [
                f'load "{left}" "{right}"',
                "expand all" if include_subfolders else "",
                "select all.files",
            ]

            # Add report generation if requested
            if output_report:
                report_path = self._validate_path(output_report)
                report_path.parent.mkdir(parents=True, exist_ok=True)
                script_commands.append(
                    f'report layout:summary options:display-mismatches output-to:"{report_path}"'
                )

            # Add final command to close after completion
            script_commands.append("script-exit")

            # Create and run script
            script_path = self._create_script(script_commands, "folder_compare")
            try:
                result = self._run_bc_command([f"@{str(script_path)}"])
            finally:
                # Clean up script file
                try:
                    script_path.unlink(missing_ok=True)
                except Exception as e:
                    logger.warning(f"Failed to clean up script file {script_path}: {e}")

            return {
                "success": True,
                "left_path": str(left),
                "right_path": str(right),
                "include_subfolders": include_subfolders,
                "differences_found": result["has_differences"],
                "output_report": output_report,
                "message": (
                    "Folders are identical"
                    if not result["has_differences"]
                    else "Differences found between folders"
                ),
            }

        except Exception as e:
            logger.error(f"Folder comparison failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "left_path": left_path,
                "right_path": right_path,
                "message": f"Comparison failed: {e}",
            }

    def _sync_folders(
        self,
        source_path: str,
        target_path: str,
        sync_mode: str = "mirror",
        dry_run: bool = True,
    ) -> Dict[str, Any]:
        """Synchronize folders using Beyond Compare."""
        try:
            # Validate sync mode
            valid_modes = ["mirror", "update", "backup"]
            if sync_mode not in valid_modes:
                return {
                    "success": False,
                    "error": f"Invalid sync mode. Must be one of: {', '.join(valid_modes)}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "sync_mode": sync_mode,
                }

            # Validate and resolve paths
            source = self._validate_path(source_path)
            target = self._validate_path(target_path)

            if not source.exists():
                return {
                    "success": False,
                    "error": f"Source folder not found: {source_path}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "sync_mode": sync_mode,
                }

            # Create target directory if it doesn't exist
            target.mkdir(parents=True, exist_ok=True)

            # Build script commands based on sync mode
            script_commands = [
                f'load "{source}" "{target}"',
                "expand all",
                "select all.files all.folders",
            ]

            # Add sync command based on mode
            if sync_mode == "mirror":
                script_commands.append("sync mirror:left->right")
            elif sync_mode == "update":
                script_commands.append("sync update:left->right")
            elif sync_mode == "backup":
                script_commands.append("sync create:left->right")

            # Add dry run option
            if dry_run:
                script_commands[-1] += " preview"

            # Add final command to close after completion
            script_commands.append("script-exit")

            # Create and run script
            script_path = self._create_script(script_commands, f"sync_{sync_mode}")
            try:
                result = self._run_bc_command([f"@{str(script_path)}"])
            finally:
                # Clean up script file
                try:
                    script_path.unlink(missing_ok=True)
                except Exception as e:
                    logger.warning(f"Failed to clean up script file {script_path}: {e}")

            return {
                "success": True,
                "source_path": str(source),
                "target_path": str(target),
                "sync_mode": sync_mode,
                "dry_run": dry_run,
                "changes_detected": result["has_differences"],
                "message": (
                    f"Synchronization {'preview' if dry_run else 'completed'} successfully"
                ),
            }

        except Exception as e:
            logger.error(f"Folder synchronization failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "source_path": source_path,
                "target_path": target_path,
                "sync_mode": sync_mode,
                "message": f"Synchronization failed: {e}",
            }

    def run(self) -> None:
        """Run the MCP server over stdio."""
        if _is_stdio_mode and hasattr(sys, "_original_stdout"):
            sys.stdout = sys._original_stdout
            if os.name == "nt":
                try:
                    import msvcrt

                    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
                except (ImportError, OSError, AttributeError):
                    pass
            sys.stdout.flush()
            os.environ.setdefault("PYTHONUNBUFFERED", "1")
            logging.basicConfig(
                level=logging.CRITICAL,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                handlers=[logging.StreamHandler(sys.stderr)],
                force=True,
            )
        else:
            logger.info("Starting Beyond Compare MCP Server (FastMCP 3.x)")
            if self.bc_path:
                logger.info("Beyond Compare path: %s", self.bc_path)
            else:
                logger.warning("Beyond Compare executable not found")
        asyncio.run(self.mcp.run_stdio_async(show_banner=False))


def main(
    bc_path: Optional[str] = None,
    scripts_dir: Optional[str] = None,
) -> None:
    """Run a local stdio MCP server."""
    BeyondCompareMCP(bc_path=bc_path, scripts_dir=scripts_dir).run()


if __name__ == "__main__":
    main()
