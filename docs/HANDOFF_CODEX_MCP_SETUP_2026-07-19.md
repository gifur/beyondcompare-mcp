# Handoff: Beyond Compare MCP Packaging and Codex Setup

Date: 2026-07-19
Repository: `D:\OpenSources\beyondcompare-mcp`

## Goal

The user asked to build/package a release of `beyondcompare-mcp`, understand the generated artifacts, and learn how to use this MCP server inside Codex.

## Completed Work

1. Built the MCPB package for Claude Desktop / MCP extension distribution.
   - Output: `D:\OpenSources\beyondcompare-mcp\dist\beyondcompare-mcp.mcpb`
   - Build command used from `mcpb\`:
     ```powershell
     npx --yes @anthropic-ai/mcpb pack . ..\dist\beyondcompare-mcp.mcpb
     ```
   - Manifest validation passed before packaging:
     ```powershell
     npx --yes @anthropic-ai/mcpb validate manifest.json
     ```
   - The MCPB pack command reported package version `0.1.0`, size about `50.4kB`, shasum `cc199cbd04521570a94c62c93333c383ffc243f5`.

2. Built Python distribution artifacts.
   - Outputs:
     - `D:\OpenSources\beyondcompare-mcp\dist\beyondcompare_mcp-0.1.0-py3-none-any.whl`
     - `D:\OpenSources\beyondcompare-mcp\dist\beyondcompare_mcp-0.1.0.tar.gz`
   - Build command:
     ```powershell
     python -m build
     ```

3. Verified package integrity.
   - `python -m zipfile --test dist\beyondcompare_mcp-0.1.0-py3-none-any.whl` returned `Done testing`.
   - `python -m zipfile --test dist\beyondcompare-mcp.mcpb` returned `Done testing`.
   - `python -m tarfile --test dist\beyondcompare_mcp-0.1.0.tar.gz` listed tar members successfully.

4. Explained artifact usage to the user.
   - `.mcpb`: for Claude Desktop / MCP extension install.
   - `.whl`: for pip installation in a Python environment.
   - `.tar.gz`: source distribution, mainly for source install, archival, or PyPI-style distribution.

5. Investigated how to wire this MCP into Codex.
   - Codex local config file found at:
     `C:\Users\guifa\.codex\config.toml`
   - Existing config already has a `[mcp_servers]` section and an example server entry for `node_repl`.
   - Recommended adding this entry:
     ```toml
     [mcp_servers.beyondcompare]
     command = "python"
     args = ["-m", "beyondcompare_mcp", "--stdio"]
     startup_timeout_sec = 120

     [mcp_servers.beyondcompare.env]
     PYTHONPATH = 'D:\OpenSources\beyondcompare-mcp\src'
     PYTHONUNBUFFERED = "1"
     MCP_STDIO_MODE = "true"
     BEYOND_COMPARE_PATH = 'C:\Program Files\Beyond Compare 5\BCompare.exe'
     BC_SCRIPTS_DIR = 'D:\OpenSources\beyondcompare-mcp\bc_scripts'
     ```
   - Alternative if installing the wheel first:
     ```powershell
     pip install D:\OpenSources\beyondcompare-mcp\dist\beyondcompare_mcp-0.1.0-py3-none-any.whl
     ```
     Then `PYTHONPATH` can usually be omitted from the Codex MCP config.

## Current State

- Release artifacts exist in `D:\OpenSources\beyondcompare-mcp\dist`.
- No source-code edits were made during packaging.
- `git status --short` was empty after the packaging work.
- The Codex config was read, but not edited. The user still needs either to add the MCP server block manually or ask the next agent to edit `C:\Users\guifa\.codex\config.toml`.

## Current Blockers / Open Items

1. Codex MCP server entry has not yet been installed into `config.toml`.
   - The prior response only gave the user the TOML block.
   - Next agent can add it if the user wants.

2. Codex has not been restarted after MCP configuration.
   - MCP server changes generally require a new Codex task or app restart before tools appear.

3. Actual tool discovery inside Codex has not yet been verified.
   - Expected tool names after restart are likely similar to:
     - `mcp__beyondcompare__compare_files`
     - `mcp__beyondcompare__compare_folders`
     - `mcp__beyondcompare__sync_folders`
   - Need verify in a fresh Codex session after config is applied.

4. Beyond Compare executable path was assumed.
   - Suggested path:
     `C:\Program Files\Beyond Compare 5\BCompare.exe`
   - If not present, check common alternatives:
     - `C:\Program Files\Beyond Compare 4\BCompare.exe`
     - `C:\Program Files (x86)\Beyond Compare 5\BCompare.exe`
     - `C:\Program Files (x86)\Beyond Compare 4\BCompare.exe`

## Pitfalls Encountered

1. Windows sandbox process launch failed initially.
   - Error: `CreateProcessAsUserW failed: 1312`
   - Workaround used: run read/build commands with `sandbox_permissions=require_escalated`.

2. `mcpb` was not installed globally.
   - `mcpb --version` failed.
   - `npx --version` worked.
   - Successful path was:
     ```powershell
     npx --yes @anthropic-ai/mcpb ...
     ```

3. `uv` was not available in PATH.
   - `uv --version` failed.
   - Python build was done with:
     ```powershell
     python -m build
     ```
   - Installed Python reported as `Python 3.14.4`; `build 1.5.0` was available.

4. Python build emitted setuptools warnings.
   - Warnings were about deprecated license metadata style and overwritten setuptools fields.
   - The build still succeeded.
   - These warnings do not block current artifact use, but are worth cleaning up before a polished release.

5. Official Codex manual helper failed to fetch current docs.
   - Command attempted:
     ```powershell
     node C:\Users\guifa\.codex\skills\.system\openai-docs\scripts\fetch-codex-manual.mjs
     ```
   - Failure: HTTP 403 on `https://developers.openai.com/codex/codex-manual.md`.
   - Workaround: inspect local `C:\Users\guifa\.codex\config.toml` to confirm MCP config shape.

