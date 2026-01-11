# Infrastructure Reference

> **📘 Official Docs:**
> - [Hooks reference](https://code.claude.com/docs/en/hooks) - Complete official hooks documentation
> - [MCP Integration](https://code.claude.com/docs/en/mcp) - Official Model Context Protocol guide
> - [Claude Code settings](https://code.claude.com/docs/en/settings) - Configuration reference

Integration details for Hooks, MCP, LSP, and Runtime configuration.

> **Note**: These are setup and integration details, not core philosophy. Refer here when configuring infrastructure, not when learning the framework.

---

## Hooks (Event Interception)

> **📘 Official Docs:** [Get started with Claude Code hooks](https://code.claude.com/docs/en/hooks-guide) - Quickstart guide with examples

Hooks are the **immune system** of the runtime—they intercept events for safety and compliance.

### Events & Types

| Event | When Fired | Use Case |
|:------|:----------|:---------|
| `SessionStart` | Claude starts/resumes | Setup, validation, env setup |
| `SessionEnd` | Session ends | Cleanup, persistence, logging |
| `UserPromptSubmit` | User sends message (before processing) | Input validation, rate limiting |
| `PreToolUse` | Before tool call | Safety checks, permission gates |
| `PermissionRequest` | Permission dialog shown | Auto-allow/deny |
| `PostToolUse` | After tool completes | Logging, validation |
| `Notification` | Claude Code notifications | Custom handling |
| `Stop` | Main agent finishes | Cleanup, persistence |
| `SubagentStop` | Subagent completes | Cleanup, validation |
| `PreCompact` | Before compact | Pre-compact checks |

**Hook Types:** `command` (exit codes, exit `2` = blocking) for fast checks. `prompt` (LLM JSON, `ok: false` = blocking) for complex validation.

**Event Matchers:** SessionStart (`startup`, `resume`, `clear`, `compact`), SessionEnd (`clear`, `logout`, `prompt_input_exit`, `other`), PreCompact (`manual`, `auto`), Notification (`permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`).

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
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/safety-check.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Prompt Hooks (JSON Protocol)

Prompt-based hooks use an LLM (Haiku) to evaluate actions and return structured JSON decisions.

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

**Configuration:**
```json
{
  "type": "prompt",
  "prompt": "Evaluate if action is safe: $ARGUMENTS",
  "timeout": 30
}
```

**Supported events:** All hook events, most useful for `Stop`, `SubagentStop`, `UserPromptSubmit`, `PreToolUse`, and `PermissionRequest`.

**Best for:** Complex, context-aware decisions that require understanding intent rather than simple rule-based checks.

### Environment Variables & Configuration Locations

| Variable | Purpose | Availability |
|:---------|:--------|:---------------|
| `$CLAUDE_PROJECT_DIR` / `${CLAUDE_PROJECT_DIR}` | Project root | All hooks |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin root | Plugin hooks only |
| `CLAUDE_ENV_FILE` | Persist env vars for session | SessionStart hooks only |

**SessionStart Persistence:** Write to `$CLAUDE_ENV_FILE` to persist env vars: `echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"`

| Location | Scope | File Path | Use Case |
|:---------|:------|:----------|:---------|
| **User** | Global | `~/.claude/settings.json` | Personal preferences |
| **Project** | Project-wide | `.claude/settings.json` | Team-shared hooks |
| **Local** | Project (private) | `.claude/settings.local.json` | Personal overrides |
| **Plugin** | Plugin-scoped | `plugins/*/hooks/hooks.json` or `plugin.json` | Plugin hooks |
| **Component** | Component-scoped | Skill/Agent/Command frontmatter | Component lifecycle |

**Component hooks:** Support `PreToolUse`, `PostToolUse`, `Stop`. Skills/Commands support `once: true`.

### Safety Standards

- **Always use `${CLAUDE_PLUGIN_ROOT}` in plugin paths** — prevents path traversal
- Use `$CLAUDE_PROJECT_DIR` or `${CLAUDE_PROJECT_DIR}` for project-relative paths
- **Validate all tool input parameters** (received via stdin as JSON)
- **Prevent directory traversal attacks** (`..` in paths)
- **Review hook security** — hooks run with your environment's credentials

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
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/safety-check.sh",
            "timeout": 30
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if file write is safe. Context: $ARGUMENTS. Return JSON with ok field.",
            "timeout": 30
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

**Installation:** CLI (`claude mcp add --transport http <name> <url>`) or `.mcp.json` config. Management: `claude mcp list/get/remove`, `/mcp` (in Claude Code).

**Configuration:** Project-scoped in `.mcp.json` at root. Env var expansion: `${VAR}` or `${VAR:-default}` (supported in `command`, `args`, `env`, `url`, `headers`).

**Transport Types:** HTTP (recommended, remote), SSE (deprecated), stdio (local processes).

**Installation Scopes:** Local (`~/.claude.json` per-project), Project (`.mcp.json`, shared), User (`~/.claude.json` global), Managed (system, enterprise). Precedence: Local > Project > User.

**Plugin MCP:** Bundle in `.mcp.json` at plugin root or inline in `plugin.json` via `mcpServers`. Changes require restart.

**Security:** Explicitly allow servers, avoid wildcard `*`, validate capabilities, review third-party servers, beware untrusted content.

**Capabilities:** `resources` (read-access), `tools` (executable functions), `prompts` (reusable templates). Dynamic updates via `list_changed` notifications.

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
| Large codebases | ✓ | Type safety critical |
| Complex refactoring | ✓ | Real-time error detection |
| Strong type systems | ✓ | Maximizes benefits |
| Simple scripts (<100 files) | ✗ | CLI linters sufficient |
| No type system | ✗ | Limited value |
| CLI linters adequate | ✗ | Simpler tooling |

---

## Runtime Configuration

Configure via settings files or environment variables.

### Configuration Scopes

Settings follow a hierarchical scope system (more specific overrides less specific):

| Scope | Location | Who It Affects | Shared |
|:------|:---------|:---------------|:-------|
| **Managed** | System directories | All users | Yes (IT deployed) |
| **Command line** | CLI arguments | Current session | No (temporary) |
| **Local** | `.claude/*.local.*` files | You (this project) | No (gitignored) |
| **Project** | `.claude/settings.json` | All collaborators | Yes (committed) |
| **User** | `~/.claude/settings.json` | You (all projects) | No |

### Settings Files

**Primary configuration:** `.claude/settings.json`

```json
{
  "model": "sonnet",
  "permissions": {
    "allow": ["Bash(git:*)"],
    "deny": ["Read(./.env)"]
  },
  "hooks": { ... },
  "env": {
    "NODE_ENV": "production"
  }
}
```

**Common settings:**
- `model` - Model alias or name (see Model Configuration)
- `permissions` - Tool permission rules
- `hooks` - Hook configurations
- `env` - Environment variables for sessions
- `enableAllProjectMcpServers` - Auto-approve project MCP servers

### Model Configuration

**Model aliases:**
- `default` - Recommended model for account type
- `sonnet` - Latest Sonnet (currently Sonnet 4.5)
- `opus` - Opus model (currently Opus 4.5)
- `haiku` - Fast, efficient Haiku model
- `sonnet[1m]` - Sonnet with 1M token context window
- `opusplan` - Uses Opus for planning, Sonnet for execution

**Configuration methods (priority order):**
1. `/model <alias|name>` - During session
2. `claude --model <alias|name>` - At startup
3. `ANTHROPIC_MODEL=<alias|name>` - Environment variable
4. `"model": "<alias|name>"` - In settings.json

**Model environment variables:**
- `ANTHROPIC_DEFAULT_OPUS_MODEL` - Model for `opus` alias
- `ANTHROPIC_DEFAULT_SONNET_MODEL` - Model for `sonnet` alias
- `ANTHROPIC_DEFAULT_HAIKU_MODEL` - Model for `haiku` alias
- `CLAUDE_CODE_SUBAGENT_MODEL` - Model for subagents

### Environment Variables

| Variable | Purpose | Example |
|:---------|:--------|:--------|
| `ANTHROPIC_BASE_URL` | API endpoint | `https://api.minimax.ai/v1` (for Z.ai/Minimax proxy) |
| `ANTHROPIC_API_KEY` | Authentication token | `sk-...` |
| `ANTHROPIC_MODEL` | Model alias or name | `opus` or `claude-sonnet-4-5-20250929-v1:0` |

### Common Proxy Configurations

| Provider | BASE_URL | Notes |
|:---------|:----------|:-------|
| Anthropic (default) | `https://api.anthropic.com` | Official endpoint |
| Z.ai | `https://api.minimax.ai/v1` | MiniMax proxy |
| Custom proxy | Your proxy URL | For internal/enterprise setups |

---

## Quick Reference

**Hook Exit Codes:** `0` = success (continues), `1` = non-blocking error (logs, continues), `2` = blocking error (stops with stderr).

**Environment Variables:** `${CLAUDE_PLUGIN_ROOT}` (plugin-relative), `$CLAUDE_PROJECT_DIR` / `${CLAUDE_PROJECT_DIR}` (project-relative).

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
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/safety-check.sh",
            "timeout": 30
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
