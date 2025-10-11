# 📚 Beyond Compare MCP - API Documentation

## Overview

The Beyond Compare MCP Server provides 6 powerful tools for file and directory comparison, synchronization, and multimedia management. All tools are accessible through the Model Context Protocol (MCP) interface.

---

## 🛠️ Tool Reference

### 1. `compare_files`

**Purpose**: Compare two files using Beyond Compare and get detailed comparison results.

**Parameters**:
- `left_path` (string, required): Path to the first file to compare
- `right_path` (string, required): Path to the second file to compare  
- `output_report` (string, optional): Path where to save HTML comparison report

**Returns**:
```json
{
  "success": true,
  "data": {
    "comparison_result": "different|identical|binary_different|left_newer|right_newer|left_missing|right_missing",
    "left_path": "/path/to/file1.txt",
    "right_path": "/path/to/file2.txt",
    "report_path": "/path/to/report.html",
    "execution_time": 1.23
  }
}
```

**Example Usage**:
```python
result = compare_files(
    left_path="/docs/version1.txt",
    right_path="/docs/version2.txt",
    output_report="/reports/comparison.html"
)
```

**Use Cases**:
- Code review and diff analysis
- Document version comparison
- Configuration file validation
- Content verification

---

### 2. `compare_folders`

**Purpose**: Compare two directories using Beyond Compare to identify differences in structure and content.

**Parameters**:
- `left_path` (string, required): Path to the first directory
- `right_path` (string, required): Path to the second directory
- `output_report` (string, optional): Path for HTML comparison report
- `include_subfolders` (boolean, default: true): Whether to compare subdirectories recursively

**Returns**:
```json
{
  "success": true,
  "data": {
    "comparison_summary": {
      "total_files": 156,
      "identical_files": 120,
      "different_files": 25,
      "left_only_files": 8,
      "right_only_files": 3
    },
    "report_path": "/path/to/report.html",
    "execution_time": 5.67
  }
}
```

**Example Usage**:
```python
result = compare_folders(
    left_path="/project/v1.0",
    right_path="/project/v1.1",
    output_report="/reports/folder_diff.html",
    include_subfolders=True
)
```

**Use Cases**:
- Project version comparison
- Backup verification
- Directory synchronization planning
- Code base analysis

---

### 3. `sync_folders`

**Purpose**: Synchronize two directories using Beyond Compare's powerful sync capabilities.

**Parameters**:
- `source_path` (string, required): Source directory path
- `target_path` (string, required): Target directory path
- `sync_mode` (string, default: "mirror"): Sync mode - "mirror", "update", "merge"
- `dry_run` (boolean, default: true): Preview changes without executing
- `delete_orphans` (boolean, default: false): Delete files that exist only in target
- `include_subfolders` (boolean, default: true): Sync subdirectories recursively

**Returns**:
```json
{
  "success": true,
  "data": {
    "sync_summary": {
      "files_copied": 15,
      "files_updated": 8,
      "files_deleted": 2,
      "total_operations": 25
    },
    "dry_run": true,
    "execution_time": 3.45
  }
}
```

**Example Usage**:
```python
# Preview sync operations
result = sync_folders(
    source_path="/data/master",
    target_path="/backup/mirror",
    sync_mode="mirror",
    dry_run=True
)

# Execute actual sync
result = sync_folders(
    source_path="/data/master",
    target_path="/backup/mirror",
    sync_mode="mirror", 
    dry_run=False
)
```

**Use Cases**:
- Automated backups
- Directory mirroring
- Content deployment
- Data migration

---

### 4. `multimedia_drive_scanner`

**Purpose**: Scan Sandra's multimedia drives (E:, F:, K:, L:) for complete inventory of media files.

**Parameters**:
- `drives` (array, optional): List of drive letters to scan (default: ["E:", "F:", "K:", "L:"])
- `file_types` (array, optional): File extensions to include (default: multimedia types)
- `include_metadata` (boolean, default: true): Extract file metadata (size, date, etc.)
- `output_format` (string, default: "json"): Output format - "json", "csv", "html"

