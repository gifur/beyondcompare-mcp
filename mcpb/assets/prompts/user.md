# Beyond Compare MCP User Guide

Beyond Compare MCP provides powerful file and directory comparison using Beyond Compare, along with multimedia drive scanning, duplicate detection, USB monitoring, and development workspace analysis.

## Installation

### Prerequisites

- Beyond Compare 3, 4, or 5 installed
- Python 3.10+
- Windows (primary target; macOS/Linux support for comparison operations)

### Quick Install

```bash
git clone https://github.com/sandraschi/beyondcompare-mcp.git
cd beyondcompare-mcp
pip install -e .
```

### MCP Client Configuration

**Claude Desktop:**
```json
{
  "mcpServers": {
    "beyondcompare-mcp": {
      "command": "python",
      "args": ["-m", "beyondcompare_mcp"],
      "env": {
        "BEYOND_COMPARE_PATH": "C:\\Program Files\\Beyond Compare 5\\BCompare.exe",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Cursor:**
```json
{
  "mcpServers": {
    "beyondcompare-mcp": {
      "command": "python",
      "args": ["-m", "beyondcompare_mcp"],
      "env": {
        "BEYOND_COMPARE_PATH": "C:\\Program Files\\Beyond Compare 5\\BCompare.exe"
      }
    }
  }
}
```

## Tutorials

### Tutorial 1: Compare Two Files

Compare two text files to find differences:

```python
result = await compare_files(
    left_path="C:/documents/report_v1.txt",
    right_path="C:/documents/report_v2.txt"
)
if result["success"]:
    if result["identical"]:
        print("Files are identical")
    else:
        print(f"Differences found: {result['differences_found']}")
```

### Tutorial 2: Generate Comparison Report

Compare files and generate a report:

```python
result = await compare_files(
    left_path="C:/code/main.py",
    right_path="C:/code/main_refactored.py",
    output_report="C:/reports/diff_report.txt"
)
if result["success"]:
    print(f"Report saved to: {result['output_report']}")
```

### Tutorial 3: Compare Folders

Compare two directories:

```python
result = await compare_folders(
    left_path="C:/project_v1",
    right_path="C:/project_v2",
    include_subfolders=True
)
if result["success"]:
    if result["differences_found"]:
        print("Folders differ")
    else:
        print("Folders are identical")
```

### Tutorial 4: Generate Folder Report

Compare folders and generate a summary report:

```python
result = await compare_folders(
    left_path="C:/backup/week1",
    right_path="C:/backup/week2",
    output_report="C:/reports/folder_diff.txt"
)
print(f"Report: {result['message']}")
```

### Tutorial 5: Sync Folders (Dry Run)

Preview what would happen during folder synchronization:

```python
result = await sync_folders(
    source_path="C:/project/src",
    target_path="D:/backup/src",
    sync_mode="mirror",
    dry_run=True
)
if result["success"]:
    print(f"Changes detected: {result['changes_detected']}")
    print(f"Mode: {result['sync_mode']} (dry run)")

# Perform actual sync by setting dry_run=False
actual = await sync_folders(
    source_path="C:/project/src",
    target_path="D:/backup/src",
    sync_mode="mirror",
    dry_run=False
)
```

### Tutorial 6: Update Sync Mode

Use update mode to copy only newer files:

```python
result = await sync_folders(
    source_path="C:/project",
    target_path="D:/backup",
    sync_mode="update",
    dry_run=False
)
print(f"Updated: {result['message']}")
```

### Tutorial 7: Backup Sync Mode

Use backup mode to create timestamped backups:

```python
result = await sync_folders(
    source_path="C:/project",
    target_path="D:/backups/project",
    sync_mode="backup",
    dry_run=False
)
print(f"Backup: {result['message']}")
```

### Tutorial 8: Scan Multimedia Drives

Inventory all multimedia drives:

```python
result = await multimedia_drive_scanner()
if result["success"]:
    print(f"Scan completed in {result['scan_time_seconds']}s")
    print(f"Total files: {result['total_files']}")
    print(f"Total size: {result['total_size_gb']} GB")
    print(f"Summary: {result['summary']}")
```

### Tutorial 9: Filter by Media Type

Scan only video files on selected drives:

```python
result = await multimedia_drive_scanner(
    drives=["E:", "F:"],
    file_types=["video"]
)
if result["success"]:
    for drive, data in result["results"].items():
        if data["success"]:
            print(f"{drive}: {data['file_count']} video files")
```

### Tutorial 10: Find Duplicate Files

Find duplicate multimedia files across drives:

```python
result = await find_multimedia_duplicates(
    min_size_mb=10,
    use_content_hash=True
)
if result["success"]:
    print(f"Checked {result['total_files_checked']} files")
    print(f"Found {result['total_duplicate_groups']} duplicate groups")
    print(f"Potential savings: {result['total_savings_gb']} GB")
    
    for group in result["duplicate_groups"][:5]:
        print(f"\n  {group['size_mb']} MB - {group['duplicate_count']} copies")
        print(f"  Recommendation: {group.get('recommendation', 'N/A')}")
