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
/plugin install sys-core@cattoolkit sys-builder@cattoolkit sys-cognition@cattoolkit sys-meta@cattoolkit sys-edge@cattoolkit sys-multimodal@cattoolkit sys-research@cattoolkit
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
