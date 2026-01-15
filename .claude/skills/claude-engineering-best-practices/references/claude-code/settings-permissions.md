# Settings & Permissions — Stable Patterns

Claude Code configuration uses a layered settings system with scope-based precedence.

## Configuration Scopes

### Scope Hierarchy (Highest to Lowest Precedence)

1. **Managed Settings** (`managed-settings.json`)
   - Admin-controlled, read-only
   - Enforced across organization

2. **Local Project** (`.claude/settings.local.json`)
   - Gitignored
   - Per-machine overrides

3. **Project** (`.claude/settings.json`)
   - Version controlled
   - Team-shared configuration

4. **User** (`~/.claude/settings.json`)
   - Personal settings
   - All projects inherit

### File Locations
```
~/
├── .claude/
│   ├── settings.json         # User scope
│   └── settings.local.json    # Local overrides

project/
├── .claude/
│   ├── settings.json          # Project scope
│   └── settings.local.json   # Local overrides

# Enterprise
managed-settings.json          # Managed scope (read-only)
```

## Common Configuration Patterns

### Pattern 1: User Settings (~/.claude/settings.json)
```json
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep", "Edit", "Bash"],
    "allowedDomains": ["github.com", "*.company.com"]
  },
  "sandbox": {
    "mode": "auto-allow"
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "~/bin/validate.sh"}
        ]
      }
    ]
  }
}
```

### Pattern 2: Project Settings (.claude/settings.json)
```json
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep", "Edit"],
    "deniedTools": ["WebFetch", "WebSearch"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {"type": "command", "command": "./.claude/hooks/format.sh"}
        ]
      }
    ]
  },
  "outputStyles": [".claude/styles/"]
}
```

### Pattern 3: Local Settings (.claude/settings.local.json)
```json
{
  "sandbox": {
    "network": {
      "allowedDomains": ["localhost", "127.0.0.1", "*.local"]
    }
  }
}
```

## Permission System

### Permission Modes

#### default
- Standard interaction
- Permission prompts for sensitive operations
- Interactive approval required

#### plan
- Generate plans only
- No execution
- For reviewing Claude's approach

#### acceptEdits
- Auto-accept file edit permissions
- Reduces prompts for code modifications
- Still prompts for dangerous operations

#### dontAsk
- No permission prompts
- Use with extreme caution
- All operations auto-approved

#### bypassPermissions
- Ignore permission settings
- Use only in controlled environments
- Most permissive mode

### Tool Permissions

#### Allowed Tools Pattern
```json
{
  "permissions": {
    "allowedTools": [
      "Read",
      "Glob",
      "Grep",
      "Edit",
      "Write",
      "Bash",
      "WebFetch",
      "WebSearch"
    ]
  }
}
```

**Common tool groups**:

**Safe (Read-only)**:
```json
"allowedTools": ["Read", "Glob", "Grep", "Bash"]
```

**Development**:
```json
"allowedTools": ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]
```

**Full Access**:
```json
"allowedTools": ["Read", "Glob", "Grep", "Edit", "Write", "Bash", "WebFetch", "WebSearch"]
```

#### Denied Tools Pattern
```json
{
  "permissions": {
    "deniedTools": ["WebFetch", "WebSearch"],
    "allowedTools": ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]
  }
}
```

### Domain Permissions

#### Allowed Domains Pattern
```json
{
  "permissions": {
    "allowedDomains": [
      "github.com",
      "*.company.com",
      "api.company.com"
    ]
  }
}
```

**Domain patterns**:
- `domain.com`: Exact match
- `*.domain.com`: Subdomain wildcard
- `*domain.com`: Prefix wildcard (not recommended)

#### Domain Security Best Practices
1. **Be specific**: Use exact domains when possible
2. **Avoid wildcards**: Especially `*` alone
3. **Group related**: Use wildcard for internal services
4. **Document**: Comment why each domain is allowed

## Hook Configuration

### User Hooks
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/validate-bash.sh",
            "timeout": 30
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/format.sh"
          }
        ]
      }
    ]
  }
}
```

### Project Hooks
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/hooks/project-init.sh"
          }
        ]
      }
    ]
  }
}
```

### Hook Scoping
- **User hooks**: Apply to all projects
- **Project hooks**: Apply to specific project
- **Plugin hooks**: Apply when plugin enabled
- **Merged at runtime**: All sources combined

## Output Styles

### Custom Output Format
```json
{
  "outputStyles": [".claude/styles/"]
}
```

**Directory structure**:
```
.claude/
└── styles/
    ├── json.md
    ├── yaml.md
    └── custom-format.md
```

**Style file format**:
```markdown
---
name: json
description: Structured JSON output
---

# JSON Output

Use this format for:
- Machine-readable results
- API responses
- Structured data

## Format
```json
{
  "status": "success|error",
  "data": { ... }
}
```
```

## Sandbox Settings

### Enable Sandboxing
```json
{
  "sandbox": {
    "mode": "auto-allow",
    "filesystem": {
      "allowedPaths": ["./"],
      "deniedPaths": ["~/.ssh", "~/.*_key"]
    },
    "network": {
      "allowedDomains": ["github.com", "registry.npmjs.org"]
    }
  }
}
```