```

### Tutorial 11: Detect USB Drives

List connected USB drives:

```python
result = await detect_usb_drives()
if result["success"]:
    print(f"Found {result['count']} USB drive(s)")
    for drive in result["usb_drives"]:
        print(f"  {drive['drive_letter']} - {drive['label']}")
        print(f"    Free: {drive['space_info']['free_gb']} GB / {drive['space_info']['total_gb']} GB")
```

### Tutorial 12: Workspace Analysis

Analyze your development workspace:

```python
result = await analyze_dev_workspace(
    workspace_path="D:/Dev/repos",
    depth=2
)
if result["success"]:
    print(f"Total repos: {result['total_repos']}")
    print(f"Total LOC: {result['total_loc']}")
    for lang, stats in result["languages"].items():
        print(f"  {lang}: {stats['repos']} repos, {stats['loc']} LOC")
```

### Tutorial 13: Scan Repository Health

Check the health of a specific repository:

```python
result = await scan_repo_health(
    repo_path="D:/Dev/repos/my-project"
)
if result["success"]:
    print(f"Status: {result['status']}")
    for issue_type, issue_data in result["issues"].items():
        print(f"  {issue_type}: {issue_data}")
    for suggestion in result["suggestions"]:
        print(f"  Suggestion: {suggestion}")
```

### Tutorial 14: Clean Up Build Artifacts

Preview and clean up build artifacts:

```python
# Preview what would be cleaned
preview = await cleanup_dev_artifacts(
    workspace_path="D:/Dev/repos",
    dry_run=True
)
if preview["success"]:
    print(f"Found {preview['artifacts_found']} artifacts")
    print(f"Potential savings: {preview['potential_savings_gb']} GB")

# Perform actual cleanup by setting dry_run=False
if preview["artifacts_found"] > 0:
    cleanup = await cleanup_dev_artifacts(
        workspace_path="D:/Dev/repos",
        dry_run=False
    )
```

### Tutorial 15: Find Duplicate Code

Find duplicate code blocks across repositories:

```python
result = await find_duplicate_code(
    workspace_path="D:/Dev/repos",
    min_lines=15,
    extensions=[".py", ".js", ".ts"]
)
if result["success"]:
    print(f"Scanned {result['total_files_scanned']} files")
    print(f"Found {result['refactoring_opportunities']} opportunities")
    for block in result["duplicate_blocks"][:3]:
        print(f"\n  {block['similarity']*100:.0f}% similar, {block['lines']} lines")
        for file in block["files"]:
            print(f"    {file['path']}:{file['start_line']}")
```

### Tutorial 16: Selective Restore from Backup

Restore specific files from a backup archive:

```python
result = await selective_restore(
    backup_path="D:/backups/my-project.zip",
    restore_path="D:/restored/project",
    patterns=["src/**/*.py", "tests/**/*.py"],
    overwrite=False
)
if result["success"]:
    print(f"Restored {result['files_restored']} files")
    print(f"Total: {result['total_size_mb']} MB")
```

### Tutorial 17: Compare Workspace Snapshots

Compare two workspace state snapshots:

```python
result = await compare_workspace_snapshots(
    snapshot_a="D:/snapshots/before_cleanup.json",
    snapshot_b="D:/snapshots/after_cleanup.json"
)
if result["success"]:
    print(f"Added: {result['added']}")
    print(f"Removed: {result['removed']}")
    print(f"Modified: {result['modified']}")
