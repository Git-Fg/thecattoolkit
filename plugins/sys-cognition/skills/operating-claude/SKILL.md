---
name: operating-claude
description: "Operational manual for driving the Claude runtime. Use when needing to optimize context usage, troubleshoot performance, or understand runtime mechanics. Do not use for architectural definitions or building plugins."
allowed-tools: [Read]
---

# Operational Mechanics

## Runtime Operations

### 1. Context Management
- **Monitoring**: Check tokens via `/status` or observing response latency.
- **Optimization**: Use `managing-context` for compression strategies.
- **Degradation**: Performance drops >40% usage. Reset or fork session.

### 2. Session Control
- **Plan Mode**: Double `Shift+Tab` for high-reasoning tasks.
- **Forking**: Isolate heavy tasks to avoid polluting main context.
- **Checkpoints**: Use `_state.md` to persist progress across sessions.

## Architecture References

For strict definitions of how the system is built, refer to the core documentation:

- **Plugin Architecture**: `docs/guides/infrastructure.md`
- **Skill Standards**: `docs/guides/skills.md`
- **Engineering Patterns**: `docs/REFERENCES.md`
