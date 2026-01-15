# Sandboxing — Stable Security Patterns

Sandboxing provides filesystem and network isolation for safer agent execution with reduced permission prompts.

## Core Concepts

### Why Sandboxing
- **Reduces approval fatigue**: Fewer permission dialogs
- **Defines clear boundaries**: Explicit access limits
- **Enables autonomy**: Safe operations auto-approved
- **Maintains security**: Attempts outside sandbox blocked

### Dual Isolation Principle
**Both** filesystem and network isolation required:
- Network isolation prevents exfiltration even if filesystem compromised
- Filesystem isolation prevents backdoors even if network compromised

## Filesystem Isolation

### Default Behavior
- **Read access**: Current directory and subdirectories (read/write)
- **Global read**: Most of filesystem (read-only, blocked from config areas)
- **Write restriction**: Cannot modify files outside current directory
- **Configurable**: Custom allowed/denied paths via settings

### Safe Configuration Patterns

#### Pattern 1: Restrictive (Recommended for Production)
```json
{
  "sandbox": {
    "filesystem": {
      "allowedPaths": ["./"],
      "deniedPaths": ["~/.ssh", "~/.aws", "/etc", "~/.*"]
    }
  }
}
```

#### Pattern 2: Project-Specific
```json
{
  "sandbox": {
    "filesystem": {
      "allowedPaths": ["./", "../shared-utilities"],
      "deniedPaths": ["../secrets", "../config"]
    }
  }
}
```

#### Pattern 3: Development
```json
{
  "sandbox": {
    "filesystem": {
      "allowedPaths": ["./", "~/.cache"],
      "deniedPaths": ["~/.ssh", "~/.*_key", "*/.env*"]
    }
  }
}
```

## Network Isolation

### How It Works
- **Proxy-based**: All network traffic through controlled proxy
- **Domain filtering**: Only approved domains accessible
- **Transparent**: Applies to all spawned processes
- **Prompted access**: New domains trigger permission requests

### Configuration Pattern
```json
{
  "sandbox": {
    "network": {
      "allowedDomains": [
        "github.com",
        "registry.npmjs.org",
        "*.company.com"
      ],
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

### Domain Best Practices

#### Allowlist Strategy (Recommended)
```json
"allowedDomains": [
  "github.com",           # Code repositories
  "registry.npmjs.org",   # Node packages
  "pypi.org",            # Python packages
  "fonts.googleapis.com", # Web fonts (if needed)
  "*.yourcompany.com"    # Internal services
]
```

**Never allow wildcard `*`** - too permissive

#### Common Allowlists by Use Case

**Web Development**:
```json
"allowedDomains": [
  "github.com",
  "registry.npmjs.org",
  "fonts.googleapis.com",
  "cdnjs.cloudflare.com"
]
```

**Data Science**:
```json
"allowedDomains": [
  "github.com",
  "pypi.org",
  "huggingface.co",
  "*.kaggle.com"
]
```

**Enterprise Development**:
```json
"allowedDomains": [
  "github.company.com",        # Internal Git
  "artifactory.company.com",  # Internal registry
  "*.internal.company.com"
]
```

## Sandbox Modes

### Auto-Allow Mode
- **Behavior**: Sandbox commands auto-execute without prompts
- **Fallback**: Non-sandboxable commands use normal permission flow
- **Best for**: Trusted development environments
- **Enable**: Via `/sandbox` command or settings

### Regular Permissions Mode
- **Behavior**: All commands require approval (sandboxed or not)
- **Best for**: Production/secure environments
- **More control**: Every action explicit

**Settings**:
```json
{
  "sandbox": {
    "mode": "auto-allow|regular"
  }
}
```

## Escape Hatch Mechanism

### What It Is
Intentional fallback for incompatible commands:
1. Command fails due to sandbox restrictions
2. Claude analyzes failure
3. May retry with `dangerouslyDisableSandbox` parameter
4. Requires explicit user permission

### When It Triggers
- Network access to non-allowed domains
- Filesystem access to denied paths
- Incompatible tools (e.g., docker, watchman)

### Disabling (Maximum Security)
```json
{
  "sandbox": {
    "allowUnsandboxedCommands": false
  }
}
```

**Effect**: All commands must be sandboxable or fail

## OS-Level Implementation

### Linux
- **Technology**: bubblewrap (bwrap)
- **Strength**: Strong isolation
- **Special case**: `enableWeakerNestedSandbox` for Docker environments (weaker security)

### macOS
- **Technology**: Seatbelt
- **Integration**: Native macOS sandboxing

**Note**: Both ensure child processes inherit restrictions

## Common Workflows

### Workflow 1: Enable Sandboxing
```bash
# Interactive
/sandbox

# Or in settings.json
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

### Workflow 2: Add Network Domain
1. Command fails: "Domain not allowed"
2. Review failure message
3. Add domain to allowlist:
   ```json
   "allowedDomains": ["newdomain.com"]
   ```
4. Re-run command

### Workflow 3: Handle Incompatible Tool
```bash
# Command fails: "docker incompatible with sandbox"
# Solution: Exclude from sandbox

{
  "sandbox": {
    "excludedCommands": ["docker", "vagrant"]
  }
}
```

## Security Patterns

