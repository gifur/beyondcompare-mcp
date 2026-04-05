# Antigravity IDE Python MCP Server Bug Report

**Date**: 2025-12-13  
**Status**: Confirmed Antigravity IDE bug affecting Python MCP servers  
**Impact**: Python MCP servers cannot connect to Antigravity IDE

## Problem Summary

Antigravity IDE reports `"invalid trailing data at the end of stream"` when attempting to initialize ANY Python MCP server. This prevents all Python MCP servers from working in Antigravity IDE.

**Confirmed affected servers:**
- advanced-memory-mcp
- beyondcompare-mcp
- Minimal test servers

**Working alternatives:**
- npx-based servers (Brighthand, etc.) work perfectly
- Same servers work in Cursor IDE, Claude Desktop, Zed IDE

## Root Cause Analysis

This is **NOT a bug in our MCP server code**. The issue is in Antigravity IDE's subprocess handling:

1. **Subprocess stdout corruption**: Antigravity's Python subprocess spawning corrupts stdout
2. **Line ending conversion**: Windows `\r\n` → `\n` conversion interpreted as trailing data
3. **Timing issues**: Subprocess initialization writes to stdout before JSON-RPC protocol starts

**Evidence:**
- Same server code works perfectly in other IDEs
- npx servers work fine (different subprocess handling)
- All stdout protection measures implemented but still fails
- Binary mode fixes, stdout patching, logging suppression - all tried and failed

## Technical Details

### Attempts Made (All Failed)

1. **Binary Mode**: Set stdin/stdout to binary mode before imports
2. **Stdout Patching**: Patch stdout to /dev/null during initialization
3. **Logging Suppression**: Suppress all INFO/DEBUG logs in stdio mode
4. **Wrapper Scripts**: Run server through wrapper to set binary mode early
5. **Minimal Test**: Created minimal FastMCP server - still fails
6. **Environment Variables**: Set PYTHONUNBUFFERED=1, PYTHONIOENCODING=utf-8

### Error Pattern

```
[12/13/25 00:02:44] INFO Starting MCP server 'Server Name' with transport 'stdio'
: calling "initialize": invalid trailing data at the end of stream.
```

The error occurs during the `initialize` call, suggesting stdout corruption during subprocess startup.

## Workarounds

### ✅ Confirmed Working
- Use **npx-based MCP servers** (Brighthand works fine)
- Use **other IDEs**: Cursor IDE, Claude Desktop, Zed IDE (all work perfectly)

### ❌ Not Recommended
- Converting Python servers to Node.js (major rewrite)
- Disabling Antigravity IDE features

## Report to Antigravity

This should be reported as a bug to Antigravity IDE developers:

**Bug Report Template:**
```
Title: Python MCP servers fail with "invalid trailing data" error

Description:
Python MCP servers consistently fail to connect with "invalid trailing data at the end of stream" during initialize call.

Steps to reproduce:
1. Install any Python MCP server (e.g., advanced-memory-mcp, beyondcompare-mcp)
2. Configure in Antigravity mcp_config.json
3. Attempt to use any tool
4. Error occurs: "invalid trailing data at the end of stream"

Expected behavior:
Python MCP servers should connect and work like npx servers do.

Environment:
- Antigravity IDE: [version]
- Python: 3.10+
- OS: Windows 11

Additional notes:
- Same servers work perfectly in Cursor IDE, Claude Desktop, Zed IDE
- npx servers work fine in Antigravity IDE
- Issue appears to be with Python subprocess stdout handling
```

## References

- [FastMCP GitHub Issues](https://github.com/jlowin/fastmcp/issues) - Similar reports
- [Laravel Boost Issue #362](https://github.com/laravel/boost/issues/362) - Same error
- [Flutter MCP Issue #179048](https://github.com/flutter/flutter/issues/179048) - Similar issues

## Conclusion

This is an Antigravity IDE bug, not a server code issue. Python MCP servers cannot be made to work in Antigravity IDE until they fix their subprocess handling.

**Recommendation**: Use other IDEs or switch to npx-based MCP servers for Antigravity IDE.


