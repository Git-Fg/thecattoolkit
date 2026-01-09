# Implementation Guide & Specs

## 1. Directory Structure (Standard Plugin Layout)

```text
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Manifest (Required)
├── commands/                # Orchestration Workflows
├── agents/                  # Personas (System Prompts)
├── skills/                  # Capabilities (Forked Contexts)
├── hooks/                   # Lifecycle Automation
│   └── hooks.json
└── .mcp.json                # MCP Configuration
```

## 2. Component Configuration

### Agents (`agents/*.md`)
Defines **Who** is working.
```yaml
---
name: senior-engineer
description: "A careful, experienced TypeScript engineer."
tools: [Read, Write, Bash] # Whitelist of CAPABILITIES
skills: [typescript-best-practices] # Pre-loaded skills
---
```

### Skills (`skills/*/SKILL.md`)
Defines **What** is being done.
```yaml
---
name: refactor-module
description: "Refactors a legacy module to modern patterns."
context: fork              # Runs in isolation
agent: senior-engineer     # Uses the persona above
user-invocable: true       # Creates /refactor-module
allowed-tools: [Read, Write] # Runtime RESTRICTION
---
```

## 3. Configuration Scopes

| Scope | Location | Use Case |
|:---|:---|:---|
| **User** | `~/.claude/settings.json` | Global preferences. |
| **Project** | `.claude/settings.json` | Team standards. |
| **Plugin** | `.claude-plugin/plugin.json` | Distributable logic. |

## 4. Testing & Validation

### Validate hooks.json

```bash
python3 plugins/meta/skills/manage-hooks/assets/scripts/hook-tester.py hooks.json
```

**Checks:**
- Valid hook events
- Required fields present
- JSON syntax
- Matcher patterns

### Check Command Structure

```bash
# Verify frontmatter
grep -E "^---$" commands/*.md

# Check required fields
for file in commands/*.md; do
  if ! grep -q "description:" "$file"; then
    echo "Missing description: $file"
  fi
done
```

### Verify Skill Structure

```bash
# Check SKILL.md exists
find skills -name "SKILL.md" -type f

# Verify frontmatter
for skill in skills/*/SKILL.md; do
  if ! grep -q "name:" "$skill"; then
    echo "Missing name: $skill"
  fi
done
```

## 5. Permission System Deep Dive

### `tools` vs `allowed-tools`: Critical Difference

| Aspect | `tools` (Agents) | `allowed-tools` (Commands/Skills) |
|:-------|:-----------------|:----------------------------------|
| **Purpose** | Whitelist - defines what agent CAN use | Whitelist - restricts execution to ONLY these tools |
| **Default Behavior** | Inherits ALL tools if omitted | No restriction if omitted |
| **Security Impact** | CRITICAL - determines agent capabilities | Important - runtime restrictions |

#### **Agent Tool Inheritance (CRITICAL)**

```yaml
# ❌ DANGEROUS - Agent inherits ALL tools
---
name: simple-reader
description: "Reads files safely"
# tools field OMITTED
---

# Result: Agent can use ALL tools including:
# - Read, Write, Edit, Bash
# - AskUserQuestion
# - Task, Skill
# - All MCP tools
```

```yaml
# ✅ SECURE - Explicit restrictions
---
name: simple-reader
description: "Reads files safely"
tools: Read, Grep  # ONLY these tools
---

# Result: Agent CANNOT use Write, Edit, Bash, AskUserQuestion
```

## 6. Glue Code Detection & Removal

### The Single-Skill Wrapper Rule

**Check all `commands/*.md` files. If a command's only instruction is "Use the X skill", DELETE the command.**

Instead, go to `skills/X/SKILL.md` and ensure:
1. `user-invocable: true`
2. `context: fork`
3. `agent: [appropriate-persona]`

**Example Transformation:**

**BEFORE (Wrapper Command):**
```yaml
# commands/security-audit.md
---
description: "Analyze code for security issues"
---
Use skill: security-analyzer with $ARGUMENTS
```

**AFTER (Direct Skill):**
```yaml
# skills/security-analyzer/SKILL.md
---
name: security-analyzer
description: "Analyze code for security vulnerabilities"
context: fork
agent: security-expert
user-invocable: true
---
# Delete commands/security-audit.md
```

### The 10-Line Rule

> **If a wrapper is >10 lines with no business logic, it's over-engineered. If it's <3 lines, it's definitely glue code.**

**Rule:** Any Command file that contains *only* a `Task()` call pointing to a single Skill should be refactored into a Forked Skill.

### Refactoring Strategy: Command → Forked Skill

**BEFORE (Deprecated Pattern):**
```yaml
# commands/analyze-security.md
---
description: "Analyze code for security issues"
allowed-tools: [Task]
---

Task(
  description="Security analysis: $ARGUMENTS",
  prompt="Analyze the codebase for security vulnerabilities...",
  subagent_type="security-analyzer",
  skills=["security-standards"]
)
```

