"""FastAPI gateway and fleet REST endpoints."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from beyondcompare_mcp.server import app, reset_fleet_stack_for_tests


@pytest.fixture
def fake_bc_exe(tmp_path: Path) -> Path:
    p = tmp_path / "BCompare.exe"
    p.write_bytes(b"\x00\x00")
    return p


def test_health_and_capabilities(fake_bc_exe: Path, tmp_path: Path) -> None:
    reset_fleet_stack_for_tests()
    from beyondcompare_mcp.server import ensure_fleet_stack

    scripts = tmp_path / "bcscripts"
    scripts.mkdir()
    ensure_fleet_stack(bc_path=str(fake_bc_exe), scripts_dir=str(scripts))
    client = TestClient(app)
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "online"
    assert data["beyond_compare"]["detected"] is True
    assert "fleet" in data

    c = client.get("/api/capabilities")
    assert c.status_code == 200
    cap = c.json()
    assert cap["status"] == "ok"
    assert "beyondcompare_agentic_workflow" in cap["tool_surface"]["agentic"]

    logs = client.get("/api/v1/logs")
    assert logs.status_code == 200
    assert "entries" in logs.json()


def test_llm_settings_roundtrip(fake_bc_exe: Path) -> None:
    reset_fleet_stack_for_tests()
    from beyondcompare_mcp.server import ensure_fleet_stack

    sd = fake_bc_exe.parent / "scripts"
    sd.mkdir(parents=True, exist_ok=True)
    ensure_fleet_stack(bc_path=str(fake_bc_exe), scripts_dir=str(sd))
    client = TestClient(app)
    p = client.post("/api/v1/llm/settings", json={"model": "llama3", "provider": "ollama"})
    assert p.status_code == 200
    g = client.get("/api/v1/llm/settings")
    assert g.json().get("model") == "llama3"