### Pattern 1: Defense in Depth
```json
{
  "sandbox": {
    "filesystem": { /* fs restrictions */ },
    "network": { /* network restrictions */ }
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "validate.sh"}
        ]
      }
    ]
  }
}
```

**Result**: Sandbox + IAM + hooks = multiple security layers

### Pattern 2: Zero Trust Validation
```bash
#!/bin/bash
# validate.sh - Command hook

command=$(echo "$input" | jq -r '.tool_input.command')

# Block dangerous patterns
if [[ "$command" =~ (\>\s*\>\s*|\||\;|\&\&|\|\|) ]]; then
  echo "Complex shell operators not allowed in sandbox" >&2
  exit 2
fi

# Block file destruction
if [[ "$command" =~ (rm\s+-rf|dd\s+|mkfs) ]]; then
  echo "Destructive commands blocked" >&2
  exit 2
fi

exit 0
```

### Pattern 3: Network Monitoring
```json
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080,
      "socksProxyPort": 8081,
      "customProxy": "/path/to/proxy.sh"
    }
  }
}
```

**Custom proxy can**:
- Log all requests
- Inspect HTTPS traffic
- Apply custom filtering
- Integrate with SIEM

## Security Limitations

### Network Sandboxing
- **Domain filtering only**: Does not inspect traffic content
- **Domain fronting risk**: Possible bypass via cloud provider domains
- **User responsibility**: Only allow trusted domains

**Warning**: Broad domains like `github.com` may allow data exfiltration

### Unix Socket Access
```json
{
  "sandbox": {
    "allowUnixSockets": true
  }
}
```

**Risk**: Can grant access to powerful services (e.g., docker socket = host access)

**Mitigation**: Only allow specific sockets, not `*`

### Filesystem Permissions
```json
{
  "sandbox": {
    "filesystem": {
      "allowedPaths": ["./"],
      "deniedPaths": []
    }
  }
}
```

**Risk**: Allowing writes to `$PATH`, shell configs, or system directories enables privilege escalation

**Mitigation**: Strictly limit write permissions

### Linux Nested Sandbox
```json
{
  "sandbox": {
    "enableWeakerNestedSandbox": true
  }
}
```

**Risk**: Considerably weakens security

**Use only when**: Additional isolation enforced elsewhere (e.g., container runtime)

## Best Practices

### 1. Start Restrictive
```json
{
  "sandbox": {
    "filesystem": {
      "allowedPaths": ["./"]
    },
    "network": {
      "allowedDomains": []
    }
  }
}
```
Add permissions as needed, not the reverse.

### 2. Monitor Violations
```bash
# Enable debug mode
claude --debug

# Watch for sandbox violation messages
# Review logs regularly
```

### 3. Use Environment-Specific Configs
```
.claude/
├── settings.json          # Base config
├── settings.dev.json     # Development
├── settings.prod.json    # Production
└── settings.local.json   # Local overrides
```

### 4. Combine with IAM
```json
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep"]
  },
  "sandbox": {
    "network": {
      "allowedDomains": ["github.com"]
    }
  }
}
```

### 5. Test Configurations
```bash
# Test script
#!/bin/bash
# Attempt various operations
ls ~/.ssh  # Should fail
curl google.com  # Should fail (unless allowed)
echo "Test complete"
```

## Troubleshooting

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Command works outside, fails inside | Tool requires special access | Add to `excludedCommands` |
| Network requests failing | Domain not in allowlist | Add domain to `allowedDomains` |
| Can't read file | Outside allowed paths | Add path to `allowedPaths` |
| Write fails | Outside write scope | Stay within current directory |
| Permission prompts still showing | Using regular mode | Switch to auto-allow mode |

### Debug Steps
1. Enable debug mode: `claude --debug`
2. Run command
3. Review violation messages
4. Adjust configuration
5. Test again

### Performance Considerations
- Minimal overhead for filesystem operations
- Network proxy adds latency (acceptable)
- Child processes inherit restrictions (efficient)

## Integration Examples

### With DevContainers
```json
{
  "sandbox": {
    "filesystem": {
      "allowedPaths": ["./", "/workspaces"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.docker.io"]
    }
  }
}
```

### With Enterprise Proxy
```json
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080,
      "customProxy": "/opt/company-proxy/proxy.sh"
    }
  }
}
```

### With CI/CD
```json
{
  "sandbox": {
    "mode": "regular",
    "filesystem": {
      "allowedPaths": ["./", "/tmp/ci-artifacts"]
    },
    "network": {
      "allowedDomains": ["github.com", "registry.npmjs.org"]
    },
    "allowUnsandboxedCommands": false
  }
}
```

## Volatile Details (Look Up)

These change frequently:
- Exact configuration field names
- New sandbox modes
- OS-specific implementation details
- Proxy configuration options

**Always verify**: Use `curl -sL https://code.claude.com/docs/en/sandboxing.md | rg pattern`

---

## Official Documentation Links

- **Sandboxing Reference**: https://code.claude.com/docs/en/sandboxing.md
- **Settings & Configuration**: https://code.claude.com/docs/en/settings.md
- **CLI Reference**: https://code.claude.com/docs/en/cli-reference
- **Security Features**: https://code.claude.com/docs/en/security
- **Claude Code Overview**: https://code.claude.com/docs/en/overview

### Verification
Last verified: 2026-01-13
