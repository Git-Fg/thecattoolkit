# Implementation Guide

This document provides practical implementation guidance. For complete component specifications and YAML schemas, see:
- [CLAUDE.md](../CLAUDE.md) - Core specifications
- [SKILL_FRONTMATTER_STANDARD.md](SKILL_FRONTMATTER_STANDARD.md) - Skill YAML schema

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
