# Database Performance for MCP Integration

Complete guide to optimizing database performance in MCP-based plugins.

## Overview

Database performance is critical for responsive applications. This guide covers connection pooling, query optimization, indexing strategies, and monitoring techniques for database MCP servers.

## Connection Pooling

### PostgreSQL Connection Pool

**Basic configuration:**
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"],
    "env": {
      "DATABASE_URL": "${POSTGRES_URL}",
      "PGPOOL_SIZE": "10",
      "PGPOOL_MAX": "20",
      "PGPOOL_MIN": "5"
    }
  }
}
```

**Pool size calculation:**
- Formula: `(CPU cores × 2) + disk_count`
- Example: 4 cores, 2 disks → `(4 × 2) + 2 = 10` connections
- Typical range: 5-25 connections

**Environment variables:**
```bash
# Minimum connections (always available)
PGPOOL_MIN=5

# Normal pool size (average load)
PGPOOL_SIZE=10

# Maximum connections (peak load)
PGPOOL_MAX=20

# Maximum idle time before closing connection (seconds)
PGPOOL_IDLE_TIMEOUT=300

# Maximum lifetime of a connection (seconds)
PGPOOL_MAX_LIFETIME=3600
```

### MySQL Connection Pool

**Configuration:**
```json
{
  "mysql": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-mysql", "${MYSQL_URL}"],
    "env": {
      "MYSQL_URL": "${MYSQL_CONNECTION_STRING}",
      "MYSQL_POOL_SIZE": "10",
      "MYSQL_POOL_MAX": "20",
      "MYSQL_POOL_MIN": "5"
    }
  }
}
```

**MySQL-specific settings:**
```bash
MYSQL_POOL_SIZE=10              # Default connections
MYSQL_POOL_MAX=20               # Maximum connections
MYSQL_POOL_MIN=5                # Minimum connections
MYSQL_POOL_TIMEOUT=60000        # Timeout in milliseconds
MYSQL_POOL_QUEUE_TIMEOUT=30000  # Queue wait timeout
MYSQL_POOL_ENABLE_KEEP_ALIVE=true  # Keep connections alive
```

### SQLite Connection

**SQLite has no connection pool (single process):**
```json
{
  "sqlite": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sqlite", "${SQLITE_DB_PATH}"],
    "env": {
      "SQLITE_DB_PATH": "${SQLITE_PATH}",
      "SQLITE_TIMEOUT": "5000",      # Lock timeout in milliseconds
      "SQLITE_BUSY_TIMEOUT": "5000"   # Busy handler timeout
    }
  }
}
```

**SQLite optimization:**
```bash
# Enable WAL mode for better concurrency
SQLITE_WAL_AUTOCHECKPOINT=1000   # Checkpoint interval

# Set busy timeout (wait for lock before failing)
SQLITE_TIMEOUT=5000

# Cache size (negative = KB, positive = pages)
SQLITE_CACHE_SIZE=-64000         # 64 MB cache
```

## Query Optimization

### Indexing Strategies

**Identify slow queries:**
```sql
-- PostgreSQL - Find slow queries
SELECT query, mean_exec_time, calls, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- MySQL - Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  # Log queries > 1 second
```

**Create indexes:**
```sql
-- PostgreSQL - Basic index
CREATE INDEX idx_users_email ON users(email);

-- MySQL - Full-text index
CREATE FULLTEXT INDEX idx_products_search ON products(title, description);

-- Composite index
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Partial index (PostgreSQL only)
CREATE INDEX idx_active_users ON users(email)
WHERE status = 'active';
```

**Index best practices:**
- Index frequently queried columns
- Use composite indexes for multi-column queries
- Index foreign keys for joins
- Consider partial indexes for filtered data
- Monitor index usage and remove unused indexes

### Query Patterns

### GOOD: Efficient queries:
```sql
-- Use specific columns
SELECT id, name, email FROM users WHERE id = $1;

-- Use indexes effectively
SELECT * FROM orders
WHERE user_id = $1
  AND created_at >= $2
ORDER BY created_at DESC
LIMIT 20;

-- Proper join with indexes
SELECT u.id, u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id, u.name
ORDER BY order_count DESC;
```

### BAD: Inefficient queries:
```sql
-- SELECT * (avoid in production)
SELECT * FROM users WHERE id = $1;

-- Missing WHERE clause
SELECT * FROM orders;

-- Functions on indexed columns (breaks index usage)
SELECT * FROM users WHERE LOWER(email) = LOWER($1);

-- OR in WHERE clause (can be slow)
SELECT * FROM products WHERE category = 'A' OR category = 'B';

