# The Cat Toolkit Marketplace

Official plugin marketplace for **The Cat Toolkit** - Vibecoding plugins for autonomous AI development.
Huge thanks to https://github.com/glittercowboy/taches-cc-resources ; https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering and many other for inspiration. 

## Core Philosophy: Native Intelligence & Delegation

This toolkit is built on three non-negotiable pillars that separate "CLI Tool Thinking" from "AI-Native Engineering."

### 1. The Law of Atomic Independence
Every component is a sovereign entity.
*   **Agents are Intelligent:** They operate autonomously with full context. They can parse natural language, make decisions, and execute tasks without micromanagement.
*   **Skills are Libraries:** They are passive. They provide declarative standards and templates. They are books that can be read by anyone (User or Agent).
*   **Commands are Minimal Wrappers:** They force new tasks while preserving context. They delegate to agents, trusting their intelligence. If the Command is deleted, the Agent still works.

### 2. Context-Isolated Delegation
We leverage context isolation for focused, efficient delegation.
*   **Vector Pattern (/think):** Uses current context with user interaction. Fast, interactive, perfect for surgical tasks.
*   **Triangle Pattern (/brainstorm):** Spawns a subagent in a **separate context window** with injected context. Use this for heavy lifting (coding, planning, searching) to maintain clean separation and prevent context bloat.
*   **Time-Server Pattern:** Background execution for long-running tasks with minimal context cost.

> **Note:** Pattern names (Triangle, Vector, Time-Server, Swarm) are **custom conventions** specific to this project, not official Claude Code patterns.

### 3. The Mathematics of Parallelism
We leverage the "Task" tool to run **Swarm Architectures**.
*   **Speed:** Parallelize search and discovery across multiple file trees.
*   **Cost:** Offload heavy context reading to cheaper, transient sub-agents while the Main AI Agent acts only as the synthesizer.
*   **Hygiene:** Parallel agents cannot pollute each other's context. This forces clean code and clear separation of concerns.

---

## Architecture Patterns

### Triangle Pattern (Context-Isolated Delegation)
**Components:** `Command → Agent → Skill`
*   **Standard Mode:** One agent solves a complex problem.
*   **Swarm Mode:** The Command acts as a Load Balancer, spawning multiple agents to attack a problem in parallel (Map-Reduce).
*   **Why:** Clean context separation prevents main thread pollution. The Command reads files and injects context, allowing agents to focus on their specialized task without context bloat.

### Vector Pattern (Interactive)
**Components:** `Command → Skill`
*   **Logic:** The Command guides the user through a workflow in the main thread.
*   **Why:** For tasks requiring human feedback loops or teaching.
*   **Example:** `/think` asks the user questions to select a mental framework.

### Time-Server Pattern (Background Execution)
**Components:** `Command → Async Agent → Poll → Result`
*   **Logic:** Background execution for long-running tasks.
*   **Why:** For tasks >1 minute, side effects, or external dependencies.
*   **Example:** `/setup` commands for deployment.

### Swarm Pattern (Parallel Execution)
**Components:** `Command → [Agent A, B, C] → Synthesis`
*   **Logic:** Multiple agents working in parallel on atomic tasks.
*   **Why:** For search, audit, or batch operations across large codebases.
*   **Example:** Auditing all plugins simultaneously.

> **Important:** These patterns are **project-specific conventions**. See [docs/VECTOR_vs_TRIANGLE.md](docs/VECTOR_vs_TRIANGLE.md) for the complete guide with official Claude Code terminology.

## Installation

### Add the Marketplace

```bash
# For local testing
claude plugin marketplace add path/to/thecattoolkit

# For GitHub (when published)
claude plugin marketplace add Git-Fg/thecattoolkit
```

### Install Plugins

```bash
claude plugin install project-orchestrator@thecattoolkit
```

## Available Plugins

### Builder (The Unified Builder)

**License:** MIT

Unified planning and engineering suite that consolidates project strategy with code execution. Features autonomous execution, systematic debugging, and test-driven development.

**Features:**
- Hierarchical Planning: BRIEF.md → ROADMAP.md → phased PLAN.md structure
- Autonomous Execution: Agents execute in Uninterrupted Flow with self-verification
- Quality Assurance: Systematic protocols for debugging, TDD, and code review
- State-in-Files: All decisions and progress tracked in disk-based files

**Commands:**
- `/plan` [project description] - Creates hierarchical project plans
- `/execute` [path to PLAN.md] - Orchestrates plan execution
- `/debug` - Systematic debugging protocol
- `/tdd` - Test-Driven Development workflow
- `/review` - Code review and quality assessment

**Agents:**
- `director` - Orchestrates complex plan execution with dependency analysis
- `worker` - Universal builder for autonomous implementation

**Skills:**
- `execution-core` - Universal behavioral standards (Uninterrupted Flow, Self-Verification, Handoffs)
- `project-strategy` - Document templates and format standards (BRIEF.md, ROADMAP.md, PLAN.md, SUMMARY.md, HANDOFF.md)
- `software-engineering` - Engineering protocols (TDD, Debugging, Code Review, Security)

### Strategist (The Brain)

**License:** MIT

Interactive thinking, analysis, and prompt crafting system.

**Features:**
- 12 structured thinking frameworks across 3 categories
- Interactive selection and application
- Prompt crafting and editing capabilities
- Shared skill resources for both Vector and Triangle patterns
- Standardized output templates

