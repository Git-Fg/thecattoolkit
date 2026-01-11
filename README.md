# The Cat Toolkit Marketplace

Plugin marketplace for **The Cat Toolkit** - Vibecoding plugins for autonomous AI development.

> **For developers, the primary source of truth is [CLAUDE.md](CLAUDE.md).**

---

## Available Plugins

| Plugin | Purpose |
|--------|---------|
| **sys-cognition** | Brain layer for thinking frameworks, prompt engineering, and context management |
| **sys-meta** | Meta-build tools for plugin creation, auditing, and maintenance |
| **sys-builder** | File modifications, project strategy, and software engineering protocols |
| **sys-core** | Infrastructure and Safety layer for plugin management, security auditing, and toolkit maintenance |
| **sys-edge** | Edge AI management, offline sync, and mobile optimization |
| **sys-multimodal** | Multimodal understanding and processing capabilities |
| **sys-research** | Research tools and documentation analysis |

---

## Installation

Load plugins using the `--plugin-dir` flag:

```bash
# Load individual plugins
claude --plugin-dir ./plugins/sys-builder
claude --plugin-dir ./plugins/sys-cognition

# Load multiple plugins
claude --plugin-dir ./plugins/sys-builder --plugin-dir ./plugins/sys-cognition --plugin-dir ./plugins/sys-core
```

---

## Development

- **[CLAUDE.md](CLAUDE.md)** - The Universal Agentic Runtime (Constitution & Manual)

---

**The Cat Toolkit** - Building the future of autonomous AI development.
