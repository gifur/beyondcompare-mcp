# 🚀 Beyond Compare MCP - User Guide

## Quick Start Guide

### 1. Installation

**Option A: MCPB Package (Recommended)**
1. Download `beyondcompare-mcp.mcpb` from the [releases page](https://github.com/user/repo/releases)
2. Drag the `.mcpb` file directly to Claude Desktop
3. Follow the configuration prompts
4. Restart Claude Desktop

**Option B: Manual Installation**
```bash
# Clone the repository
git clone https://github.com/user/repo/beyondcompare-mcp.git
cd beyondcompare-mcp

# Install the package
pip install -e .

# Add to Claude Desktop configuration
# Edit ~/.config/claude/claude_desktop_config.json
```

### 2. Beyond Compare Setup

**Windows**: Usually auto-detected at:
- `C:\Program Files\Beyond Compare 5\BCompare.exe`
- `C:\Program Files\Beyond Compare 4\BCompare.exe`

**macOS**: 
- `/Applications/Beyond Compare.app/Contents/MacOS/bcomp`

**Linux**:
- `/usr/bin/bcompare`

**Manual Configuration**:
```bash
export BEYOND_COMPARE_PATH="/path/to/your/BCompare.exe"
```

---

## 🛠️ Tool Examples

### File Comparison

**Basic File Comparison**:
```
Compare these two configuration files:
- /project/config/development.json
- /project/config/production.json
```

**With Report Generation**:
```
Compare /docs/v1.0/manual.md with /docs/v2.0/manual.md and save a detailed HTML report to /reports/manual_changes.html
```

**Expected Response**:
```json
{
  "success": true,
  "data": {
    "comparison_result": "different",
    "left_path": "/docs/v1.0/manual.md",
    "right_path": "/docs/v2.0/manual.md", 
    "report_path": "/reports/manual_changes.html",
    "execution_time": 2.34
  }
}
```

### Directory Comparison

**Project Version Comparison**:
```
Compare the project directories:
- Left: /projects/myapp/v1.0
- Right: /projects/myapp/v1.1

Include subdirectories and generate an HTML report at /reports/version_diff.html
```

**Backup Verification**:
```
Verify my backup by comparing:
- Source: /important/documents
- Backup: /backup/documents
```

### Folder Synchronization

**Preview Sync (Dry Run)**:
```
Preview synchronizing /data/master to /backup/mirror using mirror mode. Show me what would be changed without actually doing it.
```

**Execute Sync**:
```
Now execute the sync from /data/master to /backup/mirror in mirror mode. Delete orphaned files in the target.
```

**Expected Response**:
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
    "dry_run": false,
    "execution_time": 12.45
  }
}
```

### Multimedia Management

**Drive Scanning**:
```
Scan my multimedia drives E:, F:, K:, and L: for all video and audio files. Include metadata like file size and modification date.
```

**Duplicate Detection**:
```
Find duplicate multimedia files across drives E:, F:, K:, and L:. Focus on files larger than 10MB and use content hashing for accuracy.
```

**USB Drive Detection**:
```
Show me all connected USB drives with their capacity and free space information.
```

---

## 💡 Use Case Examples

### 1. Code Review Workflow

**Scenario**: Reviewing changes before deployment

```
1. Compare /app/current/config.py with /app/staging/config.py
2. Compare the entire /app/current directory with /app/staging 
3. Generate HTML reports for both comparisons
4. Preview sync from staging to production (dry run)
```

### 2. Backup Management

**Scenario**: Automated backup verification

```
1. Compare /important/documents with /backup/documents
2. Detect any USB backup drives
3. If backup drive found, sync /important/documents to the USB drive
4. Scan the backup for any duplicate files to save space
```

### 3. Media Library Organization

**Scenario**: Organizing Sandra's multimedia collection

```
1. Scan drives E:, F:, K:, L: for complete media inventory
2. Find duplicate files across all drives
3. Generate a report showing potential space savings
4. Sync unique files to a master archive drive
```

### 4. Project Migration

**Scenario**: Moving project to new structure

```
1. Compare old project structure with new template
2. Preview sync from old to new structure
3. Execute sync with careful file mapping
4. Verify migration by comparing final directories
```

---

## 🔧 Advanced Configuration

### Environment Variables

```bash
# Beyond Compare executable path
export BEYOND_COMPARE_PATH="/path/to/BCompare.exe"

# Temporary scripts directory
export BC_SCRIPTS_DIR="./bc_scripts"

# Logging configuration
export LOG_LEVEL="DEBUG"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Operation timeouts
export COMMAND_TIMEOUT=600    # 10 minutes for large operations
export API_TIMEOUT=60        # 1 minute for API calls

# Python environment
export PYTHONUNBUFFERED=1    # Immediate output
```

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "beyondcompare": {
      "command": "python",
      "args": ["-m", "beyondcompare_mcp"],
      "cwd": "/path/to/beyondcompare-mcp",
      "env": {
        "BEYOND_COMPARE_PATH": "C:\\Program Files\\Beyond Compare 5\\BCompare.exe",
        "LOG_LEVEL": "INFO",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

---

## 🚨 Troubleshooting

### Common Issues

**1. "Beyond Compare not found"**
```bash
# Solution: Set the path explicitly
export BEYOND_COMPARE_PATH="/full/path/to/BCompare.exe"

