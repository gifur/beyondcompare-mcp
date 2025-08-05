# Beyond Compare MCP

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A FastMCP 2.10 compliant MCP server that provides file and directory comparison capabilities using Beyond Compare.

## ✨ Features

- **File and Folder Comparison**: Compare files and directories with Beyond Compare's powerful engine
- **Directory Synchronization**: Keep folders in sync with various sync modes (mirror, update, backup)
- **Diff Report Generation**: Generate detailed comparison reports in multiple formats
- **FastMCP 2.10 Compliant**: Seamless integration with the MCP ecosystem
- **DXT Packaging**: Easy deployment with DXT packages
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- [Beyond Compare](https://www.scootersoftware.com/) installed on your system

### Install from PyPI

```bash
pip install beyondcompare-mcp
```

### Install from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/beyondcompare-mcp.git
   cd beyondcompare-mcp
   ```

2. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

## ⚙️ Configuration

Create a `.env` file in your project directory:

```ini
# Path to Beyond Compare executable (auto-detected if not specified)
BEYOND_COMPARE_PATH="C:\\Program Files\\Beyond Compare 4\\BCompare.exe"

# Server configuration
HOST=0.0.0.0
PORT=8000

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Directory to store temporary script files
BC_SCRIPTS_DIR="./bc_scripts"
```

## 🏃‍♂️ Usage

### Command Line Interface

```bash
# Start the MCP server
beyondcompare-mcp

# With custom configuration
beyondcompare-mcp --host 0.0.0.0 --port 8080 --log-level DEBUG
```

### Python API

```python
from beyondcompare_mcp import BeyondCompareMCP

# Create and start the server
server = BeyondCompareMCP(
    host="0.0.0.0",
    port=8000,
    bc_path="C:\\Program Files\\Beyond Compare 4\\BCompare.exe"
)
server.start()
```

### MCP Tools

The server provides the following MCP tools:

1. **compare_files**
   ```python
   result = await client.compare_files(
       left_path="/path/to/left/file.txt",
       right_path="/path/to/right/file.txt",
       output_report="/path/to/report.html"
   )
   ```

2. **compare_folders**
   ```python
   result = await client.compare_folders(
       left_path="/path/to/left/folder",
       right_path="/path/to/right/folder",
       output_report="/path/to/report.html",
       include_subfolders=True
   )
   ```

3. **sync_folders**
   ```python
   result = await client.sync_folders(
       source_path="/path/to/source",
       target_path="/path/to/target",
       sync_mode="mirror",  # 'mirror', 'update', or 'backup'
       dry_run=True
   )
   ```

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage report
pytest --cov=beyondcompare_mcp --cov-report=term-missing
```

## 📦 DXT Packaging

To create a DXT package:

```bash
# Install build dependencies
pip install build

# Build the DXT package
python dxt_build.py
```

The package will be created in the `dist` directory.

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to contribute to this project.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Documentation

For detailed documentation, please see the [docs](docs/) directory:

- [MCP Compliance](docs/mcp-compliance.md)
- [DXT Packaging Guide](docs/dxt-packaging.md)

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a history of changes to this project.