-- LIKE with leading wildcard
SELECT * FROM products WHERE name LIKE '%searchterm%';
```

### Pagination

**Limit/Offset (simple but can be slow on large tables):**
```sql
SELECT id, name, email
FROM users
ORDER BY id
LIMIT 20 OFFSET 1000;  -- Slow on large offsets
```

**Keyset pagination (better for large datasets):**
```sql
-- First page
SELECT id, name, email
FROM users
ORDER BY id
LIMIT 20;

-- Next page (using last ID from previous page)
SELECT id, name, email
FROM users
WHERE id > $1
ORDER BY id
LIMIT 20;
```

**Cursor-based pagination:**
```sql
-- Use cursor for efficient scrolling
DECLARE cursor_name CURSOR FOR SELECT * FROM large_table;
FETCH 20 FROM cursor_name;
```

## Caching Strategies

### Query Result Caching

**Cache frequently accessed data:**
```markdown
Steps:
1. Check cache first
2. If cache hit, return cached data
3. If cache miss, query database
4. Store result in cache with TTL
5. Return data to user

Example caching rules:
- User profiles: Cache for 1 hour
- Product lists: Cache for 30 minutes
- Static configuration: Cache for 24 hours
- Real-time data: No cache
```

**Cache invalidation:**
```markdown
Steps:
1. Update database
2. Delete/expire cache entry
3. Refresh cache with new data
4. Verify cache consistency

Example:
When user updates profile:
1. UPDATE users SET name = $1 WHERE id = $2;
2. DELETE FROM cache WHERE key = 'user_profile_' || $2;
3. SELECT * FROM users WHERE id = $2;
4. SETEX cache key new_data 3600;
```

### Application-Level Caching

**Redis for caching:**
```bash
# Install Redis MCP server
npm install -g @modelcontextprotocol/server-redis
```

```json
{
  "redis": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-redis", "${REDIS_URL}"],
    "env": {
      "REDIS_URL": "${REDIS_CONNECTION_STRING}"
    }
  }
}
```

**Cache patterns:**
```markdown
Cache patterns for database queries:

1. Read-through:
   - Application checks cache first
   - On miss, query database and store in cache
   - Best for: Frequently read, rarely updated data

2. Write-through:
   - Update database and cache simultaneously
   - Best for: Data that must be consistent

3. Write-behind:
   - Update cache immediately
   - Async write to database
   - Best for: High-write scenarios, eventual consistency OK

4. Cache-aside:
   - Application manages cache explicitly
   - On read: Check cache → DB if miss
   - On write: Update DB → Delete cache
   - Best for: Simple caching needs
```

### Database Query Cache

**PostgreSQL:**
```sql
-- Enable query plan caching
SET shared_preload_libraries = 'pg_stat_statements';

-- Configure cache size
ALTER SYSTEM SET pg_stat_statements.max = 10000;
SELECT pg_reload_conf();
```

**MySQL:**
```sql
-- Enable query cache
SET GLOBAL query_cache_type = ON;
SET GLOBAL query_cache_size = 1048576;  -- 1 MB
SET GLOBAL query_cache_limit = 1048576;  -- 1 MB max query size
```

## Performance Monitoring

### Database Metrics

**PostgreSQL - Key metrics:**
```sql
-- Connections
SELECT count(*) FROM pg_stat_activity;

-- Database size
SELECT pg_size_pretty(pg_database_size('myapp'));

-- Table sizes
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index usage
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 100  -- Average > 100ms
ORDER BY mean_exec_time DESC
LIMIT 10;
```

**MySQL - Key metrics:**
```sql
-- Connection count
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';

-- Database size
SELECT
  table_schema AS 'Database',
  ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'DB Size in MB'
FROM information_schema.tables
GROUP BY table_schema;

-- Table sizes
SELECT
  table_name,
  ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.tables
WHERE table_schema = 'myapp'
ORDER BY (data_length + index_length) DESC;

-- Slow query log
SHOW VARIABLES LIKE 'slow_query_log';
SHOW VARIABLES LIKE 'long_query_time';
```

### Application-Level Monitoring

**Track query performance:**
```markdown
Steps:
1. Log query execution time
2. Track query frequency
3. Identify slow queries
4. Monitor query errors
5. Set performance thresholds

Example metrics:
- Query count per operation
- Average execution time
- 95th percentile latency
- Error rate
- Cache hit rate
```

**Example monitoring script:**
```bash
#!/bin/bash
# monitor-db-performance.sh

# Check connection pool usage
echo "=== Connection Pool Status ==="
psql -c "SELECT count(*) as active_connections FROM pg_stat_activity;"

