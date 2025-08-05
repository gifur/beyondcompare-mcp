"""
Beyond Compare MCP Server

A FastMCP 2.10 compliant MCP server that provides file and directory comparison
capabilities using Beyond Compare.
"""

import logging
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastmcp import FastMCP, MCPTool
from pydantic import BaseModel, Field

from .config import settings
from .exceptions import (
    BeyondCompareCommandError,
    BeyondCompareError,
    BeyondCompareNotInstalledError,
    BeyondCompareScriptError,
    BeyondCompareTimeoutError,
    BeyondCompareValidationError,
)

logger = logging.getLogger(__name__)


class ComparisonRequest(BaseModel):
    """Request model for file/folder comparison."""
    
    left_path: str = Field(..., description="Path to the left file or folder")
    right_path: str = Field(..., description="Path to the right file or folder")
    output_report: Optional[str] = Field(
        None, 
        description="Optional path to save the comparison report"
    )
    include_subfolders: bool = Field(
        True, 
        description="Whether to include subfolders in directory comparison"
    )


class SyncRequest(BaseModel):
    """Request model for folder synchronization."""
    
    source_path: str = Field(..., description="Source directory path")
    target_path: str = Field(..., description="Target directory path")
    sync_mode: str = Field(
        "mirror", 
        description="Synchronization mode: 'mirror', 'update', or 'backup'"
    )
    dry_run: bool = Field(
        True, 
        description="If True, only show what would be done without making changes"
    )


