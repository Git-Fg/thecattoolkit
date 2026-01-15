# Claude Code Plugins — Stable Patterns

Plugins provide extensibility for Claude Code through five component types: commands, agents, skills, hooks, MCP servers, and LSP servers.

## Architecture Overview

### Stable Structure
```
plugin/
├── .claude-plugin/plugin.json  # Required manifest
├── commands/                    # Slash commands (Markdown)
├── agents/                      # Subagents (Markdown)
├── skills/                      # Agent Skills (SKILL.md files)
├── hooks/hooks.json            # Hook configurations
├── .mcp.json                   # MCP server definitions
└── .lsp.json                   # LSP server definitions
```

**Core principle**: Components live at plugin root, only manifest lives in `.claude-plugin/`.

## Core Components

### Commands (Slash Commands)

**Pattern**: Markdown files with frontmatter
```yaml
---
description: Brief description for discovery
---

# Command Name

## Usage
/command-name [arguments]

## Description
What this command does and when to use it
```

**Stable requirements**:
- Must be in `commands/` directory at root
- File name determines command name (minus .md)
- Description used for discovery

### Agents (Subagents)

**Pattern**: Markdown files describing specialized agents
```yaml
---
description: What this agent specializes in
capabilities: ["task1", "task2"]
---

# Agent Name

## Capabilities
- Specific task the agent excels at
- Another specialized capability

## Context
When to use this agent vs built-in options
```

### Skills (Agent Skills)

**Pattern**: Directories with SKILL.md files
```
skills/
├── skill-name/
│   ├── SKILL.md           # Required: YAML frontmatter + instructions
│   ├── reference.md       # Optional: additional docs
│   └── scripts/           # Optional: executable helpers
```

**Progressive disclosure pattern**:
1. **Level 1** (metadata): `name` + `description` from YAML frontmatter
2. **Level 2** (instructions): SKILL.md body loaded when triggered
3. **Level 3** (resources): Bundled files executed via bash as needed

### Hooks

**Pattern**: Event-driven automation
```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command|prompt",
            "command": "script.sh",
            "prompt": "Evaluation prompt"
          }
        ]
      }
    ]
  }
}
```

### MCP Servers

**Pattern**: External tool integration
```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable",
      "args": ["arg1", "arg2"],
      "env": {
        "VAR": "value"
      }
    }
  }
}
```

## Plugin Manifest (plugin.json)

### Required Fields
- `name`: Unique identifier (kebab-case)

### Common Fields
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief description",
  "commands": ["./custom/commands/"],
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": "./hooks.json",
  "mcpServers": "./.mcp.json",
  "lspServers": "./.lsp.json"
}
```

**Path rules**:
- Custom paths supplement default directories
- All paths must be relative and start with `./`
- Multiple paths allowed as arrays

## Installation Scopes

| Scope | Settings File | Purpose |
|-------|--------------|---------|
| `user` | `~/.claude/settings.json` | Personal plugins (default) |
| `project` | `.claude/settings.json` | Team plugins (version controlled) |
| `local` | `.claude/settings.local.json` | Local plugins (gitignored) |
| `managed` | `managed-settings.json` | Admin-managed (read-only) |

## Caching & Portability

### How Caching Works
1. Plugin files copied to cache directory on install
2. Paths outside plugin root NOT copied
3. Plugins run from cache, not original location

### Portable Path Pattern
**Always use `${CLAUDE_PLUGIN_ROOT}`** environment variable:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

**Why**: Ensures scripts work regardless of cache location.

## Stable Design Principles

### 1. Separation of Concerns
- Manifest defines structure
- Components implement behavior
- Scripts provide execution

### 2. Progressive Disclosure
- Load metadata at startup (~100 tokens)
- Load instructions on trigger (<5k tokens)
- Access resources via bash (unlimited)

### 3. Security First
- Plugin root is read-only (enforced by caching)
- Scripts execute with plugin permissions
- Hooks can validate/modify behavior

### 4. Composability
- Plugins can provide multiple component types
- Components can reference each other
- Hooks can coordinate across components

## Common Patterns

### Command Orchestration Pattern
```yaml
# commands/deploy.md
---
description: Orchestrate deployment workflow
---

