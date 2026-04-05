# Minimal Test Server Setup

**Purpose**: Test if the issue is with FastMCP itself or with the server's initialization code.

## Test Server

Created `test_minimal.py` - the absolute minimum FastMCP server:
- No Beyond Compare code
- No complex initialization
- Just FastMCP + one test tool
- All stdout protection in place

## Setup in Antigravity

Update `mcp_config.json`:

```json
{
  "mcpServers": {
    "minimal-test": {
      "command": "python",
      "args": [
        "D:\\Dev\\repos\\beyondcompare-mcp\\test_minimal.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

## What This Tests

1. **If this works**: The issue is with beyondcompare-mcp's initialization code
2. **If this fails**: The issue is with FastMCP itself or Antigravity's Python subprocess handling

## Expected Behavior

- **Success**: Server connects, `test_tool` is available, no "invalid trailing data" error
- **Failure**: Same "invalid trailing data" error → indicates FastMCP/Antigravity issue

## Next Steps Based on Results

### If Minimal Test Works
- The issue is in beyondcompare-mcp's initialization
- Check what's different between minimal and full server
- Look for stdout writes during BeyondCompareMCP.__init__()

### If Minimal Test Fails
- The issue is with FastMCP or Antigravity
- Check FastMCP GitHub for Antigravity-specific issues
- Consider reporting to FastMCP maintainers
- May need to wait for FastMCP/Antigravity fix



