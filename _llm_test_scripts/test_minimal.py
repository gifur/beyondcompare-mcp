#!/usr/bin/env python
"""
Minimal FastMCP server test for Antigravity IDE.

This is the absolute minimum FastMCP server to test if the issue
is with FastMCP itself or with the server's initialization code.
"""

import sys
import os

# CRITICAL: Set binary mode FIRST, before ANY other imports
if os.name == 'nt':  # Windows
    try:
        import msvcrt
        try:
            msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        except (OSError, AttributeError):
            pass
        try:
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        except (OSError, AttributeError):
            pass
    except (ImportError, OSError, AttributeError):
        pass

# Set unbuffered mode
os.environ.setdefault('PYTHONUNBUFFERED', '1')

# Patch stdout to prevent ANY writes during initialization
if not sys.stdout.isatty():
    class DevNullStdout:
        def write(self, s: str) -> int:
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
    
    if not hasattr(sys, '_original_stdout'):
        sys._original_stdout = sys.stdout
    sys.stdout = DevNullStdout()

# Configure logging to stderr only
import logging
logging.basicConfig(
    level=logging.CRITICAL,
    format="%(message)s",
    stream=sys.stderr,
    force=True,
)

# Suppress all loggers
root_logger = logging.getLogger()
root_logger.setLevel(logging.CRITICAL)
root_logger.handlers = []

for logger_name in ['fastmcp', 'mcp', 'httpx', 'httpcore', 'h11', 'uvicorn', 'asyncio']:
    log = logging.getLogger(logger_name)
    log.setLevel(logging.CRITICAL)
    log.handlers = []
    log.propagate = False

# NOW import FastMCP (after stdout is patched)
from fastmcp import FastMCP

# Create minimal MCP server - absolute minimum
# FastMCP handles initialize automatically, we can't override it
mcp = FastMCP(name="Minimal Test MCP")

# Add one minimal tool (optional - can remove if needed)
@mcp.tool()
def test_tool() -> str:
    """Minimal test tool."""
    return "Test successful"

# Restore stdout before running
if hasattr(sys, '_original_stdout'):
    sys.stdout = sys._original_stdout
    
    # Set binary mode after restoration
    if os.name == 'nt':
        try:
            import msvcrt
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        except (ImportError, OSError, AttributeError):
            pass
    
    sys.stdout.flush()
    os.environ.setdefault('PYTHONUNBUFFERED', '1')

# Run server
if __name__ == "__main__":
    mcp.run(show_banner=False)

