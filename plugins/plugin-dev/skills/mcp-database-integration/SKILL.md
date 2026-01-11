---
name: mcp-database-integration
description: USE when user wants to integrate database via MCP, set up database connection, query databases through MCP, configure PostgreSQL/MySQL/SQLite via MCP, or mentions database MCP servers. Provides comprehensive guidance for connecting databases to Claude Code via Model Context Protocol for secure database operations.
---

# Database MCP Integration for Claude Code Plugins

## Overview

Integrate databases into Claude Code plugins using Model Context Protocol (MCP). Database MCP servers provide secure, structured access to databases including PostgreSQL, MySQL, SQLite, and other database systems through a standardized interface.

**Key capabilities:**
- Connect to multiple database types (PostgreSQL, MySQL, SQLite, etc.)
- Execute SQL queries safely through MCP interface
- Manage database connections with environment variables
- Support for connection pooling and transaction management
- Schema introspection and metadata queries
- Batch operations for performance

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

**Example with connection pooling:**
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"],
    "env": {
      "DATABASE_URL": "${POSTGRES_URL}",
      "PGSSLMODE": "require",
      "PGPOOL_SIZE": "10"
    }
  }
}
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

**Environment setup:**
```bash
export MYSQL_CONNECTION_STRING="mysql://user:pass@localhost:3306/database_name"
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

**Environment setup:**
```bash
export SQLITE_DB_PATH="/path/to/your/database.db"
```

### Custom Database Servers

For specialized database needs or proprietary systems, create custom MCP servers.

**Configuration:**
```json
{
  "custom-db": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/custom-database-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config/db.json"],
    "env": {
      "DB_TYPE": "${DB_TYPE}",
      "DB_HOST": "${DB_HOST}",
      "DB_PORT": "${DB_PORT}",
      "DB_NAME": "${DB_NAME}",
      "DB_USER": "${DB_USER}",
      "DB_PASSWORD": "${DB_PASSWORD}"
    }
  }
}
```

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

```bash
export POSTGRES_URL="postgresql://user:pass@host:port/dbname"
```

### Pattern 2: Individual Parameters

Break connection into components for better configuration management:

```json
{
  "postgres": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/postgres-server",
    "env": {
      "PGHOST": "${DB_HOST}",
      "PGPORT": "${DB_PORT}",
      "PGDATABASE": "${DB_NAME}",
      "PGUSER": "${DB_USER}",
      "PGPASSWORD": "${DB_PASSWORD}",
      "PGSSLMODE": "require"
    }
  }
}
```

### Pattern 3: Environment File

Use .env files for development (add to .gitignore):

```bash
# .env file
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=myuser
DB_PASSWORD=mypassword
DB_SSL=true
```

```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"],
    "env": {
      "DATABASE_URL": "postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"
    }
  }
}
```

## Using Database MCP Tools

### Tool Naming

Database MCP tools follow the standard naming convention:

```
mcp__plugin_<plugin-name>_<server-name>__<operation>
```

**Common operations:**
- `query` - Execute SELECT queries
- `execute` - Execute INSERT/UPDATE/DELETE
- `describe` - Get table/schema information
- `list_tables` - List all tables/views

**Example:**
- `mcp__plugin_myplugin_postgres__query`
- `mcp__plugin_myplugin_postgres__execute`
- `mcp__plugin_myplugin_postgres__list_tables`

### Pre-allowing Database Tools

In command frontmatter:

```markdown
---
allowed-tools: [
  "mcp__plugin_myplugin_postgres__query",
  "mcp__plugin_myplugin_postgres__execute",
  "mcp__plugin_myplugin_postgres__list_tables"
]
---
```

### Query Execution Pattern

```markdown
Steps:
1. **Validate SQL**: Ensure query is safe (SELECT only for query operations)
2. **Execute query**: Use mcp__plugin_myplugin_postgres__query with SQL string
3. **Process results**: Format returned data
4. **Handle errors**: Check for SQL errors and timeouts
5. **Present data**: Display results to user
```

### Example: Data Retrieval Command

```markdown
# Command: query-data.md
---
description: Query data from PostgreSQL database
allowed-tools: [
  "mcp__plugin_myplugin_postgres__query",
  "mcp__plugin_myplugin_postgres__list_tables"
]
---

