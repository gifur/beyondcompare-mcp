"""
Beyond Compare MCP Server Setup

A Model Context Protocol (MCP) server that provides file and directory comparison
capabilities using Beyond Compare.
"""

from pathlib import Path
from setuptools import setup, find_packages

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "Beyond Compare MCP Server for file and directory comparison"

# Read version from _version.py
version_path = Path(__file__).parent / "src" / "beyondcompare_mcp" / "_version.py"
version = "0.1.0"
if version_path.exists():
    with open(version_path, "r", encoding="utf-8") as f:
        exec(f.read())
        version = locals().get("__version__", "0.1.0")

setup(
    name="beyondcompare-mcp",
    version=version,
    author="Beyond Compare MCP Team",
    author_email="developer@example.com",
    description="Modern MCP server for Beyond Compare file and directory comparison",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sandraschi/beyondcompare-mcp",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "mcp>=1.12.4",
        "fastmcp>=2.11.3",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "anyio>=4.0.0",
        "structlog>=23.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.21.0",
            "pytest-mock>=3.11.0",
            "black>=23.9.0",
            "isort>=5.12.0",
            "mypy>=1.6.0",
            "ruff>=0.1.0",
            "types-python-dotenv>=1.0.0",
            "pre-commit>=3.4.0",
            "build>=1.0.0",
        ],
        "build": [
            "build>=1.0.0",
            "wheel>=0.41.0",
            "twine>=4.0.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.4.0",
            "mkdocstrings[python]>=0.23.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "beyondcompare-mcp=beyondcompare_mcp.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
        "Framework :: AsyncIO",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    keywords=[
        "mcp",
        "beyond-compare",
        "file-comparison",
        "directory-sync",
        "model-context-protocol",
    ],
    project_urls={
        "Homepage": "https://github.com/sandraschi/beyondcompare-mcp",
        "Documentation": "https://github.com/sandraschi/beyondcompare-mcp/docs",
        "Repository": "https://github.com/sandraschi/beyondcompare-mcp.git",
        "Issues": "https://github.com/sandraschi/beyondcompare-mcp/issues",
        "Changelog": "https://github.com/sandraschi/beyondcompare-mcp/blob/main/CHANGELOG.md",
    },
    include_package_data=True,
    zip_safe=False,
)
