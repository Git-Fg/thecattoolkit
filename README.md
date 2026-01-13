# The Cat Toolkit Marketplace

Plugin marketplace for **The Cat Toolkit** - Vibecoding plugins for autonomous AI development.

> **For developers, the primary source of truth is [CLAUDE.md](CLAUDE.md).**

---

## Available Plugins

| Plugin | Purpose |
|--------|---------|
| **sys-core** | Infrastructure and Safety layer for plugin management, security auditing, and toolkit maintenance |
| **sys-builder** | Development & Engineering domain for software development, architecture design, planning, execution, and testing |
| **sys-cognition** | AI/ML & Cognitive domain for context engineering, memory systems, reasoning, and prompt engineering |
| **sys-research** | Research & Knowledge domain for research tools, knowledge retrieval, codebase analysis, and gitingest |
| **sys-edge** | Edge & Tooling domain for edge AI, mobile optimization, offline-first systems, and Python tooling |
| **sys-multimodal** | Media & Multimodal domain for video editing, media processing, multimodal AI, and data visualization |
| **sys-nodejs** | Node.js domain for JavaScript/TypeScript development, build tools, and package management |
| **llm-application-dev** | LLM Applications domain for RAG systems, vector databases, hybrid search, and semantic retrieval |

---

## Installation

### Marketplace Installation (Recommended)

Add The Cat Toolkit marketplace and install plugins:

```bash
# Add the marketplace
/plugin marketplace add Git-Fg/thecattoolkit

# Install individual plugins
/plugin install sys-core@cattoolkit
/plugin install sys-builder@cattoolkit
/plugin install sys-cognition@cattoolkit

# Or install all plugins
/plugin install sys-core@cattoolkit sys-builder@cattoolkit sys-cognition@cattoolkit sys-edge@cattoolkit sys-multimodal@cattoolkit sys-research@cattoolkit sys-nodejs@cattoolkit llm-application-dev@cattoolkit
```

### Development Installation

For local development, load plugins using the `--plugin-dir` flag:

```bash
# Load individual plugins
claude --plugin-dir ./plugins/sys-builder
claude --plugin-dir ./plugins/sys-cognition

# Load multiple plugins
claude --plugin-dir ./plugins/sys-builder --plugin-dir ./plugins/sys-cognition --plugin-dir ./plugins/sys-core
```

### Installation Scopes

- **User scope** (default): Personal use across all projects
- **Project scope**: Team-shared plugins, committed to git
- **Local scope**: Personal overrides, gitignored

```bash
# Project scope (team-shared)
/plugin install sys-core@cattoolkit --scope project
```

See [Marketplace Configuration Guide](docs/REFERENCES.md#1-marketplace-configuration) for complete installation and configuration details.

---

## Documentation

- **[CLAUDE.md](CLAUDE.md)** — The Universal Agentic Runtime (Constitution & Manual)
- **[Marketplace Reference](docs/REFERENCES.md#1-marketplace-configuration)** — Complete marketplace configuration and plugin distribution guide
- **[Commands Reference](docs/REFERENCES.md#3-commands--permissions)** — Commands: Shortcuts & AI Macros
- **[Infrastructure Reference](docs/REFERENCES.md#4-infrastructure)** — Hooks, MCP, LSP, and runtime configuration
- **[Permissions Reference](docs/REFERENCES.md#3-commands--permissions)** — Complete permissions and security guide

## Development

---

**The Cat Toolkit** - Building the future of autonomous AI development.
