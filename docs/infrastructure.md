# Infrastructure Reference

Integration details for Hooks, MCP, LSP, and Runtime configuration.

> **Note**: These are setup and integration details, not core philosophy. Refer here when configuring infrastructure, not when learning the framework.

---

## Hooks (Event Interception)

Hooks are the **immune system** of the runtime—they intercept events for safety and compliance.

### Key Events

| Event | When Fired | Use Case |
|:------|:----------|:---------|
| `SessionStart` | Claude starts | Initial setup, validation |
| `UserPromptSubmit` | User sends message | Input validation, rate limiting |
| `PreToolUse` | Before tool call | Safety checks, permission gates |
| `PostToolUse` | After tool completes | Logging, result validation |
| `Stop` | Session ends | Cleanup, persistence |

### Hook Types

| Type | Communication | Blocking | Use When |
|:-----|:-------------|:---------|:---------|
| **command** | Exit codes + stdout/stderr | Exit code `2` = blocking error | Fast checks, scripts |
| **prompt** | LLM returns JSON | `ok: false` = blocks with reason | Complex validation, AI-based checks |

### Command Hooks (Exit Code Protocol)

**Exit codes:**
- `0` → Continue (success)
- `2` → **Blocking error** (standard block code)

**Exit code 2 behavior:**
- Only `stderr` is used as error message returned to Claude
- Can block the action depending on event (e.g., `PreToolUse` blocks tool call)
- JSON in `stdout` is **not** processed for exit code 2

**Example Command Hook:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/safety-check.sh"
          }
        ]
      }
    ]
  }
}
```

### Prompt Hooks (JSON Protocol)

**Response format:**
```json
{
  "ok": true  // or false to block
}
```

**When `ok: false`:**
```json
{
  "ok": false,
  "reason": "Explanation for why the action was blocked"
}
```

### Environment Variables

| Variable | Purpose | Usage |
|:---------|:--------|:------|
| `$CLAUDE_PROJECT_DIR` | Project root directory | Project-relative paths |
| `${CLAUDE_PROJECT_DIR}` | Project root directory | Alternative syntax |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin root directory | Portable plugin paths |

### Safety Standards

- **Always use `${CLAUDE_PLUGIN_ROOT}` in plugin paths** — prevents path traversal
- Use `$CLAUDE_PROJECT_DIR` or `${CLAUDE_PROJECT_DIR}` for project-relative paths
- **Validate all `TOOL_INPUT` parameters**
- **Prevent directory traversal attacks** (`..` in paths)

### Hook Configuration Example

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/safety-check.sh"
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if file write is safe. Return JSON with ok field."
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/init-check.sh"
          }
        ]
      }
    ]
  }
}
```

---

## MCP Integration

**MCP** (Model Context Protocol) connects external tools and APIs to Claude Code.

### Configuration: `.mcp.json`

```json
{
  "allowedMcpServers": [
    {
      "serverUrl": "https://approved-api.com/*",
      "capabilities": ["resources", "tools"]
    }
  ]
}
```

### Security Rules

| Rule | Why |
|:-----|:-----|
| Explicitly allow servers | Prevents unauthorized access |
| Avoid wildcard `*` | Limits attack surface |
| Validate capabilities | Ensures only intended features exposed |

### Common MCP Capabilities

| Capability | Description | Example Use |
|:-----------|:-------------|:------------|
| `resources` | Read-access to data sources | Database queries, file systems |
| `tools` | Executable functions | API calls, computations |
| `prompts` | Reusable prompt templates | Standardized interactions |

---

## LSP Integration

**LSP** (Language Server Protocol) provides real-time code intelligence: diagnostics, go-to-definition, hover info, completion.

### Configuration: `.lsp.json`

```json
{
  "lspServers": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "extensionToLanguage": {
        ".ts": "typescript",
        ".tsx": "typescript",
        ".js": "javascript"
      }
    }
  }
}
```

### Common LSP Servers

| Language | Server | Install Command |
|:---------|:--------|:----------------|
| TypeScript | `typescript-language-server` | `npm install -g typescript-language-server` |
| Python | `pyright-langserver` | `npm install -g pyright` |
| Rust | `rust-analyzer` | Included with Rust |
| Go | `gopls` | `go install golang.org/x/tools/gopls@latest` |
| HTML/CSS | `vscode-css-language-server` | `npm install -g vscode-css-language-server` |

### When to Use LSP

| Scenario | Use LSP? | Reason |
|:---------|:--------|:--------|
| Large codebases | ✓ | Type safety critical for navigation |
| Complex refactoring | ✓ | Real-time error detection prevents breakage |
| Strong type systems | ✓ | Maximizes language server benefits |
| Simple scripts | ✗ | Overhead exceeds benefit |
| No type system | ✗ | LSP provides limited value |
| CLI linters sufficient | ✗ | Simpler tooling adequate |

### LSP Decision Tree

```
Does project have a type system?
  ├─ No → Skip LSP, use CLI linters
  └─ Yes
      ├─ Is it a simple script (<100 files)?
      │   └─ Yes → CLI linters likely sufficient
      └─ No (large codebase)
          ├─ Need real-time diagnostics?
          │   ├─ Yes → Configure LSP
          │   └─ No → CLI tools adequate
          └─ Complex refactors planned?
              ├─ Yes → Configure LSP
              └─ No → CLI tools adequate
```

---

## Runtime Configuration

Configure via `.claude/settings.json` or environment variables.

### Environment Variables

| Variable | Purpose | Example |
|:---------|:--------|:--------|
| `ANTHROPIC_BASE_URL` | API endpoint | `https://api.minimax.ai/v1` (for Z.ai/Minimax proxy) |
| `ANTHROPIC_API_KEY` | Authentication token | `sk-...` |

### Configuration: `.claude/settings.json`

```json
{
  "baseUrl": "https://api.example.com/v1",
  "apiKey": "sk-..."
}
```

### Common Proxy Configurations

| Provider | BASE_URL | Notes |
|:---------|:----------|:-------|
| Anthropic (default) | `https://api.anthropic.com` | Official endpoint |
| Z.ai | `https://api.minimax.ai/v1` | MiniMax proxy |
| Custom proxy | Your proxy URL | For internal/enterprise setups |

---

## Quick Reference: Hook Exit Codes

| Exit Code | Meaning | Effect |
|:----------|:--------|:-------|
| `0` | Success | Continues execution |
| `1` | Non-blocking error | Logs warning, continues |
| `2` | Blocking error | Stops action with stderr message |

---

## Quick Reference: Environment Variables in Hooks

| Variable | Scope | Example |
|:---------|:------|:--------|
| `${CLAUDE_PLUGIN_ROOT}` | Plugin-relative | `${CLAUDE_PLUGIN_ROOT}/scripts/check.sh` |
| `$CLAUDE_PROJECT_DIR` | Project-relative | `$CLAUDE_PROJECT_DIR/.claude/hooks.json` |
| `${CLAUDE_PROJECT_DIR}` | Project-relative (alt) | `${CLAUDE_PROJECT_DIR}/src/main.ts` |

---

## Common Hook Patterns

### 1. Safety Check Before Tool Use
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/safety-check.sh"
          }
        ]
      }
    ]
  }
}
```

### 2. Session Initialization
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/init.sh"
          }
        ]
      }
    ]
  }
}
```

### 3. Logging After Tool Use
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/log-write.sh"
          }
        ]
      }
    ]
  }
}
```