class BeyondCompareMCP:
    """Beyond Compare MCP server implementation."""
    
    def __init__(
        self,
        host: str = settings.HOST,
        port: int = settings.PORT,
        bc_path: Optional[str] = None,
        scripts_dir: Optional[str] = None,
    ):
        """Initialize the Beyond Compare MCP server.
        
        Args:
            host: Host to bind the server to
            port: Port to listen on
            bc_path: Path to Beyond Compare executable (auto-detected if None)
            scripts_dir: Directory to store temporary scripts (default: ./bc_scripts)
        """
        self.host = host
        self.port = port
        self.bc_path = self._find_bc_executable(bc_path) if bc_path else None
        self.scripts_dir = Path(scripts_dir or settings.BC_SCRIPTS_DIR)
        self.scripts_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize FastAPI and FastMCP
        self.app = FastAPI(
            title="Beyond Compare MCP Server",
            description="MCP server for Beyond Compare file and directory comparison",
            version=settings.DXT_PACKAGE_VERSION,
        )
        
        self.mcp = FastMCP(
            name="Beyond Compare MCP",
            description="File and directory comparison using Beyond Compare",
            version=settings.DXT_PACKAGE_VERSION,
        )
        
        # Register MCP tools
        self._register_tools()
        
        # Mount MCP router
        self.app.include_router(self.mcp.router, prefix="/mcp")
        
        # Add health check endpoint
        @self.app.get("/health")
        async def health_check():
            return {"status": "ok", "service": "beyondcompare-mcp"}
    
    def _find_bc_executable(self, bc_path: Optional[str] = None) -> Path:
        """Find the Beyond Compare executable."""
        # If path is provided, verify it exists
        if bc_path:
            path = Path(bc_path).expanduser().resolve()
            if path.exists():
                return path
            raise BeyondCompareNotInstalledError(str(path))
        
        # Check common installation paths
        if platform.system() == "Windows":
            program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
            common_paths = [
                Path(program_files) / "Beyond Compare 4" / "BCompare.exe",
                Path(program_files) / "Beyond Compare 3" / "BCompare.exe",
                Path(program_files) / "Beyond Compare" / "BCompare.exe",
                Path("C:\\Program Files (x86)\\Beyond Compare 4\\BCompare.exe"),
                Path("C:\\Program Files (x86)\\Beyond Compare 3\\BCompare.exe"),
            ]
            
            for path in common_paths:
                if path.exists():
                    return path
        
        # Check PATH
        bc_exe = "BCompare.exe" if platform.system() == "Windows" else "bcompare"
        which_bc = shutil.which(bc_exe)
        if which_bc:
            return Path(which_bc)
        
        raise BeyondCompareNotInstalledError()
    
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
    
    def _run_bc_command(
        self,
        args: List[Union[str, Path]],
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Run a Beyond Compare command.
        
        Args:
            args: List of command-line arguments
            timeout: Command timeout in seconds
            
        Returns:
            Dictionary with command results
            
        Raises:
            BeyondCompareCommandError: If command fails
            BeyondCompareTimeoutError: If command times out
        """
        if not self.bc_path:
            self.bc_path = self._find_bc_executable()
        
        cmd = [str(self.bc_path)] + [str(arg) for arg in args if arg is not None]
        
        try:
            logger.debug(f"Executing: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=timeout or settings.COMMAND_TIMEOUT,
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0,
            )
            
            # Beyond Compare returns:
            # 0 = success, no differences
            # 1 = success, differences found
            # >1 = error
            if result.returncode > 1:
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
            
            # Create a unique script filename
            script_path = self.scripts_dir / f"{script_name}.bcscript"
            
            # Write the script with proper line endings
            script_content = "\r\n".join(commands) + "\r\n"
            script_path.write_text(script_content, encoding='utf-8')
            
            return script_path
            
        except Exception as e:
            raise BeyondCompareScriptError(
                script_path=str(script_path),
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
            # Validate paths
            left = Path(left_path).expanduser().resolve()
            right = Path(right_path).expanduser().resolve()
            
            if not left.exists():
                raise FileNotFoundError(f"Left file not found: {left_path}")
            if not right.exists():
                raise FileNotFoundError(f"Right file not found: {right_path}")
            
            # Build command arguments
            args = [str(left), str(right)]
            
            # Add report generation if requested
            if output_report:
                report_path = Path(output_report).expanduser().resolve()
                report_path.parent.mkdir(parents=True, exist_ok=True)
                args.extend(["/silent", "/qc=text-conflicts", f"/o=\"{report_path}\""])
            
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
            # Validate paths
            left = Path(left_path).expanduser().resolve()
            right = Path(right_path).expanduser().resolve()
            
            if not left.exists():
                raise FileNotFoundError(f"Left folder not found: {left_path}")
            if not right.exists():
                raise FileNotFoundError(f"Right folder not found: {right_path}")
            
            # Create script for folder comparison
            script_commands = [
                f'load "{left}" "{right}"',
                'expand all' if include_subfolders else '',
                'select all.files',
            ]
            
            # Add report generation if requested
            if output_report:
                report_path = Path(output_report).expanduser().resolve()
                report_path.parent.mkdir(parents=True, exist_ok=True)
                script_commands.append(
                    f'report layout:summary options:display-mismatches output-to:"{report_path}"'
                )
            
            # Add final command to close after completion
            script_commands.append('script-exit')
            
            # Create and run script
            script_path = self._create_script(script_commands, "folder_compare")
            result = self._run_bc_command([f'@{script_path}'])
            
            # Clean up script file
            try:
                script_path.unlink(missing_ok=True)
            except Exception as e:
                logger.warning(f"Failed to clean up script file {script_path}: {e}")
            
            return {
                "success": True,
                "left_path": str(left),
                "right_path": str(right),
                "identical": not result["has_differences"],
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
                raise ValueError(f"Invalid sync mode. Must be one of: {', '.join(valid_modes)}")
            
            # Validate paths
            source = Path(source_path).expanduser().resolve()
            target = Path(target_path).expanduser().resolve()
            
            if not source.exists():
                raise FileNotFoundError(f"Source folder not found: {source_path}")
            
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
            result = self._run_bc_command([f'@{script_path}'])
            
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
                "changes_made": not dry_run and result["has_differences"],
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
    
    def start(self) -> None:
        """Start the MCP server."""
        logger.info(f"Starting Beyond Compare MCP Server on {self.host}:{self.port}")
        logger.info(f"Beyond Compare path: {self.bc_path}")
        
        uvicorn.run(
            self.app,
            host=self.host,
            port=self.port,
            log_level=settings.LOG_LEVEL.lower(),
            timeout_keep_alive=settings.API_TIMEOUT,
        )


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    server = BeyondCompareMCP()
    return server.app
