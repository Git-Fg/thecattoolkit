# Zero-Token Retention Standard

## The Problem

Every tool definition in the system prompt consumes context tokens. The tool definitions have a budget of approximately **15,000 characters**.

Too many commands push useful skills out of context, reducing the AI's ability to semantically discover relevant capabilities.

## The Solution

Use **`disable-model-invocation: true`** in the command frontmatter.

### Effect

When `disable-model-invocation: true`:

1. **The command does NOT appear** in the AI's system prompt tool definitions
2. **The AI CANNOT invoke it autonomously** via semantic intent
3. **The human CAN still invoke it** via `/command` syntax

### Token Savings

| Component | Token Cost (with `false`) | Token Cost (with `true`) |
|:----------|:------------------------:|:------------------------:|
| Command definition | ~200-500 tokens | **0 tokens** |
| Skill tool reference | ~100-300 tokens | **0 tokens** |

**Savings:** A single command can save 300-800 tokens in the system prompt.

## When to Use

### Use `disable-model-invocation: true` for:

1. **Heavy Playbooks**
   - Complex release procedures
   - Multi-step deployment workflows
   - Long-running maintenance tasks

2. **Human Shortcuts**
   - Convenience aliases for common tasks
   - `/lint` → `uv run ruff check`
   - `/format` → `uv run ruff format`

3. **Interactive Wizards**
   - Workflows requiring `AskUserQuestion`
   - Setup procedures
   - Configuration workflows

4. **Personal Utilities**
   - Developer-specific shortcuts
   - Project-specific commands
   - Rarely-used automation

### Use `disable-model-invocation: false` (default) for:

1. **Analysis Tools**
   - Commands the AI needs to gather information
   - `/ingest` for repository scanning
   - `/analyze` for codebase analysis

2. **Frequently Invoked**
   - Commands the AI uses regularly
   - Core workflow automation

## Decision Matrix

| Command Type | Autonomous Use | Human-Only | `disable-model-invocation` |
|:-------------|:--------------:|:----------:|:--------------------------:|
| Analysis tool | ✓ | | `false` |
| Workflow orchestrator | ✓ | | `false` |
| Human shortcut | | ✓ | `true` |
| Interactive wizard | | ✓ | `true` |
| Heavy playbook | | ✓ | `true` |

## Examples

### Human-Only Shortcut (Zero Retention)

```yaml
---
description: "Quick format check"
allowed-tools: [Bash]
disable-model-invocation: true
---

# Format Check

Run ruff format check:
```bash
uv run ruff format --check .
```
```

**Why:** This is a convenience shortcut. The AI can run `ruff` directly via Bash tool if needed. The command saves humans from remembering the full syntax.

### Interactive Wizard (Zero Retention)

```yaml
---
description: "Interactive project scaffolding"
argument-hint: "Optional template name"
disable-model-invocation: true
---

# Scaffold Wizard

Guide user through project creation:
1. Gather requirements via AskUserQuestion
2. Select template
3. Generate structure
```

**Why:** Wizards require `AskUserQuestion`, which doesn't work well with autonomous invocation. The command exists for human convenience.

### Analysis Tool (Keep Enabled)

```yaml
---
description: "Scan repository for analysis"
allowed-tools: [Skill(gitingest), Bash]
---

# Repository Scan

Scan current repository and generate analysis for AI consumption.

**Goal:** Load repository context into session
**Output:** Structured repository digest
```

**Why:** The AI needs to invoke this autonomously when it needs to understand a codebase. Disabling would prevent semantic discovery.

## Best Practices

1. **Default to `false`:** Only set to `true` if you have a specific reason
2. **Document why:** Add comments explaining the decision
3. **Consider frequency:** Frequently-used AI commands should stay enabled
4. **Test discovery:** Verify AI can still find relevant capabilities

## Validation Checklist

- [ ] Command purpose documented
- [ ] Human-only vs AI-use considered
- [ ] `disable-model-invocation` set correctly
- [ ] If `true`: Human shortcut or wizard
- [ ] If `false`: AI needs autonomous access
- [ ] Token budget impact considered
