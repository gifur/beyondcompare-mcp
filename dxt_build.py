"""
DXT packaging script for Beyond Compare MCP.

This script creates a DXT package for the Beyond Compare MCP server.
"""

import json
import shutil
import sys
from pathlib import Path
from typing import Dict, Any

# Project root
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
DIST_DIR = PROJECT_ROOT / "dist"
DXT_DIR = PROJECT_ROOT / "dxt"

# Package information
PACKAGE_NAME = "beyondcompare-mcp"
PACKAGE_VERSION = "0.1.0"
PACKAGE_DESCRIPTION = "Beyond Compare MCP Server for FastMCP 2.10"
PACKAGE_AUTHOR = "Your Name"
PACKAGE_AUTHOR_EMAIL = "your.email@example.com"

# DXT package structure
DXT_PACKAGE_STRUCTURE = {
    "name": PACKAGE_NAME,
    "version": PACKAGE_VERSION,
    "description": PACKAGE_DESCRIPTION,
    "author": PACKAGE_AUTHOR,
    "author_email": PACKAGE_AUTHOR_EMAIL,
    "python": ">=3.8",
    "dependencies": [
        "fastmcp>=2.10.0",
        "python-dotenv>=1.0.0",
        "pydantic>=1.10.0",
        "uvicorn>=0.20.0",
    ],
    "entry_points": {
        "console_scripts": [
            "beyondcompare-mcp=beyondcompare_mcp.cli:main",
        ],
    },
    "include": [
        "beyondcompare_mcp/*.py",
        "beyondcompare_mcp/*.json",
        "beyondcompare_mcp/*.md",
        "beyondcompare_mcp/prompts/*",
    ],
    "prompts": [
        "beyondcompare_mcp/prompts/init.txt"
    ],
}


def clean() -> None:
    """Clean build artifacts."""
    print("Cleaning build artifacts...")
    
    # Remove dist directory
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    
    # Remove DXT directory
    if DXT_DIR.exists():
        shutil.rmtree(DXT_DIR)
    
    # Remove Python cache files
    for pycache in PROJECT_ROOT.rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)
    
    print("Clean complete.")


def build_dxt_package() -> Path:
    """Build the DXT package.
    
    Returns:
        Path to the built DXT package file.
    """
    print("Building DXT package...")
    
    # Create directories
    DIST_DIR.mkdir(exist_ok=True, parents=True)
    DXT_DIR.mkdir(exist_ok=True, parents=True)
    
    # Copy source files to DXT directory
    shutil.copytree(
        SRC_DIR / "beyondcompare_mcp",
        DXT_DIR / "beyondcompare_mcp",
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo')
    )
    
    # Copy README and LICENSE to DXT directory
    for file in ["README.md", "LICENSE"]:
        if (PROJECT_ROOT / file).exists():
            shutil.copy2(PROJECT_ROOT / file, DXT_DIR)
    
    # Create package metadata
    package_json = DXT_DIR / "package.json"
    with open(package_json, "w", encoding="utf-8") as f:
        json.dump(DXT_PACKAGE_STRUCTURE, f, indent=2)
    
    # Create DXT package
    dxt_package = DIST_DIR / f"{PACKAGE_NAME}-{PACKAGE_VERSION}.dxt"
    shutil.make_archive(
        str(dxt_package.with_suffix('')),  # Remove .dxt extension
        "zip",
        root_dir=DXT_DIR,
    )
    
    # Rename .zip to .dxt
    dxt_zip = dxt_package.with_suffix('.zip')
    if dxt_zip.exists():
        dxt_zip.rename(dxt_package)
    
    print(f"DXT package built: {dxt_package}")
    return dxt_package


def build_wheel() -> Path:
    """Build a wheel distribution.
    
    Returns:
        Path to the built wheel file.
    """
    print("Building wheel...")
    
    # Clean build directory
    build_dir = PROJECT_ROOT / "build"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # Build the wheel
    import subprocess
    subprocess.check_call([sys.executable, "-m", "build", "--wheel", "--outdir", str(DIST_DIR)])
    
    # Find the built wheel
    wheels = list(DIST_DIR.glob("*.whl"))
    if not wheels:
        raise FileNotFoundError("No wheel file found in dist directory")
    
    wheel_path = wheels[0]
    print(f"Wheel built: {wheel_path}")
    return wheel_path


def main() -> int:
    """Main entry point for the build script."""
    try:
        clean()
        build_dxt_package()
        build_wheel()
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
