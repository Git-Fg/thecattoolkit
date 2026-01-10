# The Cat Toolkit Marketplace

Plugin marketplace for **The Cat Toolkit** - Vibecoding plugins for autonomous AI development.

> **For developers, the primary source of truth is [CLAUDE.md](CLAUDE.md).**

---

## Available Plugins

| Plugin | Purpose |
|--------|---------|
| **reason** | Strategic thinking frameworks (first-principles, SWOT, Pareto, 5-whys) |
| **guide** | Prompt engineering and design templates |
| **execute** | File modifications, project strategy, software engineering protocols |
| **verify** | Validation hooks (security, type-checking, protected files) |
| **persist** | Session state management and context engineering |
| **bootstrap** | System initialization, healing, and plugin management |

---

## Installation

Load plugins using the `--plugin-dir` flag:

```bash
# Load individual plugins
claude --plugin-dir ./plugins/execute
claude --plugin-dir ./plugins/reason

# Load multiple plugins
claude --plugin-dir ./plugins/execute --plugin-dir ./plugins/reason --plugin-dir ./plugins/verify
```

---

## Development

- **[CLAUDE.md](CLAUDE.md)** - The Universal Agentic Runtime (Constitution & Manual)

---

**The Cat Toolkit** - Building the future of autonomous AI development.
