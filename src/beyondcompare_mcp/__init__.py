"""Beyond Compare MCP package."""

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.1.0"

__all__ = [
    "__version__",
    "BeyondCompareMCP",
    "BeyondCompareError",
    "BeyondCompareNotInstalledError",
    "BeyondCompareCommandError",
    "BeyondCompareTimeoutError",
    "BeyondCompareScriptError",
]


def __getattr__(name: str):
    if name == "BeyondCompareMCP":
        from .server import BeyondCompareMCP

        return BeyondCompareMCP

    if name in {
        "BeyondCompareError",
        "BeyondCompareNotInstalledError",
        "BeyondCompareCommandError",
        "BeyondCompareTimeoutError",
        "BeyondCompareScriptError",
    }:
        from . import exceptions

        return getattr(exceptions, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