**Commands:**
- `/think` - Interactive framework application (Vector pattern)
- `/brainstorm` - Comprehensive delegated analysis (Triangle pattern)
- `/create-prompt` - Create new single prompts or meta-prompt chains
- `/edit-prompt` - Modify existing prompts with validation
- `/prompt-engineer` - Advanced prompt engineering with autonomous agent
- `/run-prompt` - Execute saved prompts

**Agents:**
- `brainstormer` - Applies thinking frameworks in isolated context
- `prompt-engineer` - Advanced prompt engineering and optimization

**Skills:**
- `thinking-frameworks` - Framework selection prompts, methodology, and templates
- `prompt-crafting` - Prompt structure, patterns, and best practices

### Meta (The Toolkit Builder)

**License:** MIT

Tools to build, maintain, and audit the AI system itself.

**Features:**
- Command creation and management
- Agent creation and editing
- Skill development workflows
- Plugin building automation

**Commands:**
- `/build` - Natural language entry point for building commands, agents, and skills
- `/heal` - Self-correction and diagnostic protocol
- `/setup` - Generic deployment command for hooks and scripts
- `/setup-py` - Deploy Python guard hooks (in guard-python plugin)
- `/setup-ts` - Deploy TypeScript guard hooks (in guard-ts plugin)

**Agents:**
- `plugin-expert` - System maintainer persona for plugin development

**Skills:**
- `manage-commands` - Command creation templates and workflows
- `manage-subagents` - Agent creation and best practices
- `manage-hooks` - Safety and automation hooks

## Plugin Structure

Each plugin in this marketplace follows the standard structure:

```
plugins/
└── plugin-name/
    ├── .claude-plugin/
    │   └── plugin.json          # Plugin manifest
    ├── commands/                # Orchestrators (Workflows)
    ├── agents/                  # Executors (Context-Isolated Workers)
    ├── skills/                  # Standards (Templates & References)
    │   └── skill-name/
    │       ├── SKILL.md
    │       ├── assets/
    │       │   └── templates/
    │       └── references/
    ├── CLAUDE.md                # Project instructions
    └── README.md                # Plugin documentation
```

## Development

### Adding a New Plugin

1. Create a new directory in `plugins/your-plugin-name`
2. Follow the standard plugin structure
3. Add an entry to `.claude-plugin/marketplace.json`
4. Include a `README.md` documenting your plugin
5. Test locally before pushing

### Marketplace Manifest

To register your plugin, add it to `.claude-plugin/marketplace.json`:

```json
{
  "name": "your-plugin-name",
  "source": "./plugins/your-plugin-name",
  "description": "Brief description of your plugin"
}
```

### Development Standards

All plugins must follow these architectural standards:

- **Follow the Triangle, Vector, Time-Server, or Swarm patterns** (see [docs/VECTOR_vs_TRIANGLE.md](docs/VECTOR_vs_TRIANGLE.md))
- **Trust agent intelligence** - Don't micromanage or treat agents like CLI tools (see [docs/AI-ARCHITECTURE.md](docs/AI-ARCHITECTURE.md))
- **No "Zombie Skill" logic** - Skills must be passive (no active execution or AskUserQuestion)
- **No Skill-Command Coupling** - Skills don't reference Commands
- **No Skill-to-Skill Coupling** - Skills must be self-contained (no `../` references)
- **Single-purpose skills** - Agents can leverage multiple skills via `skills:` frontmatter
- **Comprehensive documentation** - Include README.md and follow directory structure
- **Relative paths only** - Use `references/file.md` not absolute paths

See [CLAUDE.md](CLAUDE.md) for complete development guidelines and forbidden patterns.

## Documentation

### Core Architecture
- **[docs/AI-ARCHITECTURE.md](docs/AI-ARCHITECTURE.md)** - Native AI agent intelligence vs CLI tools philosophy
- **[docs/VECTOR_vs_TRIANGLE.md](docs/VECTOR_vs_TRIANGLE.md)** - Comprehensive guide to architectural patterns with examples
- **[CLAUDE.md](CLAUDE.md)** - Development standards and forbidden patterns

### Plugin-Specific
- **[plugins/builder/README.md](plugins/builder/README.md)** - Builder plugin documentation
- **[plugins/think/README.md](plugins/think/README.md)** - Strategist plugin documentation
- **[plugins/meta/README.md](plugins/meta/README.md)** - Meta plugin documentation

## Contributing

We welcome contributions! Please ensure your plugins:

1. Follow the Triangle, Vector, Time-Server, or Swarm architecture patterns
2. Trust agent intelligence (don't treat them like CLI tools)
3. Have no Zombie Skill logic (active execution in Skills)
4. Have no Skill-Command Coupling (Skills don't reference Commands)
5. Have no Skill-to-Skill Coupling (Skills must be self-contained)
6. Have single-purpose skills (agents can leverage multiple skills)
7. Include comprehensive documentation
8. Follow the standard directory structure
9. Use relative paths (no hardcoded absolute paths)

## License

Each plugin may have its own license. Please refer to individual plugin directories for specific licensing information.

## Support

For issues, questions, or contributions, please visit:
- GitHub: https://github.com/thecattoolkit
- Documentation: See individual plugin README files

---

**The Cat Toolkit** - Building the future of autonomous AI development.