```

### Tutorial 18: Agentic Workflow

Use the agentic workflow for complex multi-step tasks:

```python
result = await beyondcompare_agentic_workflow(
    workflow_prompt="Compare the src folders of project-a and project-b, then generate a report"
)
print(result)
```

## REST API Reference

### GET /health
**Response:** `{"status": "ok", "server": "Beyond Compare MCP"}`

### POST /api/v1/compare/files
**Request:**
```json
{"left_path": "C:/a.txt", "right_path": "C:/b.txt", "output_report": null}
```

### POST /api/v1/compare/folders
**Request:**
```json
{"left_path": "C:/folder_a", "right_path": "C:/folder_b", "include_subfolders": true}
```

### POST /api/v1/sync/folders
**Request:**
```json
{"source_path": "C:/src", "target_path": "D:/dst", "sync_mode": "mirror", "dry_run": true}
```

### POST /api/v1/multimedia/scan
**Request:**
```json
{"drives": ["E:", "F:"], "recent_days": 30, "file_types": ["video", "audio"]}
```

### POST /api/v1/multimedia/duplicates
**Request:**
```json
{"min_size_mb": 1.0, "use_content_hash": true}
```

### GET /api/v1/usb/detect
**Response:** `{"success": true, "usb_drives": [...], "count": 1}`

### POST /api/v1/workspace/analyze
**Request:** `{"workspace_path": "D:/Dev", "depth": 2}`

### POST /api/v1/repo/health
**Request:** `{"repo_path": "D:/Dev/repos/my-project", "auto_fix": false}`

### POST /api/v1/workspace/cleanup
**Request:** `{"workspace_path": "D:/Dev", "dry_run": true}`

### POST /api/v1/code/duplicates
**Request:** `{"workspace_path": "D:/Dev", "min_lines": 10}`

### POST /api/v1/snapshots/compare
**Request:** `{"snapshot_a": "path1.json", "snapshot_b": "path2.json"}`

### POST /api/v1/restore/selective
**Request:** `{"backup_path": "backup.zip", "restore_path": "D:/restore", "patterns": ["src/**"]}`

## Troubleshooting

### Issue 1: Beyond Compare executable not found
Install Beyond Compare (3, 4, or 5) or set BEYOND_COMPARE_PATH explicitly. The server checks common install paths and PATH.

### Issue 2: File comparison fails with "not found"
Verify paths exist. Use absolute paths. The server validates paths before comparison. Ensure Beyond Compare can access the files.

### Issue 3: Folder sync fails silently
Check that the source folder exists. The server creates the target folder if missing. Verify Beyond Compare scripting works with `@script.bcscript` arguments.

### Issue 4: Multimedia scan finds no drives
The server looks for drives E:, F:, K:, L: with a "multimedia files" folder. Specify drives explicitly if your setup differs.

### Issue 5: Duplicate detection is slow
Content hashing (SHA-256) is accurate but slow for large files. Use `use_content_hash=False` for name-based detection (faster but less accurate).

### Issue 6: USB detection returns no drives
The server requires pywin32 for Windows USB detection. Install with `pip install pywin32`. Without it, fallback detection scans drive letters G-Z.

### Issue 7: Command injection warning
The server blocks dangerous characters (`;`, `|`, `&`, etc.) in paths. Use clean file paths without special characters.

### Issue 8: BC script creation fails
Check BC_SCRIPTS_DIR is writable. The server uses NamedTemporaryFile for secure script creation. Disk space may be low.

### Issue 9: Large folder comparisons timeout
Default timeout is 300 seconds. Increase COMMAND_TIMEOUT for very large comparisons. BC itself may be slow for deeply nested folders.

### Issue 10: Report generation creates empty files
Verify BC supports the report format. The "layout:summary options:display-mismatches" format requires BC's scripting engine.

### Issue 11: Permission denied on paths
Run the MCP client (Claude Desktop) with appropriate permissions. Some system paths may require administrator access.

### Issue 12: Workspace analysis misses repos
The default depth of 3 may not find deeply nested repos. Increase the depth parameter. The server searches for .git directories.

## FAQ

### What is Beyond Compare MCP?
An MCP server that integrates Beyond Compare's file/folder comparison engine with AI-powered multimedia scanning and dev workspace analysis.

### Do I need Beyond Compare installed?
Yes for comparison and sync tools. Multimedia scanning, USB detection, and workspace analysis tools work without it.

### What versions of Beyond Compare are supported?
Versions 3, 4, and 5. The server auto-detects the installed version. Version 5 is recommended for best scripting support.

### Can I compare files across drives?
Yes. BC supports comparing files on any accessible drive. Network paths may require additional configuration.

### How does duplicate detection work?
By default, SHA-256 content hashing compares file contents byte-for-byte. Name-based mode groups files by name and size.

### What multimedia drives are scanned?
Default targets are E:, F:, K:, L: with a "multimedia files" subfolder. Customize by specifying drives explicitly.

### Can I use this for code comparison?
Yes. compare_files and compare_folders work with any file type. The workspace analysis tools specifically target code repos.

### How do I update Beyond Compare configuration?
Set BEYOND_COMPARE_PATH to your BC executable path. Restart the MCP server after changes.

### Is this safe for production use?
All sync operations default to dry_run=True to prevent accidental data loss. Set dry_run=False only after verifying the preview.

### What platforms are supported?
Windows (primary). Linux/macOS support for file comparison if BC is installed via WINE or native macOS version.

### Can I schedule regular scans?
The server exposes tools for on-demand use. Schedule via cron/Task Scheduler calling the REST API endpoints.

### How are temporary files handled?
BC script files are created with NamedTemporaryFile and deleted after execution. No persistent temp files remain.

### What about large file support?
Files up to available memory are supported. BC's command-line engine handles large files efficiently. Timeout may need adjustment.

### Does this work with cloud drives?
Local filesystem paths only. Cloud storage mapped as a local drive letter should work. Direct cloud URLs are not supported.

### How do I update the Beyond Compare path?
Set the BEYOND_COMPARE_PATH environment variable to your installation path. The server auto-detects BC 3, 4, and 5 in standard locations.

### Can I compare binary files?
Yes. Beyond Compare's file comparison works with any file type. Binary comparison shows hex-level differences. Use output_report for detailed results.

### What happens if a scan takes too long?
Long operations will timeout based on COMMAND_TIMEOUT (default 300s). For very large scans, increase the timeout or narrow the scope with filters.

### How does the folder sync handle conflicts?
The sync mode determines conflict behavior: mirror overwrites target, update copies newer files, backup creates copies of changed files. Dry-run preview shows all planned changes.

### Can I scan network drives?
Network drives mapped to a drive letter are supported. UNC paths may not work. Use Windows mapped network drives for best results.

### How accurate is code duplicate detection?
Name-based detection is fast but may produce false positives. Content-based (SHA-256) is accurate but slower. The min_lines parameter filters out trivial matches.

### Does the scanner detect renamed duplicates?
Content-based detection (SHA-256) finds renamed duplicates since it compares file contents. Name-based detection only finds files with the same name.

### Can I undo a sync operation?
Sync operations are irreversible when dry_run=false. Always use dry_run=true first to preview changes. Consider taking a backup before destructive operations.

### What happens if Beyond Compare exits with error?
The server maps BC return codes: 0=no differences, 1=differences found, 2+=error. Errors >=2 raise BeyondCompareCommandError with the BC error output.

### How are temporary script files managed?
BC script files are created using NamedTemporaryFile in the scripts directory. They are deleted after each operation. Orphaned files from crashes are cleaned on server restart.

### Can I customize comparison rules?
Beyond Compare's built-in rules are used. Custom rules configured in BC itself (file formats, conversion, importance) are respected when BC runs in command-line mode.

## Additional REST Endpoints

### GET /api/v1/multimedia/drives
Returns detected multimedia drives and their availability.
**Response:**
```json
{
  "drives": ["E:", "F:", "K:", "L:"],
  "available": ["E:", "F:"],
  "multimedia_folder": "multimedia files"
}
```

### GET /api/v1/multimedia/stats
Returns cached multimedia scan statistics (after a scan has been run).
**Response:**
```json
{
  "has_scan_results": true,
  "last_scan_time_seconds": 12.5,
  "total_files": 15234,
  "total_size_gb": 245.8,
  "drives_scanned": ["E:", "F:"]
}
```

### POST /api/v1/sync/preview
Preview a sync operation without executing.
**Request:** `{"source_path": "C:/src", "target_path": "D:/dst", "sync_mode": "mirror"}`
**Response:** `{"success": true, "changes_detected": true, "message": "Preview completed"}`

### GET /api/v1/workspace/languages
Returns detected programming languages and their statistics.
**Query:** `?workspace_path=D:/Dev/repos`
**Response:**
```json
{
  "languages": {"Python": {"repos": 10, "files": 500}, "TypeScript": {"repos": 5, "files": 200}}
}
```

### POST /api/v1/repo/cleanup
Non-destructive cleanup preview.
**Request:** `{"workspace_path": "D:/Dev", "dry_run": true}`
**Response:** `{"success": true, "artifacts_found": 15, "potential_savings_gb": 5.0}`

## Advanced Usage

### Batch File Comparison
```python
pairs = [
    ("C:/v1/main.py", "C:/v2/main.py"),
    ("C:/v1/utils.py", "C:/v2/utils.py"),
    ("C:/v1/config.py", "C:/v2/config.py"),
]
for left, right in pairs:
    result = await compare_files(left_path=left, right_path=right)
    status = "identical" if result["identical"] else "differs"
    print(f"{left.split('/')[-1]}: {status}")
