"""
Tests for the Beyond Compare MCP server.

These tests verify the core functionality of the Beyond Compare MCP server.
"""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from beyondcompare_mcp.server import BeyondCompareMCP
from beyondcompare_mcp.config import settings
from beyondcompare_mcp.exceptions import (
    BeyondCompareCommandError,
    BeyondCompareNotInstalledError,
)


class TestBeyondCompareMCP(unittest.TestCase):
    """Test cases for the BeyondCompareMCP class."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        # Create temporary test directory
        cls.test_dir = Path(tempfile.mkdtemp(prefix="beyondcompare_mcp_test_"))
        cls.left_dir = cls.test_dir / "left"
        cls.right_dir = cls.test_dir / "right"

        # Create test directories
        cls.left_dir.mkdir()
        cls.right_dir.mkdir()

        # Create test files
        (cls.left_dir / "test.txt").write_text("Hello, World!")
        (cls.right_dir / "test.txt").write_text("Hello, World!")
        (cls.left_dir / "different.txt").write_text("This is different")
        (cls.right_dir / "different.txt").write_text("This is not the same")

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        shutil.rmtree(cls.test_dir, ignore_errors=True)

    def setUp(self):
        """Set up test case."""
        # Use real Beyond Compare executable path
        self.bc_path = "C:\\Program Files\\Beyond Compare 5\\BCompare.exe"

    @patch("subprocess.run")
    def test_compare_files_identical(self, mock_run):
        """Test comparing identical files."""
        # Mock subprocess.run to return success with no differences
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Create test server with real BC path
        server = BeyondCompareMCP(bc_path=self.bc_path)

        # Test comparing files
        left_file = str(self.left_dir / "test.txt")
        right_file = str(self.right_dir / "test.txt")

        result = server._compare_files(left_file, right_file)

        # Verify results
        self.assertTrue(result["success"])
        self.assertFalse(result.get("differences_found", False))

    @patch("subprocess.run")
    def test_compare_files_different(self, mock_run):
        """Test comparing different files."""
        # Mock subprocess.run to return success with differences
        mock_result = MagicMock()
        mock_result.returncode = 1  # Differences found
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Create test server with real BC path
        server = BeyondCompareMCP(bc_path=self.bc_path)

        # Test comparing files
        left_file = str(self.left_dir / "different.txt")
        right_file = str(self.right_dir / "different.txt")

        result = server._compare_files(left_file, right_file)

        # Verify results
        self.assertTrue(result["success"])
        self.assertTrue(result["differences_found"])

    def test_compare_files_missing_left(self):
        """Test comparing files when left file is missing."""
        # Create test server with real BC path
        server = BeyondCompareMCP(bc_path=self.bc_path)

        # Test comparing files with missing left file
        left_file = str(self.left_dir / "nonexistent.txt")
        right_file = str(self.right_dir / "test.txt")

        result = server._compare_files(left_file, right_file)

        # Verify results
        self.assertFalse(result["success"])
        self.assertIn("Left file not found", result["error"])

    def test_compare_files_missing_right(self):
        """Test comparing files when right file is missing."""
        # Create test server with real BC path
        server = BeyondCompareMCP(bc_path=self.bc_path)

        # Test comparing files with missing right file
        left_file = str(self.left_dir / "test.txt")
        right_file = str(self.right_dir / "nonexistent.txt")

        result = server._compare_files(left_file, right_file)

        # Verify results
        self.assertFalse(result["success"])
        self.assertIn("Right file not found", result["error"])

    @patch("subprocess.run")
    def test_compare_folders(self, mock_run):
        """Test comparing folders."""
        # Mock subprocess.run to return success with differences
        mock_result = MagicMock()
        mock_result.returncode = 1  # Differences found
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Create test server with real BC path
        server = BeyondCompareMCP(bc_path=self.bc_path)

        # Test comparing folders
        result = server._compare_folders(
            str(self.left_dir),
            str(self.right_dir),
            include_subfolders=True
        )

        # Verify results
        self.assertTrue(result["success"])

    @patch("subprocess.run")
    def test_sync_folders(self, mock_run):
        """Test synchronizing folders."""
        # Mock subprocess.run to return success
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Create test server with real BC path
        server = BeyondCompareMCP(bc_path=self.bc_path)

        # Test syncing folders
        result = server._sync_folders(
            str(self.left_dir),
            str(self.right_dir),
            sync_mode="mirror",
            dry_run=True
        )

        # Verify results
        self.assertTrue(result["success"])
        self.assertTrue(result["dry_run"])

    def test_sync_folders_invalid_mode(self):
        """Test sync with invalid mode."""
        # Create test server with real BC path
        server = BeyondCompareMCP(bc_path=self.bc_path)

        # Test syncing folders with invalid mode
        result = server._sync_folders(
            str(self.left_dir),
            str(self.right_dir),
            sync_mode="invalid",
            dry_run=True
        )

        # Verify results
        self.assertFalse(result["success"])
        self.assertIn("Invalid sync mode", result["error"])

    def test_bc_not_found(self):
        """Test behavior when Beyond Compare is not found."""
        # Use a fake path that doesn't exist
        fake_path = "C:\\fake\\path\\BCompare.exe"

        # This should raise an exception during initialization
        with self.assertRaises(BeyondCompareNotInstalledError):
            BeyondCompareMCP(bc_path=fake_path)

    @patch("subprocess.run")
    def test_command_error_handling(self, mock_run):
        """Test error handling for failed commands."""
        # Mock subprocess.run to raise an exception
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=2,  # Error code from Beyond Compare
            cmd="bcompare",
            output=b"Some error occurred",
            stderr=b"Detailed error message"
        )

        # Create test server with real BC path
        server = BeyondCompareMCP(bc_path=self.bc_path)

        # Test error handling - should return error result rather than raise
        result = server._compare_files("file1.txt", "file2.txt")

        # Verify error result
        self.assertFalse(result["success"])
        self.assertIn("error", result)

    def test_path_validation_security(self):
        """Test path validation prevents path traversal attacks."""
        server = BeyondCompareMCP(bc_path=self.bc_path)

        # Test that path traversal is rejected
        with self.assertRaises(ValueError):
            server._validate_path("../../../etc/passwd")

        # Test that normal paths work
        valid_path = server._validate_path(str(self.left_dir / "test.txt"))
        self.assertTrue(isinstance(valid_path, Path))

    def test_argument_validation_security(self):
        """Test that dangerous command line arguments are blocked."""
        server = BeyondCompareMCP(bc_path=self.bc_path)

        # Test dangerous characters are blocked
        self.assertFalse(server._is_safe_argument("file.txt; rm -rf /"))
        self.assertFalse(server._is_safe_argument("file.txt | cat /etc/passwd"))
        self.assertFalse(server._is_safe_argument("file.txt && malicious_command"))

        # Test normal arguments are allowed
        self.assertTrue(server._is_safe_argument("normal_file.txt"))
        self.assertTrue(server._is_safe_argument("/path/to/file.txt"))
        self.assertTrue(server._is_safe_argument("C:\\Windows\\file.txt"))

    def test_server_instantiation_with_auto_detect(self):
        """Test server can be created with auto-detection."""
        try:
            # This should work since BC 5 is installed
            server = BeyondCompareMCP()
            self.assertIsNotNone(server.bc_path)
            self.assertTrue(server.bc_path.exists())
        except BeyondCompareNotInstalledError:
            # If BC somehow isn't found, that's also a valid test result
            self.skipTest("Beyond Compare not found for auto-detection test")

    def test_mcp_integration(self):
        """Test MCP integration components."""
        server = BeyondCompareMCP(bc_path=self.bc_path)

        # Verify MCP instance exists
        self.assertIsNotNone(server.mcp)
        self.assertTrue(hasattr(server.mcp, 'tool'))

    def test_scripts_directory_creation(self):
        """Test that scripts directory is created."""
        # Use a custom scripts directory
        custom_scripts_dir = self.test_dir / "custom_scripts"
        server = BeyondCompareMCP(
            bc_path=self.bc_path,
            scripts_dir=str(custom_scripts_dir)
        )

        # Verify directory was created
        self.assertTrue(custom_scripts_dir.exists())
        self.assertTrue(custom_scripts_dir.is_dir())


if __name__ == "__main__":
    unittest.main()