# Database Query Command

## Listing Tables

To see available tables:
1. Use mcp__plugin_myplugin_postgres__list_tables
2. Display table list to user

## Querying Data

To query table data:
1. Ask user for table name and optional WHERE clause
2. Validate table name (prevent SQL injection)
3. Use mcp__plugin_myplugin_postgres__query with constructed SQL:
   - SELECT * FROM table_name WHERE condition
   - LIMIT results to prevent overflow
4. Format results as markdown table
5. Show row count and execution time
```

### Example: Data Insertion Command

```markdown
# Command: insert-data.md
---
description: Insert data into PostgreSQL database
allowed-tools: [
  "mcp__plugin_myplugin_postgres__execute"
]
---

# Insert Data Command

## Safety First

⚠️ This command executes write operations on your database.

## Insert Process

1. **Gather data**: Collect values from user
2. **Validate data**: Check required fields and data types
3. **Construct SQL**: Build INSERT statement with parameterized values
4. **Execute**: Use mcp__plugin_myplugin_postgres__execute
5. **Confirm**: Show affected rows and new record ID
6. **Error handling**: Rollback on failure, show helpful error

## Required Information

- Table name
- Column values (as JSON object)
- Optional: RETURNING clause for inserted ID
```

## Security Best Practices

### Credential Management

**DO:**
- ✅ Use environment variables for all credentials
- ✅ Use .gitignore for .env files
- ✅ Use connection pooling for performance
- ✅ Use SSL/TLS for production databases
- ✅ Rotate database credentials regularly
- ✅ Use read-only users for query operations
- ✅ Validate table/column names before query

**DON'T:**
- ❌ Hardcode credentials in configuration
- ❌ Commit .env files to git
- ❌ Use database root/admin accounts
- ❌ Skip SSL in production
- ❌ Execute unvalidated user input
- ❌ Run without connection limits

### SQL Injection Prevention

**Use parameterized queries:**
```markdown
Steps:
1. Validate table names against whitelist
2. Validate column names against schema
3. Use parameterized values for user data
4. Never concatenate user input directly into SQL
5. Example:
   ✅ SELECT * FROM users WHERE id = $1 (with parameterized value)
   ❌ SELECT * FROM users WHERE id = ' + user_input + ' (DANGER!)
```

**Validate identifiers:**
```markdown
Steps:
1. Get schema via mcp__plugin_myplugin_postgres__describe
2. Build whitelist of valid tables/columns
3. Check user input against whitelist
4. Reject invalid identifiers
```

### Connection Security

**Production configuration:**
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"],
    "env": {
      "DATABASE_URL": "${POSTGRES_URL}",
      "PGSSLMODE": "require",
      "PGSSLROOTCERT": "${SSL_CERT_PATH}",
      "PGSSLCERT": "${SSL_CLIENT_CERT}",
      "PGSSLKEY": "${SSL_CLIENT_KEY}"
    }
  }
}
```

**Environment variables:**
```bash
export POSTGRES_URL="postgresql://app_user:secure_password@db.example.com:5432/production_db"
export SSL_CERT_PATH="/path/to/ca-cert.pem"
export SSL_CLIENT_CERT="/path/to/client-cert.pem"
export SSL_CLIENT_KEY="/path/to/client-key.pem"
```

## Performance Optimization

### Connection Pooling

Configure pool size based on workload:

```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"],
    "env": {
      "DATABASE_URL": "${POSTGRES_URL}",
      "PGPOOL_SIZE": "20",          # Production: 10-20
      "PGPOOL_MAX": "30",           # Max connections
      "PGPOOL_MIN": "5"             # Min connections
    }
  }
}
```

### Query Optimization