# Deploy

Usage: /deploy [environment]

Orchestrates the deployment process:
1. Validates environment
2. Runs pre-deploy hooks
3. Executes deployment
4. Runs post-deploy verification
```

### Hook Validation Pattern
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-changes.sh"
          }
        ]
      }
    ]
  }
}
```

### Skill Progressive Disclosure
```yaml
# skills/code-reviewer/SKILL.md
---
name: code-reviewer
description: Automated code quality and security reviews
---

# Code Reviewer Skill

## Quick Start
Use for reviewing code changes:
- /code-reviewer --scan-changed-files
- /code-reviewer --full-audit

## For Advanced Use
See [ADVANCED.md](reference.md) for:
- Custom rule configuration
- Integration with security tools
- CI/CD integration
```

## Anti-Patterns (Avoid)

❌ **Absolute paths**: Breaks in cache
❌ **External file references**: Not copied during install
❌ **Hardcoded locations**: Won't work across scopes
❌ **Circular hook dependencies**: Causes deadlocks
❌ **No validation hooks**: Risk of errors
❌ **Monolithic SKILL.md**: Violates progressive disclosure

## Verification Checklist

Before distributing a plugin:

- [ ] All paths use relative references starting with `./`
- [ ] Scripts use `${CLAUDE_PLUGIN_ROOT}` for absolute paths
- [ ] Components separated by type (commands/, agents/, etc.)
- [ ] SKILL.md files follow progressive disclosure
- [ ] Hooks have validation logic
- [ ] No hardcoded usernames/paths
- [ ] Version follows semantic versioning (MAJOR.MINOR.PATCH)
- [ ] Description is clear and actionable
- [ ] All scripts are executable
- [ ] Hooks handle errors gracefully

## Debugging Patterns

### Enable Debug Mode
```bash
claude --debug
```

Shows:
- Plugin loading status
- Component registration
- Hook execution
- Error messages

### Common Issues
| Symptom | Cause | Solution |
|---------|-------|----------|
| Plugin not loading | Invalid JSON | Validate with `claude plugin validate` |
| Commands missing | Wrong directory | Must be at root, not in `.claude-plugin/` |
| Hooks not firing | Script not executable | `chmod +x script.sh` |
| MCP failing | Missing env vars | Use `${CLAUDE_PLUGIN_ROOT}` |
| Path errors | Absolute paths | Convert to relative paths |

## Security Considerations

### Read-Only Root
- Plugin directory is read-only at runtime
- Caching enforces isolation
- Scripts cannot modify plugin files

### Permission Model
- Scripts inherit user's permissions
- Hooks run with plugin's context
- Network access follows user's settings

### Best Practices
1. Validate all inputs in hooks
2. Use absolute paths via environment variables
3. Log security-relevant events
4. Provide audit trails
5. Follow principle of least privilege

## Volatile Details (Look Up)

These change frequently - verify in latest docs:
- Exact plugin.json field names
- Hook event schemas (input/output)
- MCP server protocol versions
- LSP server configurations
- Command flag names

**Always check**: Use `curl -sL URL.md | rg pattern` before implementation.

---

## Official Documentation Links

- **Plugin Components Reference**: https://code.claude.com/docs/en/plugins-reference.md
- **Hooks Reference**: https://code.claude.com/docs/en/hooks.md
- **Settings & Configuration**: https://code.claude.com/docs/en/settings.md
- **Claude Code Overview**: https://code.claude.com/docs/en/overview
- **Setup Guide**: https://code.claude.com/docs/en/setup

### Verification
Last verified: 2026-01-13
