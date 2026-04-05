# Beyond Compare MCP User Guide

## Getting Started

1. **Compare Files**: Use file comparison to see differences between two files
2. **Sync Folders**: Synchronize directories with automatic conflict detection
3. **Find Duplicates**: Scan for duplicate files and manage storage
4. **Scan Media**: Inventory external drives and USB devices

## Common Workflows

### File Comparison
```
1. Compare files: compare_files(path1, path2)
2. View differences: get_comparison_details(session_id)
3. Export results: export_comparison(session_id, format)
```

### Folder Synchronization
```
1. Compare folders: compare_folders(path1, path2)
2. Preview sync: preview_sync(session_id, direction)
3. Execute sync: execute_sync(session_id, direction)
```

### Duplicate Detection
```
1. Scan for duplicates: scan_duplicates(paths)
2. View results: get_duplicate_report(scan_id)
3. Remove duplicates: remove_duplicates(scan_id, criteria)
```

### Media Scanning
```
1. Scan drive: scan_media_drive(drive_path)
2. Get inventory: get_media_inventory(scan_id)
3. Export catalog: export_media_catalog(scan_id, format)
```

## Configuration

- **Comparison Rules**: Configure file comparison rules and filters
- **Sync Options**: Set synchronization preferences and conflict resolution
- **Scan Settings**: Configure media scanning depth and file types
- **Export Formats**: Choose report formats (HTML, XML, CSV, JSON)

## Troubleshooting

- **Comparison fails**: Check file access permissions and paths
- **Sync conflicts**: Review conflict resolution options
- **Large scans**: Use filtering to limit scan scope
- **Performance issues**: Adjust comparison rules for better performance



