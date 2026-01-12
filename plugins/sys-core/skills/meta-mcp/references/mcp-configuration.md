# Database MCP Configuration Guide

## Database MCP Server Types

### PostgreSQL MCP Server

Connect to PostgreSQL databases using environment variables for secure credential management.

**Configuration:**
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"],
    "env": {
      "DATABASE_URL": "${POSTGRES_URL}",
      "PGSSLMODE": "require"
    }
  }
}
```

**Environment setup:**
```bash
export POSTGRES_URL="postgresql://username:password@localhost:5432/database_name"
```

### MySQL MCP Server

Connect to MySQL databases with similar configuration patterns.

**Configuration:**
```json
{
  "mysql": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-mysql", "${MYSQL_URL}"],
    "env": {
      "MYSQL_URL": "${MYSQL_CONNECTION_STRING}"
    }
  }
}
```

### SQLite MCP Server

Connect to SQLite databases, perfect for local development and lightweight applications.

**Configuration:**
```json
{
  "sqlite": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sqlite", "${SQLITE_DB_PATH}"],
    "env": {
      "SQLITE_DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data/app.db"
    }
  }
}
```

### Custom Database Servers

For specialized database needs or proprietary systems, create custom MCP servers.

## Database Connection Patterns

### Pattern 1: Direct Connection String

Use complete connection strings for simple setups:

```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "${POSTGRES_URL}"]
  }
}
```

### Pattern 2: Individual Parameters

Break connection into components for better configuration management:

```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres"],
    "env": {
      "PGHOST": "${DB_HOST}",
      "PGPORT": "${DB_PORT}",
      "PGDATABASE": "${DB_NAME}",
      "PGUSER": "${DB_USER}",
      "PGPASSWORD": "${DB_PASSWORD}"
    }
  }
}
```

## Configuration Files

### settings.json

Configure MCP servers in your plugin's settings:

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

### Environment Variables

Use environment variables for sensitive credentials:

```bash
# PostgreSQL
export POSTGRES_URL="postgresql://user:pass@host:5432/db"

# MySQL
export MYSQL_CONNECTION_STRING="mysql://user:pass@host:3306/db"

# SQLite
export SQLITE_DB_PATH="/path/to/database.db"
```

## Available Tools

Once configured, MCP servers provide tools for database operations:

### PostgreSQL Tools
- `postgres_query` - Execute SELECT queries
- `postgres_execute` - Execute INSERT, UPDATE, DELETE
- `postgres_describe_table` - Get table schema
- `postgres_list_tables` - List all tables

### MySQL Tools
- `mysql_query` - Execute SELECT queries
- `mysql_execute` - Execute INSERT, UPDATE, DELETE
- `mysql_describe_table` - Get table schema
- `mysql_list_tables` - List all tables

### SQLite Tools
- `sqlite_query` - Execute SELECT queries
- `sqlite_execute` - Execute INSERT, UPDATE, DELETE
- `sqlite_describe_table` - Get table schema
- `sqlite_list_tables` - List all tables

## Environment Setup

### Development Environment

```bash
# Local PostgreSQL
export POSTGRES_URL="postgresql://localhost:5432/devdb"

# Local SQLite (relative to plugin root)
export SQLITE_DB_PATH="${CLAUDE_PLUGIN_ROOT}/data/dev.db"
```

### Production Environment

```bash
# Production PostgreSQL (with SSL)
export POSTGRES_URL="postgresql://user:pass@prod-host:5432/proddb?sslmode=require"

# Production MySQL (with SSL)
export MYSQL_CONNECTION_STRING="mysql://user:pass@prod-host:3306/proddb?ssl=true"
```

## Error Handling

Common issues and solutions:

### Connection Refused
- Verify database server is running
- Check host and port configuration
- Confirm firewall settings

### Authentication Failed
- Verify credentials are correct
- Check user permissions
- Ensure SSL settings match server requirements

### SSL Errors
- Verify SSL certificate
- Check SSL mode configuration
- Ensure client and server SSL settings match
