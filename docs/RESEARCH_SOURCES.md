# Research: Agentic & Skill-Based Repositories

This document lists repositories investigated via DeepWiki that are relevant to building a marketplace, skill, or plugin architecture for `thecattoolkit`. These repositories represent the state-of-the-art in 2026 for agentic coding tools.

## Primary Targets

### 1. Claude Code
- **Repository**: `anthropics/claude-code`
- **Relevance**: **Critical**. Primary orchestration runtime.
- **Native Agentic Capacities**:
  - **Commands**: Native slash commands defined in `commands/`.
  - **Agents**: Specialized "personas" (prompts + tools) defined in `agents/`.
  - **Skills**: Filesystem-based reusable instructions in `skills/`.
  - **Hooks**: Native lifecycle event system (`hooks.json`).
  - **MCP Integration**: Native support for Model Context Protocol servers.


## Secondary Targets

### 2. GitHub Copilot CLI
- **Repository**: `github/copilot-cli`
- **Relevance**: **Medium**. Focuses more on "Custom Agents" and GitHub-specific integrations.
- **Key Capabilities**:
  - **Custom Agents**: Support for defining custom agent workflows (`3.6 Custom Agents`).
  - **GitHub MCP**: specialized MCP tools for GitHub (`4.2 GitHub MCP Tools`).
  - **Permission Model**: Strong focus on user approval and permissions (`3.5 Tool Execution & Permissions`).

### 5. Microsoft AutoGen (AgentsAI)
- **Repository**: `microsoft/autogen`
- **Relevance**: **Medium**. Focuses on multi-agent orchestration rather than single-agent CLI dominance, but valuable for "Team" concepts.
- **Key Capabilities**:
  - **Multi-Agent Teams**: Orchestration of multiple agents (`4 Multi-Agent Teams`).
  - **Agent Runtime**: Core runtime for agent execution (`2.1 Agent Runtime System`).
  - **Code Execution**: Sandboxed code execution patterns (`6.1 Code Execution`).



## External Tool & Community References

### 6. CloudAI-X/claude-workflow-v2
- **Repository**: `CloudAI-X/claude-workflow-v2`
- **Relevance**: **High**. A community-driven implementation of complex workflows.
- **Key Insights**: Provides patterns for `agents/`, `skills/`, and `hooks/` directory structures that mimic native behaviors.

### 7. Anthropic Skills
- **Repository**: `anthropics/skills`
- **Relevance**: **Critical**. The definitive source for "Skill" definitions.
- **Key Specs**:
  - **SKILL.md Standard**: Defines the official format (YAML frontmatter + Markdown body).
  - **Progressive Disclosure**: Best practices for linking external references to keep context light.

### 8. Context Engineering Skills
- **Repository**: `muratcankoylan/Agent-Skills-for-Context-Engineering`
- **Relevance**: **Medium**. Focuses on context management patterns.

## Official vs. Custom Skill Endpoints

Based on recent investigations, skills are divided into two main categories:

### 1. Official Skills (Anthropic-Managed)
- **Host**: Anthropic Servers.
- **Discovery**: Pre-built and available globally (e.g., `pptx`, `xlsx`, `pdf`).
- **Endpoint**: Integrated into the core Messages API/Claude.ai without configuration.
- **Execution**: Runs in Anthropic's managed environment.

### 2. Custom Skills (User-Defined)
- **Host**: Local Filesystem (Claude Code) or User-Managed API.
- **Structure**: `SKILL.md` (metadata frontmatter + instructions).
- **Endpoint**:
  - **Local**: `~/.claude/skills/` or project `./skills/`. Auto-discovered by CDE.
  - **API**: Uploaded to `/v1/skills` (returns a `skill_id`). Requres specific Beta headers.
- **Execution**: Uses the `code execution tool` to run scripts within the assigned context.

## Investigation Outcomes

Detailed architectural specifications have been compiled into **[`docs/ARCHITECTURE_REFERENCE.md`](docs/ARCHITECTURE_REFERENCE.md)**.

The investigation focused on:
1. **Architecture**: `anthropics/claude-code`, `CloudAI-X/claude-workflow-v2`
2. **Skills Standard**: `anthropics/skills`

### Additional Findings
- **Marketplace Standard**: The `marketplace.json` and `plugin.json` schemas have been defined in **[`docs/MARKETPLACE_REFERENCE.md`](docs/MARKETPLACE_REFERENCE.md)**.
- **Registry Pattern**: Confirmed the use of `plugin.json` for individual packages and `marketplace.json` for aggregation.
- **Universal Frontmatter**: The cross-platform specification for `SKILL.md` is defined in **[`docs/SKILL_FRONTMATTER_STANDARD.md`](docs/SKILL_FRONTMATTER_STANDARD.md)**.

---

## Official Claude Code Documentation

- [Changelog](https://raw.githubusercontent.com/anthropics/claude-code/refs/heads/main/CHANGELOG.md)
- [CLI reference](https://code.claude.com/docs/en/cli-reference.md)
- [Common workflows](https://code.claude.com/docs/en/common-workflows.md)
- [Plugin Marketplaces](https://code.claude.com/docs/en/discover-plugins.md)
- [Headless Usage](https://code.claude.com/docs/en/headless.md)
- [Hooks Reference](https://code.claude.com/docs/en/hooks.md)
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide.md)
- [MCP Integration](https://code.claude.com/docs/en/mcp.md)
- [Plugin Marketplaces Development](https://code.claude.com/docs/en/plugin-marketplaces)
- [Create Plugins](https://code.claude.com/docs/en/plugins.md)
- [Plugins Reference](https://code.claude.com/docs/en/plugins-reference.md)
- [Quickstart](https://code.claude.com/docs/en/quickstart.md)
- [Agent Skills](https://code.claude.com/docs/en/skills.md)
- [Slash Commands](https://code.claude.com/docs/en/slash-commands.md)
- [Status Line Configuration](https://code.claude.com/docs/en/statusline.md)
- [Subagents](https://code.claude.com/docs/en/sub-agents.md)

