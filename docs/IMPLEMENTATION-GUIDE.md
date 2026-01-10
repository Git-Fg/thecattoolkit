# Implementation Guide

This document provides practical implementation guidance. For complete component specifications and YAML schemas, see:
- [CLAUDE.md](../CLAUDE.md) - Core specifications
- [SKILL_FRONTMATTER_STANDARD.md](SKILL_FRONTMATTER_STANDARD.md) - Skill YAML schema

---

## Directory Structure

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Manifest (Required)
├── commands/                # Orchestration Workflows
├── agents/                  # Personas (System Prompts)
├── skills/                  # Capabilities (Forked Contexts)
├── hooks/                   # Lifecycle Automation
│   └── hooks.json
└── .mcp.json                # MCP Configuration
```

---

## Testing & Validation

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
# Verify frontmatter
grep -E "^---$" commands/*.md

# Check required fields
for file in commands/*.md; do
  if ! grep -q "description:" "$file"; then
    echo "Missing description: $file"
  fi
done
```

### Verify Skill Structure

```bash
# Check SKILL.md exists
find skills -name "SKILL.md" -type f

# Verify frontmatter
for skill in skills/*/SKILL.md; do
  if ! grep -q "name:" "$skill"; then
    echo "Missing name: $skill"
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