### Sandbox Configuration Options
```json
{
  "sandbox": {
    "mode": "auto-allow|regular",
    "allowUnsandboxedCommands": true|false,
    "excludedCommands": ["docker", "vagrant"],
    "filesystem": {
      "allowedPaths": ["./", "../shared"],
      "deniedPaths": ["~/.ssh", "/etc"]
    },
    "network": {
      "allowedDomains": ["github.com"],
      "httpProxyPort": 8080,
      "socksProxyPort": 8081,
      "customProxy": "/path/to/proxy.sh"
    },
    "enableWeakerNestedSandbox": false
  }
}
```

## Best Practices

### 1. Scope Appropriately
- **User**: Personal preferences, tools, hooks
- **Project**: Team standards, shared hooks
- **Local**: Machine-specific overrides
- **Managed**: Organization-wide policies

### 2. Follow Principle of Least Privilege
```json
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep"],
    "deniedTools": ["WebFetch", "WebSearch"]
  }
}
```
Start restrictive, expand as needed.

### 3. Document Permissions
```json
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep", "Edit", "Write"],
    "deniedTools": ["WebFetch", "WebSearch"],
    "comments": {
      "allowedTools": "Local development only, no external access",
      "deniedTools": "Prevent data exfiltration"
    }
  }
}
```

### 4. Use Multiple Layers
```json
// User: General tools
"allowedTools": ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]

// Project: Disable web tools
"deniedTools": ["WebFetch", "WebSearch"]

// Hook: Validate bash commands
"hooks": { "PreToolUse": [...] }
```

### 5. Environment-Specific Configs
```bash
# Development
cp .claude/settings.dev.json .claude/settings.json

# Production
cp .claude/settings.prod.json .claude/settings.json
```

### 6. Validate Configuration
```bash
# Check for syntax errors
cat .claude/settings.json | jq .

# Validate against schema (if available)
claude settings validate
```

## Common Patterns by Use Case

### Pattern 1: Read-Only Analysis
```json
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep"],
    "permissionMode": "plan"
  }
}
```

### Pattern 2: Safe Development
```json
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep", "Edit", "Write", "Bash"],
    "permissionMode": "acceptEdits"
  },
  "sandbox": {
    "mode": "auto-allow",
    "network": {
      "allowedDomains": ["github.com"]
    }
  }
}
```

### Pattern 3: Production Deployment
```json
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep"],
    "permissionMode": "default"
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "./.claude/hooks/deploy-validate.sh"}
        ]
      }
    ]
  }
}
```

### Pattern 4: No Network
```json
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep", "Edit", "Write", "Bash"],
    "deniedTools": ["WebFetch", "WebSearch"]
  },
  "sandbox": {
    "network": {
      "allowedDomains": []
    }
  }
}
```

## Troubleshooting

### Configuration Not Applying

**Check scope precedence**:
1. Managed settings override all
2. Local overrides project
3. Project overrides user

**Verify file location**:
```bash
ls -la ~/.claude/settings.json
ls -la .claude/settings.json
ls -la .claude/settings.local.json
```

**Check for syntax errors**:
```bash
cat settings.json | jq . > /dev/null
# Should exit 0
```

### Permission Denied

**Check permission mode**:
```json
{
  "permissions": {
    "permissionMode": "bypassPermissions"
  }
}
```

**Verify tool is allowed**:
```json
{
  "permissions": {
    "allowedTools": ["ToolName"]
  }
}
```

### Hook Not Running

**Check hook configuration**:
```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "script.sh"
          }
        ]
      }
    ]
  }
}
```

**Verify script is executable**:
```bash
chmod +x script.sh
```

### Sandbox Blocking Operations

**Check sandbox mode**:
```json
{
  "sandbox": {
    "mode": "regular"  # May require approval
  }
}
```

**Review allowed paths/domains**:
```json
{
  "sandbox": {
    "filesystem": {"allowedPaths": ["./"]},
    "network": {"allowedDomains": ["domain.com"]}
  }
}
```

## Migration Patterns

### From No Sandbox to Sandbox
```json
{
  "sandbox": {
    "mode": "regular",
    "filesystem": {
      "allowedPaths": ["./"]
    },
    "network": {
      "allowedDomains": []
    }
  }
}
```
Gradually expand permissions as needed.

### From Permissive to Restrictive
```json
{
  "permissions": {
    "deniedTools": ["WebFetch", "WebSearch"],
    "allowedTools": ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]
  }
}
```

### Adding Hooks Incrementally
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [{"type": "command", "command": "./.claude/hooks/log.sh"}]
      }
    ]
  }
}
```

## Volatile Details (Look Up)

These change frequently:
- Exact permission mode names
- New tools (check latest docs)
- Hook event names
- Sandbox configuration options

**Always verify**: Use `curl -sL https://code.claude.com/docs/en/settings.md | rg pattern`

---

## Official Documentation Links

- **Settings & Configuration**: https://code.claude.com/docs/en/settings.md
- **IAM/Permissions**: https://code.claude.com/docs/en/iam
- **Hooks Reference**: https://code.claude.com/docs/en/hooks.md
- **Sandboxing**: https://code.claude.com/docs/en/sandboxing.md
- **Claude Code Overview**: https://code.claude.com/docs/en/overview

### Verification
Last verified: 2026-01-13
