"""
Beyond Compare MCP Server

A FastMCP 2.10 compliant MCP server that provides file and directory comparison
capabilities using Beyond Compare.
"""

__version__ = "0.1.0"

from .server import BeyondCompareMCP
from .exceptions import (
    BeyondCompareError,
    BeyondCompareNotInstalledError,
    BeyondCompareCommandError,
    BeyondCompareTimeoutError,
)

__all__ = [
    "BeyondCompareMCP",
    "BeyondCompareError",
    "BeyondCompareNotInstalledError",
    "BeyondCompareCommandError",
    "BeyondCompareTimeoutError",
]