# Check slow queries
echo -e "\n=== Slow Queries (last 1 hour) ==="
psql -c "SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE last_exec > NOW() - INTERVAL '1 hour'
ORDER BY mean_exec_time DESC
LIMIT 5;"

# Check table sizes
echo -e "\n=== Largest Tables ==="
psql -c "SELECT schemaname, tablename,
pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 5;"
```

## Database-Specific Optimizations

### PostgreSQL Optimizations

**Configuration tuning:**
```bash
# shared_buffers (25% of RAM for dedicated server)
shared_buffers = 2GB

# effective_cache_size (estimate of OS cache)
effective_cache_size = 6GB

# work_mem (per operation, adjust based on queries)
work_mem = 16MB

# maintenance_work_mem (for VACUUM, CREATE INDEX)
maintenance_work_mem = 512MB

# random_page_cost (1.1 for SSD, 1.3-1.4 for RAID)
random_page_cost = 1.1

# Enable parallelism
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
```

**WAL configuration:**
```bash
# WAL settings for write performance
wal_buffers = 16MB
checkpoint_completion_target = 0.9
max_wal_size = 4GB
min_wal_size = 1GB
```

**Query planner settings:**
```sql
-- Enable query statistics
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Set effective cache size
SET effective_cache_size = '6GB';

-- Enable parallel queries (if supported)
SET max_parallel_workers_per_gather = 4;
```

### MySQL Optimizations

**Configuration tuning:**
```ini
# my.cnf
[mysqld]
# Buffer pool (50-80% of RAM)
innodb_buffer_pool_size = 4G

# Log file size
innodb_log_file_size = 512M
innodb_log_buffer_size = 16M

# Connection limits
max_connections = 200
max_connect_errors = 1000000

# Query cache (MySQL 5.7 and earlier)
query_cache_type = 1
query_cache_size = 128M
query_cache_limit = 2M

# InnoDB settings
innodb_flush_log_at_trx_commit = 2  # Less strict for better performance
innodb_file_per_table = 1
innodb_open_files = 500
```

**MyISAM to InnoDB migration:**
```sql
-- Convert table to InnoDB
ALTER TABLE mytable ENGINE=InnoDB;

-- Check table engine
SHOW TABLE STATUS WHERE Name = 'mytable';
```

### SQLite Optimizations

**PRAGMA settings:**
```sql
-- Enable WAL mode for better concurrency
PRAGMA journal_mode = WAL;

-- Increase cache size (negative = KB)
PRAGMA cache_size = -64000;

-- Set synchronous mode (NORMAL is good balance)
PRAGMA synchronous = NORMAL;

-- Increase temp store memory
PRAGMA temp_store = MEMORY;

-- Optimize for bulk inserts
PRAGMA journal_mode = DELETE;
PRAGMA synchronous = OFF;

-- Return to normal mode after bulk operations
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
```

**Scripting WAL mode:**
```bash
#!/bin/bash
# Enable WAL mode for SQLite
sqlite3 myapp.db <<'EOF'
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = -64000;
PRAGMA temp_store = MEMORY;
EOF
```

## Bulk Operations

### Batch Inserts

**PostgreSQL - COPY for bulk data:**
```sql
-- Create temporary table
CREATE TEMP TABLE temp_users (
  id UUID,
  name TEXT,
  email TEXT
);

-- Use COPY for bulk insert (from file or STDIN)
COPY temp_users FROM STDIN WITH (FORMAT csv);
```

**MySQL - LOAD DATA:**
```sql
-- Bulk load from file
LOAD DATA INFILE '/path/to/file.csv'
INTO TABLE users
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

**Batch INSERT statement:**
```sql
-- Insert multiple rows at once
INSERT INTO users (id, name, email) VALUES
  ('uuid1', 'User 1', 'user1@example.com'),
  ('uuid2', 'User 2', 'user2@example.com'),
  ('uuid3', 'User 3', 'user3@example.com');
```

### Transaction Optimization

**Batch in single transaction:**
```markdown
Steps:
1. BEGIN transaction
2. Execute multiple INSERT/UPDATE statements
3. COMMIT if all successful
4. ROLLBACK on any error

Benefits:
- Reduces transaction overhead
- Ensures atomicity
- Better performance than individual commits

Example:
BEGIN;
INSERT INTO orders (...) VALUES (...);
INSERT INTO order_items (...) VALUES (...);
UPDATE inventory SET quantity = quantity - 1 WHERE ...;
COMMIT;
```

