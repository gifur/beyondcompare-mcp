# Antigravity IDE Wrapper Setup

**Date**: 2025-12-12  
**Purpose**: Fix "invalid trailing data" error in Antigravity IDE

## Problem

Antigravity IDE reports: `"invalid trailing data at the end of stream"` when calling `initialize`.

This is caused by Windows line ending conversion (`\r\n` → `\n`) where the `\r` is interpreted as trailing data after JSON-RPC messages.

## Solution: Use Wrapper Script

A wrapper script ensures binary mode is set **BEFORE** any imports, which is critical for Antigravity IDE.

## Setup Instructions

### Option 1: Use wrapper.py (Recommended)

1. **Update Antigravity config** (`mcp_config.json`):

```json
{
  "mcpServers": {
    "beyondcompare-mcp": {
      "command": "python",
      "args": [
        "D:\\Dev\\repos\\beyondcompare-mcp\\wrapper.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Important**: Use **absolute path** to `wrapper.py` (Antigravity requires absolute paths).

### Option 2: Use python -m (Alternative)

If wrapper.py doesn't work, try using the updated `__main__.py`:

```json
{
  "mcpServers": {
    "beyondcompare-mcp": {
      "command": "python",
      "args": [
        "-u",
        "-m",
        "beyondcompare_mcp"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Note**: This requires the package to be installed (`pip install -e .`).

### Option 3: Direct Script Execution

If both above fail, try direct script execution:

```json
{
  "mcpServers": {
    "beyondcompare-mcp": {
      "command": "python",
      "args": [
        "-u",
        "D:\\Dev\\repos\\beyondcompare-mcp\\src\\beyondcompare_mcp\\cli.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

## What the Wrapper Does

1. **Sets binary mode FIRST** - Before any imports
2. **Prevents line ending conversion** - Windows `\r\n` stays as-is
3. **Sets unbuffered mode** - Prevents buffering issues
4. **Then imports server** - Safe to import after binary mode is set

## Testing

After updating config:

1. **Restart Antigravity IDE completely**
2. **Check Antigravity logs** for the error
3. **Test a tool call** to verify it works

## Troubleshooting

### Still Getting "invalid trailing data"

1. **Verify absolute paths** - Antigravity requires absolute paths
2. **Check Python version** - Ensure Python 3.10+ is in PATH
3. **Check package installation** - Run `pip install -e .` in repo directory
4. **Try different entry point** - Try Option 2 or 3 above

### Server Doesn't Start

1. **Test wrapper manually**:
   ```powershell
   cd D:\Dev\repos\beyondcompare-mcp
   python wrapper.py
   ```
   Should see no output (stdout is for JSON-RPC only).

2. **Check stderr** for errors:
   ```powershell
   python wrapper.py 2>&1
   ```

### FastMCP Errors

If FastMCP itself has issues:
1. **Update FastMCP**: `pip install --upgrade fastmcp`
2. **Check FastMCP GitHub** for Antigravity-specific fixes
3. **Consider reporting issue** to FastMCP maintainers

## Files Modified

- `wrapper.py` - New wrapper script
- `src/beyondcompare_mcp/__main__.py` - Updated with binary mode fix
- `src/beyondcompare_mcp/server.py` - Already has binary mode fixes
- `src/beyondcompare_mcp/cli.py` - Already has binary mode fixes

## References

- [Antigravity MCP Tutorial](https://antigravity.codes/blog/antigravity-mcp-tutorial)
- [FastMCP GitHub Issues](https://github.com/jlowin/fastmcp/issues)
- [Laravel Boost Issue #362](https://github.com/laravel/boost/issues/362) - Same error