# Or add to your shell profile
echo 'export BEYOND_COMPARE_PATH="/usr/bin/bcompare"' >> ~/.bashrc
```

**2. "Permission denied"**
```bash
# Solution: Check file permissions
chmod +x /path/to/BCompare.exe

# Or run with appropriate user privileges
sudo chown $USER:$USER /path/to/scripts/directory
```

**3. "Timeout errors"**
```bash
# Solution: Increase timeout for large operations
export COMMAND_TIMEOUT=1200  # 20 minutes
```

**4. "Unicode/encoding issues"**
```bash
# Solution: Set proper encoding
export PYTHONIOENCODING=utf-8
export LC_ALL=en_US.UTF-8
```

### Debug Mode

Enable detailed logging:
```bash
export LOG_LEVEL=DEBUG
python -m beyondcompare_mcp --log-level DEBUG
```

### Test Installation

Verify everything works:
```bash
# Test the CLI directly
python -m beyondcompare_mcp --version

# Test Beyond Compare detection
python -c "from beyondcompare_mcp.server import BeyondCompareMCP; print('BC found:', BeyondCompareMCP()._find_bc_executable())"
```

---

## 📊 Performance Tips

### Large File Operations

1. **Use appropriate comparison modes**:
   - Quick compare for size/date differences
   - Full compare only when needed
   - Binary compare for executables

2. **Batch operations efficiently**:
   - Compare entire directories vs individual files
   - Use folder sync for bulk operations
   - Generate reports sparingly for large datasets

3. **Optimize for your use case**:
   - Set appropriate timeouts
   - Use dry-run mode for planning
   - Monitor system resources during large operations

### Memory Management

- Large directory comparisons: 50-200MB RAM
- Multimedia scanning: 100-500MB RAM  
- Duplicate detection: 200MB-1GB RAM (depends on file count)

---

## 🔗 Integration Examples

### Shell Scripts

```bash
#!/bin/bash
# Daily backup verification script

echo "Starting backup verification..."

# Compare critical directories
python -c "
from beyondcompare_mcp.server import BeyondCompareMCP
server = BeyondCompareMCP()

# Compare documents
result = server._compare_folders('/home/user/documents', '/backup/documents')
print(f'Documents backup: {result[\"data\"][\"comparison_result\"]}')

# Compare projects  
result = server._compare_folders('/home/user/projects', '/backup/projects')
print(f'Projects backup: {result[\"data\"][\"comparison_result\"]}')
"

echo "Backup verification complete!"
```

### Python Integration

```python
#!/usr/bin/env python3
"""Example integration script."""

from beyondcompare_mcp.server import BeyondCompareMCP
import json

def main():
    # Initialize server
    server = BeyondCompareMCP()
    
    # Define comparison tasks
    tasks = [
        {
            "name": "Config Comparison",
            "left": "/app/config/dev.json",
            "right": "/app/config/prod.json"
        },
        {
            "name": "Documentation Check", 
            "left": "/docs/current",
            "right": "/docs/updated"
        }
    ]
    
    # Execute comparisons
    results = []
    for task in tasks:
        print(f"Processing: {task['name']}")
        result = server._compare_files(task['left'], task['right'])
        results.append({
            "task": task['name'],
            "result": result['data']['comparison_result'],
            "success": result['success']
        })
    
    # Generate summary report
    with open('comparison_report.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("Report saved to comparison_report.json")

if __name__ == '__main__':
    main()
```

---

## 🎯 Best Practices

### Security

1. **File Path Validation**:
   - Always use absolute paths when possible
   - Validate paths before operations
   - Avoid comparing sensitive system files

2. **Access Control**:
   - Run with minimal required privileges
   - Use dedicated directories for temporary files
   - Clean up temporary files automatically

3. **Data Protection**:
   - Be cautious with sync operations (use dry-run first)
   - Backup important data before major operations
   - Verify results after critical operations

### Performance

1. **Operation Planning**:
   - Use dry-run mode for planning sync operations
   - Generate reports only when needed
   - Batch similar operations together

2. **Resource Management**:
   - Monitor system resources during large operations
   - Set appropriate timeouts for your environment
   - Use incremental approaches for huge datasets

3. **Efficiency**:
   - Compare directories vs individual files when possible
   - Use appropriate comparison modes for your needs
   - Cache results when doing repetitive operations

---

## 📚 Additional Resources

- **API Documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Installation Guide**: [README.md](README.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Security Policy**: [SECURITY.md](SECURITY.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🆘 Getting Help

- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and share tips
- **Documentation**: Check the docs directory for detailed guides

---

*Beyond Compare MCP Server User Guide*  
*Version: 0.1.0*  
*Last Updated: October 11, 2025*
