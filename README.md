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

To use The Cat Toolkit plugins, load them directly using the `--plugin-dir` flag:

```bash
# Load individual plugins
claude --plugin-dir ./plugins/execute
claude --plugin-dir ./plugins/reason
claude --plugin-dir ./plugins/verify

# Load multiple plugins
claude --plugin-dir ./plugins/execute --plugin-dir ./plugins/reason --plugin-dir ./plugins/verify
```

**Note:** This is a plugin marketplace for development. In production, you would typically install specific plugins from a marketplace.

## Development

Refer to [CLAUDE.md](CLAUDE.md) for core architectural laws and [docs/IMPLEMENTATION-GUIDE.md](docs/IMPLEMENTATION-GUIDE.md) for validation workflows.

---

**The Cat Toolkit** - Building the future of autonomous AI development.
