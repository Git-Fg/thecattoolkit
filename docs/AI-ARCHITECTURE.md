# AI Architecture: The Agentic Runtime Paradigm

## Overview

This document defines the architecture of AI-powered development where the AI is not a "CLI Tool" but an **Orchestration Runtime**. The model is the operating system; components are cognitive capabilities.

---

## I. The Agentic Runtime Paradigm

### Mental Model Shift

| Old Paradigm (CLI Tool) | New Paradigm (Agentic Runtime) |
|:------------------------|:-------------------------------|
| Claude receives commands | Claude orchestrates cognition |
| Components are scripts | Components are cognitive capabilities |
| State tracked externally | State emerges from conversation |
| Rigid argument parsing | Natural language intent |

### Cognitive Capabilities

- **Slash Commands are "Prompt Definitions":** Markdown files containing instructions FOR Claude. They scope capabilities via `allowed-tools`.
- **Agents are "Autonomous Specialists":** Triggered via the **Task tool** when their `description` matches the need. Claude launches them as sub-processes.
- **Skills are "Procedural Lenses":** Standards and methodologies auto-loaded when listed in agent frontmatter.
- **The SlashCommand Tool is "Self-Recursion":** An agent can invoke pre-defined workflows autonomously.

---

## II. The Interaction Trinity (Native Flow)

The architecture is defined by the **Recursive Invocation Path** with clear separation of State, Autonomy, and Protocol:

### 1. Commands = Prompt Templates
User input triggers a Command. The Command provides instructions that guide Claude's orchestration.

- Uses `!` syntax to gather "Ground Truth" (git status, file lists)
- Injects context through natural language prompting
- Captures natural language with `$ARGUMENTS`
- Manages `.local.md` files that track workflow phase state

### 2. Agents = Task Specialists (via Task Tool)
The Command instructs Claude to use the **Task tool** to spawn an Agent. The Agent is selected based on its `description` frontmatter—this is the API.

**Native Capacities:**
- Agent reads its own `description` and `examples` to understand its "Start State"
- Agent automatically adopts any `skills` listed in its frontmatter
- Agent has full intelligence—trust it to select tools
- Agent reports back to orchestrator when complete

### 3. Skills = Procedural Anchor
If an Agent discovers it needs a standard workflow (e.g., a `feature-dev` agent realizes it needs to commit code), it uses the SlashCommand tool to invoke `/commit` programmatically. Skills ensure the Agent's execution matches the project's specific style and standards.

**This is the "Collective Intelligence" pattern:** The toolkit's own commands become tools for the agents.

### 4. The Hook System (Governance)
Hooks are the **Immune System**—they run BEFORE the AI acts.

| Hook Event | Trigger | Use Case |
|:-----------|:--------|:---------|
| `PreToolUse` | Before tool execution | Block risky ops, modify inputs |
| `PostToolUse` | After tool success | Run linters, formatters |
| `UserPromptSubmit` | Before prompt processing | Auto-activate skills |

Hooks are defined in `hooks.json` files and map events to enforcement scripts. See `docs/HOOKS-STANDARDS.md` for implementation details.

---

## III. Context: Shared, Not Isolated

> **Critical Correction:** Agents are **not** black boxes. They are sub-processes of the current conversation.

### How Context Sharing Works

| Component | Context Visibility |
|:----------|:-------------------|
| Main Thread | Full conversation history |
| Agent (via Task tool) | Fresh context + explicit prompt content |
| Nested Agent | Instructions from parent only |

### Benefits
- Agents can reference project context passed via prompts
- Commands can inject precise context without repetition
- Skills are accessible equally to any context level

### Constraints
Use **Clear Phase Boundaries** (Summary outputs) so the next agent isn't confused by the "internal monologue" of the previous one.

---

## IV. Progressive Disclosure is Context Management

We leverage native capacity by not "Dumping" all information at once.

