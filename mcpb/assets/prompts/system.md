# Beyond Compare MCP System Guide

Beyond Compare MCP is a comprehensive Model Context Protocol (MCP) server that provides powerful file and directory comparison using Beyond Compare, along with advanced multimedia drive scanning, duplicate detection, USB drive monitoring, development workspace analysis, and repository health scanning.

## Tools Reference

### `compare_files`

Compare two files using Beyond Compare and get detailed comparison results.

**Parameters:**
- `left_path` (str, required): Absolute path to the left file for comparison
- `right_path` (str, required): Absolute path to the right file for comparison
- `output_report` (str | None, optional): Optional path to save the comparison report as a text file

**Returns:**
```json
{
  "success": true,
  "left_path": "C:/file_a.txt",
  "right_path": "C:/file_b.txt",
  "identical": false,
  "differences_found": true,
  "output_report": "C:/report.txt",
  "message": "Differences found between files"
}
```

**When files are identical:**
```json
{
  "success": true,
  "identical": true,
  "differences_found": false,
  "message": "Files are identical"
}
```

**Error cases:**
- Returns `success: false` if either file does not exist
- Returns error if Beyond Compare is not installed
- Validates paths against command injection patterns (rejects `;`, `|`, `&`, `>`, `<`, `` ` ``, `$`, `(`, `)`)

### `compare_folders`

Compare two folders using Beyond Compare with optional subfolder inclusion and report generation.

**Parameters:**
- `left_path` (str, required): Absolute path to the left folder
- `right_path` (str, required): Absolute path to the right folder
- `output_report` (str | None, optional): Path to save the comparison report (supports layout:summary format)
- `include_subfolders` (bool, optional, default: True): Whether to include subfolders recursively

**Returns:**
```json
{
  "success": true,
  "left_path": "C:/folder_a",
  "right_path": "C:/folder_b",
  "include_subfolders": true,
  "differences_found": true,
  "output_report": "C:/report.txt",
  "message": "Differences found between folders"
}
```

### `sync_folders`

Synchronize folders using Beyond Compare with multiple sync modes. Supports dry-run preview before actual synchronization.

**Parameters:**
- `source_path` (str, required): Source directory path
- `target_path` (str, required): Target directory path
- `sync_mode` (str, optional, default: "mirror"): Synchronization mode. One of:
  - `"mirror"`: Mirror source to target (one-way, makes target identical to source)
  - `"update"`: Update newer files from source to target
  - `"backup"`: Create backup copies of changed files
- `dry_run` (bool, optional, default: True): If True, only shows what would be done without making changes

**Returns:**
```json
{
  "success": true,
  "source_path": "C:/source",
  "target_path": "D:/backup",
  "sync_mode": "mirror",
  "dry_run": true,
  "changes_detected": true,
  "message": "Synchronization preview completed successfully"
}
```

### `multimedia_drive_scanner`

Scan multimedia drives (E:, F:, K:, L:) for complete inventory with filtering options. Supports filtering by recency and media type.

**Parameters:**
- `drives` (list[str] | None, optional): Specific drives to scan (default: auto-detect E:, F:, K:, L:)
- `recent_days` (int | None, optional): Only include files modified in the last N days
- `file_types` (list[str] | None, optional): Filter by media types: `"video"`, `"audio"`, `"images"`, `"documents"`

**Returns:**
```json
{
  "success": true,
  "scan_time_seconds": 12.5,
  "drives_scanned": ["E:", "F:"],
  "total_files": 15234,
  "total_size_gb": 245.8,
  "results": {
    "E:": {
      "success": true,
      "file_count": 8500,
      "total_size": 150000000000,
      "files": [
        {"name": "video.mp4", "path": "E:/multimedia files/video.mp4", "size_mb": 150.0, "media_type": "video"}
      ],
      "media_stats": {"video": {"count": 500, "size": 100000000000}},
      "drive_space": {"total_gb": 1000, "used_gb": 750, "free_gb": 250, "used_percent": 75.0}
    }
  },
  "summary": {
    "successful_drives": ["E:", "F:"],
    "total_files": 15234,
    "total_size_gb": 245.8,
    "media_distribution": {"video": 8000, "audio": 5000, "images": 2000, "documents": 234},
    "largest_collection": "E:"
  }
}
```

### `find_multimedia_duplicates`

Find duplicate multimedia files across drives using content hashing (SHA-256) or name-based detection.

**Parameters:**
- `drives` (list[str] | None, optional): Specific drives to check (default: use last scan results)
- `min_size_mb` (float, optional, default: 0.1): Minimum file size in MB to consider for duplicate checking
- `file_types` (list[str] | None, optional): Filter by media types
- `use_content_hash` (bool, optional, default: True): Use SHA-256 content hash for accurate detection (slower but more accurate)

**Returns:**
```json
{
  "success": true,
  "scan_time_seconds": 45.2,
  "detection_method": "content_hash",
  "total_files_checked": 15234,
  "duplicate_groups": [
    {
      "hash": "a1b2c3...",
      "size_mb": 150.0,
      "duplicate_count": 3,
      "files": [
        {"name": "movie.mp4", "drive": "E:", "size_mb": 150.0},
        {"name": "movie.mp4", "drive": "F:", "size_mb": 150.0}
      ],
      "potential_savings_mb": 300.0,
      "recommendation": "KEEP: E:\\movie.mp4\nREMOVE:\n  - F:\\movie.mp4"
    }
  ],
  "total_duplicate_groups": 10,
  "total_duplicate_files": 25,
  "total_savings_gb": 50.0,
  "recommendations": [
    "HIGH IMPACT: 3 duplicate groups could save 5000MB",
    "Most duplicated media type: video",
    "Drive with most duplicates: F:"
  ]
}
```

### `detect_usb_drives`

Detect and list all connected USB drives with detailed space information.

**Parameters:** None

**Returns:**
```json
{
  "success": true,
  "usb_drives": [
    {
      "drive_letter": "G:",
      "label": "USB DRIVE",
      "space_info": {
        "total_gb": 500.0,
        "used_gb": 200.0,
        "free_gb": 300.0,
        "used_percent": 40.0
      },
      "multimedia_folder_exists": true
    }
  ],
  "count": 1,
  "message": "Found 1 USB drive(s)"
}
```

### `backup_dev_repositories`

Smart backup of development repositories with intelligent filtering and compression.

**Parameters:**
- `repo_paths` (list[str], optional): Specific repository paths to backup. If omitted, scans common dev directories.
- `output_dir` (str, optional): Output directory for backup archives
- `exclude_patterns` (list[str], optional): Additional exclude patterns beyond defaults (node_modules, .venv, __pycache__, .git, target, build, dist)

**Returns:**
```json
{
  "success": true,
  "backup_count": 5,
  "total_size_mb": 250.0,
  "output_dir": "D:/backups",
  "backups": [
    {"repo": "my-project", "size_mb": 50.0, "path": "D:/backups/my-project.zip"}
  ]
}
```

### `analyze_dev_workspace`

Comprehensive analysis of development workspace including languages, dependencies, and optimization opportunities.

**Parameters:**
- `workspace_path` (str, optional): Root path of the workspace to analyze. Defaults to current directory.
- `depth` (int, optional, default: 3): Directory traversal depth for analysis

**Returns:**
```json
{
  "success": true,
  "workspace_path": "D:/Dev/repos",
  "total_repos": 25,
  "languages": {
    "Python": {"repos": 15, "files": 500, "loc": 50000},
    "TypeScript": {"repos": 8, "files": 300, "loc": 30000},
    "Rust": {"repos": 2, "files": 50, "loc": 8000}
  },
  "total_loc": 88000,
  "large_files": [{"path": "data.bin", "size_mb": 500}],
  "optimization_suggestions": [
    "5 repos have node_modules > 100MB - consider using pnpm"
  ]
}
```

### `scan_repo_health`

Scan repository health and identify potential issues with automated fix options.

**Parameters:**
- `repo_path` (str, optional): Path to the repository to scan. Defaults to current directory.
- `auto_fix` (bool, optional, default: False): Apply automatic fixes for detected issues

**Returns:**
```json
{
  "success": true,
  "repo_path": "D:/Dev/repos/my-project",
  "status": "needs_attention",
  "issues": {
    "dirty_git": true,
    "unpushed_commits": 3,
    "large_files": [{"path": "model.weights", "size_mb": 200}],
    "outdated_deps": ["pytest 6.0 -> 7.0"],
    "missing_tests": true,
    "stale_branches": ["feature-old", "experiment-1"]
  },
  "suggestions": [
    "Commit or stash 3 unpushed changes",
    "Update pytest from 6.0 to 7.0",
    "Consider adding .gitignore for model.weights"
  ]
}
```

### `cleanup_dev_artifacts`

Clean up build artifacts and temporary files across repositories to reclaim disk space.

**Parameters:**
- `workspace_path` (str, optional): Root path to scan for artifacts. Defaults to current directory.
- `patterns` (list[str], optional): Custom glob patterns for artifacts. Defaults: `__pycache__`, `.venv`, `node_modules`, `target`, `build`, `dist`, `.next`, `*.pyc`
- `dry_run` (bool, optional, default: True): Preview what would be deleted without deleting
- `min_size_mb` (float, optional, default: 10): Minimum directory/file size in MB to report

**Returns:**
```json
{
  "success": true,
  "workspace_path": "D:/Dev/repos",
  "artifacts_found": 12,
  "total_wasted_mb": 5000.0,
  "artifacts": [
    {"path": "repo-a/node_modules", "size_mb": 500},
    {"path": "repo-b/.venv", "size_mb": 250}
  ],
  "potential_savings_gb": 5.0,
  "message": "Dry run: 12 artifacts found, 5.0 GB could be reclaimed"
}
```

### `find_duplicate_code`

Find duplicate code across repositories for refactoring opportunities.

**Parameters:**
- `workspace_path` (str, optional): Root path to search for duplicates. Defaults to current directory.
- `min_lines` (int, optional, default: 10): Minimum number of lines to consider as a duplicate block
- `extensions` (list[str], optional): File extensions to scan (default: .py, .js, .ts, .rs, .go, .java, .cpp)
- `exclude_patterns` (list[str], optional): Patterns to exclude

**Returns:**
```json
{
  "success": true,
  "total_files_scanned": 1500,
  "duplicate_blocks": [
    {
      "similarity": 0.95,
      "lines": 25,
      "files": [
        {"path": "repo-a/utils.py", "start_line": 10},
        {"path": "repo-b/helpers.py", "start_line": 15}
      ],
      "suggestion": "Extract to shared library"
    }
  ],
  "refactoring_opportunities": 5,
  "message": "Found 5 duplicate code blocks across 1500 files"
}
```

### `compare_workspace_snapshots`

Compare workspace snapshots to identify changes over time.

**Parameters:**
- `snapshot_a` (str, required): Path to the first snapshot file
- `snapshot_b` (str, required): Path to the second snapshot file
- `report_format` (str, optional, default: "summary"): "summary" or "detailed"

**Returns:**
```json
{
  "success": true,
  "snapshot_a": "D:/snapshots/before.json",
  "snapshot_b": "D:/snapshots/after.json",
  "added": 10,
  "removed": 3,
  "modified": 5,
  "unchanged": 100,
  "changes": [
    {"path": "src/new.py", "change": "added"},
    {"path": "src/old.py", "change": "removed"},
    {"path": "src/updated.py", "change": "modified"}
  ]
}
```

### `selective_restore`

Selectively restore specific projects or files from backup with flexible filtering.

**Parameters:**
- `backup_path` (str, required): Path to the backup archive (ZIP format)
- `restore_path` (str, required): Directory to restore files into
- `patterns` (list[str], optional): Glob patterns to filter what to restore (e.g., `["src/**/*.py"]`)
- `overwrite` (bool, optional, default: False): Overwrite existing files

**Returns:**
```json
{
  "success": true,
  "backup_path": "D:/backups/my-project.zip",
  "restore_path": "D:/restored",
  "files_restored": 50,
  "total_size_mb": 25.0,
  "message": "Restored 50 files from backup"
}
```

### `beyondcompare_agentic_workflow`

SEP-1577 agentic workflow using sampling over BC status, compare, and repo health tools.

**Parameters:**
- `workflow_prompt` (str, required): Natural language description of the workflow to execute
- `available_tools` (list[str], optional): Tool names available for the workflow
- `max_iterations` (int, optional, default: 8): Maximum sampling iterations

**Returns:** Depends on the workflow prompt and sampling result.

### `beyondcompare_sampling_hint`

Explains sampling requirements and fallback to atomic MCP tools.

**Parameters:** None

**Returns:**
```json
{
  "success": true,
  "message": "Sampling requires FastMCP 3.1+ with ctx.sample() support. Fallback to individual tools.",
  "available_tools": ["compare_files", "compare_folders", "sync_folders", "multimedia_drive_scanner", "find_multimedia_duplicates", "detect_usb_drives"]
}
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| BEYOND_COMPARE_PATH | (auto-detected) | Path to BCompare.exe |
| BC_SCRIPTS_DIR | ./bc_scripts | Directory for temporary BC script files |
| HOST | 127.0.0.1 | Server bind address |
| PORT | 8000 | Server HTTP port |
| LOG_LEVEL | INFO | Logging level |
| COMMAND_TIMEOUT | 300 | BC command timeout in seconds |
| API_TIMEOUT | 30 | REST API timeout in seconds |

### Beyond Compare Executable Detection

The server auto-detects Beyond Compare in these locations (Windows):
- `C:\Program Files\Beyond Compare 5\BCompare.exe`
- `C:\Program Files\Beyond Compare 4\BCompare.exe`
- `C:\Program Files\Beyond Compare 3\BCompare.exe`
- Any path in the system PATH

### Scripting

The server creates temporary Beyond Compare script files (`.bcscript`) in the scripts directory. These scripts use BC's native scripting language with commands like `load`, `expand all`, `select all.files`, `sync mirror:left->right`, and `report layout:summary`.

## Workflow Sequences

### File Comparison Workflow
1. Call `compare_files(left_path="C:/old.txt", right_path="C:/new.txt")` to check if files differ
2. If differences found, call `compare_files(left_path="C:/old.txt", right_path="C:/new.txt", output_report="C:/diff.txt")` to generate a report
3. Review the differences and determine if changes are acceptable
4. For folder-level changes, use `compare_folders` instead

### Folder Synchronization Workflow
1. Call `compare_folders(left_path="C:/source", right_path="D:/backup")` to identify differences
2. Call `sync_folders(source_path="C:/source", target_path="D:/backup", sync_mode="mirror", dry_run=true)` to preview sync
3. Review the preview results for expected changes
4. Call `sync_folders(source_path="C:/source", target_path="D:/backup", sync_mode="mirror", dry_run=false)` to execute
5. Verify with another `compare_folders` call

### Multimedia Inventory Workflow
1. Call `multimedia_drive_scanner()` for full inventory of all multimedia drives
2. Review summary statistics for total files, size, and media distribution
3. If duplicates are suspected, call `find_multimedia_duplicates(use_content_hash=true)`
4. Review duplicate groups sorted by potential savings
5. Use the recommendations to decide which duplicates to remove
6. Optionally call `detect_usb_drives()` to find external storage targets

### Dev Workspace Analysis Workflow
1. Call `analyze_dev_workspace(workspace_path="D:/Dev/repos")` for language overview
2. Call `scan_repo_health(repo_path="D:/Dev/repos/my-project")` for individual repo issues
3. Call `find_duplicate_code(workspace_path="D:/Dev/repos", min_lines=10)` for refactoring opportunities
4. Call `cleanup_dev_artifacts(workspace_path="D:/Dev/repos", dry_run=true)` to preview space recovery
5. If satisfied, run cleanup with `dry_run=false`
6. Call `backup_dev_repositories()` to create backups before major changes

### Selective Restore Workflow
1. Identify the backup archive containing needed files
2. Call `selective_restore(backup_path="D:/backups/project.zip", restore_path="D:/restored", patterns=["src/**/*.py"])` to restore specific files
3. Verify restored files are correct
4. If overwrite needed, call with `overwrite=true`

## Architecture

The server follows a modular architecture:

```
beyondcompare-mcp (FastMCP server)
  |-- Comparison Engine
  |     |-- Beyond Compare CLI (BCompare.exe)
  |     |-- Script generation (bcscript files)
  |     |-- Path validation and security
  |-- Multimedia Scanner
  |     |-- Drive auto-detection
  |     |-- File type categorization
  |     |-- Content hashing (SHA-256)
  |     |-- Duplicate detection
  |-- Dev Tools
  |     |-- Workspace analysis
  |     |-- Repo health scanning
  |     |-- Code duplicate detection
  |     |-- Build artifact cleanup
  |-- Backup/Restore
  |     |-- Repository backup
  |     |-- Selective file restore
  |     |-- Snapshot comparison
```

## Security

### Input Validation
- All file paths are resolved and normalized
- Path traversal attacks (`..`) are detected and blocked
- Command injection characters (`;`, `|`, `&`, `>`, `<`, `` ` ``, `$`, `(`, `)`) are rejected
- Script files use tempfile.NamedTemporaryFile for secure creation
- Script files are deleted after execution

### Tool Parameter Reference

| Tool | Parameter | Type | Required | Default |
|------|-----------|------|----------|---------|
| compare_files | left_path | str | Yes | - |
| compare_files | right_path | str | Yes | - |
| compare_files | output_report | str | No | null |
| compare_folders | left_path | str | Yes | - |
| compare_folders | right_path | str | Yes | - |
| compare_folders | output_report | str | No | null |
| compare_folders | include_subfolders | bool | No | true |
| sync_folders | source_path | str | Yes | - |
| sync_folders | target_path | str | Yes | - |
| sync_folders | sync_mode | str | No | "mirror" |
| sync_folders | dry_run | bool | No | true |
| multimedia_drive_scanner | drives | list[str] | No | null |
| multimedia_drive_scanner | recent_days | int | No | null |
| multimedia_drive_scanner | file_types | list[str] | No | null |
| find_multimedia_duplicates | drives | list[str] | No | null |
| find_multimedia_duplicates | min_size_mb | float | No | 0.1 |
| find_multimedia_duplicates | file_types | list[str] | No | null |
| find_multimedia_duplicates | use_content_hash | bool | No | true |
| detect_usb_drives | - | - | No | - |
| backup_dev_repositories | repo_paths | list[str] | No | null |
| backup_dev_repositories | output_dir | str | No | null |
| backup_dev_repositories | exclude_patterns | list[str] | No | null |
| analyze_dev_workspace | workspace_path | str | No | null |
| analyze_dev_workspace | depth | int | No | 3 |
| scan_repo_health | repo_path | str | No | null |
| scan_repo_health | auto_fix | bool | No | false |
| cleanup_dev_artifacts | workspace_path | str | No | null |
| cleanup_dev_artifacts | patterns | list[str] | No | null |
| cleanup_dev_artifacts | dry_run | bool | No | true |
| cleanup_dev_artifacts | min_size_mb | float | No | 10 |
| find_duplicate_code | workspace_path | str | No | null |
| find_duplicate_code | min_lines | int | No | 10 |
| find_duplicate_code | extensions | list[str] | No | null |
| find_duplicate_code | exclude_patterns | list[str] | No | null |
| compare_workspace_snapshots | snapshot_a | str | Yes | - |
| compare_workspace_snapshots | snapshot_b | str | Yes | - |
| compare_workspace_snapshots | report_format | str | No | "summary" |
| selective_restore | backup_path | str | Yes | - |
| selective_restore | restore_path | str | Yes | - |
| selective_restore | patterns | list[str] | No | null |
| selective_restore | overwrite | bool | No | false |

## Detailed Operation Reference

### compare_files
This tool runs Beyond Compare's Quick Compare mode (/qc flag) to compare two files. BC runs silently (/silent flag) and reports differences via its return code: 0 = no differences (files identical), 1 = differences found. When output_report is specified, the tool generates a text-format conflict report. The server validates both paths exist before invoking BC.

### compare_folders
Uses Beyond Compare's scripting engine to perform folder comparison. Generates a temporary .bcscript file with commands: load both folders, expand all subdirectories, select all files. When output_report is specified, a report command with layout:summary and options:display-mismatches is appended. The script file is created securely with NamedTemporaryFile and deleted after execution.

### sync_folders
Generates BC scripts with mode-specific sync commands: "sync mirror:left->right" for mirror mode (makes target identical to source), "sync update:left->right" for update mode (only newer files), "sync create:left->right" for backup mode (creates copies). When dry_run is true, "preview" is appended to the sync command, showing planned changes without executing them.

### multimedia_drive_scanner
Recursively walks the "multimedia files" subfolder on each target drive using os.walk(). Files are categorized by extension into video, audio, images, and documents using the MEDIA_TYPES dictionary. Each file is checked against extension filter, size filter (minimum 1KB), and optional recency filter. Results include per-drive statistics, file lists, and drive space information.

### find_multimedia_duplicates
Two detection modes: content_hash (default) computes SHA-256 for each file and groups by hash for accurate deduplication; name_and_size groups by filename and file size for faster but less accurate detection. Results are sorted by potential savings (largest first). Each duplicate group includes a recommendation showing which copy to keep (based on drive priority: E: > F: > K: > L:).

### detect_usb_drives (Windows)
Uses win32api.GetLogicalDriveStrings() to enumerate drives, then win32api.GetDriveType() to identify removable drives (type 2). Returns drive letter, volume label (via GetVolumeInformation), and space usage (via shutil.disk_usage). Falls back to scanning drive letters G-Z when win32api is not available.

## Tool Behavior Summary
| Tool | Runs BC | Generates Script | Dry Run Support | File System Impact |
|------|---------|-----------------|-----------------|-------------------|
| compare_files | Yes | No | No | Read only |
| compare_folders | Yes | Yes | No | Read only |
| sync_folders | Yes | Yes | Yes | Writes target |
| multimedia_drive_scanner | No | No | N/A | Read only |
| find_multimedia_duplicates | No | No | N/A | Read only |
| detect_usb_drives | No | No | N/A | Read only |
| backup_dev_repositories | No | No | N/A | Creates backups |
| analyze_dev_workspace | No | No | N/A | Read only |
| scan_repo_health | No | No | N/A | Read only (auto_fix may modify) |
| cleanup_dev_artifacts | No | No | Yes | Deletes files (dry_run=false) |
| find_duplicate_code | No | No | N/A | Read only |
| compare_workspace_snapshots | No | No | N/A | Read only |
| selective_restore | No | No | N/A | Creates files |

## Tool Category Summary
| Category | Tools | Requires BC |
|----------|-------|-------------|
| File Comparison | compare_files, compare_folders | Yes |
| Folder Sync | sync_folders | Yes |
| Multimedia Scanning | multimedia_drive_scanner, find_multimedia_duplicates | No |
| USB Detection | detect_usb_drives | No |
| Dev Workspace | analyze_dev_workspace, scan_repo_health, cleanup_dev_artifacts, find_duplicate_code | No |
| Backup/Restore | backup_dev_repositories, selective_restore, compare_workspace_snapshots | No |
| Agentic | beyondcompare_agentic_workflow, beyondcompare_sampling_hint | No |

## Beyond Compare Script Generation

The server generates Beyond Compare script files (.bcscript) for all comparison and sync operations. Scripts are created using NamedTemporaryFile for security and deleted after execution. Each script follows this pattern:

### File Comparison Script
```
load "{left}" "{right}"
select all.files
script-exit
```

### Folder Comparison Script
```
load "{left}" "{right}"
expand all
select all.files
report layout:summary options:display-mismatches output-to:"{report}"
script-exit
```

### Sync Script (Mirror)
```
load "{source}" "{target}"
expand all
select all.files all.folders
sync mirror:left->right preview
script-exit
```

The preview keyword is appended for dry_run=true. Without preview, BC executes the sync immediately.

## Media Type Detection
The multimedia scanner categorizes files by extension. The extension-to-type mapping is defined in MultimediaDriveScanner.MEDIA_TYPES. Files with unknown extensions are categorized as "other" and excluded from scans unless explicitly included. The minimum file size for scanning is 1 KB (MIN_FILE_SIZE constant). Files smaller than this are skipped to avoid processing noise like desktop.ini and thumbs.db.

## Disk Space Calculation
Available drive space is calculated using shutil.disk_usage() on Windows. The function returns total, used, and free bytes which are converted to GB for reporting. The used_percent field shows what fraction of the drive is consumed. This information is included in scan results for capacity planning.

## USB Detection Fallback
When the pywin32 library is not available (not installed or on non-Windows platforms), USB detection falls back to testing drive letters G through Z with os.path.exists() and os.path.is_dir(). This is less reliable than the win32api method but provides basic functionality without additional dependencies.

## Temporary Script Cleanup
All generated BC scripts are created using Python's tempfile.NamedTemporaryFile with delete=False. After the BC command completes, the script file is explicitly deleted with unlink(missing_ok=True). If the server crashes during script execution, the temporary file may be orphaned. These orphaned files are cleaned on next server start by the BC_SCRIPTS_DIR recreation.

## Tool Return Code Reference

Beyond Compare return codes mapped by the server:
| Code | Meaning | Server Behavior |
|------|---------|----------------|
| 0 | Success, no differences | Returns identical=true |
| 1 | Success, differences found | Returns differences_found=true |
| 2+ | Error | Raises BeyondCompareCommandError |

## Script Command Reference

The server generates these Beyond Compare script commands:
- `load "{path}" "{path}"`: Load two paths for comparison
- `expand all`: Recursively expand all folders
- `select all.files all.folders`: Select all items
- `sync mirror:left->right`: Mirror source to target
- `sync update:left->right`: Copy newer files
- `sync create:left->right`: Create backup copies
- `sync ... preview`: Show preview without executing
- `report layout:summary options:display-mismatches output-to:"{path}"`: Generate report
- `script-exit`: Close BC after script completion

## Error Handling

All tools return structured error responses:

```json
{
  "success": false,
  "error": "Human-readable error description",
  "message": "Additional context about the failure"
}
```

### Custom Exception Classes

| Exception | Cause |
|-----------|-------|
| `BeyondCompareNotInstalledError` | BC executable not found |
| `BeyondCompareCommandError` | BC command failed (return code >= 2) |
| `BeyondCompareTimeoutError` | BC command timed out |
| `BeyondCompareScriptError` | BC script creation or execution failed |

### Input Validation

- All file paths are validated against path traversal attacks
- Command injection characters (`;`, `|`, `&`, `>`, `<`, `` ` ``, `$`, `(`, `)`) are blocked
- Paths are resolved and expanded securely
- Temp script files use `tempfile.NamedTemporaryFile` for secure creation
- Script files are cleaned up after execution
