#!/usr/bin/env python3
"""Test script to check MCP server functionality."""

import sys
import traceback

def test_basic_imports():
    """Test basic Python functionality."""
    try:
        print("✅ Python is working!")
        print(f"Python version: {sys.version}")
        return True
    except Exception as e:
        print(f"❌ Basic Python test failed: {e}")
        return False

def test_mcp_imports():
    """Test MCP-related imports."""
    try:
        import mcp
        print("✅ MCP package imported successfully")
        return True
    except ImportError as e:
        print(f"❌ MCP package not found: {e}")
        return False
    except Exception as e:
        print(f"❌ MCP import error: {e}")
        return False

def test_fastmcp_imports():
    """Test FastMCP imports."""
    try:
        import fastmcp
        print("✅ FastMCP package imported successfully")
        print(f"FastMCP version: {getattr(fastmcp, '__version__', 'unknown')}")
        return True
    except ImportError as e:
        print(f"❌ FastMCP package not found: {e}")
        return False
    except Exception as e:
        print(f"❌ FastMCP import error: {e}")
        return False

def test_server_import():
    """Test beyondcompare_mcp server import."""
    try:
        sys.path.insert(0, 'src')
        from beyondcompare_mcp.server import BeyondCompareMCP
        print("✅ BeyondCompare MCP server imported successfully")
        return True
    except ImportError as e:
        print(f"❌ BeyondCompare MCP server import failed: {e}")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"❌ Server import error: {e}")
        traceback.print_exc()
        return False

def test_server_instantiation():
    """Test server instantiation."""
    try:
        sys.path.insert(0, 'src')
        from beyondcompare_mcp.server import BeyondCompareMCP
        from beyondcompare_mcp.exceptions import BeyondCompareNotInstalledError
        
        try:
            server = BeyondCompareMCP()
            print("✅ Server instantiation successful (Beyond Compare found)")
            return True
        except BeyondCompareNotInstalledError:
            print("⚠️  Beyond Compare not found, but server instantiation code works")
            return True
    except Exception as e:
        print(f"❌ Server instantiation failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Beyond Compare MCP Server Dependencies...")
    print("=" * 60)
    
    tests = [
        ("Basic Python", test_basic_imports),
        ("MCP Package", test_mcp_imports),
        ("FastMCP Package", test_fastmcp_imports),
        ("Server Import", test_server_import),
        ("Server Instantiation", test_server_instantiation),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Testing: {test_name}")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MCP server is ready to work.")
        return 0
    else:
        print("💥 Some tests failed. Dependencies need to be installed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
