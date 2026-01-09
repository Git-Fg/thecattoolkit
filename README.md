# The Cat Toolkit Marketplace

Official plugin marketplace for **The Cat Toolkit** - Vibecoding plugins for autonomous AI development.
Huge thanks to https://github.com/glittercowboy/taches-cc-resources ; https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering and many other for inspiration. 

## Core Philosophy: Atomic Independence & Context Economics

This toolkit is built on three non-negotiable pillars that separate "Scripting" from "Agentic Engineering."

### 1. The Law of Atomic Independence
Every component is a sovereign entity.
*   **Agents are Mercenaries:** They do not know who called them. They can be hired by a Command, by a User, or by another Agent. They work given an input, produce an output, and vanish.
*   **Skills are Libraries:** They are passive. They do not contain "active" logic. They are books that can be read by anyone (User or Agent).
*   **Commands are Receptionists:** They are optional interfaces. They take a messy user request, tidy it up, gather the files, and hand it to an Agent. If the Command is deleted, the Agent still works.

### 2. The Physics of Context Rot
We acknowledge that LLM intelligence drops significantly as the context window fills.
*   **The Vector Pattern (/think):** Uses the *current* context. Fast, interactive, but degrades main chat performance. Use for quick thoughts.
*   **The Triangle Pattern (/brainstorm):** Spawns a Subagent. The Subagent starts with a **Fresh Context (0% Rot)**. Use this for heavy lifting (coding, planning, searching) to ensure maximum intelligence.

### 3. The Mathematics of Parallelism
We leverage the "Task" tool to run **Swarm Architectures**.
*   **Speed:** Parallelize search and discovery across multiple file trees.
*   **Cost:** Offload heavy context reading to cheaper, transient sub-agents while the Main AI Agent acts only as the synthesizer.
*   **Hygiene:** Parallel agents cannot pollute each other's context. This forces clean code and clear separation of concerns.

---

## Architecture Patterns

### Sovereign Triangle (The Anti-Rot Pattern)
**Components:** `Command (Generalizer) → Agent (Sanitizer) → Skill (Standard)`
*   **Standard Mode:** One agent solves a complex problem.
*   **Swarm Mode:** The Command acts as a Load Balancer, spawning multiple agents to attack a problem in parallel (Map-Reduce).
*   **Why:** Maximum speed, minimum cost, zero context rot.

### Sovereign Vector (The Interactive Pattern)
**Components:** `Command (Guide) → Skill (Standard)`
*   **Logic:** The Command guides the user through a workflow in the main thread.
*   **Why:** For tasks requiring human feedback loops or teaching.
*   **Example:** `/think` asks the user questions to select a mental framework.

**[Read the full Architecture Guide (VECTOR_vs_TRIANGLE.md)](docs/VECTOR_vs_TRIANGLE.md)**

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

### Planner (Project Orchestrator)

**License:** MIT

End-to-end project planning and execution suite using the Orchestrator-Executor pattern.

**Features:**
- Hierarchical Planning: BRIEF.md → ROADMAP.md → phased PLAN.md structure
- Autonomous Execution: Agents execute tasks with fresh context each session
- Quality Assurance: Orchestrators verify all outputs by reading modified files
- State-in-Files: All decisions and progress tracked in disk-based files

**Commands:**
- `/create-plan` [project description] - Creates hierarchical project plans
- `/run-plan` [path to PLAN.md] - Orchestrates plan execution with QA
- `/sync-rules` - Synchronizes project rules across the toolkit
- `/contexteng` - Engineering context management

**Agents:**
- `plan-author` - Creates hierarchical project plans (BRIEF, ROADMAP, PHASES)
- `phase-executor` - Executes individual tasks within a phase (The Project Worker)

**Skills:**
- `project-standards` - Document templates and format standards (BRIEF.md, ROADMAP.md, PLAN.md, SUMMARY.md, HANDOFF.md)
- `plan-authoring` - Planning standards and best practices (plan types, task structure, evaluation criteria)

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

### Engineer (The Builder)

**License:** MIT

Code execution, debugging, testing, and git operations.

**Features:**
- Test-Driven Development workflow
- Comprehensive code review and debugging protocols
- System design and architecture analysis
- Git workflow automation
- Code mentorship and explanation

**Commands:**
- `/debug` - Debugging with systematic protocols
- `/review` - Comprehensive code review
- `/tdd` - Test-Driven Development workflow
- `/commit` - Git commit with message standards
- `/mentor` - Code explanation and concept teaching
- `/system-design` - System architecture and design analysis

**Agents:**
- `code-implementer` - Executes engineering tasks (code, tests, debugging) (The Muscle)
- `architect` - System design and architecture analysis

**Skills:**
- `engineering` - TDD protocols, debugging, code review, security audit
- `git-workflow` - Commit standards, PR workflows
- `mentorship` - Teaching workflows, code explanation

### Meta (The Toolkit Builder)

**License:** MIT

Tools to build, maintain, and audit the AI system itself.

**Features:**
- Command creation and management
- Agent creation and editing
- Skill development workflows
- Plugin building automation

**Commands:**
- `/build` - Universal entry point for building commands, agents, and skills
- `/setup` - Generic deployment command for hooks and scripts
- `/setup-py` - Deploy Python guard hooks (in guard-python plugin)
- `/setup-ts` - Deploy TypeScript guard hooks (in guard-ts plugin)
- `/expert` - Access plugin expert for system maintenance

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

- **Follow the Sovereign Triangle or Sovereign Vector patterns** (see [docs/VECTOR_vs_TRIANGLE.md](docs/VECTOR_vs_TRIANGLE.md))
- **No "Zombie Skill" logic** - Skills must be passive (no active execution or AskUserQuestion)
- **No Skill-Command Coupling** - Skills don't reference Commands
- **No Skill-to-Skill Coupling** - Skills must be self-contained (no `../` references)
- **Single-purpose skills** - Agents can leverage multiple skills via `skills:` frontmatter
- **Comprehensive documentation** - Include README.md and follow directory structure
- **Relative paths only** - Use `references/file.md` not absolute paths

See [CLAUDE.md](CLAUDE.md) for complete development guidelines and forbidden patterns.

## Documentation

### Core Architecture
- **[docs/VECTOR_vs_TRIANGLE.md](docs/VECTOR_vs_TRIANGLE.md)** - Comprehensive guide to architectural patterns with examples
- **[CLAUDE.md](CLAUDE.md)** - Development standards and forbidden patterns

### Plugin-Specific
- **[plugins/planner/README.md](plugins/planner/README.md)** - Planner plugin documentation
- **[plugins/think/README.md](plugins/think/README.md)** - Strategist plugin documentation
- **[plugins/engineer/README.md](plugins/engineer/README.md)** - Engineer plugin documentation
- **[plugins/meta/README.md](plugins/meta/README.md)** - Meta plugin documentation

## Contributing

We welcome contributions! Please ensure your plugins:

1. Follow the Sovereign Triangle or Vector architecture patterns
2. Have no Zombie Skill logic (active execution in Skills)
3. Have no Skill-Command Coupling (Skills don't reference Commands)
4. Have no Skill-to-Skill Coupling (Skills must be self-contained)
5. Have single-purpose skills (agents can leverage multiple skills)
6. Include comprehensive documentation
7. Follow the standard directory structure
8. Use relative paths (no hardcoded absolute paths)

## License

Each plugin may have its own license. Please refer to individual plugin directories for specific licensing information.

## Support

For issues, questions, or contributions, please visit:
- GitHub: https://github.com/thecattoolkit
- Documentation: See individual plugin README files

---

**The Cat Toolkit** - Building the future of autonomous AI development.
