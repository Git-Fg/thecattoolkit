/// WARNING CRITICAL: AGENTS ARE RUNTIME CONFIGURATION ONLY (2026 PHILOSOPHY) ///

**Agents are NOT for:**
- BAD Persona-based instruction (use Skills with protocols)
- BAD Workflow orchestration (use Skills)
- BAD Domain knowledge (use Skills)

**Agents ARE for:**
- GOOD Tool/permission scoping (runtime configuration)
- GOOD Skill injection (preload required capabilities)
- GOOD Hook configuration (event-driven automation)

**95% of the time: Use Skills (with `context: fork` for isolation)**
 
### WARNING The Subagent Crisis (2026 Warning)
**CRITICAL:** Subagents incur a ~20,000 token startup cost per spawn and consume 1 "Prompt" quota (on subscription models). Use `context: fork` (~3x inline cost) for isolation instead.
 
# Agents (Runtime Configuration Only)

An Agent is a **configuration-only** runtime environment for tool/permission scoping.

## Quick Reference (Cat Toolkit Specific - 2026)

### 1. Anatomy (`agents/*.md`)

#### Frontmatter (Complete Configuration)
```yaml
---
name: code-reviewer
description: Config-only agent for code review tool scoping
tools: [Read, Grep, Edit]              # Whitelist
skills: [code-quality-standards]       # INJECTION: Preload capabilities
permissionMode: acceptEdits            # AUTONOMY: Write without confirmation
hooks:                                  # EVENT: Run validation on edits
  PostToolUse:
    - agent: linter
      condition: edit.completed
---
```

#### Agent Body (Minimal)
**2026 Standard: No persona content in agent files**

```markdown
# Code Reviewer Agent

## Purpose
Configuration-only agent for scoped code review operations.

## Tool Access
- Read: Source code analysis
- Grep: Pattern searching
- Edit: Apply fixes

## Preloaded Skills
- code-quality-standards: Quality criteria and patterns

## Operations
Auto-accepts edits for linting fixes. Requires confirmation for logic changes.
```

**Why This Works:**
- **Clear configuration**: Tools and permissions explicit
- **No persona bloat**: No "You are a senior engineer" narrative
- **Skill injection**: Preloads domain knowledge
- **Event-driven**: Hooks for automation

**Legacy Pattern (Deprecated):**
```markdown
# DO NOT USE THIS PATTERN
## Persona
You are a Senior Software Engineer with 15 years of experience...

## Responsibilities
- Review code for quality issues
- Suggest improvements...
```

**Reason for Deprecation:**
- Persona content belongs in **Skills** (as protocols), not Agents
- Agents should be pure configuration files
- Reduces token overhead and improves clarity

### 2. Agent Selection

Agents **can be auto-discovered** by the model, but 2026 philosophy prefers Skills for most use cases.

Invocation methods:
- Tool calls: `Task(agent-name)` - Explicit invocation
- Model selection: Via `description` field - Auto-discovery (discouraged in 2026)
- Command delegation: Command creates agent
- Fork configuration: `context: fork` with `agent: agent-name`

**For model-discoverable capabilities, use Skills instead.**

### 3. Skill Injection (Configuration)

**Purpose:** Preload domain knowledge into agent at startup.

**Configuration:**
```yaml
skills: [security-protocols, code-quality-standards]
```

**Effect:** Loads SKILL.md content into agent's system prompt.

**When to Use:**
- GOOD Agent requires specific domain knowledge
- GOOD Agent needs consistent protocol adherence
- GOOD Skill is too large for inline inclusion

**Cost Consideration:**
- Each injected skill adds to agent's token cost
- Use sparingly (prefer `context: fork` for heavy skills)

### 4. Interaction Strategies

*   **Subagent (Delegation):** Called via the `Task` tool. Blocks the main interface (Foreground).
*   **Recursive Handoff:** An agent can create a context file and ask the user to launch another agent ("Swarm" Pattern).
*   **LSP Access:** By default, the agent inherits the `LSP` tool (unless `tools:` is restrictive and omits it). Remember to add `LSP` to `tools:` for code agents.

### 5. Persistence & Resume