**AFTER (Unified Capability Pattern):**
```yaml
# skills/security-analyzer/SKILL.md
---
name: security-analyzer
description: |
  USE when analyzing security vulnerabilities in codebases.
  Scans for common security issues including SQL injection, XSS, and authentication flaws.
  Keywords: security audit, vulnerability scan, code analysis
context: fork
agent: security-reviewer
user-invocable: true
allowed-tools: [Read, Grep, Bash]
---

# Operational Protocol
1. Scan codebase for security vulnerabilities
2. Generate detailed security report
3. Provide remediation recommendations
```

**Migration Steps:**
1. Copy Command's `description` → Skill's `description`
2. Add `context: fork` to run in isolation
3. Add `agent: [name]` for persona binding
4. Ensure user-invocable (defaults to true) if it was user-facing
5. Move `allowed-tools` from Command to Skill
6. Delete the Command file

## 7. Hooks Configuration

### Valid Hook Events (Execution Order)

1. `SessionStart` - New session begins
2. `UserPromptSubmit` - Before prompt processing
3. `PreToolUse` - Before tool execution
4. `PermissionRequest` - Permission dialog shown
5. `PostToolUse` - After tool success
6. `Notification` - System notifications
7. `Stop` - Main agent finishes
8. `SubagentStop` - Subagent finishes
9. `PreCompact` - Before compact operation
10. `SessionEnd` - Session ends

### Hook Input/Output Format

**Input (JSON via stdin):**
```json
{
  "session_id": "abc123",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
```

**Valid Outputs:**

1. **Exit code only:**
   - `0` = Success
   - `2` = Block action

2. **JSON with exit code 0:**
```json
{
  "continue": true,
  "systemMessage": "Operation completed",
  "hookSpecificOutput": {
    "permissionDecision": "allow"
  }
}
```

## 8. MCP & Endpoint Config

### MCP Servers (`.mcp.json`)
Manage external tools (Database, Browser, etc.).
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://..."]
    }
  }
}
```

### MCP Security (Critical)

```yaml
# ✅ Good: Specific domain restrictions
allowedMcpServers:
  - serverUrl: "https://api.githubcopilot.com/mcp/"
  - serverUrl: "https://mcp.company.com/api/*"
  - serverCommand: ["npx", "-y", "@company/approved-package"]

# ❌ Bad: Wildcard access
allowedMcpServers:
  - serverUrl: "*"
```

### Unofficial Endpoints (Zai/Minimax)
The runtime is agnostic. Set environment variables to bridge the gap:
```bash
export ANTHROPIC_BASE_URL="https://api.zai.chat/v1"
export ANTHROPIC_API_KEY="sk-..."
```

**Zai Code (Z.ai / GLM):**
```bash
export ANTHROPIC_BASE_URL="https://api.z.ai/v1"
export ANTHROPIC_API_KEY="your-zai-key"
```

**Minimax Code (MiniMax-M2):**
```bash
export ANTHROPIC_BASE_URL="https://api.minimax.chat/v1/text/chat"
export ANTHROPIC_API_KEY="your-minimax-key"
```

### Unified Configuration (`.claude/settings.json`)

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.z.ai/v1",
    "ANTHROPIC_CUSTOM_HEADERS": {
      "X-Provider-Name": "Zai"
    }
  },
  "default_model": "glm-4.5"
}
```

## 9. When to use Commands vs Agents vs Forked Skills

| Component | Use When | Avoid When |
|:----------|:---------|:-----------|
| **Forked Skill** | Single atomic capability with optional persona binding | Orchestrating multiple phases |
| **Command** | Managing multi-phase workflows (Skill A → Skill B → Skill C) | Wrapping single Skills (use Forked Skill instead) |
| **Agent** | Defining reusable **specialized persona** used by multiple Skills | Generic tool restrictions (use allowed-tools instead) |

**Decision Tree:**

1. **Is this a single atomic task?**
   - YES → Make it a Forked Skill (user-invocable by default)
   - NO → Continue to step 2

2. **Does it require multiple phases?**
   - YES → Use a Command to orchestrate multiple Skills
   - NO → Make it a simple Forked Skill

3. **Does the agent define a specialized persona?**
   - YES (detailed system prompt, specific role, unique tone) → **Keep as separate Agent**
   - NO (generic instructions, only tool restrictions) → Delete agent, use `allowed-tools` in Skill

4. **Is the persona reused across multiple Skills?**
   - YES → Keep as separate Agent
   - NO → Inline into Skill as `context: fork` with `allowed-tools`

**Key Principle:**
- **Skills** define the **Task** (procedural knowledge)
- **Agents** define the **Persona** (identity, tone, role)
- **Commands** define the **Workflow** (orchestration)
