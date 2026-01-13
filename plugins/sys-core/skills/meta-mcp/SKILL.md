---
name: meta-mcp
description: "Provides comprehensive MCP integration guidance for Claude Code plugins. MUST Use when integrating databases via MCP, setting up MCP servers, or configuring connections. Do not use for API integration, web services, or general database access."
---

# MCP Integration for Claude Code Plugins

Integrate external services into Claude Code plugins using Model Context Protocol (MCP). MCP servers provide secure, structured access to databases, APIs, and other services through a standardized interface.

## Critical: Tool Definition Bloat Problem

**As MCP usage scales, two common patterns increase cost and latency:**

1. **Tool definitions overload the context window**
2. **Intermediate tool results consume additional tokens**

### The Problem:
More MCP servers → More tool definitions bloating context → Higher costs and slower performance

### Solutions:

#### 1. Code Execution Pattern (Recommended)
Instead of direct tool calls, **expose code APIs** rather than tool call definitions:

```json
{
  "mcpServers": {
    "code-exec": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-code-exec"],
      "env": {
        "SANDBOX_PATH": "/tmp/sandbox"
      }
    }
  }
}
```

**Benefits:**
- Give Claude a sandbox execution environment with filesystem
- Let Claude write code to make tool calls
- Elegant, prompt-on-demand pattern (similar to skills)
- Reduces token overhead

#### 2. Selective Tool Exposure
Only expose essential tools:

```json
{
  "mcpServers": {
    "minimal-db": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "MCP_TOOLS": "query,schema"
      }
    }
  }
}
```

#### 3. Connection Management
- **Pool connections** to reuse
- **Lazy load** servers only when needed
- **Disconnect** inactive servers

---

## Database Integration

### Quick Reference

**1. Choose Database Type and Configure**
- PostgreSQL: `@modelcontextprotocol/server-postgres`
- MySQL: `@modelcontextprotocol/server-mysql`
- SQLite: `@modelcontextprotocol/server-sqlite`

**2. Set Environment Variables**
```bash
export POSTGRES_URL="postgresql://user:pass@host:5432/db?sslmode=require"
```

**3. Add to settings.json**
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${POSTGRES_URL}"]
    }
  }
}
```

---

## Context Optimization Best Practices

### Token Management
- **Cache tool definitions** when possible
- **Batch operations** to reduce calls
- **Stream results** for large datasets
- **Compress** intermediate outputs

### Performance Guidelines
- **Connection pooling** for database servers
- **Query optimization** - limit result sets
- **Pagination** for large datasets
- **Async operations** for non-blocking execution

### Security Considerations
- **Authentication** - use environment variables
- **SSL/TLS** - encrypt all connections
- **Access control** - limit permissions
- **Input validation** - sanitize queries

---

## Resources

### References
- **[references/mcp-configuration.md](references/mcp-configuration.md)**: Master configuration guide.
- **[references/security.md](references/security.md)**: Security best practices.
- **[references/performance.md](references/performance.md)**: Performance tuning.
- **[references/schema-management.md](references/schema-management.md)**: Schema operations.

### Examples
- **[examples/postgres-config.json](examples/postgres-config.json)**: PostgreSQL configuration.
- **[examples/multi-db-config.json](examples/multi-db-config.json)**: Multiple database setup.
