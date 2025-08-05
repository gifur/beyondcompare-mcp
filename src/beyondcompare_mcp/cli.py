"""Command-line interface for Beyond Compare MCP server."""

import argparse
import logging
import sys
from typing import Optional, List

from .server import BeyondCompareMCP
from .config import settings


def setup_logging(log_level: str = "INFO") -> None:
    """Configure logging for the application."""
    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Beyond Compare MCP Server")
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to run the MCP server on (default: 8000)",
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind the MCP server to (default: 0.0.0.0)",
    )
    
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
        print(f"Beyond Compare MCP Server v{__version__}")
        return 0
    
    # Configure logging
    setup_logging(parsed_args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        # Create and start the MCP server
        server = BeyondCompareMCP(
            host=parsed_args.host,
            port=parsed_args.port,
            bc_path=parsed_args.bc_path,
        )
        
        logger.info(f"Starting Beyond Compare MCP Server on {parsed_args.host}:{parsed_args.port}")
        logger.info(f"Beyond Compare path: {server.bc_path}")
        
        server.start()
        return 0
        
    except KeyboardInterrupt:
        logger.info("Shutting down Beyond Compare MCP Server...")
        return 0
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
