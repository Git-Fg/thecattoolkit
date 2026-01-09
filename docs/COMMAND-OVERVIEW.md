# Command Standards: Reusable Prompts

## 1. Philosophy: Commands are Prompts

In the Agentic Runtime, a Command is an **Instruction FOR Claude**, not a message TO the user. It is a Markdown file whose content becomes Claude's internal mission statement for the current turn.
1.  **Gathers Context:** Uses `!bash` to get the ground truth from the environment.
2.  **Captures Intent:** Injects the user's natural language requirements via `$ARGUMENTS`.
3.  **Delegates (The Task Tool):** Instructs the Main Agent to solve the problem, often by spawning specialized agents in parallel via the `Task` tool.

> **The Law of Native Delegation:** Never write in code what can be described in intent.

---

## 2. Anatomy of a Command

Location: `plugins/<plugin-name>/commands/<command-name>.md`

```markdown
---
description: Natural language description for AI discovery
argument-hint: [string] # Optional: UI documentation hint only
---

# Context
!ls -R src/  # Example: Get ground truth

# Instruction
Standardize on the **Parallel Agent Pattern** to handle complexity.
Launch 3 agents **in parallel** via the `Task` tool. Each agent should focus on a specific sub-problem (e.g. logic, tests, docs).
Pass the user's requirements: rules: $ARGUMENTS

**The Task Tool:** Commands guide the Main Agent, which then invokes the `Task` tool to spawn subagents. Subagents return their results to the Main Agent for final synthesis.

---

## 3. Rules & Standards

### ✅ DO: Use `$ARGUMENTS` for Everything
Native intelligence can parse "fix the login button" better than you can regex it.
- **Good:** "Launch agent to fix $ARGUMENTS"
- **Bad:** Rigid argument parsing (e.g., `$1`, `$2`) or fixed positional schemas.

### ❌ DON'T: Use Rigid Positional Parsing
Claude Code does not enforce rigid positional parsing from a frontmatter `args:` list.
- **Anti-Pattern:** Building complex `!bash` find/grep chains in the command itself to handle rigid inputs.
- **Native Pattern:** Accept `$ARGUMENTS` and let the agent's native intelligence determine the file paths/actions.

### ❌ DON'T: Use XML for Prompt Structure
Do not use tags like `<assignment>`, `<context>`, or `<instruction>` to structure your Command file. The Agentic Runtime is optimized for **Markdown**.

*   **Bad:** `<context>Here is the file list...</context>`
*   **Good:** `# Context` followed by `!ls -la`

XML tags in Commands should *only* be used if you are teaching the agent how to generate XML outputs (see **The XML Signaling Pattern** in Hooks).

### Real Pattern Example
The `/commit` command serves as a perfect template:

```markdown
# Context
!git diff --staged

# Instructions
Based on the changes above, write a conventional commit message.
```

---

## 4. Tool Restrictions
Commands can use the `allowed-tools` frontmatter to enforce safety or focus. This restriction cascades: if the Main Agent is restricted to `[Read, Grep]`, any subagents it spawns via the `Task` tool will inherit these restrictions.

```yaml
---
description: Read-only codebase explorer
allowed-tools: [Read, Grep, LS, find]
---
```

---

## 5. The "Skill Tool" Recursive Pattern
Agents can invoke Commands via the `Skill` tool. This is how we build complex workflows from simple primitives.
- An Agent handling a feature can call `/commit` to save its work.
- An Agent debugging can call `/test` to verify.

This turns your Commands into the **"Standard Library"** for your Agents.

> **Note:** The `SlashCommand` tool has been deprecated and merged into the `Skill` tool.