```

### Scheduled Multimedia Backup
```python
import schedule
import asyncio

def run_backup():
    asyncio.run(sync_folders(
        source_path="E:/multimedia files",
        target_path="G:/backup/multimedia",
        sync_mode="update",
        dry_run=False
    ))

# Weekly backup
schedule.every().monday.at("02:00").do(run_backup)
```

### Automated Workspace Health Report
```python
async def health_report():
    scan = await scan_repo_health(repo_path="D:/Dev/repos")
    if scan["status"] == "needs_attention":
        print("Issues found:")
        for issue_type, data in scan["issues"].items():
            print(f"  {issue_type}: {data}")
    
    cleanup = await cleanup_dev_artifacts(dry_run=True)
    if cleanup["artifacts_found"] > 0:
        print(f"Cleanup opportunity: {cleanup['potential_savings_gb']} GB")
    
    return scan, cleanup
```

## Version Compatibility
The server requires FastMCP 2.11+ and Beyond Compare 3, 4, or 5 for comparison operations. Multimedia and dev workspace tools work without BC. Python 3.10+ is required. Windows is the primary platform but macOS and Linux support basic file operations.

## Error Handling Pattern
All tools return success=false with an error message on failure. The error message is human-readable and includes the specific failure reason. For comparison tools, path validation errors include the invalid path. For sync tools, invalid mode errors list valid options. For multimedia tools, drive detection errors list checked paths.

## Tool Output Summary
compare_files returns identical and differences_found booleans. compare_folders returns differences_found and include_subfolders. sync_folders returns changes_detected, sync_mode, and dry_run. multimedia_drive_scanner returns total_files, total_size_gb, and per-drive results. find_multimedia_duplicates returns duplicate_groups and total_savings_gb.

## File Scanning Behavior
The multimedia scanner walks directories using os.walk(). Files smaller than 1 KB are skipped. Only files with recognized media extensions are included. The scanner reports file count, total size, and per-type distribution statistics.

## Dev Tool Dependencies
The workspace analysis tools (analyze_dev_workspace, scan_repo_health, cleanup_dev_artifacts, find_duplicate_code, compare_workspace_snapshots, selective_restore) require only Python standard library and operate on file system metadata without external dependencies.

## Non-BC Tools Reference
multimedia_drive_scanner, find_multimedia_duplicates, detect_usb_drives, backup_dev_repositories, analyze_dev_workspace, scan_repo_health, cleanup_dev_artifacts, find_duplicate_code, compare_workspace_snapshots, and selective_restore all work without Beyond Compare installed. These tools provide comprehensive workspace management independently.

## Tool Categories
File operations (compare, sync) require Beyond Compare. Multimedia operations (scan, duplicates, USB) work standalone. Dev tools (analyze, health, cleanup, dedup, snapshots, restore) also work standalone. Agentic tools require sampling support.

## REST API Endpoints
GET /health for server status. POST /api/v1/compare/files for file comparison. POST /api/v1/compare/folders for folder comparison. POST /api/v1/sync/folders for synchronization. POST /api/v1/multimedia/scan for multimedia inventory. GET /api/v1/usb/detect for USB detection.

## Tool Usage Pattern
Comparison and sync tools require Beyond Compare installed. Multimedia and dev tools work standalone. Always use dry_run=true for sync operations first. Use content hash for accurate duplicate detection. Use name-based detection for fast previews.

## Quick Start Steps
1. Health check: GET /health
2. Compare files: compare_files(left_path="C:/a.txt", right_path="C:/b.txt")
3. Compare folders: compare_folders(left_path="C:/folder_a", right_path="C:/folder_b")
4. Sync folders (preview): sync_folders(source_path="C:/src", target_path="D:/dst", dry_run=true)
5. Scan multimedia: multimedia_drive_scanner()
6. Find duplicates: find_multimedia_duplicates()
7. Detect USB: detect_usb_drives()

## Default Scanner Drives
The multimedia scanner checks drives E:, F:, K:, L: by default. Each drive must contain a "multimedia files" subfolder. Drives without this folder are skipped. You can override with the drives parameter.

## Dev Tools Glossary
* **Workspace**: Root directory containing development repositories
* **LOC**: Lines of code metric for codebase size estimation
* **Repo health**: Assessment of git state, dependencies, and code quality
* **Build artifacts**: Temporary files from compilation and dependency installation
* **Duplicate code**: Similar code blocks that could be refactored into shared libraries
* **Snapshot**: Point-in-time record of workspace state for change tracking
* **Selective restore**: Partial recovery of specific files from a backup archive

## File Comparison Workflow
Always start with compare_files or compare_folders to detect differences, then use sync_folders with dry_run=true to preview changes, then sync_folders with dry_run=false to execute. Use find_multimedia_duplicates to identify space-saving opportunities. Use compare_workspace_snapshots to track directory changes over time.

## BC Script Commands Reference
The server generates these Beyond Compare script commands:
- `load "{path1}" "{path2}"`: Load two paths for comparison
- `expand all`: Recursively expand folders
- `select all.files all.folders`: Select everything
- `sync mirror:left->right`: Mirror mode (target = source)
- `sync update:left->right`: Update mode (newer files only)
- `sync create:left->right`: Backup mode (create copies)
- `sync ... preview`: Preview without executing
- `report layout:summary options:display-mismatches output-to:"{path}"`: Generate text report
- `script-exit`: Close BC after script finishes

## Tool Purpose Summary
| Tool | Best For | When NOT to Use |
|------|----------|-----------------|
| compare_files | Checking two specific files | When you need folder-level comparison |
| compare_folders | Checking directory differences | When you need to sync, not just compare |
| sync_folders | Actually synchronizing data | When you only need to see differences |
| multimedia_drive_scanner | Inventorying media drives | On systems without E/F/K/L drives |
| find_multimedia_duplicates | Freeing disk space | On first scan (scan first) |
| detect_usb_drives | Finding external targets | On systems without USB drives |
| backup_dev_repositories | Protecting work | Just before major refactoring |
| analyze_dev_workspace | Understanding codebase size | During workspace setup or review |
| scan_repo_health | Pre-commit checks | When CI is catching issues |
| cleanup_dev_artifacts | Reclaiming disk space | Before using dry_run=false |
| find_duplicate_code | Refactoring planning | When code quality needs improvement |
| selective_restore | Recovering specific files | When you need individual files, not full restore |

## Multimedia Scanner Extension Reference
The scanner recognizes these extensions per media type:
- video: .mp4, .avi, .mkv, .mov, .wmv, .flv, .m4v, .webm, .mpg, .mpeg
- audio: .mp3, .flac, .wav, .aac, .ogg, .m4a, .wma, .opus
- images: .jpg, .jpeg, .png, .gif, .bmp, .tiff, .raw, .webp, .svg
- documents: .pdf, .doc, .docx, .txt, .rtf, .epub, .mobi
Files with other extensions are ignored. Add new extensions by updating the MEDIA_TYPES dictionary in multimedia_scanner.py.

## Duplicate Detection Methods
The find_multimedia_duplicates tool supports two detection methods:
1. Content hash (SHA-256): Groups files by their cryptographic hash. Most accurate, detects renamed duplicates. Slower for large files (reads entire file into memory in 8KB chunks).
2. Name and size: Groups files by filename and exact byte size. Fastest method, scans metadata only. May miss renamed duplicates or produce false positives for common filenames.
Use content hash for accurate results before cleanup. Use name and size for quick previews.

## Beyond Compare Detection Order
The server searches for Beyond Compare in this order:
1. Explicit path from BEYOND_COMPARE_PATH environment variable
2. C:\Program Files\Beyond Compare 5\BCompare.exe
3. C:\Program Files\Beyond Compare 4\BCompare.exe
4. C:\Program Files\Beyond Compare 3\BCompare.exe
5. C:\Program Files (x86)\Beyond Compare 5\BCompare.exe
6. C:\Program Files (x86)\Beyond Compare 4\BCompare.exe
7. C:\Program Files (x86)\Beyond Compare 3\BCompare.exe
8. System PATH for BCompare.exe or bcompare
9. Falls back to bcompare default name in PATH

If none found, comparison and sync tools will fail. Multimedia and dev tools work without BC.

## Tool Error Recovery Guide
1. **compare_files fails with "file not found"**: Verify both paths exist. Use absolute paths. Check file permissions. Beyond Compare requires read access to both files.
2. **compare_folders fails**: One or both folders may not exist. The source folder must exist; the sync target is created if missing. Check include_subfolders parameter.
3. **sync_folders fails with "invalid sync mode"**: Use one of: mirror, update, backup. The mode is case-sensitive. Always use dry_run=true first to preview changes.
4. **multimedia_drive_scanner fails**: No multimedia drives found. Check drives E:, F:, K:, L: exist with a "multimedia files" folder. Specify custom drives with the drives parameter.
5. **find_multimedia_duplicates fails**: Run multimedia_drive_scanner first to populate scan data. The duplicate finder uses cached scan results unless drives are explicitly specified.
6. **detect_usb_drives fails**: Requires pywin32 on Windows. Install with pip install pywin32. Fallback mode scans letters G-Z but may miss some drives.
7. **Beyond Compare not installed**: Install BC 3, 4, or 5, or set BEYOND_COMPARE_PATH environment variable. Comparison and sync tools require BC.
8. **Command timeout**: Large comparisons may exceed the default 300s timeout. Increase COMMAND_TIMEOUT environment variable. Very large folders (100k+ files) should be narrowed with filters.

## REST API Quick Reference
```bash
# Health check
curl http://localhost:8000/health

