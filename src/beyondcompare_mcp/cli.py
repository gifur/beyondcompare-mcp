"""Command-line interface for Beyond Compare MCP server."""

# CRITICAL: Set stdio to binary mode on Windows for Antigravity IDE compatibility
# MUST be done BEFORE any imports that might use stdout
# Antigravity IDE is strict about JSON-RPC protocol and interprets trailing \r as "invalid trailing data"
# Binary mode prevents Python from automatically converting line endings
import os
if os.name == 'nt':  # Windows
    try:
        import msvcrt
        import sys
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

import argparse
import logging
import sys
from typing import Optional, List

from .server import BeyondCompareMCP
from .config import settings


def setup_logging(log_level: str = "INFO") -> None:
    """Configure logging for the application.
    
    CRITICAL: For MCP servers using stdio transport, logs MUST go to stderr,
    not stdout. stdout is reserved for JSON-RPC messages only.
    
    In stdio mode, we suppress ALL logging to prevent any interference with JSON-RPC.
    """
    # Detect if we're in stdio mode (MCP server)
    is_stdio_mode = (
        not sys.stdout.isatty() 
        or os.getenv("MCP_STDIO_MODE", "").lower() == "true"
        or "stdio" in sys.argv
    )
    
    if is_stdio_mode:
        # CRITICAL: In stdio mode, suppress ALL logging to prevent stdout pollution
        # Even stderr logging can cause issues if Antigravity is strict about it
        logging.basicConfig(
            level=logging.CRITICAL,  # Only CRITICAL, suppress everything else
            format="%(message)s",
            handlers=[logging.StreamHandler(sys.stderr)],
            force=True,
        )
        # Suppress all loggers
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.CRITICAL)
        root_logger.handlers = []
        for logger_name in ['fastmcp', 'mcp', 'httpx', 'httpcore', 'h11', 'uvicorn', 'asyncio', 'beyondcompare_mcp']:
            log = logging.getLogger(logger_name)
            log.setLevel(logging.CRITICAL)
            log.handlers = []
            log.propagate = False
    else:
        # Normal mode - use requested log level
        level = getattr(logging, log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(sys.stderr),  # Use stderr instead of stdout
            ],
        )


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Beyond Compare MCP Server")

    parser.add_argument(
        "--log-level",
        type=str,
        default=settings.LOG_LEVEL,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO)",
    )

    parser.add_argument(
        "--bc-path",
        type=str,
        default=settings.BEYOND_COMPARE_PATH,
        help="Path to Beyond Compare executable (default: auto-detect)",
    )

    parser.add_argument(
        "--scripts-dir",
        type=str,
        default=settings.BC_SCRIPTS_DIR,
        help="Directory for temporary script files (default: ./bc_scripts)",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version and exit",
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Run the Beyond Compare MCP server from the command line."""
    parsed_args = parse_args(args)

    if parsed_args.version:
        from . import __version__
        logger = logging.getLogger(__name__)
        logger.info(f"Beyond Compare MCP Server v{__version__}")
        return 0

    # Configure logging
    setup_logging(parsed_args.log_level)
    logger = logging.getLogger(__name__)

    try:
        # CRITICAL: Ensure binary mode is set before creating server for Antigravity IDE compatibility
        # This prevents "invalid trailing data" errors caused by Windows line ending conversion
        if os.name == 'nt':  # Windows
            try:
                import msvcrt
                # Set stdout to binary mode if not already set (may have been set at module level)
                try:
                    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
                except (OSError, AttributeError):
                    pass  # stdout might not be a real file descriptor or already in binary mode
            except (ImportError, OSError, AttributeError):
                pass  # If msvcrt is not available, continue anyway

        # Detect if we're in stdio mode
        is_stdio_mode = (
            not sys.stdout.isatty() 
            or os.getenv("MCP_STDIO_MODE", "").lower() == "true"
            or "stdio" in sys.argv
        )

        # Create and start the MCP server
        server = BeyondCompareMCP(
            bc_path=parsed_args.bc_path,
            scripts_dir=parsed_args.scripts_dir,
        )

        # CRITICAL: Only log if NOT in stdio mode
        # In stdio mode, ANY logging can cause "invalid trailing data" errors
        if not is_stdio_mode:
            logger.info("Starting Beyond Compare MCP Server")
            if server.bc_path:
                logger.info(f"Beyond Compare path: {server.bc_path}")
            else:
                logger.warning("Beyond Compare executable not found - server may not function properly")

        server.run()
        return 0

    except KeyboardInterrupt:
        # Only log if not in stdio mode
        is_stdio_mode = (
            not sys.stdout.isatty() 
            or os.getenv("MCP_STDIO_MODE", "").lower() == "true"
            or "stdio" in sys.argv
        )
        if not is_stdio_mode:
            logger.info("Shutting down Beyond Compare MCP Server...")
        return 0
    except Exception as e:
        # Critical errors should always be logged (to stderr)
        logger.critical(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
