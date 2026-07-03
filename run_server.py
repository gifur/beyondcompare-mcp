"""PyInstaller entry point."""
import _strptime  # noqa: F401
import os
import sys
sys.path.insert(0, "src")
import _strptime  # noqa: F401
import uvicorn
from beyondcompare_mcp.server import app
port = int(os.environ.get("PORT", os.environ.get("BEYONDCOMPARE_PORT", "10841")))
uvicorn.run(app, host="127.0.0.1", port=port)

