# Agent SDK — Stable Architecture Patterns

The Claude Agent SDK provides programmable agentic capabilities with built-in tools, hooks, subagents, and session management.

## Core Architecture

### What the SDK Provides
- **Built-in tools**: Read, Write, Edit, Bash, Glob, Grep
- **Agent loop**: Autonomous tool use and iteration
- **Session management**: Persistent context across requests
- **Hooks**: Lifecycle event interception
- **Subagents**: Specialized agent delegation
- **Type safety**: Python and TypeScript APIs

### SDK vs Client SDK
```
Client SDK: You implement tool loop
    ↓
    User prompt → Model → Tool use → You execute → Result → Model

Agent SDK: Built-in tool loop
    ↓
    User prompt → Model → Autonomous tool execution → Done
```

## Built-in Tools (Stable)

### Tool Categories

**File Operations**:
- `Read`: Read file contents
- `Write`: Create new files
- `Edit`: Modify existing files
- `Glob`: Find files by pattern
- `Grep`: Search file contents

**System Operations**:
- `Bash`: Execute shell commands
- `Task`: Spawn subagents

**Web Operations**:
- `WebFetch`: Fetch web content
- `WebSearch`: Search the web

**Interaction**:
- `AskUserQuestion`: Get user input with choices

### Tool Configuration Pattern
```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Analyze this codebase",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep", "Bash"]
    )
):
    print(message)
```

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Analyze this codebase",
  options: {
    allowedTools: ["Read", "Glob", "Grep", "Bash"]
  }
})) {
  console.log(message);
}
```

## Sessions (Stable Pattern)

### Session Concept
- **Persistent context**: Files read, analysis done, conversation history
- **Resume capability**: Continue previous session later
- **Fork capability**: Explore different approaches

### Basic Session Pattern
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    session_id = None

    # First query: capture session ID
    async for message in query(
        prompt="Read the authentication module",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Glob"])
    ):
        if hasattr(message, 'subtype') and message.subtype == 'init':
            session_id = message.session_id

    # Resume with full context
    async for message in query(
        prompt="Now find all places that call it",
        options=ClaudeAgentOptions(resume=session_id)
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

### Session Patterns

#### Pattern 1: Capture and Resume
```python
# Capture
session_id = None
async for message in query(prompt="Initial task", options=options):
    if hasattr(message, 'session_id'):
        session_id = message.session_id

# Resume
async for message in query(
    prompt="Continue the work",
    options=ClaudeAgentOptions(resume=session_id)
):
    # Work continues with full context
```

#### Pattern 2: Fork Session
```python
# Create multiple branches
for approach in ["approach_a", "approach_b", "approach_c"]:
    async for message in query(
        prompt=f"Try {approach}",
        options=ClaudeAgentOptions(resume=base_session_id)
    ):
        # Each branch has full base context
```

#### Pattern 3: Ephemeral Sessions
```python
# Default: persistent sessions
options = ClaudeAgentOptions(
    persistSession=False  # Ephemeral
)
```

## Permissions (Stable)

### Permission Modes

#### bypassPermissions
```python
options = ClaudeAgentOptions(
    permissionMode="bypassPermissions"
)
```
- Ignores all permission checks
- Use only in controlled environments

#### acceptEdits
```python
options = ClaudeAgentOptions(
    permissionMode="acceptEdits"
)
```
- Auto-accepts file edit permissions
- Still prompts for dangerous operations

#### default
```python
options = ClaudeAgentOptions(
    permissionMode="default"
)
```
- Standard permission flow
- Interactive approval required

#### plan
```python
options = ClaudeAgentOptions(
    permissionMode="plan"
)
```
- Generate plans only
- No execution

### Permission Configuration
```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep"],  # Whitelist
    permission_mode="acceptEdits",           # Mode
    setting_sources=["project"]              # Use project settings
)
```

## Hooks (Stable Architecture)

### SDK Hook Architecture
Hooks intercept agent lifecycle events:
- `PreToolUse`: Before tool execution
- `PostToolUse`: After tool execution
- `Stop`: Agent completion
- `SessionStart`: Session begin
- `SessionEnd`: Session end

### Hook Pattern
```python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher

async def log_file_change(input_data, tool_use_id, context):
    file_path = input_data.get('tool_input', {}).get('file_path', 'unknown')
    with open('./audit.log', 'a') as f:
        f.write(f"Modified: {file_path}\n")
    return {}

