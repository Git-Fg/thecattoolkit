# The Cat Toolkit Marketplace

Plugin marketplace for **The Cat Toolkit** - Vibecoding plugins for autonomous AI development.

> **For developers, the primary source of truth is [CLAUDE.md](CLAUDE.md).**

---

## Plugin Architecture

The Cat Toolkit organizes capabilities into domain-specific plugins:

| Plugin | Domain | Focus |
|:-------|:-------|:------|
| **sys-core** | Infrastructure | Validation, scaffolding, hooks, MCP, security |
| **sys-builder** | Engineering | Architecture, planning, execution, testing, TDD |
| **sys-cognition** | Reasoning | Thinking frameworks, prompt engineering, analysis (directly actionable) |
| **sys-agents** | Agent Development | Context engineering, memory systems, orchestration (requires implementation) |
| **sys-research** | Knowledge | Research tools, documentation, codebase analysis |
| **sys-multimodal** | Media | Vision, audio, video processing |
| **sys-edge** | Edge/Mobile | Optimization, offline-first, resource-constrained environments |
| **sys-nodejs** | Node.js | JavaScript/TypeScript development, build tools |
| **sys-browser** | Browser Automation | Web interaction, crawling, testing |
| **llm-application-dev** | LLM Applications | RAG systems, vector databases, hybrid search, semantic retrieval |

**Key Distinction:** `sys-cognition` provides directly actionable skills (prompt patterns, reasoning frameworks), while `sys-agents` covers skills requiring external frameworks (Vector DBs, GraphRAG, multi-agent architectures).

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