# Compare files
curl -X POST http://localhost:8000/api/v1/compare/files \
  -H "Content-Type: application/json" \
  -d '{"left_path":"C:/a.txt","right_path":"C:/b.txt","output_report":null}'

# Compare folders
curl -X POST http://localhost:8000/api/v1/compare/folders \
  -H "Content-Type: application/json" \
  -d '{"left_path":"C:/folder_a","right_path":"C:/folder_b","include_subfolders":true}'

# Sync folders (dry run)
curl -X POST http://localhost:8000/api/v1/sync/folders \
  -H "Content-Type: application/json" \
  -d '{"source_path":"C:/src","target_path":"D:/dst","sync_mode":"mirror","dry_run":true}'

# Scan multimedia
curl -X POST http://localhost:8000/api/v1/multimedia/scan \
  -H "Content-Type: application/json" \
  -d '{"drives":["E:","F:"],"file_types":["video"]}'

# Find duplicates
curl -X POST http://localhost:8000/api/v1/multimedia/duplicates \
  -H "Content-Type: application/json" \
  -d '{"use_content_hash":true,"min_size_mb":1.0}'
```

## Common Use Case Summary

### Quick File Diff
```python
r = await compare_files(left_path="old.py", right_path="new.py")
print("Identical" if r["identical"] else "Different")
```

### Folder Sync Preview
```python
r = await sync_folders(source_path="C:/src", target_path="D:/dst", dry_run=True)
print(f"Changes: {r['changes_detected']}")
```

### Multimedia Inventory
```python
r = await multimedia_drive_scanner(file_types=["video"])
print(f"Videos: {r['total_files']}, Size: {r['total_size_gb']} GB")
```

### Workspace Size
```python
r = await analyze_dev_workspace(workspace_path="D:/Dev")
print(f"Repos: {r['total_repos']}, LOC: {r['total_loc']}")
```

### Repository Cleanup Preview
```python
r = await cleanup_dev_artifacts(dry_run=True)
print(f"Can free: {r['potential_savings_gb']} GB")
```

### USB Drive Check
```python
r = await detect_usb_drives()
for d in r["usb_drives"]:
    print(f"{d['drive_letter']}: {d['space_info']['free_gb']} GB free")
