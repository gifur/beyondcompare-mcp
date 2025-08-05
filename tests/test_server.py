"""
Tests for the Beyond Compare MCP server.

These tests verify the core functionality of the Beyond Compare MCP server.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from beyondcompare_mcp.server import BeyondCompareMCP, create_app
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
        # Create temporary directories for testing
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
        # Mock Beyond Compare executable
        self.mock_bc_path = "/fake/path/to/bcompare"
        
        # Create a test app
        self.app = create_app()
        self.client = TestClient(self.app)
    
    @patch("subprocess.run")
    def test_compare_files_identical(self, mock_run):
        """Test comparing identical files."""
        # Mock subprocess.run to simulate Beyond Compare
        mock_result = MagicMock()
        mock_result.returncode = 0  # No differences
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Create test server
        server = BeyondCompareMCP(bc_path=self.mock_bc_path)
        
        # Test comparing files
        left_file = str(self.left_dir / "test.txt")
        right_file = str(self.right_dir / "test.txt")
        
        result = server._compare_files(left_file, right_file)
        
        # Verify results
        self.assertTrue(result["success"])
        self.assertTrue(result["identical"])
        self.assertFalse(result.get("differences_found", True))
    
    @patch("subprocess.run")
    def test_compare_files_different(self, mock_run):
        """Test comparing different files."""
        # Mock subprocess.run to simulate Beyond Compare
        mock_result = MagicMock()
        mock_result.returncode = 1  # Differences found
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Create test server
        server = BeyondCompareMCP(bc_path=self.mock_bc_path)
        
        # Test comparing files
        left_file = str(self.left_dir / "different.txt")
        right_file = str(self.right_dir / "different.txt")
        
        result = server._compare_files(left_file, right_file)
        
        # Verify results
        self.assertTrue(result["success"])
        self.assertFalse(result["identical"])
        self.assertTrue(result["differences_found"])
    
    @patch("subprocess.run")
    def test_compare_folders(self, mock_run):
        """Test comparing folders."""
        # Mock subprocess.run to simulate Beyond Compare
        mock_result = MagicMock()
        mock_result.returncode = 1  # Differences found
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Create test server
        server = BeyondCompareMCP(bc_path=self.mock_bc_path)
        
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
        # Mock subprocess.run to simulate Beyond Compare
        mock_result = MagicMock()
        mock_result.returncode = 0  # Success
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Create test server
        server = BeyondCompareMCP(bc_path=self.mock_bc_path)
        
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
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "service": "beyondcompare-mcp"})
    
    @patch("beyondcompare_mcp.server.BeyondCompareMCP._find_bc_executable")
    def test_bc_not_found(self, mock_find):
        """Test behavior when Beyond Compare is not found."""
        # Mock _find_bc_executable to raise an exception
        mock_find.side_effect = BeyondCompareNotInstalledError()
        
        # This should raise an exception during initialization
        with self.assertRaises(BeyondCompareNotInstalledError):
            BeyondCompareMCP()
    
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
        
        # Create test server
        server = BeyondCompareMCP(bc_path=self.mock_bc_path)
        
        # Test error handling
        with self.assertRaises(BeyondCompareCommandError):
            server._compare_files("file1.txt", "file2.txt")


if __name__ == "__main__":
    unittest.main()
