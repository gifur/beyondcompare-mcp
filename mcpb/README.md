# Beyond Compare MCP - MCPB Package

This directory contains all MCPB (MCP Bundle) packaging files for the Beyond Compare MCP server.

## 📦 Package Contents

- **mcpb.json** - Build configuration for MCPB CLI
- **manifest.json** - Runtime configuration for Claude Desktop
- **scripts/** - Build and deployment scripts
- **assets/** - Icons and screenshots for the package

## 🔨 Building the Package

### Prerequisites

```bash
# Install MCPB CLI
npm install -g @anthropic-ai/mcpb

# Install Python dependencies
pip install "fastmcp>=2.12.0,<3.0.0"
pip install -r ../requirements.txt
```

### Build Commands

```powershell
# Build without signing (development)
.\scripts\build-mcpb-package.ps1 -NoSign

# Build with signing (production - when configured)
.\scripts\build-mcpb-package.ps1

# Build with custom output directory
.\scripts\build-mcpb-package.ps1 -OutputDir "C:\builds"
```

### Manual Build

```bash
# Validate manifest
cd mcpb
mcpb validate manifest.json

# Build package
mcpb pack . ../dist/beyondcompare-mcp.mcpb
```

## 📋 Package Details

| Property | Value |
|----------|-------|
| **Name** | beyondcompare-mcp |
| **Version** | 0.1.0 |
| **Tools** | 6 |
| **Platform** | Windows, macOS, Linux |
| **Python** | >=3.10 |
| **FastMCP** | >=2.12.0 |

## 🛠️ Tools Included

1. **compare_files** - Compare two files using Beyond Compare
2. **compare_folders** - Compare two folders with optional subfolders
3. **sync_folders** - Synchronize folders (mirror, update, backup modes)
4. **multimedia_drive_scanner** - Scan multimedia drives for inventory
5. **find_multimedia_duplicates** - Find duplicate multimedia files
6. **detect_usb_drives** - Detect and list USB drives

## ⚙️ User Configuration

The package prompts users for:

1. **Beyond Compare Path** (optional) - Auto-detected if not specified
2. **Scripts Directory** (optional) - For temporary script files
3. **Log Level** (optional) - DEBUG, INFO, WARNING, ERROR, CRITICAL

## 🚀 Installation

1. Build the package: `.\scripts\build-mcpb-package.ps1 -NoSign`
2. Drag `dist/beyondcompare-mcp.mcpb` to Claude Desktop
3. Configure Beyond Compare path and preferences
4. Restart Claude Desktop

## 🔍 Troubleshooting

### Build Issues

- **MCPB CLI not found**: Install with `npm install -g @anthropic-ai/mcpb`
- **Manifest validation fails**: Check JSON syntax in manifest.json
- **Python import errors**: Ensure FastMCP 2.12.0+ is installed

### Installation Issues

- **Package won't install**: Check Claude Desktop version compatibility
- **Configuration prompts don't appear**: Verify manifest.json user_config section
- **Server fails to start**: Check Beyond Compare installation and paths

## 📚 Documentation

- [MCPB Building Guide](../docs/mcpb-packaging/MCPB_BUILDING_GUIDE.md)
- [MCPB Implementation Summary](../docs/mcpb-packaging/MCPB_IMPLEMENTATION_SUMMARY.md)
- [Main README](../README.md)

## 🔗 Related Files

- `../src/beyondcompare_mcp/` - Python source code
- `../requirements.txt` - Python dependencies
- `../pyproject.toml` - Python project configuration
- `../.github/workflows/build-mcpb.yml` - CI/CD workflow
