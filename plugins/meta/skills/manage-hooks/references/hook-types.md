# Hook Events & Matchers Specification

## 1. Matcher Syntax (JS Regex)

Matchers filter which tools trigger a hook using `new RegExp(pattern).test(toolName)`.

| Pattern | Meaning | Example Matcher |
|---------|---------|-----------------|
| `Exact` | Match single tool | `"matcher": "Bash"` |
| `OR` | Multiple tools | `"matcher": "Write\|Edit"` |
| `Prefix` | Starts with | `"matcher": "^Bash"` |
| `MCP` | MCP server/tool | `"matcher": "mcp__server__.*"` |
| `All` | Match everything | Omit `"matcher"` field |

---

## 2. event Reference

### PreToolUse
- **Fires**: Before execution.
- **Can Block**: Yes.
- **Input**: Tool name and input arguments.
- **Output**: `approve` | `block` | `updatedInput`.

### PostToolUse
- **Fires**: After execution.
- **Can Block**: No.
- **Input**: Tool input + `tool_output`.
- **Output**: `systemMessage`.

### UserPromptSubmit
- **Fires**: On user input submission.
- **Can Block**: Yes.
- **Input**: `prompt` string.

### Stop / SubagentStop
- **Fires**: When Claude/Agent attempts to finish.
- **Can Block**: Yes.
- **Input**: `stop_hook_active` (Check to avoid loops).

### SessionStart / SessionEnd
- **Fires**: At session lifecycle boundaries.
- **Use**: Inject context (Start) or archive transcripts (End).

---

## 3. MCP Naming Convention
Format: `mcp__{server}__{tool}`

- **Match server**: `mcp__github__.*`
- **Match tool type**: `mcp__.*__write.*`
