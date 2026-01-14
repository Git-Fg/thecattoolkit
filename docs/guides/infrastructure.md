# Infrastructure (Hooks, MCP, LSP)

Connecting Claude to the outside world. This chapter covers technical integrations and the hybrid security model.

## Quick Reference (Cat Toolkit Specific)

### 1. Hooks (The Nervous System)

Intercept and modify Claude's behavior.

#### Hook Types
*   **`command` (Script):** Fast, deterministic. For regex validation or file checks.
*   **`prompt` (LLM):** Decision-making. "Is this safe?".
*   **`agent` (Complex):** Launches a validation agent.
    *   *Crisis Warning:* Incurs ~20k token startup cost. Use only for complex, multi-step validation logic that requires distinct tool access.
    *   *Circularity Warning:* If a validation agent uses a tool that is itself hooked, infinite loop risk. The validation agent must use "out-of-band" tools (e.g., `Read` to validate `Write`).

#### Critical Events
*   **`PreToolUse`:** The only time to change reality.
    *   Can return `updatedInput` to modify arguments (e.g., force absolute path) BEFORE execution.
*   **`PostToolUseFailure`:** Observer.
    *   CANNOT modify the result. Serves only to log or add a help `systemMessage`.
*   **`SubagentStop`:** Final quality control before letting the agent leave.

#### Advanced Hook Options
*   **`once: true`:** The hook runs only ONE time per session.
    *   *Usage:* Initialization scripts (e.g., `check-dependencies.sh`).
    *   *Config:* Add `"once": true` in the hook definition object.

### 2. MCP (Model Context Protocol)

The bridge to external data (GitHub, Linear, Postgres).

#### The Security Model (Warning!)
Unlike Bash scripts (which are Sandboxed), **local MCP servers launched by the plugin inherit the user's rights.**
*   They are NOT subject to the Sandbox.
*   They can access the network and system files.
*   *Responsibility:* You are responsible for the security of the MCP binary you distribute.

#### Platform-Agnostic Configuration
Claude Code supports multiple API providers through environment configuration. See **CLAUDE.md Section 1.5** for complete details on provider-agnostic setup.

##### Local MCP Servers (Standard)
Use `${CLAUDE_PLUGIN_ROOT}` to point to your server scripts.

```json
{
  "sql-tools": {
    "command": "python",
    "args": ["${CLAUDE_PLUGIN_ROOT}/servers/sql_server.py"]
  }
}
```

##### Remote MCP Servers (HTTP/SSE)
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

#### Z.AI Exclusive MCP Servers (Coding Plan Required)
Z.AI provides **4 exclusive MCP servers** available only to GLM Coding Plan subscribers:

##### 1. Vision MCP (`@z_ai/mcp-server`)
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

##### 2. Web Search MCP
Remote HTTP service for real-time web search.

```bash
claude mcp add -s user -t http web-search-prime \
  https://api.z.ai/api/mcp/web_search_prime/mcp \
  --header "Authorization: Bearer your_api_key"
```

**Tool:** `webSearchPrime` - retrieves titles, URLs, summaries, site info

##### 3. Web Reader MCP
Remote HTTP service for webpage content extraction.

```bash
claude mcp add -s user -t http web-reader \
  https://api.z.ai/api/mcp/web_reader/mcp \
  --header "Authorization: Bearer your_api_key"
```

**Tool:** `webReader` - extracts title, content, metadata, links

##### 4. ZRead MCP (GitHub Repository Q&A)
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

#### MCP Server Type Comparison

| Type | Deployment | Security | Latency | Use Case |
|:-----|:-----------|:---------|:--------|:---------|
| **Local (stdio)** | User's machine | Sandboxed (user rights) | Low | Development tools, file access |
| **Remote (HTTP)** | Provider's server | Network-based auth | Medium | Cloud services, APIs |
| **Remote (SSE)** | Provider's server | Network-based auth | Medium | Streaming, real-time data |

### 3. LSP (Code Intelligence)

Transform Claude into an IDE.

*   **Unified Tool:** Configure `.lsp.json`, and Claude gains a unique `LSP` tool.
*   **Sub-tools:** `hover`, `goToDefinition`, `findReferences` are *operations* of the `LSP` tool.
*   **Inheritance:** Subagents inherit `LSP` by default.
*   **Best Practice:** Add a "Self-Check" step in your agents. If the LSP does not respond (server not installed by user), fallback to `Grep`.

