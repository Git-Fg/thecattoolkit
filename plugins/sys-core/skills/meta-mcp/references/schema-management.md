# Schema Management for Database MCP Integration

Complete guide to schema introspection, migration strategies, and version management for database MCP servers.

## Overview

Schema management is crucial for maintaining database integrity and enabling dynamic operations through MCP. This guide covers schema introspection, migration strategies, versioning, and best practices for database schema management.

## Schema Introspection

### PostgreSQL Schema Discovery

**List all tables:**
```sql
SELECT table_schema, table_name, table_type
FROM information_schema.tables
WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
ORDER BY table_schema, table_name;
```

**Get table structure:**
```sql
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default,
    character_maximum_length,
    numeric_precision,
    numeric_scale
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'users'
ORDER BY ordinal_position;
```

**Get indexes:**
```sql
SELECT
    i.relname AS index_name,
    a.attname AS column_name,
    ix.indisunique AS is_unique,
    ix.indisprimary AS is_primary
FROM pg_class t
JOIN pg_index ix ON t.oid = ix.indrelid
JOIN pg_class i ON i.oid = ix.indexrelid
JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(ix.indkey)
WHERE t.relkind = 'r'
  AND t.relname = 'users';
```

**Get foreign keys:**
```sql
SELECT
    tc.constraint_name,
    tc.table_name AS foreign_table_name,
    kcu.column_name AS foreign_column_name,
    ccu.table_name AS referenced_table_name,
    ccu.column_name AS referenced_column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_name = 'orders';
```

**Get triggers:**
```sql
SELECT
    trigger_name,
    event_manipulation,
    action_statement
FROM information_schema.triggers
WHERE event_object_table = 'users';
```

### MySQL Schema Discovery

**List all tables:**
```sql
SELECT table_schema, table_name, table_type
FROM information_schema.tables
WHERE table_schema NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys')
ORDER BY table_schema, table_name;
```

**Get table structure:**
```sql
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default,
    character_maximum_length,
    column_key,
    extra
FROM information_schema.columns
WHERE table_schema = 'myapp'
  AND table_name = 'users'
ORDER BY ordinal_position;
```

**Get indexes:**
```sql
SELECT
    index_name,
    non_unique,
    column_name,
    seq_in_index
FROM information_schema.statistics
WHERE table_schema = 'myapp'
  AND table_name = 'users'
ORDER BY index_name, seq_in_index;
```

**Get foreign keys:**
```sql
SELECT
    constraint_name,
    table_name,
    column_name,
    referenced_table_name,
    referenced_column_name
FROM information_schema.key_column_usage
WHERE table_schema = 'myapp'
  AND referenced_table_name IS NOT NULL;
```

### SQLite Schema Discovery

**List all tables:**
```sql
SELECT name AS table_name, type
FROM sqlite_master
WHERE type IN ('table', 'view')
  AND name NOT LIKE 'sqlite_%'
ORDER BY name;
```

**Get table structure:**
```sql
PRAGMA table_info(users);
```

**Get indexes:**
```sql
PRAGMA index_list(users);

-- Get index details
PRAGMA index_info('index_name');
```

**Get foreign keys:**
```sql
PRAGMA foreign_key_list(users);
```

## Schema Versioning

### Migration Tracking Table

**PostgreSQL migration tracking:**
```sql
CREATE TABLE schema_migrations (
    id SERIAL PRIMARY KEY,
    version VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    applied_at TIMESTAMP DEFAULT NOW(),
    checksum VARCHAR(64)
);

-- Insert initial version
INSERT INTO schema_migrations (version, description, checksum)
VALUES ('001', 'Initial schema', 'abc123...');
```

**MySQL migration tracking:**
```sql
CREATE TABLE schema_migrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    version VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    checksum VARCHAR(64)
);
```

**SQLite migration tracking:**
```sql
CREATE TABLE schema_migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    checksum VARCHAR(64)
);
```

### Version Management Script

**Check current version:**
```sql
-- PostgreSQL/MySQL
SELECT version FROM schema_migrations
ORDER BY applied_at DESC
LIMIT 1;

-- SQLite
SELECT version FROM schema_migrations
ORDER BY applied_at DESC
LIMIT 1;
```

**Check if migration applied:**
```sql
-- PostgreSQL/MySQL
SELECT EXISTS(
    SELECT 1 FROM schema_migrations
    WHERE version = '002'
);
```

### Migration Naming Convention

**Use semantic versioning:**
- Format: `YYYYMMDD_HHMMSS_description.sql`
- Examples:
  - `20240115_143000_create_users_table.sql`
  - `20240115_144500_add_user_email_index.sql`
  - `20240115_150000_create_orders_table.sql`

