# Infrastructure (Hooks, MCP, LSP)

Connecting Claude to the outside world. This chapter covers technical integrations and the hybrid security model.

## 1. Hooks (The Nervous System)

Intercept and modify Claude's behavior.

### Hook Types
*   **`command` (Script):** Fast, deterministic. For regex validation or file checks.
*   **`prompt` (LLM):** Decision-making. "Is this safe?".
*   **`agent` (Complex):** Launches a validation agent.
    *   *Circularity Warning:* If a validation agent uses a tool that is itself hooked, infinite loop risk. The validation agent must use "out-of-band" tools (e.g., `Read` to validate `Write`).

### Critical Events
*   **`PreToolUse`:** The only time to change reality.
    *   Can return `updatedInput` to modify arguments (e.g., force absolute path) BEFORE execution.
*   **`PostToolUseFailure`:** Observer.
    *   CANNOT modify the result. Serves only to log or add a help `systemMessage`.
*   **`SubagentStop`:** Final quality control before letting the agent leave.

### Advanced Hook Options
*   **`once: true`:** The hook runs only ONE time per session.
    *   *Usage:* Initialization scripts (e.g., `check-dependencies.sh`).
    *   *Config:* Add `"once": true` in the hook definition object.

## 2. MCP (Model Context Protocol)

The bridge to external data (GitHub, Linear, Postgres).

### The Security Model (Warning!)
Unlike Bash scripts (which are Sandboxed), **local MCP servers launched by the plugin inherit the user's rights.**
*   They are NOT subject to the Sandbox.
*   They can access the network and system files.
*   *Responsibility:* You are responsible for the security of the MCP binary you distribute.

### Platform-Agnostic Configuration
Claude Code supports multiple API providers through environment configuration. See **CLAUDE.md Section 1.5** for complete details on provider-agnostic setup.

#### Local MCP Servers (Standard)
Use `${CLAUDE_PLUGIN_ROOT}` to point to your server scripts.

```json
{
  "sql-tools": {
    "command": "python",
    "args": ["${CLAUDE_PLUGIN_ROOT}/servers/sql_server.py"]
  }
}
```

#### Remote MCP Servers (HTTP/SSE)
Configure remote MCP services via URL endpoints:

```json
{
  "web-search": {
    "type": "http",
    "url": "https://api.z.ai/api/mcp/web_search_prime/mcp",
    "headers": {
      "Authorization": "Bearer ${Z_AI_API_KEY}"
    }
  }
}
```

### Z.AI Exclusive MCP Servers (Coding Plan Required)
Z.AI provides **4 exclusive MCP servers** available only to GLM Coding Plan subscribers:

#### 1. Vision MCP (`@z_ai/mcp-server`)
Local npm-based server for image/video understanding.

```bash
# Installation
claude mcp add -s user zai-mcp-server \
  --env Z_AI_API_KEY=your_key Z_AI_MODE=ZAI -- \
  npx -y "@z_ai/mcp-server"
```

**Capabilities:**
- `ui_to_artifact`: UI screenshots → code/specs
- `extract_text_from_screenshot`: OCR for text extraction
- `diagnose_error_screenshot`: Error analysis
- `understand_technical_diagram`: Architecture diagram interpretation
- `analyze_data_visualization`: Chart/dashboard analysis
- `ui_diff_check`: UI comparison
- `image_analysis`: General image understanding
- `video_analysis`: Video content analysis (≤8MB)

#### 2. Web Search MCP
Remote HTTP service for real-time web search.

```bash
claude mcp add -s user -t http web-search-prime \
  https://api.z.ai/api/mcp/web_search_prime/mcp \
  --header "Authorization: Bearer your_api_key"
```

**Tool:** `webSearchPrime` - retrieves titles, URLs, summaries, site info

#### 3. Web Reader MCP
Remote HTTP service for webpage content extraction.

```bash
claude mcp add -s user -t http web-reader \
  https://api.z.ai/api/mcp/web_reader/mcp \
  --header "Authorization: Bearer your_api_key"
```

**Tool:** `webReader` - extracts title, content, metadata, links

#### 4. ZRead MCP (GitHub Repository Q&A)
Remote HTTP service for open source repository analysis.

```bash
claude mcp add -s user -t http zread \
  https://api.z.ai/api/mcp/zread/mcp \
  --header "Authorization: Bearer your_api_key"
```

**Tools:**
- `search_doc`: Search documentation, code, comments
- `get_repo_structure`: Get directory structure and file lists
- `read_file`: Read complete code content

### MCP Server Type Comparison

| Type | Deployment | Security | Latency | Use Case |
|:-----|:-----------|:---------|:--------|:---------|
| **Local (stdio)** | User's machine | Sandboxed (user rights) | Low | Development tools, file access |
| **Remote (HTTP)** | Provider's server | Network-based auth | Medium | Cloud services, APIs |
| **Remote (SSE)** | Provider's server | Network-based auth | Medium | Streaming, real-time data |

## 3. LSP (Code Intelligence)

Transform Claude into an IDE.

*   **Unified Tool:** Configure `.lsp.json`, and Claude gains a unique `LSP` tool.
*   **Sub-tools:** `hover`, `goToDefinition`, `findReferences` are *operations* of the `LSP` tool.
*   **Inheritance:** Subagents inherit `LSP` by default.
*   **Best Practice:** Add a "Self-Check" step in your agents. If the LSP does not respond (server not installed by user), fallback to `Grep`.

## 4. Patterns (Cookbook)

### The "Ralph Wiggum" Pattern (Autonomous Loop)

**Problem:** Claude gives up too early or claims "I'm done" when tests are failing.
**Solution:** A feedback loop that blocks the exit until success criteria are met.

1.  **The State (`.local.md`):** Store iteration count and goal.
2.  **The Interceptor (`Stop` Hook):** A script that runs when Claude tries to exit.
3.  **The Gatekeeper:**
    *   Reads the `.local.md` state.
    *   Checks the transcript or project files for success (e.g., `tests_passed: true`).
    *   **If Failed:** Returns `decision: "block"` and sends the original prompt back as a `systemMessage` ("I'm not done. Fix the errors.").
    *   **If Success:** Returns `decision: "allow"` and deletes the state file.

