# Command Permissions Specification

## 1. Core Tools Reference

| Tool | Purpose | Restriction Pattern |
|------|---------|---------------------|
| `Read` | File access | `[Read]` |
| `Write` | File creation | `[Write]` |
| `Edit` | Targeted edits | `[Edit]` |
| `Bash` | Shell execution | `Bash(cmd:*)` |
| `Task` | Agent delegation | `[Task]` |
| `Skill` | Skill execution | `Skill(name)` |

## 2. Bash Execution Rules

- **Prefix Matching**: Wildcard `:*` ONLY works at the end.
- **Security**: Must be explicitly listed if using `!` dynamic context.
- **Example**: `Bash(git status:*)`, `Bash(npm test:*)`.

## 3. Web & MCP Patterns

- **WebFetch**: `WebFetch(domain:example.com)`
- **MCP**: `mcp__server__tool` or `mcp__server__*`

## 4. Execution Logic

- **Default**: Command inherits ALL tools if `allowed-tools` is omitted.
- **Restriction**: If `allowed-tools` is present, ONLY those tools are available.
- **Autonomous Goal**: Omit `AskUserQuestion` to favor zero-interaction workflows.