async def main():
    async for message in query(
        prompt="Refactor utils.py",
        options=ClaudeAgentOptions(
            permission_mode="acceptEdits",
            hooks={
                "PostToolUse": [
                    HookMatcher(
                        matcher="Edit|Write",
                        hooks=[log_file_change]
                    )
                ]
            }
        )
    ):
        if hasattr(message, "result"):
            print(message.result)
```

### Common Hook Patterns

#### Pattern 1: Audit Logging
```python
async def audit_hook(input_data, tool_use_id, context):
    timestamp = datetime.now().isoformat()
    tool_name = input_data.get('tool_name')
    log_entry = {
        'timestamp': timestamp,
        'tool': tool_name,
        'tool_use_id': tool_use_id
    }
    with open('audit.log', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    return {}
```

#### Pattern 2: Security Validation
```python
async def security_hook(input_data, tool_use_id, context):
    tool_input = input_data.get('tool_input', {})

    # Block dangerous patterns
    if tool_input.get('command', '').startswith('rm -rf'):
        raise Exception("Dangerous command blocked")

    return {}
```

#### Pattern 3: Rate Limiting
```python
import time

last_call = 0

async def rate_limit_hook(input_data, tool_use_id, context):
    global last_call
    now = time.time()
    if now - last_call < 1:  # 1 second limit
        time.sleep(1)
    last_call = now
    return {}
```

## Subagents (Stable)

### Subagent Pattern
```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def main():
    async for message in query(
        prompt="Review this code",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Task"],
            agents={
                "code-reviewer": AgentDefinition(
                    description="Expert code reviewer",
                    prompt="Analyze code quality and suggest improvements.",
                    tools=["Read", "Glob", "Grep"]
                )
            }
        )
    ):
        if hasattr(message, "result"):
            print(message.result)
```

### Subagent Communication
```python
# Parent can pass context
async for message in query(
    prompt="Use code-reviewer to review auth.py",
    options=ClaudeAgentOptions(
        agents={"code-reviewer": {...}}
    )
):
    # Messages from subagent include parent_tool_use_id
    # Track which messages belong to which subagent
```

### Subagent Patterns

#### Pattern 1: Specialist Delegation
```python
agents = {
    "security-auditor": AgentDefinition(
        description="Security vulnerability detection",
        prompt="Focus on security issues: SQL injection, XSS, auth flaws.",
        tools=["Read", "Grep"]
    ),
    "performance-analyzer": AgentDefinition(
        description="Performance bottleneck detection",
        prompt="Focus on performance: N+1 queries, inefficient loops.",
        tools=["Read", "Grep"]
    )
}
```

#### Pattern 2: Sequential Handoff
```python
# Step 1: Discovery
prompt1 = "Find all API endpoints in the codebase"
# ... collect results ...

# Step 2: Security review
prompt2 = "Review these endpoints for security issues: [results from step 1]"
# ... review results ...
```

#### Pattern 3: Parallel Evaluation
```python
# Multiple subagents evaluate same code
agents = {
    "style-checker": {...},
    "logic-reviewer": {...},
    "security-scanner": {...}
}

# All subagents run on same code
prompt = "Review this code from multiple perspectives"
```

## MCP Integration (Stable)

### MCP Pattern
```python
async def main():
    async for message in query(
        prompt="Use browser to test this page",
        options=ClaudeAgentOptions(
            mcp_servers={
                "playwright": {
                    "command": "npx",
                    "args": ["@playwright/mcp@latest"]
                }
            }
        )
    ):
        if hasattr(message, "result"):
            print(message.result)