```

## Command Line Reference

### Starting the Server
```bash
# Default mode (STDIO transport)
python -m beyondcompare_mcp

# With custom BC path
BEYOND_COMPARE_PATH="C:\Program Files\Beyond Compare 5\BCompare.exe" python -m beyondcompare_mcp

# With increased timeout
COMMAND_TIMEOUT=600 python -m beyondcompare_mcp
```

### Quick Curl Commands
```bash
# Health check
curl http://localhost:8000/health

# Compare files
curl -X POST http://localhost:8000/api/v1/compare/files \
  -H "Content-Type: application/json" \
  -d '{"left_path":"C:/a.txt","right_path":"C:/b.txt"}'

# Scan multimedia
curl -X POST http://localhost:8000/api/v1/multimedia/scan \
  -H "Content-Type: application/json" \
  -d '{"file_types":["video"]}'

# Check USB drives
curl http://localhost:8000/api/v1/usb/detect

# Sync folders (dry run)
curl -X POST http://localhost:8000/api/v1/sync/folders \
  -H "Content-Type: application/json" \
  -d '{"source_path":"C:/src","target_path":"D:/dst","sync_mode":"mirror","dry_run":true}'
```

## Quick Reference Card

### Tool Summary
| Tool | Input Parameters | Output Fields | Requires BC |
|------|-----------------|---------------|-------------|
| compare_files | left_path, right_path, output_report | identical, differences_found | Yes |
| compare_folders | left_path, right_path, output_report, include_subfolders | differences_found | Yes |
| sync_folders | source_path, target_path, sync_mode, dry_run | changes_detected | Yes |
| multimedia_drive_scanner | drives, recent_days, file_types | total_files, total_size_gb | No |
| find_multimedia_duplicates | drives, min_size_mb, file_types, use_content_hash | duplicate_groups, total_savings_gb | No |
| detect_usb_drives | none | usb_drives, count | No |
| backup_dev_repositories | repo_paths, output_dir, exclude_patterns | backup_count, total_size_mb | No |
| analyze_dev_workspace | workspace_path, depth | languages, total_loc | No |
| scan_repo_health | repo_path, auto_fix | status, issues, suggestions | No |
| cleanup_dev_artifacts | workspace_path, patterns, dry_run, min_size_mb | artifacts_found, potential_savings_gb | No |
| find_duplicate_code | workspace_path, min_lines, extensions | duplicate_blocks, refactoring_opportunities | No |
| compare_workspace_snapshots | snapshot_a, snapshot_b, report_format | added, removed, modified | No |
| selective_restore | backup_path, restore_path, patterns, overwrite | files_restored, total_size_mb | No |

### Environment Variables
| Variable | Default | Purpose |
|----------|---------|---------|
| BEYOND_COMPARE_PATH | auto-detect | BC executable path |
| BC_SCRIPTS_DIR | ./bc_scripts | Temp script directory |
| HOST | 127.0.0.1 | Server bind address |
| PORT | 8000 | Server port |
| LOG_LEVEL | INFO | Logging level |
| COMMAND_TIMEOUT | 300 | BC command timeout (seconds) |

### Sync Mode Reference
| Mode | BC Script Command | Behavior |
|------|------------------|----------|
| mirror | sync mirror:left->right | Makes target identical to source |
| update | sync update:left->right | Copies newer/added files only |
| backup | sync create:left->right | Creates copies of changed files |

### Media Type Extensions
| Type | Extensions |
|------|-----------|
| video | .mp4, .avi, .mkv, .mov, .wmv, .flv, .m4v, .webm, .mpg, .mpeg |
| audio | .mp3, .flac, .wav, .aac, .ogg, .m4a, .wma, .opus |
| images | .jpg, .jpeg, .png, .gif, .bmp, .tiff, .raw, .webp, .svg |
| documents | .pdf, .doc, .docx, .txt, .rtf, .epub, .mobi |

### Default Multimedia Drives
| Drive | Purpose |
|-------|---------|
| E: | Primary multimedia drive |
| F: | Secondary multimedia drive |
| K: | Tertiary multimedia drive |
| L: | Quaternary multimedia drive |

## Error Code Reference
| Error | Cause | Recovery |
|-------|-------|----------|
| Left file not found | Left path does not exist | Verify path and file permissions |
| Right file not found | Right path does not exist | Verify path and file permissions |
| Left folder not found | Source directory missing | Check path or create directory |
| Invalid sync mode | Unknown mode string | Use mirror, update, or backup |
| Beyond Compare not installed | BC not found | Install BC or set BEYOND_COMPARE_PATH |
| No multimedia drives found | Targets unavailable | Check drive letters or specify explicitly |
| Backup not found | Archive missing | Verify backup path |
| Command timeout | BC not responding | Increase COMMAND_TIMEOUT |

## Additional Tutorials

### Tutorial 19: Large-Scale Deduplication
Find and resolve duplicates across all drives with recommended actions:
```python
async def full_deduplication_audit():
    results = await find_multimedia_duplicates(use_content_hash=True, min_size_mb=10)
    if not results["success"]:
        return {"error": results.get("error")}
    total_savings = results["total_savings_gb"]
    groups = results["duplicate_groups"]
    print(f"Found {len(groups)} groups, potential savings: {total_savings} GB")
    for g in groups[:5]:
        print(f"  {g['size_mb']} MB x {g['duplicate_count']} copies")
        if "recommendation" in g:
            print(f"    -> {g['recommendation'][:80]}...")
    return results