**Alternative: Sequential versioning:**
- Format: `V{version}__{description}.sql`
- Examples:
  - `V001__create_users_table.sql`
  - `V002__add_user_email_index.sql`
  - `V003__create_orders_table.sql`

## Migration Strategies

### Forward Migrations

**Creating a table:**
```sql
-- PostgreSQL/MySQL/SQLite
CREATE TABLE users (
    id UUID PRIMARY KEY,  -- PostgreSQL
    id CHAR(36) PRIMARY KEY,  -- MySQL/SQLite
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add index
CREATE INDEX idx_users_email ON users(email);

-- Add foreign key
ALTER TABLE orders
ADD CONSTRAINT fk_orders_user_id
FOREIGN KEY (user_id) REFERENCES users(id);
```

**Adding a column:**
```sql
ALTER TABLE users
ADD COLUMN status VARCHAR(50) DEFAULT 'active';

-- PostgreSQL - Add NOT NULL with default
ALTER TABLE users
ALTER COLUMN status SET DEFAULT 'active';

-- MySQL/SQLite - Add column with default
ALTER TABLE users
ADD COLUMN status VARCHAR(50) DEFAULT 'active';
```

**Creating an index:**
```sql
-- PostgreSQL/MySQL/SQLite
CREATE INDEX idx_users_created_at ON users(created_at);

-- PostgreSQL - Partial index
CREATE INDEX idx_active_users ON users(email)
WHERE status = 'active';
```

### Rollback Migrations

**Drop table:**
```sql
-- Reverse: Drop foreign keys first
ALTER TABLE orders DROP CONSTRAINT IF EXISTS fk_orders_user_id;

-- Drop table
DROP TABLE IF EXISTS users;
```

**Remove column:**
```sql
-- PostgreSQL/MySQL 8.0+
ALTER TABLE users DROP COLUMN IF EXISTS status;

-- MySQL < 8.0 (requires recreating table)
-- More complex, see migration script
```

**Drop index:**
```sql
-- PostgreSQL/MySQL/SQLite
DROP INDEX IF EXISTS idx_users_email;
```

### Transactional Migrations

**PostgreSQL:**
```sql
BEGIN;

-- Multiple operations in single transaction
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_orders_user_id ON orders(user_id);

ALTER TABLE orders
ADD CONSTRAINT fk_orders_user_id
FOREIGN KEY (user_id) REFERENCES users(id);

COMMIT;
```

**MySQL (InnoDB only):**
```sql
START TRANSACTION;

CREATE TABLE orders (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_user_id ON orders(user_id);

COMMIT;
```

**SQLite:**
```sql
BEGIN TRANSACTION;

CREATE TABLE orders (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_user_id ON orders(user_id);

COMMIT;
```

## Schema Validation

### Data Type Validation

**Validate against schema:**
```sql
-- PostgreSQL - Check data types
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'users';

-- MySQL - Check data types
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'myapp'
  AND table_name = 'users';
```

**Validate constraints:**
```sql
-- Check constraints
SELECT
    tc.constraint_name,
    tc.constraint_type,
    tc.table_name,
    kcu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
WHERE tc.table_name = 'users';
```

### Schema Consistency Checks

**Check referential integrity:**
```sql
-- PostgreSQL - Find orphaned records
SELECT o.id
FROM orders o
LEFT JOIN users u ON o.user_id = u.id
WHERE u.id IS NULL;

-- MySQL - Find orphaned records
SELECT o.id
FROM orders o
LEFT JOIN users u ON o.user_id = u.id
WHERE u.id IS NULL;
```

**Check index consistency:**
```sql
-- PostgreSQL - Verify indexes exist
SELECT t.relname AS table_name,
       i.relname AS index_name,
       a.attname AS column_name
FROM pg_class t,
     pg_class i,
     pg_index ix,
     pg_attribute a
WHERE t.oid = ix.indrelid
  AND i.oid = ix.indexrelid
  AND a.attrelid = t.oid
  AND a.attnum = ANY(ix.indkey)
  AND t.relkind = 'r'
  AND t.relname = 'users';
```

## Dynamic Schema Operations

### Schema Introspection via MCP

**Use MCP tools to discover schema:**
```markdown
Steps:
1. Use mcp__plugin_myplugin_postgres__query to execute:
   SELECT table_name FROM information_schema.tables
   WHERE table_schema = 'public';
2. For each table, query its structure
3. Build complete schema representation
4. Cache schema for validation
```

**Schema cache example:**
```markdown
Schema cache structure:
{
  "tables": {
    "users": {
      "columns": [
        {"name": "id", "type": "uuid", "nullable": false},
        {"name": "email", "type": "varchar", "nullable": false}
      ],
      "indexes": [
        {"name": "idx_users_email", "columns": ["email"], "unique": true}
      ]
    }
  }
}
```

