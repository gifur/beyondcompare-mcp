"""Tests for the intentionally small stdio MCP surface."""

import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from beyondcompare_mcp.server import BeyondCompareMCP


def test_prompts_and_resource_skill_are_kept_without_agentic_layer():
    package_dir = Path("src") / "beyondcompare_mcp"

    assert (package_dir / "prompts.py").exists()
    assert (package_dir / "skills.py").exists()
    assert not (package_dir / "agentic.py").exists()


def test_stdio_run_disables_fastmcp_banner():
    with patch.object(BeyondCompareMCP, "_find_bc_executable", return_value=Path("BCompare.exe")):
        server = BeyondCompareMCP()

    with patch.object(server.mcp, "run_stdio_async", new=AsyncMock()) as run_stdio:
        server.run()

    run_stdio.assert_awaited_once_with(show_banner=False)


def test_cli_version_writes_to_stdout():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")

    result = subprocess.run(
        [sys.executable, "-m", "beyondcompare_mcp.cli", "--version"],
        capture_output=True,
        text=True,
        timeout=10,
        env=env,
    )

    assert result.returncode == 0
    assert "Beyond Compare MCP Server v0.1.0" in result.stdout
