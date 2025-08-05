# Beyond Compare MCP - MCP Compliance

This document outlines how the Beyond Compare MCP server complies with the FastMCP 2.10 specification and MCP (Model-Controller-Presenter) architecture patterns.

## FastMCP 2.10 Compliance

The Beyond Compare MCP server is designed to be fully compliant with FastMCP 2.10, providing a standardized interface for file and directory comparison operations. Below are the key compliance points:

### 1. MCP Tool Registration

All MCP tools are registered using the `@mcp.tool()` decorator from FastMCP, ensuring proper integration with the MCP ecosystem.

```python
@mcp.tool()
def compare_files(
    left_path: str,
    right_path: str,
    output_report: Optional[str] = None,
) -> Dict[str, Any]:
    """Compare two files using Beyond Compare."""
    # Implementation...
```

### 2. Standardized Response Format

All MCP tools return responses in a standardized format:

```json
{
    "success": true,
    "message": "Descriptive message about the operation",
    "data": {
        // Operation-specific data
    },
    "error": null  // Only present if success is false
}
```

### 3. Error Handling

Consistent error handling is implemented using custom exceptions that extend `BeyondCompareError`:

- `BeyondCompareNotInstalledError`: When Beyond Compare is not found
- `BeyondCompareCommandError`: When a Beyond Compare command fails
- `BeyondCompareTimeoutError`: When a command times out
- `BeyondCompareScriptError`: When there's an error in a Beyond Compare script

### 4. Configuration Management

Configuration is managed through environment variables with sensible defaults, following the 12-factor app principles. The configuration is validated using Pydantic's `BaseSettings`.

## MCP Architecture

The application follows the Model-Controller-Presenter (MCP) architecture pattern:

### Model

- `BeyondCompareAPI`: Handles low-level interaction with the Beyond Compare executable
- `Settings`: Manages configuration and environment variables

### Controller

- `BeyondCompareMCP`: Main controller that coordinates between the model and presenter
- MCP Tools: Individual functions that handle specific operations (compare, sync, etc.)

### Presenter

- `cli.py`: Command-line interface for the MCP server
- API Responses: Standardized JSON responses for MCP clients

## Dependencies

The server has minimal external dependencies:

- `fastmcp>=2.10.0`: Core MCP framework
- `python-dotenv>=1.0.0`: Environment variable management
- `pydantic>=1.10.0`: Data validation and settings management
- `uvicorn>=0.20.0`: ASGI server for FastAPI
- `fastapi>=0.95.0`: Web framework for the MCP server

## Security Considerations

1. **Input Validation**: All input paths are validated to prevent directory traversal attacks
2. **Secure Defaults**: The server binds to localhost by default
3. **Error Handling**: Sensitive information is not leaked in error messages
4. **Logging**: Logs are written to stderr by default with configurable log levels
