---
name: meta-mcp
description: "Provides comprehensive MCP integration guidance for Claude Code plugins. MUST Use when integrating databases via MCP, setting up MCP servers, or configuring connections."
---

# Database MCP Integration for Claude Code Plugins

Integrate databases into Claude Code plugins using Model Context Protocol (MCP). Database MCP servers provide secure, structured access to databases through a standardized interface.

## Guidelines

- **Configuration**: See [references/mcp-configuration.md](references/mcp-configuration.md) for server types, connection patterns, and environment setup.
- **Security**: See [references/security.md](references/security.md) for authentication, SSL, and access control.
- **Performance**: See [references/performance.md](references/performance.md) for connection pooling and query optimization.
- **Schema**: See [references/schema-management.md](references/schema-management.md) for introspection and management.

---

## Quick Reference

### 1. Choose Database Type and Configure
- PostgreSQL: `@modelcontextprotocol/server-postgres`
- MySQL: `@modelcontextprotocol/server-mysql`
- SQLite: `@modelcontextprotocol/server-sqlite`

### 2. Set Environment Variables
```bash
export POSTGRES_URL="postgresql://user:pass@host:5432/db?sslmode=require"
```

### 3. Add to settings.json
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

## Resources

### References
- **[references/mcp-configuration.md](references/mcp-configuration.md)**: Master configuration guide.
- **[references/security.md](references/security.md)**: Security best practices.
- **[references/performance.md](references/performance.md)**: Performance tuning.
- **[references/schema-management.md](references/schema-management.md)**: Schema operations.

### Examples
- **[examples/postgres-config.json](examples/postgres-config.json)**: PostgreSQL configuration.
- **[examples/mysql-config.json](examples/mysql-config.json)**: MySQL configuration.
- **[examples/sqlite-config.json](examples/sqlite-config.json)**: SQLite configuration.
- **[examples/multi-db-config.json](examples/multi-db-config.json)**: Multiple database setup.