**Returns**:
```json
{
  "success": true,
  "data": {
    "scan_summary": {
      "total_files": 45678,
      "total_size_gb": 2048.5,
      "drives_scanned": ["E:", "F:", "K:", "L:"],
      "file_types": {
        "video": 12456,
        "audio": 23789,
        "image": 9433
      }
    },
    "files": [
      {
        "path": "E:\\Movies\\Action\\movie1.mp4",
        "size_bytes": 1073741824,
        "modified_date": "2024-01-15T10:30:00Z",
        "type": "video"
      }
    ],
    "execution_time": 45.23
  }
}
```

**Example Usage**:
```python
result = multimedia_drive_scanner(
    drives=["E:", "F:"],
    file_types=["mp4", "mkv", "avi", "mp3", "flac"],
    include_metadata=True,
    output_format="json"
)
```

**Use Cases**:
- Media library cataloging
- Storage analysis
- Duplicate detection preparation
- Backup planning

---

### 5. `find_multimedia_duplicates`

**Purpose**: Find duplicate multimedia files across Sandra's drives using content analysis.

**Parameters**:
- `drives` (array, optional): Drives to search (default: ["E:", "F:", "K:", "L:"])
- `comparison_method` (string, default: "hash"): Method - "hash", "content", "metadata"
- `file_types` (array, optional): File types to check for duplicates
- `min_file_size_mb` (number, default: 1): Minimum file size to consider
- `output_report` (string, optional): Path for duplicate report

**Returns**:
```json
{
  "success": true,
  "data": {
    "duplicate_groups": [
      {
        "group_id": 1,
        "file_count": 3,
        "total_size_mb": 1500.5,
        "files": [
          {
            "path": "E:\\Movies\\movie1.mp4",
            "size_mb": 500.5,
            "hash": "abc123..."
          },
          {
            "path": "F:\\Backup\\movie1.mp4", 
            "size_mb": 500.5,
            "hash": "abc123..."
          }
        ]
      }
    ],
    "summary": {
      "total_duplicates": 156,
      "potential_savings_gb": 45.2,
      "largest_duplicate_mb": 2048.0
    },
    "execution_time": 120.45
  }
}
```

**Example Usage**:
```python
result = find_multimedia_duplicates(
    drives=["E:", "F:", "K:", "L:"],
    comparison_method="hash",
    min_file_size_mb=10,
    output_report="/reports/duplicates.html"
)
```

**Use Cases**:
- Storage optimization
- Duplicate file cleanup
- Media library organization
- Backup deduplication

---

### 6. `detect_usb_drives`

**Purpose**: Detect and list all connected USB drives with detailed information.

**Parameters**: None

**Returns**:
```json
{
  "success": true,
  "data": {
    "drives": [
      {
        "drive_letter": "G:",
        "label": "USB_BACKUP",
        "file_system": "NTFS",
        "total_size_gb": 64.0,
        "free_space_gb": 32.5,
        "drive_type": "removable",
        "device_id": "USB\\VID_1234&PID_5678",
        "connected": true
      }
    ],
    "total_usb_drives": 2,
    "total_capacity_gb": 128.0,
    "total_free_space_gb": 89.3
  }
}
```

**Example Usage**:
```python
result = detect_usb_drives()
print(f"Found {result['data']['total_usb_drives']} USB drives")
for drive in result['data']['drives']:
    print(f"Drive {drive['drive_letter']}: {drive['free_space_gb']:.1f}GB free")
```

**Use Cases**:
- System administration
- Backup drive monitoring
- Storage capacity planning
- Device inventory

---

## 🚀 Getting Started

### Installation

1. **Install the MCPB Package**:
   - Download `beyondcompare-mcp.mcpb` from releases
   - Drag the file to Claude Desktop
   - Follow configuration prompts

2. **Configure Beyond Compare Path**:
   - Windows: Usually auto-detected at `C:\Program Files\Beyond Compare 5\BCompare.exe`
   - macOS: `/Applications/Beyond Compare.app/Contents/MacOS/bcomp`
   - Linux: `/usr/bin/bcompare`

