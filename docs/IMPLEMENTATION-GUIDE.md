# Implementation Guide

Practical implementation guidance for the toolkit, including validation scripts, MCP configuration, and endpoint adaptation rules.

---

## Validation Scripts

### Toolkit Lint (Comprehensive)

```bash
./scripts/toolkit-lint.sh
```

Validates all components: Skills, Commands, Agents, Hooks.

### Validate hooks.json

```bash
python3 plugins/meta/skills/manage-hooks/assets/scripts/hook-tester.py hooks.json
```

**Checks:**
- Valid hook events
- Required fields present
- JSON syntax
- Matcher patterns

### Check Command Structure

```bash
grep -E "^---$" commands/*.md

for file in commands/*.md; do
  if ! grep -q "description:" "$file"; then
    echo "Missing description: $file"
  fi
done
```

---

## Configuration Scopes

| Scope | Location | Use Case |
|:---|:---|:---|
| **User** | `~/.claude/settings.json` | Global preferences. |
| **Project** | `.claude/settings.json` | Team standards. |
| **Plugin** | `.claude-plugin/plugin.json` | Distributable logic. |

---

## Plugin Portability Principle

Each plugin in the marketplace is a **standalone unit**. While plugins in the same workspace can collaborate, they must also work independently.

### Intra-Plugin Collaboration ✅
Components within the same plugin can freely reference each other:
- Agents reference skill scripts via `skills` field or natural language instructions
- Skills specify `agent: [agent-name]` for forked execution
- Commands call `Skill(/skill-name)` for orchestration

### Cross-Plugin Coupling ❌
Never create hard dependencies between plugins:
- Don't use relative paths like `../other-plugin/scripts/tool.sh`
- Don't assume another plugin's internal structure
- Use natural language: "from the [skill-name] skill if available"

### Skill Invocation Priority

| Mechanism | When to Use |
|:----------|:------------|
| `context: fork` | Skill needs isolated context (default for atomic tasks) |
| `Skill(/name)` | Command/agent orchestrating multiple skills |
| `skills: [name]` | Agent needs skill's knowledge, not execution |

> [!TIP]
> Manual `Skill()` loading is valid and often necessary. The key is choosing the right mechanism for the task.

---

## MCP Configuration

### MCP Servers (`.mcp.json`)
Manage external tools (Database, Browser, etc.).

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://..."]
    }
  }
}
```

### MCP Security (Critical)

```yaml
# ✅ Good: Specific domain restrictions
allowedMcpServers:
  - serverUrl: "https://api.githubcopilot.com/mcp/"
  - serverUrl: "https://mcp.company.com/api/*"
  - serverCommand: ["npx", "-y", "@company/approved-package"]

# ❌ Bad: Wildcard access
allowedMcpServers:
  - serverUrl: "*"
```

---

## Environment Configuration

Configure the runtime environment for different providers:

| Variable | Purpose | Example |
|:---------|:--------|:--------|
| `ANTHROPIC_BASE_URL` | API endpoint (Zai, Minimax proxy) | `https://api.zai.com/v1` |
| `ANTHROPIC_API_KEY` | Authentication token | `sk-...` |

Ensure `.claude/settings.json` reflects the chosen provider's capabilities.

---

## Endpoint Adaptation Rules

The toolkit supports multiple agentic endpoints. Adjust behavior based on the active runtime:

### Optimization Strategy by Endpoint

| Endpoint | Optimization Strategy |
|:---------|:----------------------|
| **Anthropic (Claude)** | Full capability: large context (200k+), native `Task`/`Skill` tools |
| **Zai (GLM-4.x)** | Leverage native function calling. Vision tasks use `GLM-4.6V`. |
| **Minimax (M2)** | Prioritize **Parallel Agent Pattern** due to fast inference. Excellent for multi-file context edits. |

### Behavioral Adaptation Rules

1. **Context Window:** If limited → increase delegation frequency
2. **Vision Model:** If available → use skill-based image analysis
3. **Inference Speed:** If fast → prefer parallel agent spawning over sequential

For endpoint-specific technical details (API specs, proxy configuration), see **[ARCHITECTURE_REFERENCE.md](ARCHITECTURE_REFERENCE.md)**.
