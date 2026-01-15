# MCP & LSP Integration — Stable Patterns

Model Context Protocol (MCP) and Language Server Protocol (LSP) provide integration patterns for external tools and code intelligence.

## MCP (Model Context Protocol)

### What MCP Provides
- **Standardized interface**: Unified protocol for tool integration
- **Client-server architecture**: Standard way to connect tools to agents
- **Tool discovery**: Automatic discovery of available tools
- **Rich tool schemas**: Structured input/output definitions

### Architecture Pattern
```
Claude Code ←→ MCP Client ←→ MCP Server ←→ External Tool
                     ↕                ↕
                JSON-RPC          Actual Service
```

### Common MCP Servers

#### Filesystem Server
- Read/write files
- Directory operations
- Search capabilities

#### Git Server
- Repository operations
- Commit history
- Branch management

#### Database Servers
- SQL query execution
- Schema introspection
- Connection management

#### API Servers
- REST API calls
- Authentication handling
- Response transformation

### MCP Configuration Pattern
```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["@scope/mcp-server"],
      "cwd": "/path/to/server",
      "env": {
        "API_KEY": "value"
      },
      "transport": "stdio|sse"
    }
  }
}
```

### MCP Tool Naming
Tools appear as: `mcp__<server>__<tool>`
- `mcp__filesystem__read_file`
- `mcp__memory__create_entities`
- `mcp__github__search_repositories`

### Hooks for MCP Tools
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__.*__.*",
        "hooks": [
          {
            "type": "command",
            "command": "validate-mcp-tool.sh"
          }
        ]
      }
    ]
  }
}
```

## LSP (Language Server Protocol)

### What LSP Provides
- **Real-time diagnostics**: Immediate error feedback
- **Code navigation**: Go to definition, find references
- **Language awareness**: Type information, hover docs
- **Completion**: Intelligent code completion

### Architecture Pattern
```
Claude Code ←→ LSP Client ←→ LSP Server ←→ Language Tool
                     ↕               ↕
                Language ID        Parsing/Analyzing
```

### LSP Configuration Pattern
```json
{
  "lspServers": {
    "language-id": {
      "command": "server-binary",
      "args": ["serve"],
      "extensionToLanguage": {
        ".ext": "language-id"
      },
      "transport": "stdio|socket",
      "env": {},
      "initializationOptions": {},
      "settings": {},
      "workspaceFolder": "/path/to/workspace",
      "startupTimeout": 30000,
      "shutdownTimeout": 5000,
      "restartOnCrash": true,
      "maxRestarts": 5
    }
  }
}
```

### Common LSP Servers

#### Python
```json
{
  "python": {
    "command": "pyright-langserver",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".py": "python"
    }
  }
}
```

#### TypeScript/JavaScript
```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescript",
      ".js": "javascript",
      ".jsx": "javascript"
    }
  }
}
```

#### Rust
```json
{
  "rust": {
    "command": "rust-analyzer",
    "args": [],
    "extensionToLanguage": {
      ".rs": "rust"
    }
  }
}
```

#### Go
```json
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

## Security Considerations

### MCP Security
1. **Trust boundaries**: MCP servers run with user permissions
2. **Network access**: Servers can make external requests
3. **Data access**: Servers read files user can access
4. **Tool capabilities**: May have broad capabilities

**Best practices**:
- Run servers in sandbox
- Validate server scripts
- Limit network access
- Audit server code

### LSP Security
1. **Local execution**: Servers run locally
2. **File access**: Can read all project files
3. **Process execution**: May spawn processes
4. **Resource usage**: Can consume CPU/memory

**Best practices**:
- Use trusted language servers
- Monitor resource usage
- Limit file access if needed
- Validate server versions

## Common Patterns

### Pattern 1: MCP Server with Environment Variables
```json
{
  "mcpServers": {
    "database": {
      "command": "node",
      "args": ["./servers/db-server.js"],
      "env": {
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_NAME": "app"
      }
    }
  }
}
```

### Pattern 2: LSP with Custom Settings
```json
{
  "lspServers": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "initializationOptions": {
        "preferences": {
          "includePackageJsonAutoImports": "on"
        }
      },
      "settings": {
        "typescript": {
          "suggest": {
            "includeAutoImports": true
          }
        }
      }
    }
  }
}
```