### Dynamic Query Building

**Safe query builder:**
```markdown
Steps:
1. Validate table name against schema
2. Validate columns exist
3. Build SQL with whitelist
4. Execute via MCP tool

Example:
- Table: users
- Columns: id, name, email
- Query: SELECT id, name FROM users WHERE id = $1

Validation:
✓ Table 'users' exists
✓ Columns 'id', 'name' exist
✓ Table has permission for SELECT
✓ Build query safely
```

**Query validation:**
```markdown
Validate:
1. Table exists in schema cache
2. Columns exist in table
3. Query type allowed (SELECT/INSERT/UPDATE/DELETE)
4. No forbidden keywords (DROP, TRUNCATE, etc.)
5. User has permission for operation

Reject if:
- Table not in cache
- Column doesn't exist
- Forbidden operation
- User lacks permission
```

### Schema Migration via MCP

**Create migration command:**
```markdown
# Command: migrate-database.md
---
description: Execute database migrations
allowed-tools: [
  "mcp__plugin_myplugin_postgres__execute"
]
---

# Database Migration

## Apply Migrations

To apply pending migrations:
1. List all migration files
2. Check which migrations are applied
3. Execute pending migrations in order
4. Update migration tracking table
5. Report results

## Rollback Migrations

To rollback:
1. Ask user for target version
2. Verify rollback is safe
3. Execute rollback SQL
4. Update migration tracking table
5. Report results
```

**Migration execution:**
```markdown
Steps:
1. Read migration file
2. Parse migration metadata
3. Check if already applied
4. Execute migration in transaction
5. Record in schema_migrations table
6. Handle errors and rollback if needed
```

## Best Practices

### Migration Best Practices

1. **Always use transactions** - PostgreSQL/MySQL InnoDB
2. **Test migrations** - Apply to copy of production data
3. **Make migrations idempotent** - Can run multiple times safely
4. **Document migrations** - Include description and rationale
5. **Backup before migration** - Full database backup
6. **Plan rollback strategy** - Know how to undo changes
7. **Version migrations** - Sequential or timestamp based
8. **Test rollback** - Verify rollback works

### Schema Design Best Practices

1. **Use consistent naming** - snake_case, consistent prefixes
2. **Document schema** - Comments and documentation
3. **Avoid reserved words** - Use safe column names
4. **Plan for growth** - Consider future requirements
5. **Use appropriate data types** - Match data to type
6. **Index foreign keys** - Always index foreign key columns
7. **Use constraints** - NOT NULL, UNIQUE, CHECK, FOREIGN KEY
8. **Normalize appropriately** - Balance normalization and performance

### Validation Best Practices

1. **Validate all inputs** - Check types, lengths, constraints
2. **Use schema cache** - Avoid repeated introspection queries
3. **Cache schema metadata** - Store in application memory
4. **Update cache on changes** - Invalidate on schema updates
5. **Version schema** - Track schema changes over time
6. **Test schema operations** - Verify migration scripts work
7. **Monitor schema drift** - Detect unexpected changes
8. **Automate validation** - Include in CI/CD pipeline

## Schema Documentation

### Documenting Schema

**Use comments:**
```sql
-- PostgreSQL
COMMENT ON TABLE users IS 'User accounts and profile information';
COMMENT ON COLUMN users.email IS 'Primary email address, used for login';

-- MySQL
ALTER TABLE users COMMENT = 'User accounts and profile information';
ALTER TABLE users MODIFY COLUMN email VARCHAR(255) COMMENT 'Primary email address';
```

**Generate documentation:**
```markdown
Generate schema docs:
1. Query information_schema
2. Extract tables, columns, indexes, constraints
3. Format as markdown
4. Include example queries
5. Update documentation on schema change
```

**Documentation template:**
```markdown
# Database Schema Documentation

## Tables

### users
**Description:** User accounts and profile information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Primary email address |
| name | VARCHAR(255) | NOT NULL | User's full name |
| status | VARCHAR(50) | DEFAULT 'active' | Account status |

**Indexes:**
- idx_users_email (UNIQUE on email)

**Foreign Keys:**
- None

**Example Queries:**
```sql
SELECT id, name, email FROM users WHERE status = 'active';
INSERT INTO users (id, email, name) VALUES ($1, $2, $3);
```
```

## Automated Schema Management

### CI/CD Integration