6. `.mcpb` is not the right installation path for Codex.
   - `.mcpb` is mainly for Claude Desktop extension installation.
   - Codex uses `config.toml` MCP server entries.

## Recommended Next Steps

1. If the user wants Codex integration completed, edit:
   `C:\Users\guifa\.codex\config.toml`
   and add the `[mcp_servers.beyondcompare]` block shown above.

2. Confirm the Beyond Compare executable path exists.
   - If not, update `BEYOND_COMPARE_PATH` to the installed `BCompare.exe`.

3. Restart Codex or open a new Codex task.

4. Verify MCP tools appear.
   - Ask Codex to list available tools or attempt a simple comparison through `beyondcompare`.

5. Run a smoke test with two tiny files.
   - Create two small text files in the workspace.
   - Call `compare_files`.
   - Confirm the tool returns a structured dict with `success`, `message`, and comparison fields.

6. Optional cleanup before a formal release:
   - Modernize `pyproject.toml` license metadata to a SPDX string.
   - Decide whether `uv` should be installed or documented as required.
   - Consider installing `@anthropic-ai/mcpb` globally if frequent packaging is expected.

## Quick Commands Reference

Validate MCPB manifest:

```powershell
cd D:\OpenSources\beyondcompare-mcp\mcpb
npx --yes @anthropic-ai/mcpb validate manifest.json
```

Build MCPB:

```powershell
cd D:\OpenSources\beyondcompare-mcp\mcpb
npx --yes @anthropic-ai/mcpb pack . ..\dist\beyondcompare-mcp.mcpb
```

Build Python packages:

```powershell
cd D:\OpenSources\beyondcompare-mcp
python -m build
```

Install wheel locally:

```powershell
pip install D:\OpenSources\beyondcompare-mcp\dist\beyondcompare_mcp-0.1.0-py3-none-any.whl
```

Run server in stdio mode:

```powershell
$env:PYTHONPATH = 'D:\OpenSources\beyondcompare-mcp\src'
python -m beyondcompare_mcp --stdio
```

Run HTTP gateway:

```powershell
$env:PYTHONPATH = 'D:\OpenSources\beyondcompare-mcp\src'
python -m beyondcompare_mcp.server --http --port 10841
```