### Pattern 3: Multiple MCP Servers
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
    },
    "git": {
      "command": "node",
      "args": ["./servers/git-server.js"]
    }
  }
}
```

### Pattern 4: LSP with Socket Transport
```json
{
  "lspServers": {
    "python": {
      "command": "pyright-langserver",
      "args": ["--socket", "3000"],
      "transport": "socket",
      "startupTimeout": 10000
    }
  }
}
```

## Troubleshooting

### MCP Issues

#### Server Not Starting
```bash
# Check server logs
claude --debug

# Verify command exists
which server-binary

# Test server manually
./servers/db-server.js --help
```

#### Tools Not Appearing
1. Verify MCP config in settings
2. Check server initialized successfully
3. Ensure tool names follow `mcp__<server>__<tool>` pattern
4. Review debug logs

#### Connection Timeouts
```json
{
  "mcpServers": {
    "slow-server": {
      "command": "node",
      "args": ["server.js"],
      "timeout": 60000
    }
  }
}
```

### LSP Issues

#### Server Not Found
```bash
# Install language server
npm install -g typescript-language-server

# Or use local installation
npm install typescript-language-server
```

#### Diagnostics Not Updating
1. Restart LSP server
2. Check file associations
3. Verify server running
4. Review settings

#### Performance Issues
```json
{
  "lspServers": {
    "heavy-language": {
      "command": "server",
      "args": ["--max-memory", "512mb"]
    }
  }
}
```

## Best Practices

### MCP
1. **Version pinning**: Lock server versions
2. **Health checks**: Monitor server status
3. **Timeout settings**: Prevent hangs
4. **Resource limits**: Control memory/CPU
5. **Security audit**: Review server code

### LSP
1. **Install globally**: Better performance
2. **Configure properly**: Optimize for language
3. **Restart when needed**: Clear state
4. **Monitor resources**: Watch memory usage
5. **Use trusted servers**: Official/maintained

## Integration Patterns

### Pattern 1: MCP for External APIs
```json
{
  "mcpServers": {
    "jira": {
      "command": "node",
      "args": ["./servers/jira-server.js"],
      "env": {
        "JIRA_URL": "https://company.atlassian.net"
      }
    }
  }
}
```

### Pattern 2: LSP for Multi-Language Projects
```json
{
  "lspServers": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "extensionToLanguage": {
        ".ts": "typescript",
        ".tsx": "typescript"
      }
    },
    "python": {
      "command": "pyright-langserver",
      "args": ["--stdio"],
      "extensionToLanguage": {
        ".py": "python"
      }
    },
    "rust": {
      "command": "rust-analyzer",
      "args": [],
      "extensionToLanguage": {
        ".rs": "rust"
      }
    }
  }
}
```

### Pattern 3: Combining MCP and LSP
```json
{
  "mcpServers": {
    "database": {
      "command": "node",
      "args": ["./servers/db-server.js"]
    }
  },
  "lspServers": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"]
    }
  }
}
```

## Volatile Details (Look Up)

These change frequently:
- MCP server protocols (latest version)
- LSP server implementations
- Language server command names
- Transport mechanisms

**Always verify**: Use latest official documentation for current versions and configurations.

## Resources

### Official MCP Servers
- GitHub: https://github.com/modelcontextprotocol/servers
- npm registry: @modelcontextprotocol/server-*

### LSP Servers by Language
- Python: pyright, pylsp, jedi-language-server
- TypeScript: typescript-language-server
- Rust: rust-analyzer
- Go: gopls
- Java: jdtls
- C/C++: clangd

### Documentation
- MCP Spec: https://modelcontextprotocol.io
- LSP Spec: https://microsoft.github.io/language-server-protocol/

---

## Official Documentation Links

- **MCP Integration**: https://code.claude.com/docs/en/mcp.md
- **Model Context Protocol**: https://modelcontextprotocol.io
- **Language Server Protocol**: https://microsoft.github.io/language-server-protocol/
- **MCP Servers Repository**: https://github.com/modelcontextprotocol/servers
- **Claude Code Overview**: https://code.claude.com/docs/en/overview

### Verification
Last verified: 2026-01-13
