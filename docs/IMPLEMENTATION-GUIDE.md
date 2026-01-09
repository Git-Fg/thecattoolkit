# Claude Code Implementation Guide
**Validated against Claude Code v2025+ documentation**

---

## Table of Contents

1. [Command Frontmatter Reference](#command-frontmatter-reference)
2. [Agent Configuration Reference](#agent-configuration-reference)
3. [Skill Structure Reference](#skill-structure-reference)
4. [Hooks Configuration Reference](#hooks-configuration-reference)
5. [Task Tool Usage](#task-tool-usage)
6. [Skill Tool Usage](#skill-tool-usage)
7. [Common Patterns](#common-patterns)
8. [Testing & Validation](#testing--validation)

---

## Command Frontmatter Reference

### Valid Fields

```yaml
---
description: "Natural language description for AI discovery"
argument-hint: "[description]"  # Optional: UI documentation hint
allowed-tools: [Read, Grep, Task]  # Restrict tools
model: claude-3-5-sonnet-20241022  # Optional: specific model
disable-model-invocation: true  # Optional: prevent programmatic invocation
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate.sh"
---
```

### Important Notes

- **`description`** is required and used for auto-discovery
- **`allowed-tools`** restricts tools (not enables them)
- **`disable-model-invocation`** blocks programmatic invocation via Skill tool but allows manual `/command`
- **`argument-hint`** is UI-only documentation, not functional

---

## Agent Configuration Reference

### Valid Fields

```yaml
---
name: my-agent
description: |
  WHEN TO USE: Complex code analysis tasks
  SPECIALIZES: Security vulnerability detection
  CONSTRAINTS: Read-only exploration
tools: Read, Grep, Glob, Bash  # Comma-separated list
model: sonnet  # sonnet, opus, haiku, or inherit
permissionMode: acceptEdits  # default, acceptEdits, dontAsk, bypassPermissions, plan
skills: security-analysis, code-review  # Skills to preload
hooks:
  PostToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "./analyze.sh"
---
```

### Tool Inheritance Rules

**If `tools` field is OMITTED:**
- Inherits ALL tools from main thread
- Includes AskUserQuestion, Skill, Task, etc.

**If `tools` field is SPECIFIED:**
- ONLY has access to listed tools
- Must explicitly include AskUserQuestion if needed
- More restrictive than allowed-tools

### Skills Access

**Subagents DO NOT automatically inherit Skills from main thread**

To give a subagent access to Skills:
```yaml
skills: [skill1, skill2, skill3]
```

**Built-in subagents** (Explore, Plan, general-purpose) **cannot use Skills**

---

## Skill Structure Reference

### Directory Structure

```
skill-name/
├── SKILL.md          # Required: Instructions + Metadata
├── assets/           # Optional: Templates, data files
├── references/       # Optional: On-demand documentation
└── scripts/          # Optional: Executable scripts
```

### Valid Frontmatter Fields

```yaml
---
name: my-skill
description: |
  USE when analyzing security vulnerabilities.
  Performs comprehensive security audit of codebases.
  Examples: Web security, authentication, data validation
allowed-tools: [Read, Grep]  # Restrict tools when Skill active
model: haiku  # Optional: specific model
context: fork  # Optional: run in isolated subagent context
agent: my-custom-agent  # Optional: bind to specific agent
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./security-check.sh"
user-invocable: false  # Optional: hide from slash menu
disable-model-invocation: true  # Optional: block programmatic invocation
---
```

### Progressive Disclosure

**Level 1 (Metadata)** - Startup:
- `name` + `description` (~100 tokens)

**Level 2 (Instructions)** - On activation:
- Full `SKILL.md` body (<5000 tokens)

**Level 3 (Resources)** - On-demand:
- `references/*.md` (unlimited)

---

## Hooks Configuration Reference

### Valid Hook Events

**Complete list in execution order:**

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

**❌ Fictitious events (DO NOT USE):**
- `SubagentStart` - Does not exist

### Hook Types

**Command Hooks** (`type: "command"`):
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ./format.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Prompt Hooks** (`type: "prompt"`):
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verify all tasks are complete: $ARGUMENTS"
          }
        ]
      }
    ]
  }
}
```

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

---

## Task Tool Usage

### Basic Delegation

```yaml
Task(
  description="Review authentication code",
  prompt="Analyze the auth module for vulnerabilities...",
  subagent_type="security-reviewer",
  model="sonnet",
  permissionMode="acceptEdits",
  skills=["security-analysis"]
)
```

### Resuming Subagent Conversations

**Initial delegation returns agentId:**
```yaml
Task(
  description="Phase 1 analysis",
  prompt="...",
  subagent_type="code-analyzer"
)
# Returns: agentId: "abc123"
```

**Resume with same context:**
```yaml
Task(
  description="Phase 2 continuation",
  prompt="...",
  subagent_type="code-analyzer",
  resume="abc123"
)
```

### Agent Sovereignty (Context Scoping)

**Subagents operate as "Focused Lenses" on the current session.**

They share the conversation history but adopt a specialized persona/system prompt. They are NOT "clean slate" sessions.

**What IS shared:**
- Session history (Read-only access to previous turns)
- Filesystem state
- MCP tools (Unless restricted via `tools`)

**What is SPECIALIZED (Not Shared):**
- **System Prompt**: Replaced by the agent's distinct persona
- **Skills**: Must be explicitly listed in `skills` field (no auto-inheritance to keep focus tight)
- **Permissions**: Defined by `tools` field (Least Privilege)

**Important:** Subagents **cannot spawn other subagents**

---

## Skill Tool Usage

### Invoking Commands

**Programmatic invocation:**
```yaml
Skill(/commit -m "Fix authentication bug")
```

**Permission syntax:**
- Exact: `Skill(/commit)`
- Prefix: `Skill(/review-pr:*)`
- Wildcard: `Skill`

### Invoking Skills

**Automatic discovery:**
- Based on `description` field matching
- No explicit invocation needed

**Programmatic invocation:**
```yaml
Skill(/security-review)  # If user-invocable: true
```

### disable-model-invocation

```yaml
---
name: internal-command
disable-model-invocation: true
---

# Blocks: Skill(/internal-command)
# Allows: /internal-command (manual)
```

---

## Common Patterns

### Pattern 1: Command Delegation

**Command reads context, delegates to agent:**

```yaml
---
description: "Execute project plan with context injection"
allowed-tools: [Task, Read]
---

Read PLAN.md and context files
Task(
  description="Execute: $ARGUMENTS",
  prompt="# Context\nPlan content injected here\n\n# Assignment\nExecute the plan.",
  subagent_type="director"
)
```

### Pattern 2: Context-Isolated Agent

**Agent with injected context:**

```yaml
---
name: code-analyzer
description: "Analyze codebase for patterns"
tools: [Read, Grep, Glob]
skills: [pattern-analysis]
---

## Operational Protocol
1. **Context First**: Use the injected context from the `# Context` section. If no context was injected and DISCOVERY.md exists, read it. DO NOT regenerate discovery.
You operate in context-isolated windows. Use injected context, do not re-read files.
```

### Pattern 3: Background Execution

**Long-running task:**

```yaml
---
description: "Background security audit"
argument-hint: "[target-directory]"
allowed-tools: [Task]
---

Task(
  description="Audit: $ARGUMENTS",
  prompt="Comprehensive security analysis...",
  subagent_type="security-auditor",
  run_in_background=true
)
```

### Pattern 4: Hook-Protected Operation

**Validate before execution:**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./validate-command.sh"
          }
        ]
      }
    ]
  }
}
```

---

## Testing & Validation

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

### Test Agent Configuration

```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('agents/my-agent.md'))"

# Check tool list format
grep "tools:" agents/*.md | grep -v "," | head -5
# Should show comma-separated list
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

---

## Permission System Deep Dive

### `tools` vs `allowed-tools`: Critical Difference

| Aspect | `tools` (Agents) | `allowed-tools` (Commands/Skills) |
|:-------|:-----------------|:----------------------------------|
| **Purpose** | Whitelist - defines what agent CAN use | Blacklist - restricts what CAN be used |
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

### Permission Mode Selection Guide

```yaml
# Development Environment
---
permissionMode: default
---

# Automated CI/CD
---
permissionMode: dontAsk
---

# Code Review (Read-Only)
---
permissionMode: plan
---

# Trusted Code Editor
---
permissionMode: acceptEdits
---

# WARNING: Never use in untrusted environments
---
permissionMode: bypassPermissions
---
```

### MCP Server Security

#### **Secure Configuration Examples**

```yaml
# ✅ Good: URL-restricted
allowedMcpServers:
  - serverUrl: "https://api.githubcopilot.com/mcp/"
  - serverUrl: "https://mcp.company.com/api/*"

# ✅ Good: Command-restricted
allowedMcpServers:
  - serverCommand: ["npx", "-y", "@company/approved-package"]

# ❌ Bad: Wildcard access
allowedMcpServers:
  - serverUrl: "*"
```

### Permission Audit Workflow

#### **Step 1: List All Agent Configurations**

```bash
# Find all agents
find . -name "*.md" -path "*/agents/*" -o -path "*/subagents/*"

# Check for tools field
for agent in $(find . -name "*.md" -path "*/agents/*"); do
  if ! grep -q "^tools:" "$agent"; then
    echo "WARNING: $agent has no tools restriction"
  fi
done
```

#### **Step 2: Audit Tool Permissions**

```bash
# Find agents with Bash permission
grep -r "tools:.*Bash" agents/ --include="*.md"

# Find agents with Write permission
grep -r "tools:.*Write" agents/ --include="*.md"

# Find agents with AskUserQuestion (should be rare)
grep -r "AskUserQuestion" agents/ --include="*.md"
```

#### **Step 3: Validate Permission Rules**

```bash
# Check permissions.json exists and is valid
jq . .claude/permissions.json

# List MCP servers
claude mcp list

# Check for wildcard patterns
grep -r "serverUrl.*\*" .claude/
```

### Common Permission Vulnerabilities

#### **Vulnerability 1: Permission Escalation**

```yaml
# ❌ VULNERABLE
---
name: "file-analyzer"
description: "Analyzes log files"
# No tools restriction
---

# Attack vector: Agent can modify/delete log files
```

```yaml
# ✅ SECURE
---
name: "file-analyzer"
description: "Analyzes log files"
tools: Read, Grep
---

# Protection: Agent can only read/analyze, not modify
```

#### **Vulnerability 2: Bash Command Injection**

```yaml
# ❌ VULNERABLE
permissions:
  allow: ["Bash(npm *)"]
---

# Attack: User provides "npm && rm -rf /"
# Result: Arbitrary command execution
```

```yaml
# ✅ SECURE
permissions:
  allow:
    - "Bash(npm run build)"
    - "Bash(npm run test)"
---

# Protection: Only specific commands allowed
```

#### **Vulnerability 3: Overprivileged Agents**

```yaml
# ❌ VULNERABLE
# Built-in agent has more permissions than needed
---
tools: [Read, Write, Edit, Bash, Grep, Glob, Task, Skill]
---

# Attack: Agent can spawn other agents, modify files, execute commands
```

```yaml
# ✅ SECURE
---
tools: [Read, Grep]
model: haiku
permissionMode: plan
---

# Protection: Read-only, fast model, plan mode
```

---

## Glue Code Detection & Removal

### The 10-Line Rule

> **If a wrapper is >10 lines with no business logic, it's over-engineered. If it's <3 lines, it's definitely glue code.**

### Detection Scripts

#### **Automated Detection**

```bash
#!/bin/bash
# glue-detector.sh - Find glue code patterns

echo "=== Glue Code Detection Report ==="

# Find pure delegation methods
echo "1. Pure Delegation Methods:"
grep -r "return \$this->\w+->\w+" --include="*.ts" src/ || echo "None found"
grep -r "return \w+\.\w+\(" --include="*.js" src/ || echo "None found"

# Find wrapper classes
echo -e "\n2. Wrapper/Adapter/Facade Classes:"
rg "class (Wrapper|Adapter|Facade|Proxy|Manager)" --type ts || echo "None found"

# Find interfaces with single implementations
echo -e "\n3. Single-Implementation Interfaces:"
find . -name "*.java" -o -name "*.ts" | xargs grep -l "interface" | while read f; do
  count=$(grep -c "implements " "$f" 2>/dev/null || echo "0")
  if [ "$count" -eq "1" ]; then
    echo "  $f"
  fi
done

# Find empty abstractions
echo -e "\n4. Empty Abstract Classes:"
rg "abstract class \w+ {" --type java -A 3 || echo "None found"
```

#### **Delegation Ratio Calculator**

```python
#!/usr/bin/env python3
import ast
import sys
import os

def analyze_file(filepath):
    with open(filepath, 'r') as f:
        try:
            tree = ast.parse(f.read())
        except:
            return None

    total_methods = 0
    delegated_methods = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.MethodDef)):
            total_methods += 1
            if node.body and len(node.body) == 1:
                if isinstance(node.body[0], ast.Return):
                    if isinstance(node.body[0].value, ast.Call):
                        delegated_methods += 1

    if total_methods > 0:
        ratio = delegated_methods / total_methods
        return {
            'file': filepath,
            'total': total_methods,
            'delegated': delegated_methods,
            'ratio': ratio
        }
    return None

