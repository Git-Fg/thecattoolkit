# Architectural Primitives: Vector, Triangle, & Time-Server

Pattern mechanics and selection guide for The Cat Toolkit.

> **See also:** [docs/AI-ARCHITECTURE.md](AI-ARCHITECTURE.md) for the philosophy of leveraging native AI agent intelligence.

---

## The Core Problem: Context Rot & Fresh Intelligence

We leverage fresh context for maximum AI intelligence while managing context cost:

- **The 50% Cliff:** Reasoning degradation accelerates past 50% context
- **Attention Dilution:** More tokens = harder to attend to specific instructions
- **Lost-in-the-Middle:** Instructions buried in long contexts get ignored

**Solution:** Treat fresh context as a scarce resource.

---

## Pattern Mechanics

### Vector (Hot Path)
**Composition:** `Command + Skill`

Executes inside current context window. Interacts with user directly.

**When to use:**
- Context <30%
- User guidance needed (AskUserQuestion)
- Surgical task (<5 files)
- User wants to see reasoning

**Risk:** Pollutes history, accelerates Context Rot.

### Triangle (Cold Path)
**Composition:** `Command → Agent → Skill`

Command uses **Task tool** to launch agent in a new branch of context which don't reduce attention capacity of main Ai Agent.

**When to use:**
- Context >50%
- Heavy task (>10 files)
- Fire-and-forget (no user input)
- Output matters, not process


### Swarm (Parallel Triangle)
**Composition:** `Command → [Agent A, B, C] → Skill`

Multiple specialized agents simultaneously.

**When to use:**
- Search/audit large repo (split by directory)
- Mass refactor (batch by 10 files)
- Voting/consensus (merge feedback)

**Physics:**
- 5 agents searching 5 dirs = 1/5th time
- Zero context bleed (enforced modularity)
- Shared-Nothing: If Agent A needs Agent B's output → cannot parallelize

**Native Syntax:** Command instructs Claude: *"Launch X agents in parallel to do Y."* or "spawn X async subagents to do Y." Claude natively understands this instruction.

### Time-Server (Async)
**Composition:** `Command → Async Agent → Poll → Result`

Background execution with `run_in_background: true`.

**When to use:**
- Tasks >1 minute
- Side effects are the goal (file creation, deployment)
- External dependencies (CI, deploy)

**Flow:**
1. Launch with `Task(..., run_in_background=True)`
2. Command acknowledges: "Started task [ID]"
3. Poll `TaskOutput` or check artifact
4. Read result when complete

---

## Component Roles

### Commands: Prompt Definitions
Provide instructions FOR Claude that transform vague requests into orchestrated workflows.

```
User: "fix the auth"
    ↓ Command instructs Claude
"Analyze the authentication flow in src/auth/.
Identify the source of the login failures.
Fix any security vulnerabilities found.
Report what was changed."
```

### Agents: Autonomous Specialists
Triggered via Task tool based on `description` frontmatter. Fresh context (0% Context Rot).

**The Autonomy Principle:** Agent must work without Command if given the right context and skills. Agents operate autonomously with full intelligence.

### Skills: Passive Knowledge Base
Accessible equally to Main Thread and Agents. Read-only. Auto-loaded when listed in agent frontmatter.

---

## Pattern Selection Decision Tree

```
Is user input needed during task?
├─ Yes → Vector
└─ No → Is context >50%?
        ├─ Yes → Triangle
        └─ No → Is task heavy (>10 files)?
                ├─ Yes → Triangle
                └─ No → Is task >1 min?
                        ├─ Yes → Time-Server
                        └─ No → Vector
```

**Swarm addition:** Can task be split into non-overlapping parts?
- Yes → Swarm
- No (dependencies exist) → Serial Triangle

---

## Quick Examples

| Scenario | Pattern | Why |
|:---------|:--------|:----|
| Quick evaluation, early brainstorming | Vector | Interactive, user guidance |
| Major decision, complex analysis | Triangle | Clean context, comprehensive |
| Full test suite (5-10 min) | Time-Server | Non-blocking |
| Audit 200-file codebase | Swarm | Split by module, parallel |
| Find single bug in known file | Vector | Surgical, fast |

---

## Implementation Rules

**Critical Violations:**
- Commands duplicating agent analysis logic
- Skills containing AskUserQuestion or execution steps
- Agents using AskUserQuestion (execution phase)
- Hardcoded absolute paths
- Mixing Vector and Triangle in same command

**Path Standards:**
```
Within Skill:     references/strategic.md ✅
Cross-Component:  "from the planning skill" ✅
Absolute:         plugins/x/skills/y/... ❌
Exit-Relative:    ../../../other-skill/... ❌
```

---

## Reference

- **CLAUDE.md** - Full architectural standards and forbidden patterns
- **README.md** - Installation and marketplace
