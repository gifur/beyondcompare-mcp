# Beyond Compare MCP — Fleet unified gateway

**Canonical copy:** this file lives in `beyondcompare-mcp`. **MCP Central Docs** keeps a project summary at `mcp-central-docs/projects/beyondcompare-mcp/README.md` — update both when ports, env vars, or public HTTP paths change.

## Stack

- **FastMCP 3.2.x** with **`FastMCP.from_fastapi(app)`** (same pattern as `yahboom-mcp`): one process serves MCP streamable traffic and custom REST routes.
- **Python:** 3.12+ per `pyproject.toml`.
- **Beyond Compare:** 4+ (5 verified in the wild); auto-detect or `BEYOND_COMPARE_PATH`.

## Ports (fleet)

| Role | Port | Notes |
|------|------|--------|
| Vite dashboard | **10840** | `web_sota`; proxies `/api` and `/mcp` to 10841 |
| Gateway (uvicorn) | **10841** | FastAPI app: REST + MCP default path **`/mcp`** |

Override bind with `MCP_HOST`, `MCP_PORT`, `MCP_PATH` (see `beyondcompare_mcp.transport`).

## Start commands

**Gateway (HTTP + MCP):**

```text
uv run python -m beyondcompare_mcp.server --http --port 10841
```

**Stdio (Claude Desktop / Cursor):**

```text
uv run beyondcompare-mcp
```

**Dashboard (development):**

```text
cd web_sota
npm run dev
```

Open `http://127.0.0.1:10840`. Ensure the gateway is already listening on 10841.

## Public HTTP API

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/v1/health` | Liveness, BC executable detection, uptime, fleet hints |
| GET | `/api/capabilities` | Tool names (atomic + agentic) and endpoint map |
| GET | `/api/v1/logs` | Ring buffer of recent HTTP / lifecycle events |
| GET | `/api/v1/llm/settings` | In-process LLM prefs (defaults: Ollama) |
| POST | `/api/v1/llm/settings` | Set `model` / `provider` (JSON body) |
| GET | `/api/v1/llm/models` | Lists Ollama tags via `OLLAMA_BASE_URL` (default `http://127.0.0.1:11434`) |

## MCP surface

- **13 atomic tools** — compare, sync, multimedia, developer workspace (unchanged names).
- **Prompts** — `beyondcompare_quick_start`, `beyondcompare_backup_sync`, `beyondcompare_multimedia_inventory`.
- **Resource** — `skill://beyondcompare-mcp/SKILL.md` (markdown operator guide).
- **Agentic** — `beyondcompare_agentic_workflow` (uses `Context.sample` / SEP-1577 when the host supports it), `beyondcompare_sampling_hint`.

## Tests

- `just test` or `uv run python -m pytest tests -q --ignore=tests/test_integration.py`
- Gateway-focused: `tests/test_gateway.py` (uses a fake `BCompare.exe`).

## MCPB

Manifest lists new tools and `prompts_generated: true`. Re-pack with your usual `mcpb pack` workflow when publishing.