### 4. Patterns (Cookbook)

#### The "Ralph Wiggum" Pattern (Autonomous Loop)

**Problem:** Claude gives up too early or claims "I'm done" when tests are failing.
**Solution:** A feedback loop that blocks the exit until success criteria are met.

1.  **The State (`.local.md`):** Store iteration count and goal.
2.  **The Interceptor (`Stop` Hook):** A script that runs when Claude tries to exit.
3.  **The Gatekeeper:**
    *   Reads the `.local.md` state.
    *   Checks the transcript or project files for success (e.g., `tests_passed: true`).
    *   **If Failed:** Returns `decision: "block"` and sends the original prompt back as a `systemMessage` ("I'm not done. Fix the errors.").
    *   **If Success:** Returns `decision: "allow"` and deletes the state file.

---

## Deep Dive: Universal Infrastructure Principles

> **Note:** This section contains comprehensive, framework-agnostic principles for infrastructure design. It extends beyond the Cat Toolkit-specific patterns above.

### Division I: Universal Hook Principles

#### Core Principles

Based on analysis of hooks across software, Git, frameworks, webhooks, and systems:

**1. Extensibility Without Modification**
- Design hooks as extension points, not implementation details
- Keep hook interfaces stable while implementations evolve
- Prefer configuration over code modification

**2. Intercept and Augment**
- Always provide pass-control equivalent (pass control to next handler)
- Support both augmentation (add behavior) and interception (prevent behavior)
- Make interception points explicit in documentation

**3. Separation of Concerns**
- Keep hook implementations focused and single-purpose
- Don't embed business logic in hook registration
- Use hooks for cross-cutting concerns (logging, security, validation)

**4. Performance Sensitivity**
- **Synchronous hooks**: Complete in milliseconds
- **Asynchronous hooks**: Queue immediately, acknowledge quickly
- Cache expensive computations
- Provide ways to disable hooks in production

**Performance Budgets**:
- UI hooks: < 1ms
- Git hooks: < 100ms
- Webhook processing: < 1s
- System hooks: Context-dependent

**5. Security Considerations Are Mandatory**
- Validate all inputs to hook implementations
- Authenticate hook callers (webhooks, callbacks)
- Authorize hook actions (registration, execution)
- Sanitize data passed to hooks
- Audit hook registration and execution
- Sandbox untrusted hook code when possible

**6. Error Handling Complexity**
- Use try-catch in hook handlers
- Implement graceful degradation
- Log hook failures with context
- Never let hooks crash the main system
- Provide timeout protection

**7. Lifecycle Management**
- Initialize hooks before use
- Clean up resources (unsubscribe, remove listeners)
- Handle re-initialization safely
- Manage hook state across lifecycle

#### Hook Taxonomy

##### By Scope

**In-Process Hooks**
- Shared memory space
- Direct function calls
- Synchronous execution
- Zero network overhead
- Examples: React useEffect, DOM event listeners, RxJS subscriptions

**Cross-Process Hooks**
- OS-mediated communication
- IPC mechanisms (pipes, sockets, shared memory)
- Platform-specific implementations
- Examples: Windows DLL injection, macOS method swizzling

**Network-Based Hooks**
- Asynchronous by nature
- Subject to network latency
- HTTP-based (typically POST)
- Examples: GitHub webhooks, Stripe notifications

##### By Timing

**Synchronous Hooks**
- Block execution until they complete
- Must be fast (< 1ms UI, < 100ms others)
- Failure blocks main operation
- Examples: Git pre-commit, React useEffect (blocking)

**Asynchronous Hooks**
- Do not block execution; return immediately
- Queue work for later processing
- Don't block main operation
- Examples: Git post-commit, webhooks, event listeners

##### By Purpose

**Monitoring/Observability**
- Log, measure, trace, profile
- Examples: Performance monitoring, logging interceptors

**Validation/Enforcement**
- Enforce rules, check constraints
- Examples: Git pre-commit, input validation, access control

**Transformation/Modification**
- Transform data or behavior
- Examples: Middleware, filters, data mappers

**Notification/Callback**
- Notify of events or state changes
- Examples: Webhooks, event listeners, observers

### Division II: Universal MCP Principles

#### Core Concepts

**Model Context Protocol (MCP)** is a standardized protocol for connecting AI models to external data sources and tools.