**GitHub Actions workflow:**
```yaml
name: Database Migration
on:
  push:
    branches: [main]

jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Database
        run: |
          docker-compose up -d postgres
          sleep 10  # Wait for database ready

      - name: Run Migrations
        run: |
          for file in migrations/*.sql; do
            echo "Applying $file"
            psql $DATABASE_URL -f "$file"
          done

      - name: Verify Schema
        run: |
          psql $DATABASE_URL -c "
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
          "
```

### Schema Testing

**Test schema changes:**
```sql
-- Test: Verify table exists
SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_name = 'users'
);

-- Test: Verify column exists
SELECT EXISTS (
    SELECT FROM information_schema.columns
    WHERE table_name = 'users'
    AND column_name = 'email'
);

-- Test: Verify index exists
SELECT EXISTS (
    SELECT FROM pg_indexes
    WHERE tablename = 'users'
    AND indexname = 'idx_users_email'
);
```

## Performance Considerations

### Schema Query Performance

**Cache schema metadata:**
```markdown
Cache schema for:
- Table list (refresh hourly)
- Column list per table (refresh daily)
- Indexes per table (refresh daily)
- Foreign key relationships (refresh daily)

Benefits:
- Faster query building
- Reduced database load
- Reduced latency

Invalidate cache when:
- Migration applied
- Schema change detected
- Explicit cache clear
```

**Batch schema queries:**
```sql
-- Single query to get all table structures
SELECT
    c.table_name,
    c.column_name,
    c.data_type,
    c.is_nullable,
    c.column_default,
    tc.constraint_type
FROM information_schema.columns c
LEFT JOIN information_schema.key_column_usage kcu
    ON c.table_name = kcu.table_name
    AND c.column_name = kcu.column_name
LEFT JOIN information_schema.table_constraints tc
    ON kcu.constraint_name = tc.constraint_name
WHERE c.table_schema = 'public'
ORDER BY c.table_name, c.ordinal_position;
```

## Common Issues and Solutions

### Migration Failures

**Problem:** Migration fails midway
```sql
-- Solution: Check transaction state
SELECT * FROM pg_stat_activity WHERE state = 'active';

-- Rollback if needed
ROLLBACK;
```

**Problem:** Constraint violation
```sql
-- Solution: Check existing data
SELECT * FROM users WHERE email IS NULL;

-- Fix data before applying constraint
UPDATE users SET email = 'unknown@example.com' WHERE email IS NULL;
```

### Schema Drift

**Problem:** Schema doesn't match documentation
```sql
-- Solution: Generate current schema
\dt  -- PostgreSQL
SHOW TABLES;  -- MySQL
.tables  -- SQLite

-- Compare with documented schema
-- Update documentation or fix schema
```

**Problem:** Unversioned changes
```sql
-- Solution: Create migration for existing changes
-- Document current state as migration 001
-- Add to migration history
INSERT INTO schema_migrations (version, description)
VALUES ('001', 'Existing schema state');
```

## Quick Reference

### Common Migration Patterns

**Add column:**
```sql
ALTER TABLE table_name ADD COLUMN column_name type [constraints];
```

**Drop column:**
```sql
ALTER TABLE table_name DROP COLUMN column_name;
```

**Rename column:**
```sql
ALTER TABLE table_name RENAME COLUMN old_name TO new_name;
```

**Rename table:**
```sql
ALTER TABLE old_name RENAME TO new_name;
```

**Add foreign key:**
```sql
ALTER TABLE child_table
ADD CONSTRAINT fk_name
FOREIGN KEY (column_name)
REFERENCES parent_table (column_name);
```

**Create index:**
```sql
CREATE INDEX idx_name ON table_name (column_name);
```

### Schema Validation Queries

**PostgreSQL:**
```sql
-- List tables
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Get table structure
\d+ table_name

-- Check constraints
SELECT conname, contype, confrelid::regclass
FROM pg_constraint
WHERE conrelid = 'table_name'::regclass;
```

**MySQL:**
```sql
-- List tables
SHOW TABLES;

-- Get table structure
DESCRIBE table_name;

-- Check foreign keys
SELECT constraint_name, table_name, column_name,
       referenced_table_name, referenced_column_name
FROM information_schema.key_column_usage
WHERE referenced_table_name IS NOT NULL;
```

**SQLite:**
```sql
-- List tables
.tables

-- Get table structure
.schema table_name

-- Check foreign keys
PRAGMA foreign_key_list(table_name);
```

## Conclusion

Schema management requires:
- **Schema introspection** for dynamic operations
- **Migration tracking** with versioning
- **Safe migration strategies** with rollbacks
- **Schema validation** for consistency
- **Documentation** for maintainability
- **Automated testing** for reliability
- **Performance optimization** for efficiency
- **Common issue resolution** for reliability

Follow these practices to maintain database integrity and enable flexible schema operations in MCP-based plugins.