| Layer | When Present | Purpose |
|:------|:-------------|:--------|
| **metadata** | Always (Discovery) | Trigger activation |
| **SKILL.md body** | When triggered (Instruction) | Core procedure |
| **references/** | When agent lacks data (Deep Knowledge) | Detailed schemas, policies |

**Why:** This keeps the "Attention Mechanism" focused on the task, not the documentation.

---

## V. Interaction Graph Rules

| Path | Leverage Strategy |
|:-----|:------------------|
| **Cmd → Skill** | "Global Guards" or "Standards" visible to user (Vector Pattern). |
| **Cmd → Agent** | Uses Task tool. "Heavy Lifting" where user only wants result (Triangle Pattern). |
| **Agent → Skill** | Agent "Self-Onboards" by reading skill. No manual loading needed. |
| **Agent → Cmd** | Agent uses toolkit commands for standardized side-effects (e.g., `/heal`). |
| **Agent → Agent** | **Swarm Logic:** Orchestrator spawns multiple "Worker" agents for parallel operations. |

### Swarm Orchestration (Map-Reduce)

The most powerful pattern for parallel work:

```
1. Command instructs: "Launch X agents in parallel to do Y"
     ↓
2. Claude uses Task tool to spawn multiple agents
     ↓
3. Each agent executes independently (shared-nothing)
     ↓
4. Agents report back to orchestrator
     ↓
5. Command synthesizes final result
```

> **Native Instruction:** Claude natively understands "launch X agents in parallel" instructions. No special syntax required.

### The Triangle of Trust

The fundamental interaction pattern:

```
1. User types Command
     ↓
2. Command uses Task tool to launch Agent (fresh context)
     ↓
3. Agent auto-loads Skills from frontmatter
     ↓
4. Agent uses Tools (MCP/Bash) to execute
     ↓
5. Agent reports back to Command, which updates State for User
```

> **Philosophy:** Trust the AI's **Native Reasoning** (Agent) but verify it against your **Documented Protocol** (Skill), all while maintaining the **User's Context** (Command). This separation prevents "Prompt Bloat" and makes the system modular and easy to debug.

---

## VI. State vs. Configuration

### User Configuration (`.claude/*.local.md`)
- **Purpose:** User preferences, feature flags
- **Persistence:** Long-term, user-managed
- **Format:** YAML Frontmatter + Markdown body
- **Example:** Enabling "Strict Mode" for a security plugin

### Runtime State (`.cattoolkit/`)
- **Purpose:** Agent memory, execution logs, plan status
- **Persistence:** Session or Project duration, Agent-managed
- **Format:** JSON, Markdown logs, Status files
- **Example:** Tracking files scanned in a swarm operation

**Rule:** Agents generally *read* Configuration but *write* Runtime State.

---

## VII. Best Practices

### For Commands (Intent Envelopes)

**DO:**
- Accept natural language via `$ARGUMENTS`
- Trust agent intelligence
- Gather context with `!` bash execution
- Delegate quickly to specialized agents

**DON'T:**
- Parse rigid positional arguments
- Pre-validate state externally
- Micromanage execution steps
- Build state tracking caches

### For Agents (Contextual Personas)

**DO:**
- Define clear `tools` restrictions for safety
- Provide examples in `description` for trigger accuracy
- Operate autonomously once spawned
- Use SlashCommand tool for standardized workflows

**DON'T:**
- Use AskUserQuestion (execution phase)
- Assume specific command invoked the agent
- Leak internal reasoning to main thread
- Over-complicate with decision trees

### For Skills (Procedural Lenses)

**DO:**
- Write in imperative/infinitive form
- Use third-person descriptions for discovery
- Keep SKILL.md focused (<500 lines)
- Move heavy content to `references/`

**DON'T:**
- Execute workflows (passive only)
- Include AskUserQuestion
- Use absolute paths
- Prescribe specific tool usage

---

## VIII. Anti-Patterns

### 1. CLI Tool Thinking
**Problem:** Building JSON caches, pre-validating state, micromanaging execution.

**Solution:** Trust agent intelligence. Delegate with natural language. Let agents determine state.

### 2. Rigid Argument Parsing
**Problem:** `argument-hint: [type] [name] [intent]`

**Solution:** `argument-hint: [natural language request]` with `$ARGUMENTS`.

### 3. Black Box Assumption
**Problem:** Treating agents as completely isolated processes.

**Solution:** Understand agents report back to orchestrators. Use phase boundaries.

### 4. Over-Prescription
**Problem:** "Run ls, then grep, then parse output..."

**Solution:** "Find the authentication controller in the codebase."

---

## IX. Success Criteria

A well-designed toolkit:
- ✅ Natural language everywhere
- ✅ Commands are minimal Intent Envelopes
- ✅ Agents are trusted Contextual Personas
- ✅ Skills provide Procedural Lenses
- ✅ No external state tracking caches
- ✅ True autonomous execution

---

## See Also

- **Core Laws:** See [CLAUDE.md §VIII](../CLAUDE.md#viii-core-laws) for architectural laws
- **Architecture Patterns:** See [docs/VECTOR_vs_TRIANGLE.md](VECTOR_vs_TRIANGLE.md) for pattern mechanics
- **Frontmatter Standards:** See [docs/FRONTMAKER.md](FRONTMAKER.md) for component configuration
- **Portability Rules:** See [docs/PORTABILITY.md](PORTABILITY.md) for file path standards
