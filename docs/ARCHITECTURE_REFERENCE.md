# Architecture Reference: Agentic Marketplaces & Skills

This document contains the deep technical specifications extracted from the investigation of `anthropics/claude-code`. It serves as the blueprint for our implementation.

## 1. Native Extensibility Architecture (Reference: Claude Code)

### Directory Structure
Claude Code enables extensibility via a structured directory layout that the runtime auto-discovers.

```tree
plugin-name/
├── commands/                # Custom Slash Commands (.md)
├── agents/                  # Specialized Agents (prompts + config)
├── skills/                  # Reusable Agent Skills (SKILL.md)
├── hooks/                   # Lifecycle Automation
│   └── hooks.json           # Event-to-Script mappings
└── README.md                # Documentation
```

### Discovery & Registration
Extensibility is driven by **Auto-Discovery** rather than a centralized registry:
- **Project-Level**: `.claude/` directory in repo root.
- **User-Level**: `~/.claude/` global directory.
- **Skill Matching**: The runtime pre-loads `description` frontmatter for semantic intent matching.

## 2. Agent System & Modes

### Agent Definition (Claude Code / Copilot CLI)
Agents are distinct from generic LLM sessions. They are specialized "personas" or "workers".
- **Source**: Defined in `agents/` directory.
- **Components**:
  - **Prompt/System Message**: Specialized instructions.
  - **Tools**: Allowlist of tools (e.g., `Glob`, `Grep`, `BashOutput`).
  - **Subagents**: Ability to spawn other agents for parallel tasks.


## 3. Skill System (Cross-Reference)

Claude Code uses a standardized Markdown format for Skills. This is the **recommended standard** for our project.

### Anatomy of a Skill (Standard: Universal Superset)
**File**: `SKILL.md`

**Endpoint Classification**:
- **Official**: Pre-built (e.g., `pptx`, `pdf`). Managed by Anthropic.
- **Custom**: User-defined. Loaded via filesystem (CLI) or `/v1/skills` (API).

**Format Specification**:
```yaml
---
name: pdf-processing  # Max 64 chars, lowercase, hyphens only
description: Extract text and tables from PDF files.
allowed-tools: [Read, Write, Bash]  # Restrict tools during skill execution
---
```
# PDF Processing

[Detailed instructions for the LLM on how to perform the skill...]

## Advanced Usage
See [API Reference](reference.md) for detailed schemas.

### Best Practices
*   **Progressive Disclosure**: Keep `SKILL.md` under 500 lines. Move heavy schemas/tables to `reference.md` or `examples.md` and link them. The Agent will read them only if needed.
*   **Intent Matching**: The `description` frontmatter is pre-loaded. It must clearly state *capabilities* and *when to use* the skill.
*   **Scripts**: Supporting scripts (e.g., Python parsers) should reside in a `scripts/` subdirectory.

## 4. Hook System (Event-Driven Architecture)

Claude Code implements an "Interception" model for Hooks.

### Triggers
- `SessionStart`: Initialize environment or inject context.
- `UserPromptSubmit`: Validate or modify a prompt before processing.
- `PreToolUse`: Block/modify tool execution.
- `PostToolUse`: Automated testing or cleanup.
- `Stop`: Cleanup or summary after agent stops.
- `SubagentStop`: Teardown of specialized agents.

### Implementation (Native Schema)
- **Registry**: `hooks/hooks.json` maps events (e.g., `PreToolUse`) to commands.
- **Matchers**: Uses regex or string matching to filter when a hook fires.
- **Example**:
  ```json
  {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.sh"
      }]
    }]
  }
  ```
- **Security**:
  - Project-level hooks should be **untrusted** by default.
  - Require explicit user approval or "Allow List" for execution.
  - Return codes determine flow (e.g., `exit 1` blocks the action).

## 5. Deployment & Identity

- **Auto-Discovery**: Discovery relies on folder scanning in `~/.claude/` or `.claude/`.
- **Packaging**: Use `.claude-plugin/plugin.json` for metadata when sharing as a package, though registration is local.
- **Versioning**: Managed via semantic versioning in the package manifest.

## 6. Endpoint Optimization (Official & Unofficial)

While optimized for `anthropics/claude-code`, the toolkit is designed for **Universal Compatibility** across major agentic endpoints.

### 6.1 Official (Anthropic)
- **Standard**: Uses `claude-code` CLI and `Claude 3.5 Sonnet`.
- **Primary Mechanic**: Native `Task` and `Skill` tools.
- **Context**: Optimized for large context windows (200k+).

### 6.2 Unofficial: Zai Code (Z.ai / GLM)
- **Standard**: Uses `zai-cli` or `ZtoApi` proxy.
- **Models**: GLM-4.5, GLM-4.6V (Vision), GLM-4.7.
- **Optimization**:
  - **Tool Calling**: Leverages GLM's native function calling which maps to Claude's tool schema.
  - **Vision**: Optimized for skill-based image analysis using `GLM-4.6V`.
  - **Auto-Discovery**: Compatible with the `.claude/` structure for rules and commands.

### 6.3 Unofficial: Minimax Code (MiniMax-M2)
- **Standard**: Model endpoint `https://api.minimax.chat/v1/text/chat/completions_pro`.
- **Optimization**:
  - **Multi-File Context**: Optimized for the `MiniMax-M2` ability to handle complex multi-file edits.
  - **Parallelism**: Highly efficient when using the **Parallel Agent Pattern** due to fast inference.
  - **Testing**: Native support for coding-run-fix loops.

### 6.4 Universal Configuration
To switch endpoints, configure the runtime environment:
- **Base URL**: `ANTHROPIC_BASE_URL` (points to Zai or Minimax proxy).
- **API Key**: `ANTHROPIC_API_KEY` (compatible with specialized providers).
- **Environment**: Ensure `.claude/settings.json` reflects the chosen provider's capabilities.
