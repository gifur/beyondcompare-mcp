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

from .config import settings


def setup_logging(log_level: str = "INFO") -> None:
    """Configure logging for the application.
    
    CRITICAL: For MCP servers using stdio transport, logs MUST go to stderr,
    not stdout. stdout is reserved for JSON-RPC messages only.
    
    In stdio mode, we suppress ALL logging to prevent any interference with JSON-RPC.
    """
    # This command is stdio-only. Keep logs silent so JSON-RPC stdout is clean
    # when launched by an MCP client, and so manual runs simply wait for input.
    logging.basicConfig(
        level=logging.CRITICAL,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stderr)],
        force=True,
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.CRITICAL)
    root_logger.handlers = []
    for logger_name in ["fastmcp", "mcp", "asyncio", "beyondcompare_mcp"]:
        log = logging.getLogger(logger_name)
        log.setLevel(logging.CRITICAL)
        log.handlers = []
        log.propagate = False


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
    """Run the local Beyond Compare MCP server over stdio."""
    argv = list(args) if args is not None else sys.argv[1:]
    if "--version" in argv or "-V" in argv:
        from . import __version__

        print(f"Beyond Compare MCP Server v{__version__}")
        return 0

    parsed = parse_args(argv)
    setup_logging(parsed.log_level)
    logger = logging.getLogger(__name__)

    try:
        if os.name == "nt":
            try:
                import msvcrt

                try:
                    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
                except (OSError, AttributeError):
                    pass
            except (ImportError, OSError, AttributeError):
                pass

        from .server import BeyondCompareMCP

        BeyondCompareMCP(
            bc_path=parsed.bc_path,
            scripts_dir=parsed.scripts_dir,
        ).run()
        return 0
    except KeyboardInterrupt:
        logger.info("Shutting down Beyond Compare MCP Server...")
        return 0
    except Exception as e:
        logger.critical("Fatal error: %s", e, exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
