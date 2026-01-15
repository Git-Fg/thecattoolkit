# Hook Events

## Event Types

Hooks can be triggered at various points in the AI lifecycle. Each event has specific use cases and data available.

## Lifecycle Events

### SessionStart

**Trigger:** When Claude starts or resumes a session

**Matchers:**
- `startup` - Initial session start
- `resume` - Resuming existing session
- `clear` - After /clear command
- `compact` - After context compaction

**Use Cases:**
- Environment validation
- Dependency checks
- Setup scripts
- State initialization

**Data Available:**
- `$CLAUDE_PROJECT_DIR` - Project root directory
- `${CLAUDE_PLUGIN_ROOT}` - Plugin root (plugin hooks only)
- `$CLAUDE_ENV_FILE` - Environment file path (write-only for SessionStart)

**Example:**
```json
{
  "hooks": {
    "SessionStart": [{
      "matchers": ["startup", "resume"],
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/init.sh"
      }]
    }]
  }
}
```

### SessionEnd

**Trigger:** When Claude session ends

**Matchers:**
- `clear` - /clear command
- `logout` - User logout
- `prompt_input_exit` - User input exit
- `other` - Other session termination

**Use Cases:**
- Cleanup temporary files
- Persist state
- Log session summary
- Notify external systems

**Example:**
```json
{
  "hooks": {
    "SessionEnd": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/cleanup.sh"
      }]
    }]
  }
}
```

## Tool Events

### PreToolUse

**Trigger:** Before a tool is invoked

**Matchers:**
- Tool name: `Bash`, `Write`, `Read`, etc.
- `*` - All tools

**Use Cases:**
- Safety checks
- Input validation
- Permission gates
- Logging

**Data Available:**
- `$ARGUMENTS` - Tool arguments as JSON

**Blocking:** Exit code 2 blocks the tool call

**Example:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/bash-guard.sh",
        "timeout": 30
      }]
    }]
  }
}
```

### PostToolUse

**Trigger:** After a tool completes

**Matchers:**
- Tool name: `Bash`, `Write`, `Read`, etc.

**Use Cases:**
- Logging tool usage
- Validating outputs
- Triggering dependent actions
- Audit trails

**Data Available:**
- Tool name and arguments
- Tool result/exit code

**Example:**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/log-write.sh"
      }]
    }]
  }
}
```

## Interaction Events

### UserPromptSubmit

**Trigger:** When user submits a message

**Use Cases:**
- Input validation
- Rate limiting
- Content filtering
- Prompt enhancement

**Data Available:**
- User message content
- Context state

**Example:**
```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Check if user input is safe: $ARGUMENTS",
        "timeout": 30
      }]
    }]
  }
}
```

### PermissionRequest

**Trigger:** When permission dialog is shown

**Use Cases:**
- Auto-allow specific permissions
- Auto-deny dangerous permissions
- Log permission requests

**Example:**
```json
{
  "hooks": {
    "PermissionRequest": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/permission-guard.sh"
      }]
    }]
  }
}
```

## Notification Events

### Notification

**Trigger:** When Claude Code shows a notification

**Matchers:**
- `permission_prompt` - Permission dialog
- `idle_prompt` - Idle notification
- `auth_success` - Authentication success
- `elicitation_dialog` - Elicitation dialog

**Use Cases:**
- Custom notification handling
- Logging notifications
- External integrations

**Example:**
```json
{
  "hooks": {
    "Notification": [{
      "matchers": ["permission_prompt", "auth_success"],
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/notify-logger.sh"
      }]
    }]
  }
}
```

## Completion Events

### Stop

**Trigger:** When main agent finishes

**Use Cases:**
- Final validation
- Result reporting
- State persistence

**Example:**
```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/finalize.sh"
      }]
    }]
  }
}
```

### SubagentStop

**Trigger:** When subagent completes

**Use Cases:**
- Subagent result validation
- State cleanup
- Result aggregation

**Example:**
```json
{
  "hooks": {
    "SubagentStop": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/subagent-cleanup.sh"
      }]
    }]
  }
}
```

## Compaction Events

### PreCompact

**Trigger:** Before context compaction

**Matchers:**
- `manual` - Manual compaction trigger
- `auto` - Automatic compaction

**Use Cases:**
- Pre-compaction checks
- State preservation
- Cache invalidation

**Example:**
```json
{
  "hooks": {
    "PreCompact": [{
      "matchers": ["auto"],
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/pre-compact-check.sh"
      }]
    }]
  }
}
```

## Event Selection Guide

| Use Case | Best Event | Why |
|:---------|:-----------|:-----|
| Environment setup | SessionStart | Runs once when session begins |
| Cleanup | SessionEnd | Runs before session terminates |
| Safety checks | PreToolUse | Can block dangerous operations |
| Logging | PostToolUse | Captures tool results |
| Input validation | UserPromptSubmit | Filters user input |
| Final validation | Stop | Runs after agent completes |
| Subagent cleanup | SubagentStop | Cleans up after subagents |
