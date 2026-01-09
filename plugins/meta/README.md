# @cattoolkit/meta (The Toolkit Builder)

**Purpose**: Tools to build, maintain, and audit the AI system itself. This is the "Bootstrapper."

## Target User
The Plugin Developer / System Maintainer.

## Skills
- `manage-skills` (Create/Edit/Audit Skills)
- `manage-subagents` (Create/Edit Agents)
- `manage-commands` (Create Slash Commands)
- `manage-hooks` (Create and manage hooks - actual running hooks are in @cat-toolkit/guard)

## Agents
- `plugin-expert` (The System Maintainer persona)

## Commands
- `/build` (Natural language entry point for building components)
- `/heal` (Self-correction and diagnostic protocol)

## Integration

- **@cat-toolkit/guard** - Provides the actual running hooks (security, type-check, file protection)
- **@cat-toolkit/builder** - Project planning and execution, code execution and debugging
