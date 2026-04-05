#!/usr/bin/env python
"""
Wrapper script for Beyond Compare MCP Server.

This wrapper ensures binary mode is set on Windows BEFORE any imports,
which is critical for Antigravity IDE compatibility.

CRITICAL: Binary mode MUST be set before any imports that might use stdout.
Antigravity IDE is strict about JSON-RPC protocol and interprets trailing \r 
as "invalid trailing data" - binary mode prevents line ending conversion.
"""

import sys
import os

# CRITICAL: Set binary mode FIRST, before ANY other imports
if os.name == 'nt':  # Windows
    try:
        import msvcrt
        # Set stdin/stdout to binary mode to prevent line ending conversion
        # This fixes "invalid trailing data" errors with Antigravity IDE
        try:
            msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        except (OSError, AttributeError):
            pass  # stdin might not be a real file descriptor
        try:
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        except (OSError, AttributeError):
            pass  # stdout might not be a real file descriptor
    except (ImportError, OSError, AttributeError):
        pass  # If msvcrt is not available, continue anyway

# Set unbuffered mode
os.environ.setdefault('PYTHONUNBUFFERED', '1')

# Now import and run the server via CLI (which handles logging properly)
if __name__ == "__main__":
    from beyondcompare_mcp.cli import main
    import sys
    sys.exit(main())

