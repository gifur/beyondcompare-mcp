"""Setup script for Beyond Compare MCP."""

import os
from setuptools import setup, find_packages

# Read the README for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="beyondcompare-mcp",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Beyond Compare MCP Server for FastMCP 2.10",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/beyondcompare-mcp",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "types-python-dotenv>=1.0.0",
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
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    keywords="beyond-compare mcp fastmcp file-comparison synchronization",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/beyondcompare-mcp/issues",
        "Source": "https://github.com/yourusername/beyondcompare-mcp",
    },
)
