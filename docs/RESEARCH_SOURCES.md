# External References

Quick reference for agentic coding resources. For internal architecture, see [CLAUDE.md](../CLAUDE.md).

---

## Primary Source

| Repository | Relevance | Reference |
|:-----------|:----------|:----------|
| `anthropics/claude-code` | **Critical** | Primary orchestration runtime |

---

## Secondary Sources

| Repository | Focus Area |
|:-----------|:-----------|
| `github/copilot-cli` | Custom Agents, GitHub MCP |
| `microsoft/autogen` | Multi-agent orchestration |
| `CloudAI-X/claude-workflow-v2` | Community workflow patterns |
| `anthropics/skills` | Official SKILL.md standard |
| `muratcankoylan/Agent-Skills-for-Context-Engineering` | Context management patterns |

---

## Skill Endpoint Types

| Type | Host | Discovery |
|:-----|:-----|:----------|
| **Official** | Anthropic Servers | Pre-built, globally available (`pptx`, `xlsx`, `pdf`) |
| **Custom** | Local Filesystem | `~/.claude/skills/` or project `./skills/` |

---

## Official Claude Code Documentation

- [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)
- [Common Workflows](https://code.claude.com/docs/en/common-workflows.md)
- [Plugin Marketplaces](https://code.claude.com/docs/en/discover-plugins.md)
- [Hooks Reference](https://code.claude.com/docs/en/hooks.md)
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)
- [MCP Integration](https://code.claude.com/docs/en/mcp.md)
- [Plugin Development](https://code.claude.com/docs/en/plugins.md)
- [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)
- [Skills](https://code.claude.com/docs/en/skills.md)
- [Slash Commands](https://code.claude.com/docs/en/slash-commands.md)
- [Subagents](https://code.claude.com/docs/en/sub-agents.md)