**In commands:**
```markdown
Steps:
1. **Limit results**: Always use LIMIT for SELECT queries
2. **Use indexes**: Help users write efficient queries
3. **Paginate large results**: Implement pagination for big datasets
4. **Cache metadata**: Cache schema information
5. **Batch operations**: Use bulk insert/update when possible

Example query pattern:
SELECT column1, column2, column3
FROM table_name
WHERE condition
ORDER BY column
LIMIT 100 OFFSET 0
```

### Transaction Management

For multi-operation workflows:

```markdown
Steps:
1. **Start transaction**: BEGIN (if supported by MCP server)
2. **Execute operations**: Series of queries
3. **Commit or rollback**: Based on success
4. **Handle errors**: Automatic rollback on failure

Note: Not all MCP servers support explicit transactions.
Check server documentation for transaction support.
```

## Error Handling

### Common Database Errors

**Connection errors:**
```markdown
On connection failure:
1. Check DATABASE_URL format
2. Verify database server is running
3. Check network connectivity
4. Verify credentials
5. Check SSL configuration
6. Suggest: "Verify your DATABASE_URL environment variable"
```

**Authentication errors:**
```markdown
On auth failure:
1. Verify username/password
2. Check user permissions
3. Verify database exists
4. Check IP whitelist (if configured)
5. Suggest: "Check your database credentials in environment variables"
```

**Query errors:**
```markdown
On SQL error:
1. Check query syntax
2. Verify table/column names
3. Check data types
4. Verify permissions
5. Show helpful error (not raw SQL error)
```

### Timeout Handling

```markdown
Steps:
1. **Set reasonable timeouts**: 30 seconds for queries, 60 for complex ops
2. **Handle timeout errors**: Inform user and suggest optimization
3. **Suggest indexing**: Help users optimize slow queries
4. **Implement retry logic**: For transient network errors
```

## Testing Database Integration

### Local Testing Setup

**SQLite (easiest for testing):**
```bash
# Create test database
export SQLITE_DB_PATH="${CLAUDE_PLUGIN_ROOT}/test.db"
```

**PostgreSQL (Docker):**
```bash
# Start PostgreSQL in Docker
docker run --name test-postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=testdb \
  -p 5432:5432 \
  -d postgres:15

export POSTGRES_URL="postgresql://postgres:password@localhost:5432/testdb"
```

### Test Scenarios

**Connection test:**
```markdown
Steps:
1. Configure database MCP server
2. Use mcp__plugin_myplugin_postgres__query to execute:
   SELECT version();
3. Verify connection works
4. Check response time
```

**Query test:**
```markdown
Steps:
1. Create test table via database admin tools
2. Insert test data
3. Query via MCP tool
4. Verify results match expected
```

**Error test:**
```markdown
Steps:
1. Test with invalid credentials
2. Test with non-existent table
3. Test with invalid SQL syntax
4. Verify graceful error handling
```

## Multi-Database Support

### Multiple Database Servers

Configure multiple databases in same plugin:

```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "${POSTGRES_URL}"]
  },
  "mysql": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-mysql", "${MYSQL_URL}"]
  },
  "sqlite": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sqlite", "${SQLITE_PATH}"]
  }
}
```

### Cross-Database Commands

```markdown
# Command: sync-databases.md
---
description: Synchronize data between PostgreSQL and SQLite
allowed-tools: [
  "mcp__plugin_myplugin_postgres__query",
  "mcp__plugin_myplugin_postgres__execute",
  "mcp__plugin_myplugin_sqlite__query",
  "mcp__plugin_myplugin_sqlite__execute"
]
---

## Sync Process

1. **Query source**: Get data from PostgreSQL
2. **Transform**: Convert data format if needed
3. **Insert target**: Insert into SQLite
4. **Verify**: Check row counts match
5. **Report**: Show sync summary
```

## Database-Specific Considerations

### PostgreSQL

**Special features:**
- JSON/JSONB support
- Array types
- Full-text search
- Extensions (PostGIS, etc.)

**Example JSON query:**
```sql
SELECT data->>'field_name'
FROM table_name
WHERE data ? 'key_name'
```

### MySQL

**Special features:**
- JSON functions
- Full-text indexes
- Spatial data

