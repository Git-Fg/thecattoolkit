# Slash Command Syntax Guide

## 1. Frontmatter Reference

| Field | Type | Purpose | Required |
|-------|------|---------|----------|
| `description` | string | Command purpose (shown in `/help`) | **Yes** |
| `allowed-tools` | array | **Restrict** tool access (default: inherits all) | No |
| `argument-hint` | string | Autocomplete hint: `[optional] <required>` | No |
| `model` | string | Specific model (e.g., `claude-3-5-haiku-20241022`) | No |
| `disable-model-invocation` | boolean | Set `true` for user wrappers (prevents AI auto-call) | No |

### `allowed-tools` Patterns
- `[Read, Edit, Task]` - List of specific tools.
- `Bash(git status:*)` - Prefix-matched shell commands (required if using `!` logic).
- `WebFetch(domain:github.com)` - Domain-restricted fetching.

---

## 2. Arguments Reference

| Variable | Scope | Usage |
|----------|-------|-------|
| `$ARGUMENTS` | String | Captures all arguments as a single string |
| `$1, $2, $n` | Positional | Access specific arguments individually |
| `${ARGUMENTS:-.}` | Shell Default | Uses `.` if arguments are empty |

### Usage Patterns
- **File Reference**: `@ $ARGUMENTS` or `@ $1`
- **Dynamic Context**: `Current status: ! git status` (requires `Bash` in `allowed-tools`)
- **Bash Logic**: `! npm test && npm run deploy`

---

## 3. Semantic Categories

Cat Toolkit uses semantic naming for predictability and better AI routing.

| Category | Goal | Interface | Trigger Phrase |
|----------|------|-----------|----------------|
| **Verbs** | Load Skill | Load | "Shortcut to load the {skill} skill for {purpose}" |
| **Personas** | Delegate | Task | "[Personas] Delegate to {agent-name} for {purpose}" |
| **Objects** | Lifecycle | Manage | "Shortcut to load the {skill} skill for managing {object}" |
| **Execution** | Run Artifact | Run | "Shortcut to load the {skill} skill for executing {artifact}" |

### Wrapper Convention
Wrapper commands (Manually triggered by human, delegating to AI tools) MUST use:
- `disable-model-invocation: true`
- `allowed-tools: [Task]` (for Personas) or `allowed-tools: [Skill(skill_name)]` (for Verbs/Objects)
