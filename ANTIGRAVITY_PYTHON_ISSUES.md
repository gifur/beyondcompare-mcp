# Antigravity IDE Python MCP Server Issues

**Date**: 2025-12-12  
**Status**: Known issue affecting Python MCP servers, npx servers work fine

## Key Findings

### 1. **This is a Known Problem**
Multiple Python MCP servers have the same issue with Antigravity IDE:

- **FastMCP**: GitHub issue about Antigravity IDE compatibility
  - https://github.com/jlowin/fastmcp/issues
- **Laravel Boost**: Same "invalid trailing data" error
  - https://github.com/laravel/boost/issues/362
- **Flutter MCP Server**: Also fails in Antigravity
  - https://github.com/flutter/flutter/issues/179048

### 2. **npx Servers Work Fine**
- **Brighthand** (npx-based) works perfectly in Antigravity
- **Blender MCP Server v2** (optimized for Antigravity) works
- This suggests **Antigravity handles Node.js subprocesses differently** than Python

### 3. **Root Cause Hypothesis**

The fact that **npx servers work but Python servers don't** suggests:

1. **Subprocess Execution**: Antigravity may spawn Python processes differently than Node.js processes
2. **Environment Variables**: Python subprocesses might inherit different environment settings
3. **Stdio Handling**: Python's stdio handling in subprocess context may differ from Node.js
4. **Binary Mode**: Python's text mode vs binary mode handling might be the issue

## Current Fixes Applied

### ✅ Binary Mode (Already Applied)
- Set stdin/stdout to binary mode on Windows
- Prevents line ending conversion (`\r\n` → `\n`)

### ✅ Stdout Patching (Already Applied)
- Patch stdout to DevNullStdout during initialization
- Restore before FastMCP.run()
- Redirect all logging to stderr

### ⚠️ Still Not Working
Despite these fixes, the error persists. This suggests:

1. **FastMCP itself** might be writing to stdout
2. **Python subprocess** handling by Antigravity is different
3. **Environment variables** might affect Python's stdio behavior

## Potential Solutions

### Solution 1: Check FastMCP Version
FastMCP might have Antigravity-specific fixes in newer versions:
```bash
pip install --upgrade fastmcp
```

### Solution 2: Environment Variables
Antigravity might need specific environment variables:
```json
{
  "mcpServers": {
    "beyondcompare-mcp": {
      "command": "python",
      "args": ["-u", "-m", "beyondcompare_mcp"],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

### Solution 3: Use Python -u Flag
Force unbuffered output:
```json
{
  "args": ["-u", "-m", "beyondcompare_mcp"]
}
```

### Solution 4: Wrapper Script
Create a wrapper script that ensures binary mode:
```python
# wrapper.py
import sys
import os
import msvcrt

if os.name == 'nt':
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

from beyondcompare_mcp.server import main
main()
```

### Solution 5: Check Antigravity's Python Execution
Antigravity might be using a different Python interpreter or path. Check:
- Python version in Antigravity config
- Python path resolution
- Virtual environment activation

## Comparison: npx vs Python

### npx Servers (Work)
- Node.js handles stdio differently
- npx provides standardized execution environment
- No binary mode issues (Node.js handles this automatically)

### Python Servers (Don't Work)
- Python's subprocess stdio handling
- Text mode vs binary mode issues
- Environment variable dependencies

## Next Steps

1. **Check FastMCP GitHub Issues**
   - Look for Antigravity-specific fixes
   - Check if there's a known workaround

2. **Test with Minimal Server**
   - Create simplest possible FastMCP server
   - Test if it works in Antigravity
   - Isolate the issue

3. **Compare with Working npx Server**
   - Check how Brighthand handles stdio
   - See if we can replicate that in Python

4. **Contact Antigravity Support**
   - Report the issue
   - Ask about Python subprocess handling
   - Request documentation on Python MCP servers

5. **Try Alternative Entry Point**
   - Use `python -u -m` instead of direct script
   - Use wrapper script
   - Try different Python execution methods

## References

- [Antigravity MCP Tutorial](https://antigravity.codes/blog/antigravity-mcp-tutorial)
- [FastMCP GitHub Issues](https://github.com/jlowin/fastmcp/issues)
- [Laravel Boost Issue #362](https://github.com/laravel/boost/issues/362)
- [Flutter MCP Issue #179048](https://github.com/flutter/flutter/issues/179048)

