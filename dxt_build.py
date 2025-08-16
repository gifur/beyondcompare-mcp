#!/usr/bin/env python3
"""
DXT packaging script for Beyond Compare MCP Server.

This script creates a complete DXT package including all Python dependencies
for the Beyond Compare MCP server following the official DXT building guide.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, List, Optional

# Project configuration
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
DXT_DIR = PROJECT_ROOT / "dxt"
DIST_DIR = PROJECT_ROOT / "dist"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"

# Package information
PACKAGE_NAME = "beyondcompare-mcp"
PACKAGE_VERSION = "0.1.0"


class DXTBuilder:
    """DXT package builder with dependency bundling."""

    def __init__(self):
        self.temp_dir: Optional[Path] = None
        self.build_dir: Optional[Path] = None
        self.dependencies_dir: Optional[Path] = None

    def __enter__(self):
        """Set up temporary directories."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="dxt_build_"))
        self.build_dir = self.temp_dir / "build"
        self.dependencies_dir = self.build_dir / "dependencies"

        # Create build directories
        self.build_dir.mkdir(parents=True)
        self.dependencies_dir.mkdir(parents=True)

        print(f"Build directory: {self.build_dir}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up temporary directories."""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def clean_dist(self):
        """Clean the dist directory."""
        print("🧹 Cleaning dist directory...")
        if DIST_DIR.exists():
            shutil.rmtree(DIST_DIR)
        DIST_DIR.mkdir(parents=True, exist_ok=True)

    def validate_source(self):
        """Validate source code structure."""
        print("🔍 Validating source structure...")

        # Check required files
        required_files = [
            SRC_DIR / "beyondcompare_mcp" / "__init__.py",
            SRC_DIR / "beyondcompare_mcp" / "server.py",
            SRC_DIR / "beyondcompare_mcp" / "cli.py",
            SRC_DIR / "beyondcompare_mcp" / "config.py",
            SRC_DIR / "beyondcompare_mcp" / "exceptions.py",
            DXT_DIR / "manifest.json",
        ]

        for file_path in required_files:
            if not file_path.exists():
                raise FileNotFoundError(f"Required file missing: {file_path}")

        print("✅ Source validation passed")

    def install_dependencies(self):
        """Install Python dependencies into the build directory."""
        print("📦 Installing Python dependencies...")

        # Read requirements
        if not REQUIREMENTS_FILE.exists():
            print("⚠️ No requirements.txt found, creating minimal dependencies")
            requirements = [
                "mcp>=1.0.0",
                "python-dotenv>=1.0.0",
                "pydantic>=2.0.0"
            ]
        else:
            with open(REQUIREMENTS_FILE, 'r') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        print(f"Dependencies to install: {requirements}")

        # Install dependencies using pip
        cmd = [
            sys.executable, "-m", "pip", "install",
            "--target", str(self.dependencies_dir),
            "--no-deps",  # We'll handle dependencies recursively
            "--upgrade"
        ] + requirements

        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ Dependency installation failed:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            raise RuntimeError("Failed to install dependencies")

        # Now install with dependencies to get transitive deps
        cmd_with_deps = [
            sys.executable, "-m", "pip", "install",
            "--target", str(self.dependencies_dir),
            "--upgrade"
        ] + requirements

        print("Installing with transitive dependencies...")
        result = subprocess.run(cmd_with_deps, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"⚠️ Full dependency installation warning:")
            print(f"STDERR: {result.stderr}")
            # Continue anyway, core deps might be sufficient

        print("✅ Dependencies installed")

    def copy_source_code(self):
        """Copy source code to build directory."""
        print("📂 Copying source code...")

        # Copy the main package
        src_pkg = SRC_DIR / "beyondcompare_mcp"
        dst_pkg = self.build_dir / "src" / "beyondcompare_mcp"

        dst_pkg.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            src_pkg,
            dst_pkg,
            ignore=shutil.ignore_patterns(
                '__pycache__', '*.pyc', '*.pyo', '.pytest_cache'
            )
        )

        print("✅ Source code copied")

    def copy_manifest_and_assets(self):
        """Copy DXT manifest and assets."""
        print("📋 Copying DXT manifest and assets...")

        # Copy manifest.json
        manifest_src = DXT_DIR / "manifest.json"
        manifest_dst = self.build_dir / "manifest.json"
        shutil.copy2(manifest_src, manifest_dst)

        # Copy assets if they exist
        assets_src = DXT_DIR / "assets"
        if assets_src.exists():
            assets_dst = self.build_dir / "assets"
            shutil.copytree(assets_src, assets_dst)
        else:
            print("⚠️ No assets directory found, creating placeholder")
            assets_dst = self.build_dir / "assets"
            assets_dst.mkdir(exist_ok=True)

            # Create a simple placeholder icon
            icon_content = """<!-- SVG placeholder icon -->
<svg width="64" height="64" xmlns="http://www.w3.org/2000/svg">
  <rect width="64" height="64" fill="#4CAF50"/>
  <text x="32" y="36" font-family="Arial" font-size="24"
        text-anchor="middle" fill="white">BC</text>
</svg>"""
            with open(assets_dst / "icon.svg", 'w') as f:
                f.write(icon_content)

        # Copy documentation files
        for doc_file in ["README.md", "LICENSE", "CHANGELOG.md"]:
            src_path = PROJECT_ROOT / doc_file
            if src_path.exists():
                shutil.copy2(src_path, self.build_dir / doc_file)

        print("✅ Manifest and assets copied")

    def create_launch_script(self):
        """Create a launch script that sets up Python path correctly."""
        print("🚀 Creating launch script...")

        # Create a Python launch script
        launch_script = self.build_dir / "launch.py"
        launch_content = '''#!/usr/bin/env python3
"""
Launch script for Beyond Compare MCP Server.
This script sets up the Python path to include bundled dependencies.
"""

import sys
import os
from pathlib import Path

# Get the directory containing this script
script_dir = Path(__file__).parent.absolute()

# Add dependencies to Python path
deps_dir = script_dir / "dependencies"
if deps_dir.exists():
    sys.path.insert(0, str(deps_dir))

# Add source directory to Python path
src_dir = script_dir / "src"
if src_dir.exists():
    sys.path.insert(0, str(src_dir))

# Set environment variables
os.environ.setdefault("PYTHONUNBUFFERED", "1")

# Import and run the main CLI
if __name__ == "__main__":
    try:
        from beyondcompare_mcp.cli import main
        sys.exit(main())
    except ImportError as e:
        print(f"Failed to import beyondcompare_mcp: {e}")
        print(f"Python path: {sys.path}")
        print(f"Script directory: {script_dir}")
        sys.exit(1)
'''
        with open(launch_script, 'w', encoding='utf-8') as f:
            f.write(launch_content)

        # Make executable on Unix systems
        if hasattr(os, 'chmod'):
            os.chmod(launch_script, 0o755)

        print("✅ Launch script created")

    def update_manifest_for_bundled_deps(self):
        """Update manifest.json to use the launch script."""
        print("🔧 Updating manifest for bundled dependencies...")

        manifest_path = self.build_dir / "manifest.json"
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        # Update the server configuration to use our launch script
        manifest["server"]["mcp_config"]["command"] = "python"
        manifest["server"]["mcp_config"]["args"] = ["launch.py"]
        manifest["server"]["mcp_config"]["cwd"] = "."

        # Update environment to not override paths
        env = manifest["server"]["mcp_config"]["env"]
        if "PYTHONPATH" in env:
            del env["PYTHONPATH"]  # We handle this in launch script

        # Add note about bundled dependencies
        manifest["_bundled_dependencies"] = True
        manifest["description"] += " (Includes bundled Python dependencies)"

        # Write updated manifest
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        print("✅ Manifest updated for bundled dependencies")

    def create_dxt_package(self) -> Path:
        """Create the final DXT package."""
        print("📦 Creating DXT package...")

        dxt_filename = f"{PACKAGE_NAME}-{PACKAGE_VERSION}.dxt"
        dxt_path = DIST_DIR / dxt_filename

        # Create ZIP file with .dxt extension
        with zipfile.ZipFile(dxt_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add all files from build directory
            for root, dirs, files in os.walk(self.build_dir):
                root_path = Path(root)
                for file in files:
                    file_path = root_path / file
                    arcname = str(file_path.relative_to(self.build_dir))
                    zf.write(file_path, arcname)

        print(f"✅ DXT package created: {dxt_path}")
        print(f"📊 Package size: {dxt_path.stat().st_size / 1024 / 1024:.2f} MB")

        return dxt_path

    def validate_package(self, dxt_path: Path):
        """Validate the created DXT package."""
        print("🔍 Validating DXT package...")

        # Check if it's a valid ZIP
        try:
            with zipfile.ZipFile(dxt_path, 'r') as zf:
                file_list = zf.namelist()

                # Check for required files
                required_files = [
                    "manifest.json",
                    "launch.py",
                    "src/beyondcompare_mcp/__init__.py",
                    "dependencies/"  # Should have dependencies folder
                ]

                missing_files = []
                for req_file in required_files:
                    found = any(f.startswith(req_file) for f in file_list)
                    if not found:
                        missing_files.append(req_file)

                if missing_files:
                    raise ValueError(f"Missing required files: {missing_files}")

                print(f"✅ Package validation passed ({len(file_list)} files)")

                # Show some statistics
                total_size = sum(zf.getinfo(name).file_size for name in file_list)
                print(f"📊 Total uncompressed size: {total_size / 1024 / 1024:.2f} MB")

        except zipfile.BadZipFile:
            raise ValueError("Created file is not a valid ZIP/DXT package")

    def build(self) -> Path:
        """Execute the complete build process."""
        print("🚀 Starting DXT build process...")
        print("=" * 50)

        self.clean_dist()
        self.validate_source()
        self.install_dependencies()
        self.copy_source_code()
        self.copy_manifest_and_assets()
        self.create_launch_script()
        self.update_manifest_for_bundled_deps()

        dxt_path = self.create_dxt_package()
        self.validate_package(dxt_path)

        print("=" * 50)
        print("🎉 Build completed successfully!")
        print(f"📦 DXT package: {dxt_path}")
        return dxt_path


def main():
    """Main entry point."""
    try:
        with DXTBuilder() as builder:
            dxt_path = builder.build()

            print("\n🎯 Next steps:")
            print(f"1. Test the package by dragging {dxt_path.name} to Claude Desktop")
            print("2. Check Claude Desktop's MCP settings to verify installation")
            print("3. Test the MCP tools in a Claude conversation")

            return 0

    except KeyboardInterrupt:
        print("\n⚠️ Build cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