Subagent context persists on disk (session-scoped).
1.  **Requirement:** You must use `claude --continue` (or `--resume`) to recover the session state after a restart.
2.  **Resuming:** Use natural language. "Continue the work of the previous code-reviewer agent."
3.  **IDs:** Claude assigns a `subagentId` (visible in transcripts). You can use this ID to be explicit: "Resume subagent `123-abc`."

### 6. Advanced Configuration

*   **`permissionMode` options:**
    *   `default`: Ask user.
    *   `acceptEdits`: Auto-accept file modifications (Linting/Formatting).
    *   `dontAsk`: Fail if permission is needed (Strict automated agents).
    *   `bypassPermissions`: **DANGEROUS**. Skips all checks. Use only for internal trusted tools.
*   **`disallowedTools`:** Blacklist approach. "Everything except `Bash`" -> `disallowedTools: ["Bash"]`.
*   **`hooks` (Local):** Define hooks directly in the agent markdown (e.g., `once: true` init scripts).

### 7. Configuration Patterns (2026)

#### The Permission-Scoped Agent
**Purpose:** Restrict tool access for safety.

```yaml
---
name: read-only-analyzer
tools: [Read, Grep, Glob]
permissionMode: dontAsk
skills: [analysis-protocols]
---
```

#### The Skill-Preloading Agent
**Purpose:** Inject domain knowledge at startup.

```yaml
---
name: domain-specialist
tools: [Read, Write, Bash]
skills: [domain-protocols, quality-standards]
---
```

#### The Hook-Configured Agent
**Purpose:** Automate validation workflows.

```yaml
---
name: auto-linter
tools: [Edit, Bash]
permissionMode: acceptEdits
hooks:
  PostToolUse:
    - command: npm run lint
      condition: edit.completed
---
```

**Anti-Patterns (Avoid):**
- BAD Agents with persona content ("You are a senior engineer...")
- BAD Agents for simple skill isolation (use `context: fork` instead)
- BAD Multi-agent orchestration (use Orchestrator Skills)

---

## Alternative: Skills with Fork

For 95% of use cases where you might consider an agent, use a **Skill with `context: fork`** instead.

### Cost Comparison

| Approach | Context Cost | Use Case |
|:--------|:-------------|:---------|
| **Inline Skill** | 1× | Simple operations |
| **Fork Skill** | 3× | Isolation, heavy processing |
| **Agent** | 2×N | Permission scoping only |

### Example: Migration from Agent to Fork

**Before (Agent):**
```yaml
# agents/processor.md
---
name: file-processor
tools: [Read, Write, Bash]
skills: [processing-protocols]
---

# Persona content (deprecated)
You are a file processing specialist...
```

**After (Fork Skill):**
```yaml
# skills/file-processor/SKILL.md
---
name: file-processor
description: Processes large file batches with isolation. Use when handling >10 files.
context: fork
tools: [Read, Write, Bash]
---

## Processing Protocol

1. Read input files
2. Apply transformations
3. Validate outputs
4. Report results
```

**Benefits:**
- Model-discoverable (via description)
- No persona bloat
- Lighter than agent (3 vs 2×N)
- Same isolation benefits

---

## Quick Reference Checklist

### Agent Design Checklist (2026)

**Before deploying an agent, verify:**

**Configuration**
- [ ] Tools appropriately scoped (allowlist defined)
- [ ] Permission mode or disallowedTools set (security boundaries)
- [ ] Skills injected if domain knowledge needed
- [ ] Hooks configured for automation if needed

**Security**
- [ ] Explicit security boundaries defined
- [ ] No persona content in agent body
- [ ] Protocol content moved to Skills
- [ ] Tool access follows least privilege

**Integration**
- [ ] Agent invoked via explicit tool call or command
- [ ] Skill references use protocols, not personas
- [ ] Context fork considered as alternative
- [ ] Error handling implemented

**Quality**
- [ ] Agent is config-only (not a persona wrapper)
- [ ] Considered if Skill with fork could work instead
- [ ] Tested in isolation
- [ ] Performance acceptable

**Remember:** 95% of the time, use Skills (with `context: fork` for isolation) instead of Agents.