if __name__ == "__main__":
    results = []
    for root, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            if file.endswith(('.py', '.ts', '.js')):
                filepath = os.path.join(root, file)
                result = analyze_file(filepath)
                if result and result['ratio'] > 0.8:
                    results.append(result)

    results.sort(key=lambda x: x['ratio'], reverse=True)

    print("=== High Delegation Ratio Files ===")
    for result in results:
        print(f"{result['file']}: {result['ratio']:.0%} "
              f"({result['delegated']}/{result['total']} methods)")
```

### Refactoring Patterns

#### **Pattern 1: Remove Pass-Through Wrapper**

```typescript
// ❌ BEFORE: Unnecessary wrapper
class UserRepository {
  private api = new ApiClient();

  getUser(id: string) {
    return this.api.getUser(id);
  }

  createUser(user: User) {
    return this.api.createUser(user);
  }

  updateUser(id: string, user: User) {
    return this.api.updateUser(id, user);
  }
}

// ✅ AFTER: Direct composition
class UserService {
  constructor(private api: ApiClient) {}

  async getUser(id: string) {
    return this.api.getUser(id);
  }

  async createUser(user: User) {
    return this.api.createUser(user);
  }

  async updateUser(id: string, user: User) {
    return this.api.updateUser(id, user);
  }
}
```

#### **Pattern 2: Collapse Abstraction Layers**

```typescript
// ❌ BEFORE: Too many layers
class AuthController {
  private service = new AuthService();
  private repo = new UserRepository();
  private validator = new AuthValidator();

