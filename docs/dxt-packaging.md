# DXT Packaging Guide

This document explains how to package and distribute the Beyond Compare MCP server as a DXT (Data eXchange Toolkit) package.

## What is DXT?

DXT (Data eXchange Toolkit) is a packaging format used in the MCP ecosystem to distribute and deploy MCP servers and their dependencies in a self-contained format.

## Package Structure

The DXT package follows this structure:

```
beyondcompare-mcp-0.1.0.dxt/
├── beyondcompare_mcp/     # Main package
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── exceptions.py
│   └── server.py
├── package.json          # Package metadata
├── README.md             # Project documentation
└── requirements.txt      # Dependencies
```

## Building the DXT Package

To build the DXT package, use the provided build script:

```bash
# Install build dependencies
pip install build

# Build the DXT package
python dxt_build.py
```

This will create a `dist` directory containing the DXT package:

```
dist/
└── beyondcompare-mcp-0.1.0.dxt
```

## Package Metadata

The `package.json` file contains metadata about the package:

```json
{
    "name": "beyondcompare-mcp",
    "version": "0.1.0",
    "description": "Beyond Compare MCP Server for FastMCP 2.10",
    "author": "Your Name",
    "author_email": "your.email@example.com",
    "python": ">=3.8",
    "dependencies": [
        "fastmcp>=2.10.0",
        "python-dotenv>=1.0.0",
        "pydantic>=1.10.0",
        "uvicorn>=0.20.0"
    ],
    "entry_points": {
        "console_scripts": [
            "beyondcompare-mcp=beyondcompare_mcp.cli:main"
        ]
    }
}
```

## Dependencies

The package includes all required dependencies in the `requirements.txt` file. These will be automatically installed when the package is deployed.

## Deployment

### Prerequisites

- Python 3.8 or higher
- Beyond Compare installed on the target system
- Network access to PyPI (if not using an offline package)

### Installation

1. Copy the DXT package to the target system
2. Install the package using the MCP CLI:

```bash
mcp package install beyondcompare-mcp-0.1.0.dxt
```

### Configuration

Create a `.env` file in the deployment directory:

```ini
# Path to Beyond Compare executable (auto-detected if not specified)
BEYOND_COMPARE_PATH="C:\\Program Files\\Beyond Compare 4\\BCompare.exe"

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Directory to store temporary script files
BC_SCRIPTS_DIR="./bc_scripts"

# Server configuration
HOST=0.0.0.0
PORT=8000
```

## Running the Server

### Using the CLI

```bash
# Start the server
beyondcompare-mcp

# With custom options
beyondcompare-mcp --host 0.0.0.0 --port 8080 --log-level DEBUG
```

### As a Python Module

```python
from beyondcompare_mcp import BeyondCompareMCP

# Create and start the server
server = BeyondCompareMCP(host="0.0.0.0", port=8000)
server.start()
```

## Verifying the Installation

Check that the server is running by accessing the health endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
    "status": "ok",
    "service": "beyondcompare-mcp"
}
```

## Upgrading

To upgrade to a new version:

1. Stop the running server
2. Install the new DXT package
3. Restart the server

## Troubleshooting

### Beyond Compare Not Found

If you see an error about Beyond Compare not being found:

1. Verify that Beyond Compare is installed
2. Check that the `BEYOND_COMPARE_PATH` environment variable is set correctly
3. Ensure the user running the server has permission to execute the Beyond Compare binary

### Port Already in Use

If the default port (8000) is already in use, specify a different port:

```bash
beyondcompare-mcp --port 8001
```

### Permission Denied

If you encounter permission errors when running the server, ensure the user has the necessary permissions to:
- Read the source and target directories
- Write to the `BC_SCRIPTS_DIR` directory
- Execute the Beyond Compare binary