3. **Set Environment Variables** (optional):
   ```bash
   export BEYOND_COMPARE_PATH="/path/to/BCompare.exe"
   export BC_SCRIPTS_DIR="./bc_scripts"
   export LOG_LEVEL="INFO"
   ```

### Basic Usage

```python
# Compare two files
result = compare_files(
    left_path="/path/to/original.txt",
    right_path="/path/to/modified.txt"
)

if result["success"]:
    print(f"Files are {result['data']['comparison_result']}")
else:
    print(f"Error: {result['error']}")
```

### Error Handling

All tools return a consistent response format:

```json
{
  "success": false,
  "error": "Detailed error message",
  "error_type": "BeyondCompareNotInstalledError",
  "troubleshooting": {
    "suggestion": "Install Beyond Compare or set BEYOND_COMPARE_PATH",
    "documentation": "https://github.com/user/repo#installation"
  }
}
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BEYOND_COMPARE_PATH` | Auto-detected | Path to Beyond Compare executable |
| `BC_SCRIPTS_DIR` | `./bc_scripts` | Directory for temporary script files |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `COMMAND_TIMEOUT` | `300` | Timeout for BC operations (seconds) |
| `API_TIMEOUT` | `30` | Timeout for API requests (seconds) |

### Beyond Compare Return Codes

| Code | Meaning | Tool Response |
|------|---------|---------------|
| 0 | Files/folders identical | `"identical"` |
| 1 | Files/folders different | `"different"` |
| 2 | Binary files different | `"binary_different"` |
| 11 | Left file newer | `"left_newer"` |
| 12 | Right file newer | `"right_newer"` |
| 13 | Left file missing | `"left_missing"` |
| 14 | Right file missing | `"right_missing"` |

---

## 🎯 Best Practices

### Performance Optimization

1. **Use appropriate comparison modes**:
   - Quick compare for large files
   - Full compare for critical differences
   - Binary compare for executables

2. **Batch operations**:
   - Compare multiple files in sequence
   - Use folder comparison for bulk analysis

3. **Report generation**:
   - Generate reports only when needed
   - Use HTML format for detailed analysis
   - Use text format for automation

### Security Considerations

1. **File Access**:
   - Validate file paths before comparison
   - Use absolute paths when possible
   - Avoid comparing sensitive system files

2. **Script Security**:
   - Temporary scripts are auto-cleaned
   - Scripts directory has restricted permissions
   - No external network access required

### Troubleshooting

#### Common Issues

1. **Beyond Compare Not Found**:
   ```bash
   export BEYOND_COMPARE_PATH="/path/to/BCompare.exe"
   ```

2. **Permission Denied**:
   - Check file permissions
   - Run with appropriate user privileges
   - Verify script directory access

3. **Timeout Errors**:
   ```bash
   export COMMAND_TIMEOUT=600  # Increase timeout
   ```

4. **Unicode Issues**:
   - Ensure files are properly encoded
   - Use UTF-8 encoding when possible

---

## 📊 Performance Benchmarks

| Operation | Small Files (<1MB) | Large Files (>100MB) | Directories (1000+ files) |
|-----------|-------------------|---------------------|---------------------------|
| File Compare | < 1 second | 2-5 seconds | N/A |
| Folder Compare | N/A | N/A | 10-30 seconds |
| Sync Operations | < 2 seconds | 5-15 seconds | 30-120 seconds |
| Multimedia Scan | N/A | N/A | 60-300 seconds |

*Benchmarks are approximate and depend on system performance and file complexity.*

---

## 🔗 Related Documentation

- [Installation Guide](README.md#installation)
- [MCPB Packaging Guide](docs/mcpb-packaging/README.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- [Security Policy](SECURITY.md)
- [Contributing Guidelines](CONTRIBUTING.md)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/user/repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/user/repo/discussions)
- **Documentation**: [Project Wiki](https://github.com/user/repo/wiki)

---

*Beyond Compare MCP Server API Documentation*  
*Version: 0.1.0*  
*Last Updated: October 11, 2025*