**Optimize transaction size:**
```markdown
Guidelines:
- Batch 100-1000 rows per transaction
- Don't hold transactions open too long
- Use SAVEPOINT for complex operations
- Monitor transaction log size
```

## Scaling Strategies

### Read Replicas

**PostgreSQL - Streaming replication:**
```bash
# Primary server
export POSTGRES_URL="postgresql://user:pass@primary:5432/myapp"

# Read replica
export READ_REPLICA_URL="postgresql://user:pass@replica:5432/myapp"
```

```json
{
  "postgres_primary": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "${PRIMARY_DB_URL}"],
    "env": {
      "DATABASE_URL": "${PRIMARY_POSTGRES_URL}"
    }
  },
  "postgres_replica": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "${REPLICA_DB_URL}"],
    "env": {
      "DATABASE_URL": "${READ_REPLICA_POSTGRES_URL}"
    }
  }
}
```

**Read/write splitting:**
```markdown
Steps:
1. Route SELECT queries to read replica
2. Route INSERT/UPDATE/DELETE to primary
3. Implement connection pooling per server
4. Monitor replication lag

Example:
if query.lower().startswith('select'):
    use_read_replica()
else:
    use_primary()
```

### Sharding

**Horizontal sharding strategy:**
```markdown
Shard by:
- User ID (hash-based)
- Geographic region
- Time (date ranges)
- Business entity

Example - Shard by user ID:
Shard 1: Users 0-999
Shard 2: Users 1000-1999
Shard 3: Users 2000-2999
```

**Sharding implementation:**
```python
def get_shard(user_id):
    """Determine which shard to use based on user_id"""
    shard_number = hash(user_id) % NUM_SHARDS
    return f"shard_{shard_number}"

def get_user_data(user_id):
    shard = get_shard(user_id)
    db = connect_to_shard(shard)
    return db.query("SELECT * FROM users WHERE id = $1", user_id)
```

### Connection Pool Optimization

**Pool sizing:**
```markdown
Formula:
- Calculate max connections per pool
- Leave headroom for admin connections
- Monitor pool utilization

Example:
Total DB connections: 100
Number of application instances: 5
Pool size per instance: 100 / 5 = 20
Headroom: 20 - 5 = 15 (keep 5 for monitoring/admin)
```

**Pool monitoring:**
```markdown
Monitor:
- Pool size utilization
- Wait time for connection
- Connection age
- Errors per second

Alert when:
- Pool utilization > 80%
- Wait time > 1 second
- Connection age > 1 hour
```

## Performance Checklist

### Before Deployment

- [ ] Connection pool configured
- [ ] Database indexes created
- [ ] Slow queries identified and optimized
- [ ] Query cache configured
- [ ] Monitoring in place
- [ ] Load testing completed
- [ ] Baseline metrics established
- [ ] Connection timeouts set
- [ ] Query timeouts configured

### After Deployment

- [ ] Monitor query performance
- [ ] Track connection pool usage
- [ ] Monitor cache hit rates
- [ ] Review slow query logs
- [ ] Check index usage
- [ ] Monitor database size growth
- [ ] Track error rates
- [ ] Review replication lag
- [ ] Benchmark against baseline

## Best Practices Summary

### For Developers

1. **Use connection pooling** - Reuse connections efficiently
2. **Write efficient queries** - Select only needed columns, use indexes
3. **Implement caching** - Cache frequently accessed data
4. **Monitor performance** - Track query times and error rates
5. **Use prepared statements** - Reduce parsing overhead
6. **Batch operations** - Combine multiple queries when possible
7. **Optimize pagination** - Use keyset instead of LIMIT/OFFSET
8. **Review execution plans** - Understand how queries execute

### For Operations

1. **Size connection pools appropriately** - Based on load and resources
2. **Monitor database metrics** - Connections, cache, slow queries
3. **Set up alerting** - For performance degradation
4. **Regular maintenance** - VACUUM, ANALYZE, optimize
5. **Plan for scaling** - Read replicas, sharding
6. **Test under load** - Performance testing before production
7. **Document performance baseline** - Know your normal
8. **Automate monitoring** - Continuous performance tracking

## Conclusion

Database performance requires:
- **Proper connection pooling** for efficient resource use
- **Query optimization** with indexes and efficient SQL
- **Caching strategies** to reduce database load
- **Performance monitoring** to identify issues early
- **Database-specific tuning** for PostgreSQL, MySQL, SQLite
- **Scaling strategies** like read replicas and sharding
- **Regular maintenance** to keep databases healthy
- **Automated monitoring** for continuous performance tracking

Follow these practices to ensure optimal database performance in MCP-based plugins.