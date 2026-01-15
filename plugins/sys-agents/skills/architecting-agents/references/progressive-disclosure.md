# Progressive Disclosure for Agents

Design pattern that shows only essential information upfront and reveals more details only as needed.

## The Problem

Tool definitions overload context windows:
- GitHub MCP server: 35 tools, ~26K tokens
- More tools can confuse models (overlapping functionality)
- All loaded upfront = constant context overhead

## Disclosure Strategies by Layer

### Tool Calling Layer

**Index and Retrieve:**
1. Maintain lightweight index of tool capabilities
2. Use a search/retrieve tool to find relevant tools
3. Load full definition only when needed

**Example:**
```
Available: [file_ops, git_ops, search, ...] (short descriptions)
Agent decides: "I need git_ops"
Load: Full git_ops tool definition
```

### Shell Utilities Layer

**Manus Pattern:**
1. Provide list of available utilities in agent instructions
2. Agent uses bash to call `--help` to learn specifics
3. Full documentation loaded just-in-time

**Example:**
```
Instructions: "Available utilities: jq, ripgrep, fd, git, ..."
Agent needs jq: runs `jq --help`
Agent now has full jq knowledge
```

### MCP Servers Layer

**Cursor Pattern:**
1. Sync MCP tool descriptions to a folder
2. Give agent short list of available tools
3. Agent reads full description only when task matches

**Anthropic/Cloudflare Pattern:**
Similar indexed/on-demand loading for MCP management.

### Skills Layer

**Anthropic Skills Standard:**
1. Skills are folders containing SKILL.md files
2. YAML frontmatter is loaded into agent instructions (low cost)
3. Agent decides to read full SKILL.md only when needed (high cost)

```yaml
# Frontmatter (always loaded)
---
name: my-skill
description: "Does X. Use when Y."
---

# Full content (loaded on demand)
[Detailed instructions, references, etc.]
```

## Implementation Checklist

- [ ] Identify all action sources (tools, CLIs, MCPs, skills)
- [ ] Create lightweight index/description for each
- [ ] Design retrieval mechanism (explicit or pattern-based)
- [ ] Load full definitions only when task requires
- [ ] Track token savings from disclosure pattern

## Token Impact

| Approach | Cost |
|:---------|:-----|
| All tools loaded upfront | High (constant) |
| Progressive disclosure | Low (variable, task-dependent) |
| Typical savings | 50-80% reduction in baseline overhead |
