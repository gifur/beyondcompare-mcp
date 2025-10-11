"""
Beyond Compare MCP Server

A Model Context Protocol (MCP) server that provides file and directory comparison
capabilities using Beyond Compare. Built with modern MCP 2.11+ standards.
"""

import logging
import os
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Modern FastMCP 2.11+ import
from fastmcp import FastMCP

from .config import settings
from .exceptions import (
    BeyondCompareError,
    BeyondCompareNotInstalledError,
    BeyondCompareCommandError,
    BeyondCompareTimeoutError,
    BeyondCompareScriptError,
)
from .multimedia_scanner import MultimediaDriveScanner

logger = logging.getLogger(__name__)


class BeyondCompareMCP:
    """Beyond Compare MCP server implementation using FastMCP 2.11+."""

    def __init__(
        self,
        bc_path: Optional[str] = None,
        scripts_dir: Optional[str] = None,
    ):
        """Initialize the Beyond Compare MCP server.

        Args:
            bc_path: Path to Beyond Compare executable
            scripts_dir: Directory for temporary script files
        """
        self.bc_path = self._find_bc_executable(bc_path)
        self.scripts_dir = Path(scripts_dir or settings.BC_SCRIPTS_DIR)
        self.scripts_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize multimedia scanner
        self.multimedia_scanner = MultimediaDriveScanner()

        # Initialize modern FastMCP 2.11+
        self.mcp = FastMCP(
            name="Beyond Compare MCP"
        )

        # Register MCP tools
        self._register_tools()

    def _find_bc_executable(self, bc_path: Optional[str] = None) -> Path:
        """Find the Beyond Compare executable."""
        # If a full path is provided (not just the executable name), verify it exists
        if bc_path and (Path(bc_path).is_absolute() or "/" in bc_path or "\\" in bc_path):
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
        bc_exe = bc_path if bc_path else ("BCompare.exe" if platform.system() == "Windows" else "bcompare")
        which_bc = shutil.which(bc_exe)
        if which_bc:
            return Path(which_bc)

        # If we still haven't found it and a specific executable name was provided, also try the default
        if bc_path and bc_path != ("BCompare.exe" if platform.system() == "Windows" else "bcompare"):
            default_exe = "BCompare.exe" if platform.system() == "Windows" else "bcompare"
            which_default = shutil.which(default_exe)
            if which_default:
                return Path(which_default)

        raise BeyondCompareNotInstalledError(f"Beyond Compare not found. Searched for: {bc_exe if bc_path else 'BCompare.exe'}")

    def _register_tools(self) -> None:
        """Register MCP tools with FastMCP."""

        @self.mcp.tool()
        def compare_files(
            left_path: str,
            right_path: str,
            output_report: Optional[str] = None,
        ) -> Dict[str, Any]:
            """Compare two files using Beyond Compare.

            Args:
                left_path: Path to the left file
                right_path: Path to the right file
                output_report: Optional path to save the comparison report

            Returns:
                Dictionary with comparison results
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

            Args:
                left_path: Path to the left folder
                right_path: Path to the right folder
                output_report: Optional path to save the comparison report
                include_subfolders: Whether to include subfolders in comparison

            Returns:
                Dictionary with comparison results
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

            Args:
                source_path: Source directory path
                target_path: Target directory path
                sync_mode: Sync mode: 'mirror', 'update', or 'backup'
                dry_run: If True, only show what would be done

            Returns:
                Dictionary with sync results
            """
            return self._sync_folders(source_path, target_path, sync_mode, dry_run)
        
        # Multimedia Drive Scanner Tools
        
        @self.mcp.tool()
        def multimedia_drive_scanner(
            drives: Optional[List[str]] = None,
            recent_days: Optional[int] = None,
            file_types: Optional[List[str]] = None
        ) -> Dict[str, Any]:
            """Scan Sandra's multimedia drives (E:, F:, K:, L:) for complete inventory.
            
            Args:
                drives: Specific drives to scan (default: all available E:, F:, K:, L:)
                recent_days: Only include files modified in last N days
                file_types: Filter by media types ('video', 'audio', 'images', 'documents')
                
            Returns:
                Complete inventory with statistics and file details
            """
            return self.multimedia_scanner.scan_multimedia_drives(
                drives=drives,
                recent_days=recent_days,
                file_types=file_types
            )
        
        @self.mcp.tool()
        def find_multimedia_duplicates(
            drives: Optional[List[str]] = None,
            min_size_mb: float = 0.1,
            file_types: Optional[List[str]] = None,
            use_content_hash: bool = True
        ) -> Dict[str, Any]:
            """Find duplicate multimedia files across Sandra's drives.
            
            Args:
                drives: Specific drives to check (default: use last scan results)
                min_size_mb: Minimum file size in MB to check for duplicates
                file_types: Filter by media types
                use_content_hash: Use content hash for accurate detection (slower but better)
                
            Returns:
                Dictionary with duplicate groups and cleanup recommendations
            """
            return self.multimedia_scanner.find_multimedia_duplicates(
                drives=drives,
                min_size_mb=min_size_mb,
                file_types=file_types,
                use_content_hash=use_content_hash
            )
        
        @self.mcp.tool()
        def detect_usb_drives() -> Dict[str, Any]:
            """Detect connected USB drives for sync operations.
            
            Returns:
                List of USB drive information with space details
            """
            try:
                usb_drives = self.multimedia_scanner.get_usb_drives()
                return {
                    "success": True,
                    "usb_drives": usb_drives,
                    "count": len(usb_drives),
                    "message": f"Found {len(usb_drives)} USB drive(s)"
                }
            except Exception as e:
                logger.error(f"USB drive detection failed: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e),
                    "message": "USB drive detection failed - may require win32api dependency"
                }

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
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0,
            )

            # Beyond Compare returns:
            # 0 = success, no differences
            # 1 = success, differences found
            # 2+ = error
            if result.returncode >= 2:
                raise BeyondCompareCommandError(
                    command=' '.join(cmd),
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
                command=' '.join(cmd),
                timeout=timeout or settings.COMMAND_TIMEOUT,
            ) from e

        except Exception as e:
            raise BeyondCompareCommandError(
                command=' '.join(cmd),
                returncode=getattr(e, 'returncode', -1),
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
        dangerous_chars = [';', '|', '&', '>', '<', '`', '$', '(', ')']
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
            if '..' in path_str:
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
                mode='w',
                suffix='.bcscript',
                dir=self.scripts_dir,
                delete=False,
                encoding='utf-8'
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
                'expand all' if include_subfolders else '',
                'select all.files',
            ]

            # Add report generation if requested
            if output_report:
                report_path = self._validate_path(output_report)
                report_path.parent.mkdir(parents=True, exist_ok=True)
                script_commands.append(
                    f'report layout:summary options:display-mismatches output-to:"{report_path}"'
                )

            # Add final command to close after completion
            script_commands.append('script-exit')

            # Create and run script
            script_path = self._create_script(script_commands, "folder_compare")
            try:
                result = self._run_bc_command([f'@{str(script_path)}'])
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
                'expand all',
                'select all.files all.folders',
            ]

            # Add sync command based on mode
            if sync_mode == "mirror":
                script_commands.append('sync mirror:left->right')
            elif sync_mode == "update":
                script_commands.append('sync update:left->right')
            elif sync_mode == "backup":
                script_commands.append('sync create:left->right')

            # Add dry run option
            if dry_run:
                script_commands[-1] += ' preview'

            # Add final command to close after completion
            script_commands.append('script-exit')

            # Create and run script
            script_path = self._create_script(script_commands, f"sync_{sync_mode}")
            try:
                result = self._run_bc_command([f'@{str(script_path)}'])
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
        """Start the MCP server."""
        logger.info("Starting Beyond Compare MCP Server with FastMCP 2.11+")
        if self.bc_path:
            logger.info(f"Beyond Compare path: {self.bc_path}")
        else:
            logger.warning("Beyond Compare executable not found - server may not function properly")

        self.mcp.run()


def main() -> None:
    """Main entry point for the MCP server."""
    logging.basicConfig(level=logging.INFO)
    server = BeyondCompareMCP()
    server.run()


if __name__ == "__main__":
    main()
