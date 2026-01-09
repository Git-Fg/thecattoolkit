# The Cat Toolkit Marketplace

Official plugin marketplace for **The Cat Toolkit** - Vibecoding plugins for autonomous AI development.

## OODA Loop Architecture

The toolkit is organized around the **OODA Loop** (Observe-Orient-Decide-Act) decision cycle:

| Plugin | OODA Phase | Purpose |
|--------|------------|---------|
| **@cattoolkit/reason** | Orient + Decide | Strategic thinking and analysis without action |
| **@cattoolkit/guide** | Orient | Steering agents through structured prompts |
| **@cattoolkit/execute** | Act | File modifications and irreversible actions |
| **@cattoolkit/verify** | Observe | Validating correctness of changes |
| **@cattoolkit/persist** | All | Making ephemeral context permanent |
| **@cattoolkit/bootstrap** | Meta | Initializing and repairing the system |

---

## Available Plugins

### @cattoolkit/reason (Orient + Decide)

Strategic thinking and analysis without action. Captures the "Orient" and "Decide" phases.

**Skills:**
- `thinking-frameworks` - 12 structured frameworks (first-principles, SWOT, Pareto, 5-whys, Eisenhower)

**Agents:**
- `brainstormer` - Applies thinking frameworks in isolated context

---

### @cattoolkit/guide (Steering)

Prompt engineering as a guidance mechanism for steering agents.

**Skills:**
- `prompt-engineering` - Prompt design theory (CoT, few-shot), XML vs Markdown decisions
- `prompt-library` - Templates for single prompts, chains, and meta-prompts

**Agents:**
- `prompt-engineer` - Designs and optimizes prompts

---

### @cattoolkit/execute (Act)

The execution engine - where file modifications happen.

**Skills:**
- `execution-core` - Uninterrupted Flow, Self-Verification, Handoffs
- `project-strategy` - Document templates (BRIEF.md, ROADMAP.md, PLAN.md)
- `software-engineering` - TDD, Debugging, Code Review, Security protocols
- `architecture` - System design frameworks and ADR documentation

**Agents:**
- `director` - Orchestrates complex plan execution
- `worker` - Universal builder for autonomous implementation
- `architect` - System architecture specialist

**Commands:**
- `/plan` - Creates hierarchical project plans

---

### @cattoolkit/verify (Validation)

The immune system - verifying correctness of changes.

**Hooks:**
- `protect-files.py` - Warns about editing sensitive files
- `security-check.py` - Detects potential secrets in code
- `type-check-python.py` - Runs pyrefly/mypy on Python files
- `type-check-ts.js` - Runs tsc on TypeScript files

---

### @cattoolkit/persist (Memory)

Making ephemeral context permanent through session state management.

**Skills:**
- `context-engineering` - Scratchpad pattern, handoffs, checkpoints

**Agents:**
- `scribe` - Context management specialist

**Hooks:**
- Session lifecycle (SessionStart, PreCompact, Stop)
- Auto-logging (PostToolUse)

---

### @cattoolkit/bootstrap (Infrastructure)

Initializing and repairing the system itself.

**Skills:**
- `manage-skills`, `manage-subagents`, `manage-commands`, `manage-hooks`
- `manage-healing`, `manage-styles`

**Agents:**
- `plugin-expert` - System maintainer persona

**Commands:**
- `/heal` - Self-correction and diagnostic protocol

---

## Installation

```bash
# Add the marketplace
claude plugin marketplace add Git-Fg/thecattoolkit

# Install plugins
claude plugin install @cattoolkit/execute
claude plugin install @cattoolkit/reason
claude plugin install @cattoolkit/verify
```

## Architecture Patterns

### Triangle Pattern (Context-Isolated Delegation)
**Components:** `Command → Agent → Skill`
- Standard Mode: One agent solves a complex problem
- Swarm Mode: Multiple agents in parallel (Map-Reduce)

### Vector Pattern (Interactive)
**Components:** `Command → Skill`
- For tasks requiring human feedback loops

### Forked Skills (2026 Pattern)
**Components:** `Skill (context: fork) → Agent`
- Skills execute in isolated context with bound agent persona
- No command wrapper needed

---

## Development Standards

All plugins follow the **2026 Universal Agentic Runtime** standards:

- **Law 1:** Atomic Independence - Components function standalone
- **Law 2:** Eliminate Glue Code - Skills with `context: fork` need no wrappers
- **Law 3:** Native Delegation - Intent over scripting
- **Law 4:** Description as API - Semantic discovery via descriptions

See [CLAUDE.md](CLAUDE.md) for complete development guidelines.

---

**The Cat Toolkit** - Building the future of autonomous AI development.
