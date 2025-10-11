# Beyond Compare MCP - MCPB Package Build Script
# Version: 1.0.0
# Date: 2025-01-15

param(
    [string]$OutputDir = "dist",
    [switch]$NoSign,
    [switch]$Help,
    [string]$Version
)

# Colors for output
$Colors = @{
    Success = "Green"
    Warning = "Yellow"
    Error = "Red"
    Info = "Cyan"
    Header = "Magenta"
}

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Show-Help {
    Write-ColorOutput "Beyond Compare MCP - MCPB Package Build Script" "Header"
    Write-ColorOutput "================================================" "Header"
    Write-Host ""
    Write-ColorOutput "USAGE:" "Info"
    Write-Host "  .\scripts\build-mcpb-package.ps1 [OPTIONS]"
    Write-Host ""
    Write-ColorOutput "OPTIONS:" "Info"
    Write-Host "  -OutputDir <path>    Output directory for built package (default: dist)"
    Write-Host "  -NoSign             Skip package signing (for development)"
    Write-Host "  -Version <version>   Override version number"
    Write-Host "  -Help               Show this help message"
    Write-Host ""
    Write-ColorOutput "EXAMPLES:" "Info"
    Write-Host "  .\scripts\build-mcpb-package.ps1                    # Build and sign"
    Write-Host "  .\scripts\build-mcpb-package.ps1 -NoSign            # Build without signing"
    Write-Host "  .\scripts\build-mcpb-package.ps1 -OutputDir C:\temp # Custom output"
    Write-Host ""
    exit 0
}

if ($Help) { Show-Help }

Write-ColorOutput "🚀 Beyond Compare MCP - MCPB Package Builder" "Header"
Write-ColorOutput "=============================================" "Header"
Write-Host ""

# Check prerequisites
Write-ColorOutput "📋 Checking Prerequisites..." "Info"

# Check MCPB CLI
try {
    $mcpbVersion = mcpb --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "✅ MCPB CLI: $mcpbVersion" "Success"
    } else {
        throw "MCPB CLI not found"
    }
} catch {
    Write-ColorOutput "❌ MCPB CLI not installed" "Error"
    Write-ColorOutput "Install with: npm install -g @anthropic-ai/mcpb" "Warning"
    exit 1
}

# Check Python
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "✅ Python: $pythonVersion" "Success"
    } else {
        throw "Python not found"
    }
} catch {
    Write-ColorOutput "❌ Python not installed or not in PATH" "Error"
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "✅ Node.js: $nodeVersion" "Success"
    } else {
        throw "Node.js not found"
    }
} catch {
    Write-ColorOutput "❌ Node.js not installed or not in PATH" "Error"
    exit 1
}

Write-Host ""

# Validate manifest
Write-ColorOutput "🔍 Validating Manifest..." "Info"
Set-Location mcpb
try {
    mcpb validate manifest.json
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "✅ Manifest validation passed" "Success"
    } else {
        throw "Manifest validation failed"
    }
} catch {
    Write-ColorOutput "❌ Manifest validation failed" "Error"
    Set-Location ..
    exit 1
}
Set-Location ..

# Create output directory
Write-ColorOutput "📁 Preparing Output Directory..." "Info"
if (Test-Path $OutputDir) {
    Write-ColorOutput "🧹 Cleaning existing output directory" "Warning"
    Remove-Item "$OutputDir\*.mcpb" -Force -ErrorAction SilentlyContinue
} else {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}
Write-ColorOutput "✅ Output directory ready: $OutputDir" "Success"

Write-Host ""

# Build package
Write-ColorOutput "🔨 Building MCPB Package..." "Info"
Set-Location mcpb
try {
    $packageName = "beyondcompare-mcp.mcpb"
    mcpb pack . "../$OutputDir/$packageName"
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "✅ Package built successfully" "Success"
    } else {
        throw "Package build failed"
    }
} catch {
    Write-ColorOutput "❌ Package build failed" "Error"
    Set-Location ..
    exit 1
}
Set-Location ..

# Verify package
Write-ColorOutput "🔍 Verifying Package..." "Info"
$packagePath = "$OutputDir/$packageName"
if (Test-Path $packagePath) {
    $size = (Get-Item $packagePath).Length
    $sizeMB = [math]::Round($size / 1MB, 2)
    Write-ColorOutput "✅ Package verified: $sizeMB MB" "Success"
    
    if ($sizeMB -gt 10) {
        Write-ColorOutput "⚠️  Package size is large (>10MB)" "Warning"
    }
} else {
    Write-ColorOutput "❌ Package not found after build" "Error"
    exit 1
}

# Package signing
if (-not $NoSign) {
    Write-ColorOutput "🔐 Package Signing..." "Info"
    Write-ColorOutput "⚠️  Package signing not configured - skipping" "Warning"
    Write-ColorOutput "   To enable signing, configure MCPB signing keys" "Info"
} else {
    Write-ColorOutput "⏭️  Skipping package signing (development mode)" "Warning"
}

Write-Host ""

# Success summary
Write-ColorOutput "🎉 Build Complete!" "Success"
Write-ColorOutput "==================" "Success"
Write-Host ""
Write-ColorOutput "📦 Package: $packagePath" "Info"
Write-ColorOutput "📏 Size: $sizeMB MB" "Info"
Write-ColorOutput "🎯 Ready for distribution!" "Success"
Write-Host ""

Write-ColorOutput "📋 Next Steps:" "Info"
Write-Host "1. Test installation: Drag $packageName to Claude Desktop"
Write-Host "2. Verify configuration prompts work"
Write-Host "3. Test all 6 tools functionality"
Write-Host "4. Create GitHub release for distribution"
Write-Host ""

Write-ColorOutput "✨ Beyond Compare MCP package ready!" "Success"
