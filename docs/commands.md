# Commands: Best Practices & Tips

> **📘 Official Docs:** [Slash commands](https://code.claude.com/docs/en/slash-commands) - Complete official slash commands documentation  
> **📘 Official Docs:** [Skill tool](https://code.claude.com/docs/en/slash-commands#skill-tool) - Official programmatic invocation reference  
> **📖 Comprehensive Reference:** See [CLAUDE.md](../CLAUDE.md) for complete Cat Toolkit guidance on Skills, Commands, and Agents

Best practices and practical tips for Commands in the Cat Toolkit. This guide focuses on **Cat Toolkit conventions** and **practical patterns** not covered in official documentation.

---

## Mental Model

```
Command = Workflow Orchestrator / User Interaction Handler
├─ Human types: /deploy
├─ AI invokes: SlashCommand(deploy, args)
└─ Claude executes: Orchestrates multiple Skills/subagents → handles user interaction
```

**Key Insight:** Commands excel at orchestrating workflows and handling user interaction. Skills provide domain/process knowledge. See [CLAUDE.md](../CLAUDE.md#commands-workflow-orchestration--user-interaction) for the complete distinction.

---

## Best Use Cases

| Use Case | When to Use | Key Configuration |
|:---------|:------------|:------------------|
| **Multi-Skill/Subagent Orchestration** | Sequencing multiple Skills/subagents | `allowed-tools: [Skill, Bash]`, list skills explicitly in order |
| **User Interaction** | Workflows requiring `AskUserQuestion` | `argument-hint: "..."`, consolidate questions early |
| **Zero-Token Retention** | Heavy playbooks excluded from passive memory | `disable-model-invocation: true` |
| **Deterministic Shortcuts** | Semantic discovery unreliable, need fixed alias | Simple command wrapping Skill |

**Best Practices:** List skills in execution order, use explicit skill names, document dependencies, consolidate questions early, use `argument-hint` for user guidance.

---

## When Skills Might Be Better

**Rule:** For single capabilities, prefer Skills. Commands are for orchestration and user interaction.

**Use Skills for:** Single domain capability, complex domain logic (with `references/`), pure knowledge injection.

See [CLAUDE.md](../CLAUDE.md#the-80-golden-rule) for complete decision flow.

---

## Cat Toolkit Conventions

**Zero-Token Retention:** `disable-model-invocation: true` excludes from ~15k budget. Use for heavy playbooks, infrequent wizards, personal shortcuts. Execution still costs tokens; only retention is zero.

**Command-Skill Pattern:** Command wraps Skill via `allowed-tools: [Skill(name)]`. Benefits: lightweight wrapper, semantic discovery, zero-retention. Set `user-invocable: false` on wrapped Skills.

**argument-hint:** Use clear, concise hints matching `AskUserQuestion` prompts. Keep short (appears in autocomplete). Example: `argument-hint: Optional feature description`.

---

## Practical Patterns

| Pattern | Configuration | Key Points |
|:-------|:--------------|:-----------|
| **Safe Read-Only** | `allowed-tools: [Read, Grep]` | Restrict tools (default allows all). Grep/Glob are fine. |
| **Autonomous Wrapper** | `allowed-tools: [Read, Grep, Glob]` + "DO NOT ask questions" | Specify output format (JSON/markdown). Explicitly state no questions. |
| **User Interactive (Wizard)** | `disable-model-invocation: true` + `argument-hint` | Consolidate questions early. Use clear options. |

See [COMMAND_ORCHESTRATION_EXAMPLE.md](./COMMAND_ORCHESTRATION_EXAMPLE.md) for complete interactive wizard pattern.

---

## Best Practices & Common Pitfalls

**Quick Wins:**
- Use `argument-hint` liberally for user guidance
- Consolidate questions in one burst (Phase 3 pattern)
- List skills explicitly by name in orchestration
- Document dependencies and error handling

**Visibility Control:**

| Field | Scope | Effect |
|:-----|:------|:-------|
| `disable-model-invocation` | Commands | Excludes from ~15k budget when `true` |
| `user-invocable` | Skills | Hides from `/` menu when `false` |

**Common Pitfalls & Fixes:**

| Problem | Fix |
|:--------|:----|
| Over-orchestrating simple tasks | Prefer Skill for single capabilities |
| Missing `argument-hint` | Always include for interactive commands |
| Scattered questions | Use Phase 3 pattern (consolidate early) |
| Forgetting zero-token retention | Use `disable-model-invocation: true` for heavy workflows |
| Vague skill orchestration | List skills explicitly by name and order |

**Frontmatter:** `description` (required), `argument-hint`, `allowed-tools`, `disable-model-invocation` (optional). `permissionMode` is NOT valid (exclusive to Agents).

---

## Quick Decision Matrix

| Scenario | Consider Command? | Configuration Tip |
|:---------|:-----------------|:------------------|
| Orchestrating multiple Skills/subagents | ✓ Yes | List skills explicitly |
| User interaction requiring `AskUserQuestion` | ✓ Yes | Use `argument-hint` |
| Heavy playbook (zero-retention needed) | ✓ Yes | `disable-model-invocation: true` |
| Single capability | ✗ Prefer Skill | See [CLAUDE.md](../CLAUDE.md) |
| Simple one-shot task | ✗ Prefer Skill | Skills handle this better |

For comprehensive decision guidance, see [CLAUDE.md](../CLAUDE.md#the-prompt-churn-decision-flow-2026-standards).

---

## Common Patterns

### Release Workflow
```yaml
---
description: "Orchestrate complete release process"
allowed-tools: [Skill, Bash]
---
Execute: version-bump → tests → build → deploy → notify
```

### Interactive Wizard
```yaml
---
description: "Interactive project scaffolding"
argument-hint: Optional template name
disable-model-invocation: true
---
Guide user through template selection and setup.
```

### Analysis Shortcut
```yaml
---
description: "Quick codebase analysis"
allowed-tools: [Skill(analyzer)]
disable-model-invocation: true
---
Invoke analyzer skill for comprehensive audit.
```

---

## Further Reading

- [CLAUDE.md](../CLAUDE.md) - Complete Cat Toolkit reference
- [COMMAND_ORCHESTRATION_EXAMPLE.md](./COMMAND_ORCHESTRATION_EXAMPLE.md) - Advanced command pattern example
- [Official Slash Commands Docs](https://code.claude.com/docs/en/slash-commands) - Official Claude Code documentation
