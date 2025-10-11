#!/usr/bin/env python3
"""
MCPB packaging script for Beyond Compare MCP Server.

This script creates a complete MCPB package including all Python dependencies
for the Beyond Compare MCP server following the official MCPB building guide.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

# Project configuration
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
MCPB_DIR = Path(__file__).parent
DIST_DIR = PROJECT_ROOT / "dist"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"

# Package information
PACKAGE_NAME = "beyondcompare-mcp"
PACKAGE_VERSION = "0.1.0"


class MCPBBuilder:
    """MCPB package builder with dependency bundling."""

    def __init__(self):
        self.temp_dir: Optional[Path] = None
        self.build_dir: Optional[Path] = None

    def __enter__(self):
        """Set up temporary directories."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="mcpb_build_"))
        self.build_dir = self.temp_dir / "build"

        # Create build directories
        self.build_dir.mkdir(parents=True)

        print(f"Build directory: {self.build_dir}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up temporary directories."""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def clean_dist(self):
        """Clean the dist directory."""
        print("Cleaning dist directory...")
        if DIST_DIR.exists():
            # Only remove MCPB files
            for file in DIST_DIR.glob("*.mcpb"):
                file.unlink()
        else:
            DIST_DIR.mkdir(parents=True, exist_ok=True)

    def validate_source(self):
        """Validate source code structure."""
        print("Validating source structure...")

        # Check required files
        required_files = [
            SRC_DIR / "beyondcompare_mcp" / "__init__.py",
            SRC_DIR / "beyondcompare_mcp" / "__main__.py",
            SRC_DIR / "beyondcompare_mcp" / "server.py",
            SRC_DIR / "beyondcompare_mcp" / "cli.py",
            SRC_DIR / "beyondcompare_mcp" / "config.py",
            SRC_DIR / "beyondcompare_mcp" / "exceptions.py",
            MCPB_DIR / "manifest.json",
            MCPB_DIR / "mcpb.json",
        ]

        for file_path in required_files:
            if not file_path.exists():
                raise FileNotFoundError(f"Required file missing: {file_path}")

        print("Source validation passed")

    def check_mcpb_cli(self):
        """Check if MCPB CLI is available."""
        print("Checking MCPB CLI...")
        try:
            result = subprocess.run(["mcpb", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"MCPB CLI found: {result.stdout.strip()}")
            else:
                raise RuntimeError("MCPB CLI not working")
        except FileNotFoundError:
            raise RuntimeError("MCPB CLI not found. Install with: npm install -g @anthropic-ai/mcpb")

    def validate_manifest(self):
        """Validate the MCPB manifest."""
        print("Validating MCPB manifest...")
        
        # Change to MCPB directory and validate
        original_cwd = os.getcwd()
        try:
            os.chdir(MCPB_DIR)
            result = subprocess.run(["mcpb", "validate", "manifest.json"], capture_output=True, text=True)
            if result.returncode == 0:
                print("Manifest validation passed")
            else:
                print(f"Manifest validation failed:")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                raise RuntimeError("Manifest validation failed")
        finally:
            os.chdir(original_cwd)

    def build_package(self) -> Path:
        """Build the MCPB package using MCPB CLI."""
        print("Building MCPB package...")

        mcpb_filename = f"{PACKAGE_NAME}.mcpb"
        mcpb_path = DIST_DIR / mcpb_filename

        # Change to MCPB directory and build
        original_cwd = os.getcwd()
        try:
            os.chdir(MCPB_DIR)
            result = subprocess.run(
                ["mcpb", "pack", ".", str(mcpb_path)], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                print(f"MCPB package created: {mcpb_path}")
                if mcpb_path.exists():
                    size_mb = mcpb_path.stat().st_size / 1024 / 1024
                    print(f"Package size: {size_mb:.2f} MB")
                    return mcpb_path
                else:
                    raise RuntimeError("Package file not found after build")
            else:
                print(f"MCPB build failed:")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                raise RuntimeError("MCPB build failed")
        finally:
            os.chdir(original_cwd)

    def build(self) -> Path:
        """Execute the complete build process."""
        print("Starting MCPB build process...")
        print("=" * 50)

        self.clean_dist()
        self.validate_source()
        self.check_mcpb_cli()
        self.validate_manifest()
        mcpb_path = self.build_package()

        print("=" * 50)
        print("Build completed successfully!")
        print(f"MCPB package: {mcpb_path}")
        return mcpb_path


def main():
    """Main entry point."""
    try:
        with MCPBBuilder() as builder:
            mcpb_path = builder.build()

            print("\nNext steps:")
            print(f"1. Test the package by dragging {mcpb_path.name} to Claude Desktop")
            print("2. Check Claude Desktop's MCP settings to verify installation")
            print("3. Configure Beyond Compare path and settings")
            print("4. Test the MCP tools in a Claude conversation")

            return 0

    except KeyboardInterrupt:
        print("\nBuild cancelled by user")
        return 1
    except Exception as e:
        print(f"\nBuild failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
