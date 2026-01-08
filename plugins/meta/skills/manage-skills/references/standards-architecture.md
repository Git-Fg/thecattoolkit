# Architectural Standards

## 1. The Core Philosophy: Knowledge vs. Execution
*   **Skills are Passive:** They are encyclopedias. They contain templates, patterns, and rules. They **NEVER** contain logic flow (`if/then`), user interaction (`AskUserQuestion`), or routing instructions.
*   **Commands are Orchestrators:** They define the *Intent* and gather the *Context*. They wrap the request in an "Envelope" and dispatch it.
*   **Agents are Executors:** They are intelligent workers. They read the Skill (Knowledge) and the Envelope (Context) to determine their own workflow dynamically.

## 2. The Interaction Patterns

### The Sovereign Vector (Interactive/Fast)
**Structure:** `Command -> Main Chat`
*   **Use Case:** Quick scaffolding, clarifying questions, "thinking" tasks.
*   **Constraint:** Execution happens in the main context window.
*   **Context Cost:** High (pollutes history).

### The Sovereign Triangle (Autonomous/Deep)
**Structure:** `Command -> Subagent -> Skill`
*   **Use Case:** Coding, Auditing, Refactoring, Planning.
*   **Constraint:** The Subagent works in isolation.
*   **Async/Background:** The Command MUST NOT wait. It launches the agent and reports the `Task ID`.
*   **Context Cost:** Zero (fresh window).

## 3. Directory Structure (Canonical)
All plugins must follow this strict hierarchy:

```text
plugin-name/
├── .claude-plugin/plugin.json  # Metadata
├── commands/                   # The Entry Points (.md files)
├── agents/                     # The Executors (.md files)
├── skills/                     # The Knowledge Base (directories)
│   └── skill-name/
│       ├── SKILL.md            # Capability Index (No Routing!)
│       ├── assets/             # Passive Templates/Schemas
│       └── references/         # Rules & Standards
└── hooks/                      # Governance (Python scripts)
```

## 4. The "No Workflow" Rule
Do not create `workflows/` directories.
*   **Bad:** A file saying "Step 1: Open file. Step 2: Read line."
*   **Good:** A file saying "Standard: All files must start with a header." (The Agent figures out *how* to apply the standard).

## 5. Naming Standards

### Skill Name Rules
- **Format:** `lowercase-with-hyphens` (kebab-case)
- **Length:** Maximum 64 characters
- **Matching:** Must match directory name exactly
- **Prefixes:** Use descriptive prefixes like `create-*`, `manage-*`, `setup-*`, `generate-*`, `build-*`

### Naming Decision Logic
| Context | Naming Pattern |
|---------|---------------|
| Task execution | `{action}-{object}` (e.g., `process-pdfs`, `validate-input`) |
| Lifecycle management | `manage-{component}` (e.g., `manage-skills`, `manage-commands`) |
| Knowledge base | `{domain}-patterns` or `{domain}-expertise` (e.g., `react-patterns`) |
| Planning | `create-{artifact}` (e.g., `create-plans`, `create-prompts`) |

## 6. Template Selection Standards

### Template Decision Matrix
| Condition | Template |
|-----------|----------|
| Single workflow, under 200 lines | `minimal.md` |
| Action-oriented task execution | `task-execution.md` |
| 4+ distinct workflows requiring routing | `router-pattern.md` |
| Exhaustive domain knowledge with full lifecycle | `domain-expertise.md` |
| Detailed knowledge in separate references | `progressive-disclosure.md` |

### Template Selection Logic
```
IF single workflow + minimal knowledge
  → Use `minimal.md` template

ELIF action-oriented task execution
  → Use `task-execution.md` template

ELIF 4+ distinct workflows requiring routing
  → Use `router-pattern.md` template

ELIF exhaustive domain knowledge covering full lifecycle
  → Use `domain-expertise.md` template

ELIF detailed knowledge in separate references
  → Use `progressive-disclosure.md` template
```