  login(credentials: Credentials) {
    return this.service.authenticate(
      this.validator.validate(credentials),
      this.repo
    );
  }
}

// ✅ AFTER: Simplified
class AuthController {
  constructor(
    private authService: AuthService,
    private validator: AuthValidator,
    private userRepo: UserRepository
  ) {}

  async login(credentials: Credentials) {
    const validated = this.validator.validate(credentials);
    return this.authService.authenticate(validated, this.userRepo);
  }
}
```

#### **Pattern 3: Inline Simple Delegation**

```typescript
// ❌ BEFORE: One-liner wrapper
class Logger {
  info(message: string) {
    console.log(message);
  }

  error(message: string) {
    console.error(message);
  }
}

// ✅ AFTER: Direct usage or utility module
// Remove the wrapper entirely
// Use console.log() directly or:
export const logger = {
  info: (msg: string) => console.log(msg),
  error: (msg: string) => console.error(msg)
};
```

### Performance Impact Analysis

#### **Before Refactoring**

```typescript
class OrderProcessor {
  process(order: Order) {
    return this.validator.validate(order);         // 0.1ms
  }
}

class Validator {
  validate(order: Order) {
    return this.rulesEngine.check(order);         // 0.1ms
  }
}

class RulesEngine {
  check(order: Order) {
    return this.database.query(order);            // 0.1ms
  }
}

