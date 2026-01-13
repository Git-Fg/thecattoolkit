# Agents (Autonomous Workers)

An Agent is a specialized instance with its own execution loop.

## 1. Anatomy (`agents/*.md`)

### Frontmatter
```yaml
---
name: code-reviewer
description: ...              # See Triggering section
model: inherit                # or 'haiku'
tools: ["Read", "Edit"]       # Whitelist
permissionMode: acceptEdits   # AUTONOMY: Write without confirmation
skills: [my-standards]        # INJECTION: Required capabilities
---
```

### System Prompt (The 5 Pillars)
The Markdown body MUST define the "Brain" of the agent following this strict structure:
1.  **Persona:** "You are a Senior Engineer..." (Identity + Authority).
2.  **Responsibilities:** Bullet list of exactly what is in scope.
3.  **Process (Workflow):** Textual Algorithm. "1. Read. 2. Think. 3. Act."
4.  **Quality Standards:** "Do not remove comments. Keep indentation."
5.  **Output Format:** "Return a JSON object" or "Markdown report".

## 2. Triggering (The Art of Example)

For an agent to launch proactively, `<example>` blocks are required.

```xml
<example>
Context: User pushed a commit.
user: "Check this."
assistant: "I'll use the code-reviewer agent."
<commentary>Triggering reviewer on vague request.</commentary>
</example>
```

## 3. Skill Integration Strategies

How does an Agent get smart?

1.  **Implicit Discovery (Costly):** The agent searches for tools. Slow.
2.  **Explicit Injection (`skills: [...]`):**
    *   *Usage:* `skills: [code-standards]` in frontmatter.
    *   *Effect:* Loads the `SKILL.md` content into the Agent's system prompt at startup. **Vital** for core constraints.
3.  **Context Forking:**
    *   A Skill can "become" an agent if defined with `context: fork`.

## 4. Interaction Strategies

*   **Subagent (Delegation):** Called via the `Task` tool. Blocks the main interface (Foreground).
*   **Recursive Handoff:** An agent can create a context file and ask the user to launch another agent ("Swarm" Pattern).
*   **LSP Access:** By default, the agent inherits the `LSP` tool (unless `tools:` is restrictive and omits it). Remember to add `LSP` to `tools:` for code agents.

## 5. Persistence & Resume

Subagent context persists on disk (session-scoped).
1.  **Requirement:** You must use `claude --continue` (or `--resume`) to recover the session state after a restart.
2.  **Resuming:** Use natural language. "Continue the work of the previous code-reviewer agent."
3.  **IDs:** Claude assigns a `subagentId` (visible in transcripts). You can use this ID to be explicit: "Resume subagent `123-abc`."

## 6. Advanced Configuration

*   **`permissionMode` options:**
    *   `default`: Ask user.
    *   `acceptEdits`: Auto-accept file modifications (Linting/Formatting).
    *   `dontAsk`: Fail if permission is needed (Strict automated agents).
    *   `bypassPermissions`: **DANGEROUS**. Skips all checks. Use only for internal trusted tools.
*   **`disallowedTools`:** Blacklist approach. "Everything except `Bash`" -> `disallowedTools: ["Bash"]`.
*   **`hooks` (Local):** Define hooks directly in the agent markdown (e.g., `once: true` init scripts).

## 7. Patterns (Cookbook)

### The "Agent Swarm" Pattern (File Data Bus)

**Problem:** Subagents need to share complex context (architecture decisions, database schema) but don't share memory.
**Solution:** Explicit File Handoff.

1.  **The Architect (Main Agent):**
    *   Writes a `handoff/context.md` file with the global plan.
2.  **The Specialist (Subagent):**
    *   Is triggered with an instruction: "Read `handoff/context.md` first."
    *   Performs its task (e.g., "Write SQL").
    *   Writes its output to `handoff/db-result.md`.
3.  **The Loop:**
    *   The Architect reads `handoff/db-result.md`.
    *   Updates `handoff/context.md` for the next agent (e.g., the Frontend Specialist).
    *   *Result:* Clear, traceable state on disk used as a "Data Bus" between isolated agents.