```

### Tutorial 20: Workspace Health Dashboard
Generate a comprehensive health report for all repositories:
```python
async def workspace_health_report(workspace="D:/Dev/repos"):
    report = {
        "analysis": await analyze_dev_workspace(workspace_path=workspace),
        "duplicates": await find_duplicate_code(workspace_path=workspace, min_lines=15),
        "cleanup": await cleanup_dev_artifacts(workspace_path=workspace, dry_run=True)
    }
    analysis = report["analysis"]
    if analysis["success"]:
        print(f"Languages: {len(analysis.get('languages', {}))}")
        print(f"Total LOC: {analysis.get('total_loc', 0)}")
    dup = report["duplicates"]
    if dup["success"]:
        print(f"Duplicate blocks: {dup.get('refactoring_opportunities', 0)}")
    clean = report["cleanup"]
    if clean["success"]:
        print(f"Cleanup potential: {clean.get('potential_savings_gb', 0)} GB")
    return report
```

### Tutorial 21: Selective Multimedia Backup
Backup only video files from scanned multimedia drives:
```python
async def backup_videos_only(target_drive="G:"):
    """Backup all video files to an external drive."""
    scan = await multimedia_drive_scanner(file_types=["video"])
    if not scan["success"]:
        return {"error": "Scan failed"}
    print(f"Found {scan['total_files']} video files ({scan['total_size_gb']} GB)")
    for drive, data in scan.get("results", {}).items():
        if data.get("success"):
            print(f"  {drive}: {data['file_count']} files")
    return scan