class Database {
  query(order: Order) {
    return this.connection.execute(order);         // 0.1ms
  }
}

// Total: 0.4ms per call
// 1M calls = 400 seconds
```

#### **After Refactoring**

```typescript
class OrderProcessor {
  constructor(private db: Database) {}

  process(order: Order) {
    // All logic in one place
    if (!order.items || order.items.length === 0) {
      throw new Error("Empty order");
    }
    return this.db.query({
      type: 'INSERT',
      table: 'orders',
      data: order
    });
  }
}

// Estimated: 0.15ms per call (2.7x faster)
// 1M calls ≈ 150 seconds (62.5% reduction)
```

---

## Key Takeaways

1. **Use Task tool** for delegating to subagents (not for invoking commands)
2. **Use Skill tool** for invoking commands and skills programmatically
3. **Subagents are context-isolated** - provide exhaustive context
4. **Skills don't auto-inherit** - explicitly list in agent's `skills` field
5. **Hooks run in parallel** - can't trigger other hooks
6. **No SubagentStart event** - only SubagentStop exists
7. **PermissionMode matters** - controls tool approval behavior
8. **Context gravity rule** - delegate if >10 files or >50% context
9. **Progressive disclosure** - don't dump all tokens at once
10. **Test everything** - validate configurations before deployment

---

## Quick Reference Card

### Direct (Inline) Execution
- Context: <50% full
- Files: <10
- Duration: <1 min
- User interaction: Yes

### Delegated (Task) Execution
- Context: >50% full
- Files: >10
- Duration: >1 min
- User interaction: No

### Command Fields (Required)
- `description` ✓

### Agent Fields (Optional)
- `name` ✓
- `tools` (comma-separated)
- `skills` (array)
- `permissionMode`

### Skill Fields (Optional)
- `name` ✓
- `description` ✓
- `context: fork` (for isolation)

### Hook Events (Real)
SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, Notification, Stop, SubagentStop, PreCompact, SessionEnd

### Tool Categories
- **File Ops**: Read, Write, Edit
- **Search**: Glob, Grep
- **System**: Bash, KillShell
- **Agent**: Task
- **Invoke**: Skill
- **Web**: WebSearch, WebFetch
