# Sandra's Multimedia Sync Toolkit
*Ready-to-use prompts and tools for E:, F:, K:, L: drive synchronization*

## 🚀 QUICK-START PROMPTS

### Daily Operations

#### Check All Multimedia Drives Status
```
Check multimedia drives E:, F:, K:, L: in their "multimedia files" folders for:
- Available space on each drive
- Recently modified files (last 7 days)  
- Any obvious issues or warnings
- Summary of total content by drive
```

#### USB Drive Sync Assessment  
```
Scan for connected USB drives and:
- Compare their contents with E:, F:, K:, L: multimedia folders
- Recommend optimal sync strategy based on USB capacity
- Identify what's missing or outdated on USB
- Estimate time needed for full sync
```

#### Find Multimedia Duplicates
```
Search for duplicate files across E:, F:, K:, L: multimedia folders:
- Focus on video files (MP4, AVI, MKV) and audio (MP3, FLAC)
- Compare by file size and content, not just name
- Provide cleanup recommendations with safety warnings
- Show potential space savings
```

### Weekly Maintenance

#### Drive Balance Analysis
```
Analyze storage distribution across E:, F:, K:, L: multimedia drives:
- Show usage percentage and available space per drive
- Identify drives approaching capacity
- Recommend file moves to balance storage
- Predict when drives will be full based on current usage
```

#### Multimedia Integrity Check
```
Verify integrity of multimedia files on [specify drive]:
- Check for corrupted or unreadable files
- Verify file sizes are reasonable for media type
- Test that files aren't truncated or damaged
- Generate report of any issues found
```

## 🔧 SPECIALIZED BEYONDCOMPARE TOOLS TO IMPLEMENT

### Tool 1: `multimedia_drive_scanner`
```python
# Scans E:, F:, K:, L: multimedia folders
# Returns inventory with file types, sizes, dates
# Flags duplicates and missing files
```

**Usage**: 
- `scan_multimedia_drives()` - Full scan of all drives
- `scan_multimedia_drives(drive='E:', recent_days=7)` - Recent files on specific drive

### Tool 2: `usb_sync_manager`  
```python
# Detects USB drives and compares with fixed drives
# Recommends sync strategies based on capacity
# Handles bidirectional sync with conflict resolution
```

**Usage**:
- `detect_usb_drives()` - List connected USB drives
- `plan_usb_sync(usb_drive='G:', strategy='smart_capacity')` - Plan sync
- `execute_usb_sync(plan_id, confirm=True)` - Execute planned sync

### Tool 3: `multimedia_duplicate_finder`
```python
# Content-based duplicate detection for media files  
# Handles different formats of same content
# Provides safe cleanup recommendations
```

**Usage**:
- `find_multimedia_duplicates(drives=['E:', 'F:', 'K:', 'L:'])` - Find all duplicates
- `find_multimedia_duplicates(file_types=['video'], min_size_mb=100)` - Large video duplicates

## 📋 SYNC STRATEGIES FOR YOUR SETUP

### Strategy A: "Distributed Mirror"
- **E: Drive** → **USB-1**: Work/Recent multimedia  
- **F: Drive** → **USB-2**: Entertainment/Movies
- **K: Drive** → **USB-3**: Music/Audio collections
- **L: Drive** → **USB-4**: Archive/Photos

### Strategy B: "Smart Compilation"
- **USB Master**: Best content from all drives
- Auto-selects newest, highest quality, most accessed
- Fits optimally in USB capacity

### Strategy C: "Incremental Backup"
- **USB Rotation**: Different USB for each sync session
- Only copies changes since last sync
- Maintains version history across multiple USBs

## 🎯 IMMEDIATE ACTIONS YOU CAN TAKE

### 1. Current Drive Assessment
Use Beyond Compare now to manually compare:
```
Beyond Compare E:\multimedia files F:\multimedia files
```
Look for obvious duplicates and size differences.

### 2. USB Preparation  
When you connect a USB drive:
```
Beyond Compare [USB Drive] E:\multimedia files
```
See what's already there vs what needs updating.

### 3. Space Planning
Check current space on all drives:
```
powershell: Get-WmiObject -Class Win32_LogicalDisk | Where-Object {$_.DeviceID -match '[EFKL]:'} | Select-Object DeviceID,Size,FreeSpace
```

## 🚀 ENHANCED TOOLS IMPLEMENTATION PRIORITY

### Phase 1 (This Week)
1. **`multimedia_drive_scanner`** - Essential for understanding current state
2. **`usb_sync_manager`** - Core functionality for your daily workflow  
3. **Basic duplicate detection** - Immediate space savings

### Phase 2 (Next Week)
4. **Integrity checking** - Ensure media files aren't corrupted
5. **Smart sync profiles** - Automated strategies for different scenarios
6. **Progress tracking** - Better feedback during long operations

## 💾 EXAMPLE MULTIMEDIA SYNC WORKFLOW

### Daily USB Sync Routine
1. **Connect USB drive**
2. **Run**: `detect_usb_drives()` and `scan_multimedia_drives(recent_days=1)`  
3. **Execute**: `plan_usb_sync(strategy='incremental')`
4. **Review plan** and confirm sync
5. **Monitor progress** and verify completion
6. **Safe USB removal** after verification

### Weekly Maintenance
1. **Run**: `find_multimedia_duplicates()` across all drives
2. **Review** duplicate recommendations  
3. **Execute** safe cleanup of confirmed duplicates
4. **Run**: `multimedia_integrity_check()` on each drive
5. **Plan** any needed file moves or archiving

Would you like me to implement any of these tools first? The `multimedia_drive_scanner` would give you immediate visibility into your current setup and help optimize your sync strategies.