```

### MCP Server Configuration
```python
options = ClaudeAgentOptions(
    mcp_servers={
        "server-name": {
            "command": "executable",
            "args": ["arg1", "arg2"],
            "env": {"KEY": "value"}
        }
    }
)
```

## Settings Integration

### Project Settings Pattern
```python
options = ClaudeAgentOptions(
    setting_sources=["project"]  # Read .claude/settings.json
)
```

**Benefits**:
- Use Claude Code configuration
- Consistent behavior between CLI and SDK
- Team-shared settings

## Structured Outputs

### JSON Schema Pattern
```python
options = ClaudeAgentOptions(
    output_format={
        "type": "json_schema",
        "schema": {
            "type": "object",
            "properties": {
                "score": {"type": "number"},
                "passed": {"type": "boolean"},
                "details": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["score", "passed"]
        }
    }
)
```

### Zod Integration Pattern
```python
from zod import z

schema = z.object({
    "score": z.number().min(0).max(100),
    "passed": z.boolean(),
    "details": z.array(z.string())
})

options = ClaudeAgentOptions(
    output_format={
        "type": "json_schema",
        "schema": schema.to_json_schema()
    }
)
```

### Multi-Step Evaluation Pattern
```python
# Step 1: Initialize evaluation
session_id = None
results = {}

for step in evaluation_steps:
    for message in query(
        prompt=step["prompt"],
        options=ClaudeAgentOptions(
            resume=session_id,
            output_format={
                "type": "json_schema",
                "schema": step["schema"]
            }
        )
    ):
        if message.type === 'result':
            if message.subtype === 'success':
                results.update(message.structured_output)
                session_id = message.session_id
```

## Plugin Integration

### Local Plugin Loading
```python
options = ClaudeAgentOptions(
    plugins=[
        {"type": "local", "path": "/path/to/plugin"}
    ]
)
```

### Plugin Path Patterns
```python
# Load from filesystem
plugins = [
    {"type": "local", "path": "./plugins/my-plugin"}
]

# With validation
if os.path.exists(plugin_path):
    options = ClaudeAgentOptions(
        plugins=[{"type": "local", "path": plugin_path}]
    )
```

### Plugin Configuration
```python
options = ClaudeAgentOptions(
    plugins=[
        {
            "type": "local",
            "path": plugin_path,
            "setting_sources": ["project"]  # Use project settings
        }
    ],
    setting_sources=["project"]  # Read .claude/settings.json
)
```

## Advanced Options

### Message Handling
```python
options = ClaudeAgentOptions(
    include_partial_messages=True  # Stream partial results
)
```

### Session Persistence
```python
# Persistent sessions (default)
options = ClaudeAgentOptions(
    persist_session=True
)

# Ephemeral sessions
options = ClaudeAgentOptions(
    persist_session=False
)
```

### Settings Integration
```python
# Use project settings
options = ClaudeAgentOptions(
    setting_sources=["project"]  # Read .claude/settings.json
)

# Use user settings
options = ClaudeAgentOptions(
    setting_sources=["user"]  # Read ~/.claude/settings.json
)

# Multiple sources
options = ClaudeAgentOptions(
    setting_sources=["user", "project"]
)
```

## Best Practices

### 1. Minimize Allowed Tools
```python
# Good: Specific tools
allowed_tools=["Read", "Grep"]

# Bad: All tools
allowed_tools=["*"]
```

### 2. Use Hooks for Validation
```python
# Always validate inputs
async def validate_hook(input_data, tool_use_id, context):
    if not validate_input(input_data):
        raise Exception("Invalid input")
    return {}
```

### 3. Log Everything
```python
import logging

logging.basicConfig(
    filename='agent.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
```

### 4. Handle Errors Gracefully
```python
async for message in query(prompt="Task", options=options):
    try:
        # Process message
    except Exception as e:
        logging.error(f"Error: {e}")
        continue
```

### 5. Clean Up Resources
```python
async def main():
    try:
        async for message in query(...):
            # Work
    finally:
        # Cleanup
        pass
```

## Anti-Patterns (Avoid)

❌ **No tool restrictions**: Allows any tool
❌ **No error handling**: Assuming success
❌ **No logging**: Can't debug issues
❌ **Blocking operations**: Synchronous in async context
❌ **Global state**: Thread-unsafe operations
❌ **No validation**: Trust all inputs
❌ **Excessive permissions**: Bypass permissions everywhere

## Complete Example: Test Framework Pattern

### Three-Agent Architecture
```typescript
// Agent A: Executor with hooks and sandbox
class AgentA {
  private sessionId: string | undefined;

  getHooks() {
    const preToolUse: HookCallback = (input, toolUseID) => {
      this.logger.recordToolStart(toolUseID, input.tool_name, input.tool_input);
      return Promise.resolve({});
    };

    const postToolUse: HookCallback = (input, toolUseID) => {
      this.logger.recordToolEnd(toolUseID, input.tool_response);
      return Promise.resolve({});
    };

    return {
      PreToolUse: [{ hooks: [preToolUse] }],
      PostToolUse: [{ hooks: [postToolUse] }]
    };
  }

  async execute(task: string): Promise<string> {
    const options = {
      cwd: this.sandboxPath,
      allowedTools: ['Read', 'Write', 'Edit', 'Bash', 'Glob', 'Grep'],
      permissionMode: 'acceptEdits',
      persistSession: false,
      sandbox: {
        enabled: true,
        autoAllowBashIfSandboxed: true,
        network: {
          allowLocalBinding: true,
          allowedDomains: ['github.com']
        }
      },
      plugins: [
        { type: 'local', path: this.pluginPath }
      ],
      settingSources: ['project'],
      includePartialMessages: true,
      systemPrompt: {
        type: 'preset',
        preset: 'claude_code'
      },
      hooks: this.getHooks()
    } satisfies Options;

    for await (const message of query({ prompt: task, options })) {
      if ('result' in message) {
        // Process result
      }
    }
  }
}

// Agent B: Task generator
class AgentB {
  async generateTask(phase: string): Promise<string> {
    const options = {
      systemPrompt: 'You are an expert test engineer.'
    } satisfies Options;

    for await (const message of query({ prompt, options })) {
      if ('result' in message) {
        return message.result;
      }
    }
  }
}

// Agent C: Multi-step evaluator
class AgentC {
  async evaluate(): Promise<EvaluationResult> {
    const schema = z.object({
      score: z.number().min(0).max(100),
      passed: z.boolean(),
      details: z.array(z.string())
    });

    let sessionId: string | undefined;

    for (const step of evaluationSteps) {
      const options: Options = {
        outputFormat: {
          type: 'json_schema',
          schema: schema.toJSONSchema()
        },
        resume: sessionId
      };

      for await (const message of query({ prompt: step.prompt, options })) {
        if (message.type === 'result') {
          if (message.subtype === 'success') {
            sessionId = message.session_id;
          }
        }
      }
    }
  }
}
```

## Testing Patterns

### Pattern 1: Mock Tools
```python
from unittest.mock import Mock

# Mock Read tool
read_mock = Mock(return_value="Mocked content")

options = ClaudeAgentOptions(
    allowed_tools=["Read"],
    tool_overrides={"Read": read_mock}
)
```

### Pattern 2: Test Hooks
```python
# Capture hook calls
hook_calls = []

async def test_hook(input_data, tool_use_id, context):
    hook_calls.append((input_data, tool_use_id))
    return {}

options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="*", hooks=[test_hook])]}
)

