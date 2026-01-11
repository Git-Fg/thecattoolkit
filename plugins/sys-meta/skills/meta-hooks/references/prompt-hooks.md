# Prompt-Based Hooks

## Overview

Prompt hooks use an LLM (typically Haiku) to evaluate actions and return structured JSON decisions. They enable complex, context-aware validation that rule-based scripts cannot handle.

## When to Use Prompt Hooks

**Use Prompt Hooks for:**
- Semantic understanding of intent
- Complex context evaluation
- Nuanced decision making
- Content filtering requiring comprehension

**Use Command Hooks for:**
- Simple pattern matching
- Fast rule-based validation
- Security checks with clear rules
- Dependency verification

## JSON Response Protocol

### Success (Continue Action)

```json
{
  "ok": true
}
```

**Behavior:** Action continues normally

### Block (Stop Action)

```json
{
  "ok": false,
  "reason": "This action would modify system files"
}
```

**Behavior:** Action is blocked, reason shown to user

## Configuration

### Basic Prompt Hook

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if action is safe: $ARGUMENTS. Return JSON with ok field.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Advanced Prompt Hook

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate user input for safety:\n\n$ARGUMENTS\n\nReturn JSON with ok field. If malicious, set ok to false and include reason field explaining the issue.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Prompt Design Patterns

### Safety Validation Pattern

```json
{
  "type": "prompt",
  "prompt": "You are a safety validator. Check if this action is safe:\n\nContext: $TOOL_NAME\nArguments: $ARGUMENTS\n\nReturn JSON: {\"ok\": true|false, \"reason\": \"explanation\"}",
  "timeout": 30
}
```

### Content Filter Pattern

```json
{
  "type": "prompt",
  "prompt": "Filter this user input for harmful content:\n\n$ARGUMENTS\n\nReturn JSON: {\"ok\": true|false, \"reason\": \"if blocked\"}",
  "timeout": 30
}
```

### Permission Check Pattern

```json
{
  "type": "prompt",
  "prompt": "Check if this operation requires elevated permissions:\n\nOperation: $TOOL_NAME\nArguments: $ARGUMENTS\n\nReturn JSON: {\"ok\": true|false, \"reason\": \"why blocked\", \"suggestion\": \"alternative approach\"}",
  "timeout": 30
}
```

## Available Variables in Prompt Hooks

| Variable | Description | Example |
|:----------|:-------------|:--------|
| `$ARGUMENTS` | Tool arguments as JSON | `{"file_path": "/path/to/file"}` |
| `$TOOL_NAME` | Name of tool being invoked | `Write`, `Bash`, `Read` |
| `$CLAUDE_PROJECT_DIR` | Project directory | `/Users/user/project` |

## Event Support

Prompt hooks work with these events:

| Event | Use Case |
|:------|:---------|
| `Stop` | Final validation of results |
| `SubagentStop` | Subagent result validation |
| `UserPromptSubmit` | Input validation and filtering |
| `PreToolUse` | Semantic safety checks |
| `PermissionRequest` | Intelligent permission decisions |

## Examples

### Semantic Safety Check

**Scenario:** Block operations that seem malicious even if they don't match explicit patterns.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if this bash command is safe:\n\nCommand: $ARGUMENTS\n\nConsider:\n- Does it attempt to access sensitive files?\n- Does it try to escalate privileges?\n- Does it attempt to exfiltrate data?\n\nReturn JSON: {\"ok\": true|false, \"reason\": \"explanation if blocked\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Content Filtering

**Scenario:** Filter user input for harmful content.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate this user input for harmful content:\n\n$ARGUMENTS\n\nCheck for:\n- Hate speech\n- Dangerous instructions\n- Sexual content\n- Harassment\n\nReturn JSON: {\"ok\": true|false, \"reason\": \"why blocked\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Intelligent Permission Decision

**Scenario:** Auto-allow safe operations, prompt for risky ones.

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if this permission request should be auto-allowed:\n\nTool: $TOOL_NAME\nContext: $ARGUMENTS\n\nAuto-allow if:\n- Read operations in project directory\n- Write operations to non-system files\n\nRequire prompt if:\n- Operations outside project\n- System file modifications\n\nReturn JSON: {\"ok\": true|false, \"reason\": \"explanation\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Result Validation

**Scenario:** Validate agent outputs before completion.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Validate the agent's final result:\n\nContext: $ARGUMENTS\n\nCheck:\n- Results match the original request\n- No harmful content generated\n- No security issues introduced\n\nReturn JSON: {\"ok\": true|false, \"reason\": \"issues found\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Prompt Best Practices

### 1. Clear Instructions

```json
{
  "prompt": "Check if action is safe: $ARGUMENTS. Return JSON with ok field."
}
```

**Good:** Clear, specific instructions

### 2. Structured Output

```json
{
  "prompt": "Return JSON: {\"ok\": true|false, \"reason\": \"explanation\", \"suggestion\": \"alternative\"}"
}
```

**Good:** Defines exact JSON structure expected

### 3. Context Provision

```json
{
  "prompt": "Tool: $TOOL_NAME\nArguments: $ARGUMENTS\nProject: $CLAUDE_PROJECT_DIR\n\nEvaluate safety..."
}
```

**Good:** Provides full context for evaluation

### 4. Examples in Prompt

```json
{
  "prompt": "Evaluate safety:\n\n$ARGUMENTS\n\nExamples:\nSafe: ls -la\nUnsafe: rm -rf /etc\n\nReturn JSON: {\"ok\": true|false}"
}
```

**Good:** Few-shot examples improve accuracy

## Performance Considerations

| Factor | Impact |
|:-------|:--------|
| **Prompt length** | Longer prompts = slower evaluation |
| **Timeout** | Longer timeout allows complex evaluation |
| **LLM model** | Haiku is fast, less capable; larger models slower |
| **Frequency** | Prompt hooks on every tool call = significant overhead |

**Best Practice:** Use prompt hooks sparingly. Prefer command hooks for fast, rule-based checks.

## Cost Analysis

| Hook Type | Token Cost | Speed | Complexity |
|:----------|:----------:|:-----:|:----------:|
| Command | 0 tokens | Fast | Simple rules only |
| Prompt | ~500-2000 tokens | Slow | Complex reasoning |

**Recommendation:** Start with command hooks. Only use prompt hooks when semantic understanding is required.

## Validation Checklist

- [ ] Prompt returns valid JSON
- [ ] JSON includes `ok` field (boolean)
- [ ] Blocking response includes `reason` field
- [ ] Timeout configured appropriately
- [ ] Prompt includes sufficient context
- [ ] Prompt specifies expected output format
- [ ] Examples provided for complex decisions
- [ ] Hook tested with various inputs
