# Computer Access Pattern

Agents benefit from access to a computer, giving them primitives like a filesystem and shell.

## Core Insight

> The fundamental coding agent abstraction is the CLI, rooted in the fact that agents need access to the OS layer. It's more accurate to think of Claude Code as "AI for your operating system".

## Components

### Filesystem

Provides agents with:
- **Persistent context**: State survives across tool calls
- **External memory**: Store information outside context window
- **Coordination**: Share state between sub-agents
- **Artifacts**: Produce tangible outputs

### Shell

Enables agents to:
- Run built-in utilities (ls, grep, find)
- Execute CLIs (git, npm, docker)
- Run provided scripts
- Execute code they write

## Production Examples

| Agent | Computer Access |
|:------|:----------------|
| Claude Code | "Lives on your computer" |
| Manus | Virtual computer environment |
| Cursor | Direct filesystem + shell |
| Devin | Sandboxed computer environment |

## Implementation Pattern

```
┌─────────────────────────────────────┐
│           Agent                     │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    ▼                     ▼
┌─────────┐         ┌─────────┐
│ Bash    │         │ File    │
│ Tool    │         │ Tools   │
└────┬────┘         └────┬────┘
     │                   │
     ▼                   ▼
┌─────────────────────────────────────┐
│           Operating System          │
│  - Shell utilities                  │
│  - CLIs (git, npm, docker)          │
│  - Filesystem                       │
│  - Network (curl, etc.)             │
└─────────────────────────────────────┘
```

## Best Practices

### Filesystem Usage

| Pattern | Use |
|:--------|:----|
| Scratchpads | Temporary thinking space |
| Plan files | Long-running task coordination |
| Output files | Artifact storage |
| Log files | Session history |

### Shell Usage

| Pattern | Use |
|:--------|:----|
| Utilities | Quick system queries |
| CLIs | Specialized operations (git, docker) |
| Scripts | Complex multi-step operations |
| Generated code | Dynamic execution |

## Security Considerations

- Sandbox when possible (containers, VMs)
- Limit network access if not needed
- Audit file system writes
- Prefer read-only operations for exploration