# Run test
# Assert hook_calls contains expected calls
```

### Pattern 3: Session Testing
```python
# Test session persistence
session_id = None

# First call
async for message in query(prompt="Set value: x=42", options=options):
    if hasattr(message, 'session_id'):
        session_id = message.session_id

# Resume
async for message in query(prompt="What is x?", options=ClaudeAgentOptions(resume=session_id)):
    assert "42" in str(message)
```

## Error Handling

### Common Errors

#### Tool Not Allowed
```
Exception: Tool 'Bash' not in allowed_tools
```
**Fix**: Add to allowed_tools list

#### Permission Denied
```
Exception: Permission denied
```
**Fix**: Check permission_mode setting

#### Session Not Found
```
Exception: Session not found
```
**Fix**: Check session_id is valid

### Recovery Patterns
```python
async for message in query(prompt="Task", options=options):
    try:
        # Process
    except ToolNotAllowed:
        # Retry with expanded permissions
        options.allowed_tools.append(tool_name)
        continue
    except PermissionDenied:
        # Ask user for permission
        continue
```

## Performance Optimization

### 1. Batch Operations
```python
# Good: Read multiple files at once
file_paths = ["file1.py", "file2.py", "file3.py"]
for path in file_paths:
    # Read in loop
```

### 2. Use Appropriate Tools
```python
# Good: Use Glob for pattern matching
glob_results = await glob("**/*.py")

# Bad: Bash grep
bash_results = await bash("find . -name '*.py'")
```

### 3. Limit Context
```python
options = ClaudeAgentOptions(
    max_tokens=10000  # Limit context size
)
```

## Volatile Details (Look Up)

These change frequently:
- Exact API method names
- Hook event schemas
- Tool parameter structures
- Permission mode values

**Always verify**: Use latest SDK documentation for current API signatures.

---

## Official Documentation Links

- **Agent SDK Overview**: https://platform.claude.com/docs/en/agent-sdk/overview.md
- **Agent SDK Quickstart**: https://platform.claude.com/docs/en/agent-sdk/quickstart
- **Agent SDK Hooks**: https://platform.claude.com/docs/en/agent-sdk/hooks.md
- **Agent SDK Subagents**: https://platform.claude.com/docs/en/agent-sdk/subagents.md
- **Agent SDK Sessions**: https://platform.claude.com/docs/en/agent-sdk/sessions.md
- **Agent SDK Permissions**: https://platform.claude.com/docs/en/agent-sdk/permissions.md
- **Agent SDK Skills**: https://platform.claude.com/docs/en/agent-sdk/skills.md
- **Messages API**: https://platform.claude.com/docs/en/api/messages

### Verification
Last verified: 2026-01-13