```

### Tutorial 22: USB Drive Sync Automation
Automatically sync multimedia to connected USB drives:
```python
async def auto_sync_to_usb():
    """Detect USB drives and offer to sync multimedia."""
    usb = await detect_usb_drives()
    if not usb["success"] or usb["count"] == 0:
        print("No USB drives detected")
        return
    for drive in usb["usb_drives"]:
        dl = drive["drive_letter"]
        has_mm = drive.get("multimedia_folder_exists", False)
        print(f"{dl}: {drive['label']} ({drive['space_info']['free_gb']} GB free)")
        if has_mm:
            result = await sync_folders(
                source_path="E:/multimedia files",
                target_path=f"{dl}/multimedia files",
                sync_mode="update",
                dry_run=True
            )
            print(f"  Sync preview: {result.get('changes_detected', 'N/A')}")
```

### Tutorial 23: Code Quality Pipeline
Run code quality checks before commits:
```python
async def pre_commit_check(repo_path="."):
    health = await scan_repo_health(repo_path=repo_path)
    if not health["success"]:
        print("Health check failed")
        return False
    issues = health.get("issues", {})
    if issues.get("dirty_git"):
        print("WARNING: Uncommitted changes found")
    if issues.get("unpushed_commits", 0) > 0:
        print(f"WARNING: {issues['unpushed_commits']} unpushed commits")
    if issues.get("large_files"):
        for f in issues["large_files"]:
            print(f"LARGE FILE: {f['path']} ({f['size_mb']} MB)")
    return len(issues) == 0

ok = await pre_commit_check("D:/Dev/repos/my-project")
print(f"Pre-commit check: {'PASS' if ok else 'ISSUES FOUND'}")
```

### Tutorial 24: Repository Backup Strategy
Backup repositories with intelligent exclusion:
```python
async def backup_all_repos():
    backup = await backup_dev_repositories(
        exclude_patterns=["node_modules", ".venv", "__pycache__", ".git", "target", "build", "dist", "*.log"]
    )
    if backup["success"]:
        print(f"Backed up {backup['backup_count']} repos")
        print(f"Total size: {backup['total_size_mb']} MB")
        for b in backup.get("backups", []):
            print(f"  {b['repo']}: {b['size_mb']} MB")
    return backup
```