**Key Components**:
1. **MCP Client**: The AI system (Claude Code)
2. **MCP Server**: External service providing tools/resources
3. **Transport**: Communication layer (stdio, HTTP, SSE)
4. **Tools**: Callable functions provided by servers
5. **Resources**: Data sources exposed by servers

#### Universal Principles

**1. Capability Discovery**
- Servers expose available tools and resources
- Clients discover capabilities dynamically
- Version compatibility through capability negotiation

**2. Transport Agnosticism**
- Protocol works over multiple transports
- Servers can use stdio, HTTP, or SSE
- Clients transparently handle transport differences

**3. Security Boundaries**
- Local servers: Run with user's permissions
- Remote servers: Use authentication/authorization
- Never trust server output without validation
- Sandboxing where possible

**4. Error Resilience**
- Graceful degradation when servers fail
- Timeout protection for slow servers
- Clear error messages for debugging
- Fallback mechanisms for critical operations

**5. Performance Optimization**
- Minimize round trips
- Batch operations when possible
- Cache frequently accessed resources
- Use streaming for large responses

#### Server Types

**Local Servers (stdio)**
- Run on user's machine
- Full system access
- Low latency
- Best for: File access, development tools

**Remote Servers (HTTP)**
- Run on provider infrastructure
- Network-based authentication
- Medium latency
- Best for: Cloud services, APIs, data sources

**Remote Servers (SSE)**
- Server-Sent Events for streaming
- Real-time data push
- Medium latency
- Best for: Streaming data, notifications

#### Best Practices

**For Server Developers**:
- Provide comprehensive tool documentation
- Include validation for all inputs
- Support both batch and single operations
- Implement proper error handling
- Use descriptive tool names and descriptions
- Include examples in documentation

**For Client/Users**:
- Validate server security before installation
- Use authentication for remote servers
- Monitor server performance
- Implement timeout protection
- Have fallback mechanisms
- Keep servers updated

**For Plugin Authors**:
- Use `${CLAUDE_PLUGIN_ROOT}` for local servers
- Document all MCP dependencies
- Handle server failures gracefully
- Provide alternative implementations
- Test with multiple server configurations
- Include server health checks

### Division III: Common Patterns

#### Hook Patterns

**Validation Hook Pattern**
```markdown
Purpose: Validate before action
Timing: PreToolUse
Type: Synchronous
Example: Pre-commit validation, input checking
```

**Notification Hook Pattern**
```markdown
Purpose: Notify of events
Timing: Asynchronous
Type: Fire-and-forget
Example: Post-commit notifications, logging
```

**Transformation Hook Pattern**
```markdown
Purpose: Transform data or behavior
Timing: PreToolUse
Type: Synchronous with modification
Example: Path normalization, data sanitization
```

**State Management Hook Pattern**
```markdown
Purpose: Manage state across operations
Timing: Both pre and post
Type: Paired operations
Example: Session initialization/cleanup
```

#### MCP Integration Patterns

**Tool Provider Pattern**
- Server exposes domain-specific tools
- Client discovers and uses tools
- Examples: Database server, file system server

**Resource Provider Pattern**
- Server exposes data resources
- Client reads resources on demand
- Examples: Documentation server, API reference

**Streaming Provider Pattern**
- Server provides real-time data stream
- Client consumes stream incrementally
- Examples: Log streaming, live data feeds

**Hybrid Pattern**
- Server provides both tools and resources
- Clients use appropriate access method
- Most common for complex integrations

---

## Quick Reference Checklist

### Infrastructure Design Checklist

**Before deploying infrastructure components, verify:**

**Hooks**
- [ ] Clear purpose and timing defined
- [ ] Error handling implemented
- [ ] Performance budget established
- [ ] Security validation in place
- [ ] Lifecycle management configured
- [ ] Documentation complete

**MCP Servers**
- [ ] Transport type selected appropriately
- [ ] Security measures in place
- [ ] Error handling implemented
- [ ] Timeout protection configured
- [ ] Fallback mechanisms available
- [ ] Documentation and examples provided

**LSP Integration**
- [ ] Server configuration correct
- [ ] Fallback to grep implemented
- [ ] Tool access appropriately scoped
- [ ] Performance acceptable

**Security**
- [ ] Authentication configured
- [ ] Authorization rules defined
- [ ] Input validation implemented
- [ ] Audit logging enabled
- [ ] Sandboxing where appropriate
- [ ] Secret management configured