**Example JSON query:**
```sql
SELECT JSON_EXTRACT(data, '$.field_name')
FROM table_name
WHERE JSON_CONTAINS(data, '"value"', '$.key_name')
```

### SQLite

**Special features:**
- JSON1 extension (built-in)
- FTS5 for full-text search
- No external dependencies

**Example JSON query:**
```sql
SELECT json_extract(data, '$.field_name')
FROM table_name
WHERE json_type(data, '$.key_name') IS NOT NULL
```

## Best Practices Summary

### For Plugin Developers

1. **Choose right database type**:
   - SQLite for local/simple apps
   - PostgreSQL for complex features
   - MySQL for existing infrastructure

2. **Secure configuration**:
   - Always use environment variables
   - Enable SSL in production
   - Use connection pooling
   - Implement query timeouts

3. **User experience**:
   - Provide helpful error messages
   - Suggest optimizations
   - Limit result sets
   - Show execution time

4. **Testing**:
   - Test with real database
   - Test error scenarios
   - Test performance
   - Document requirements

### For Plugin Users

1. **Setup**:
   - Install required MCP server package
   - Set environment variables
   - Test connection before use

2. **Security**:
   - Never commit .env files
   - Use strong database passwords
   - Enable SSL
   - Rotate credentials

3. **Performance**:
   - Index frequently queried columns
   - Limit result sets
   - Use prepared statements
   - Monitor query performance

## Quick Reference

### MCP Server Types for Databases

| Database | Package | Server Type | Example |
|----------|---------|-------------|---------|
| PostgreSQL | @modelcontextprotocol/server-postgres | stdio | `npx -y @modelcontextprotocol/server-postgres $DATABASE_URL` |
| MySQL | @modelcontextprotocol/server-mysql | stdio | `npx -y @modelcontextprotocol/server-mysql $MYSQL_URL` |
| SQLite | @modelcontextprotocol/server-sqlite | stdio | `npx -y @modelcontextprotocol/server-sqlite $DB_PATH` |

### Common Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `query` | SELECT operations | Query data from tables |
| `execute` | INSERT/UPDATE/DELETE | Modify data |
| `describe` | Schema information | Get table structure |
| `list_tables` | List tables/views | Discover database schema |

### Configuration Checklist

- [ ] MCP server installed (`npm install -g @modelcontextprotocol/server-postgres`)
- [ ] Environment variables set
- [ ] Database accessible from plugin host
- [ ] SSL configured (production)
- [ ] Connection pooling configured
- [ ] Query timeout set
- [ ] Test connection works
- [ ] Error handling implemented

## Implementation Workflow

To add database integration to a plugin:

1. **Choose database type** (PostgreSQL, MySQL, SQLite)
2. **Install MCP server** (`npm install -g @modelcontextprotocol/server-postgres`)
3. **Configure in .mcp.json** with environment variables
4. **Document required environment variables** in README
5. **Create commands** for database operations
6. **Pre-allow database tools** in commands
7. **Implement error handling** for common issues
8. **Test with sample database**
9. **Add security checks** and validation
10. **Document setup instructions**

## Additional Resources

### Reference Files

For detailed information, consult:

- **`references/security.md`** - Database security patterns and best practices
- **`references/performance.md`** - Query optimization and connection management
- **`references/schema-management.md`** - Schema introspection and migration strategies

### Example Configurations

Working examples in `examples/`:
- **`postgres-config.json`** - Complete PostgreSQL configuration
- **`mysql-config.json`** - MySQL with SSL and pooling
- **`sqlite-config.json`** - SQLite for local development
- **`multi-db-config.json`** - Multiple database servers

### External Resources

- **PostgreSQL MCP Server**: https://github.com/modelcontextprotocol/servers/tree/main/src/postgres
- **MySQL MCP Server**: https://github.com/modelcontextprotocol/servers/tree/main/src/mysql
- **SQLite MCP Server**: https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Database Security**: OWASP Database Security Cheat Sheet

Focus on PostgreSQL for production databases, SQLite for local development, and always use environment variables for credentials.