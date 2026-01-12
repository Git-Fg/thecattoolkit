# Database Security for MCP Integration

Complete guide to securing database connections and operations in MCP-based plugins.

## Overview

Database security is critical when integrating databases via MCP. This guide covers authentication, encryption, access control, and security best practices for database MCP servers.

## Authentication Methods

### Environment Variables (Recommended)

**PostgreSQL:**
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

**MySQL:**
```json
{
  "mysql": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-mysql", "${MYSQL_URL}"],
    "env": {
      "MYSQL_URL": "${MYSQL_CONNECTION_STRING}",
      "MYSQL_SSL_ENABLED": "true"
    }
  }
}
```

**SQLite:**
```json
{
  "sqlite": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sqlite", "${SQLITE_DB_PATH}"],
    "env": {
      "SQLITE_DB_PATH": "${SQLITE_PATH}"
    }
  }
}
```

### Connection URL Components

**PostgreSQL format:**
```
postgresql://username:password@host:port/database_name?sslmode=require&connect_timeout=10
```

**MySQL format:**
```
mysql://username:password@host:port/database_name?ssl-mode=REQUIRE&connect-timeout=10
```

**Individual environment variables:**
```bash
export PGHOST=db.example.com
export PGPORT=5432
export PGDATABASE=myapp
export PGUSER=myuser
export PGPASSWORD=secure_password
export PGSSLMODE=require
```

### Using .env Files

Create `.env` file (add to `.gitignore`):
```bash
# Database Configuration
DB_HOST=db.example.com
DB_PORT=5432
DB_NAME=myapp
DB_USER=app_user
DB_PASSWORD=super_secure_password_123!
DB_SSL=true

# Optional: Connection Pool Settings
DB_POOL_MIN=5
DB_POOL_MAX=20

# Optional: Timeouts (in seconds)
DB_CONNECT_TIMEOUT=10
DB_QUERY_TIMEOUT=30
```

Load environment variables:
```bash
# Option 1: Using source
source .env

# Option 2: Using export
export $(cat .env | xargs)

# Option 3: Using direnv (recommended)
# Install: https://direnv.net/
# .env will auto-load when entering directory
```

## SSL/TLS Configuration

### PostgreSQL SSL

**Environment variables:**
```bash
export POSTGRES_URL="postgresql://user:pass@db.example.com:5432/dbname?sslmode=require"
```

**With certificate files:**
```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"],
    "env": {
      "DATABASE_URL": "${POSTGRES_URL}",
      "PGSSLMODE": "verify-full",
      "PGSSLROOTCERT": "/path/to/ca-cert.pem",
      "PGSSLCERT": "/path/to/client-cert.pem",
      "PGSSLKEY": "/path/to/client-key.pem"
    }
  }
}
```

**SSL modes (from least to most secure):**
- `disable` - No SSL (⚠️ Never use in production)
- `allow` - Try without SSL, then with SSL
- `prefer` - Try with SSL, then without
- `require` - Require SSL (minimum for production)
- `verify-ca` - Verify CA certificate
- `verify-full` - Verify CA and hostname (recommended)

### MySQL SSL

**Basic SSL:**
```bash
export MYSQL_URL="mysql://user:pass@db.example.com:3306/dbname?ssl-mode=REQUIRE"
```

**With certificate verification:**
```json
{
  "mysql": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-mysql", "${MYSQL_URL}"],
    "env": {
      "MYSQL_URL": "${MYSQL_CONNECTION_STRING}",
      "MYSQL_SSL_MODE": "VERIFY_IDENTITY",
      "MYSQL_SSL_CA": "/path/to/ca-cert.pem",
      "MYSQL_SSL_CERT": "/path/to/client-cert.pem",
      "MYSQL_SSL_KEY": "/path/to/client-key.pem"
    }
  }
}
```

## Access Control

### Database User Privileges

**Read-only user (for query operations):**
```sql
-- PostgreSQL
CREATE USER app_readonly WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE myapp TO app_readonly;
GRANT USAGE ON SCHEMA public TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO app_readonly;

-- MySQL
CREATE USER 'app_readonly'@'%' IDENTIFIED BY 'secure_password';
GRANT SELECT ON myapp.* TO 'app_readonly'@'%';
FLUSH PRIVILEGES;
```

**Read-write user (for insert/update operations):**
```sql
-- PostgreSQL
CREATE USER app_readwrite WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE myapp TO app_readwrite;
GRANT USAGE ON SCHEMA public TO app_readwrite;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_readwrite;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_readwrite;

-- MySQL
CREATE USER 'app_readwrite'@'%' IDENTIFIED BY 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON myapp.* TO 'app_readwrite'@'%';
FLUSH PRIVILEGES;
```

**Schema-specific permissions:**
```sql
-- PostgreSQL - Only access specific schema
CREATE USER app_specific WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE myapp TO app_specific;
GRANT USAGE ON SCHEMA app_data TO app_specific;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app_data TO app_specific;
```

### Row-Level Security (PostgreSQL)

Enable RLS for data isolation:
```sql
-- Enable RLS on table
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own data
CREATE POLICY user_own_data ON users
  FOR ALL
  TO app_user
  USING (user_id = current_setting('app.current_user_id')::uuid);

-- Set user context in environment
-- app_user role will automatically filter rows
```

Configure MCP server with user context:
```json
{
  "postgres_rls": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"],
    "env": {
      "DATABASE_URL": "${POSTGRES_URL}",
      "PGUSER": "${DB_USER}",
      "PGCURRENT_USER_ID": "${CURRENT_USER_ID}"
    }
  }
}
```

## Connection Security

### Connection String Best Practices

**✅ DO:**
```bash
# Use strong passwords
DB_PASSWORD="C0mpl3x!P@ssw0rd#2024"

# Specify SSL
POSTGRES_URL="postgresql://user:pass@db:5432/db?sslmode=require"

# Set timeouts
POSTGRES_URL="postgresql://user:pass@db:5432/db?sslmode=require&connect_timeout=10&connection_limit=10"

# Use port explicitly
MYSQL_URL="mysql://user:pass@db.example.com:3306/db"
```

**❌ DON'T:**
```bash
# Weak passwords
DB_PASSWORD="password123"

# No SSL
POSTGRES_URL="postgresql://user:pass@db:5432/db"

# Default ports exposed
POSTGRES_URL="postgresql://user:pass@db.example.com:5432/db"

# Trust all certificates (insecure)
POSTGRES_URL="postgresql://user:pass@db:5432/db?sslmode=disable"
```

### Network Security

**VPN or Private Network:**
```bash
# Use private IP/VPN
DB_HOST="10.0.1.100"  # Private network
DB_HOST="db.internal.company.com"  # VPN hostname
```

**Security Groups (Cloud):**
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

Configure security groups to allow only:
- Plugin server IP addresses
- Specific port (5432 for PostgreSQL, 3306 for MySQL)
- SSL/TLS only

**IP Whitelisting:**
```sql
-- PostgreSQL
ALTER USER app_user CONNECTION LIMIT 10;
ALTER USER app_user VALID UNTIL '2024-12-31';

-- MySQL
CREATE USER 'app_user'@'192.168.1.0/24' IDENTIFIED BY 'password';
-- Only allow connections from specific subnet
```

## SQL Injection Prevention

### Parameterized Queries

**✅ SECURE:**
```markdown
Steps:
1. Use parameterized queries
2. Validate table/column names
3. Sanitize user input
4. Use whitelists

Example:
SELECT * FROM users WHERE id = $1 AND status = $2
```

**❌ INSECURE:**
```markdown
Steps:
1. Concatenate user input into SQL
2. Directly interpolate variables
3. Execute unvalidated SQL

Example:
"SELECT * FROM users WHERE id = " + user_input + " AND status = '" + status + "'"
```

### Input Validation

**Table/Column name validation:**
```markdown
Steps:
1. Get schema via MCP tool
2. Build whitelist of valid identifiers
3. Check user input against whitelist
4. Reject invalid names

Example whitelist:
valid_tables = ['users', 'products', 'orders']
valid_columns = {
  'users': ['id', 'name', 'email', 'created_at'],
  'products': ['id', 'title', 'price', 'category']
}
```

**Value sanitization:**
```markdown
Steps:
1. Escape special characters
2. Validate data types
3. Check length limits
4. Use parameterized queries

Example:
if not isinstance(user_id, int):
    raise ValueError("user_id must be an integer")
if len(email) > 255:
    raise ValueError("email too long")
```

### Schema-Based Validation

```markdown
Steps:
1. Use mcp__plugin_myplugin_postgres__describe to get schema
2. Build validation rules from schema
3. Validate inputs before query
4. Reject invalid data

Example validation rules:
{
  'users': {
    'id': {'type': 'uuid', 'required': True},
    'name': {'type': 'string', 'max_length': 100, 'required': True},
    'email': {'type': 'string', 'pattern': '^[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,}$', 'required': True},
    'age': {'type': 'integer', 'min': 0, 'max': 150, 'required': False}
  }
}
```

## Credential Management

### Environment Variables

**Set securely:**
```bash
# Method 1: Direct export (current session)
export DATABASE_URL="postgresql://user:pass@db:5432/db"

# Method 2: Using .env (add to .gitignore)
echo "DATABASE_URL=postgresql://user:pass@db:5432/db" >> .env

# Method 3: Password manager integration
# Use 1Password, Bitwarden, etc. to generate and store
```

**Retrieve securely in code:**
```python
# Python example
import os
from urllib.parse import urlparse

database_url = os.environ.get('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL not set")

# Parse URL components
parsed = urlparse(database_url)
db_config = {
    'host': parsed.hostname,
    'port': parsed.port,
    'database': parsed.path[1:],
    'username': parsed.username,
    'password': parsed.password
}
```

### Secret Management Services

**AWS Secrets Manager:**
```bash
# Retrieve secret
aws secretsmanager get-secret-value \
  --secret-id "myapp/database" \
  --query 'SecretString' \
  --output text

# Set environment variable
export DATABASE_URL=$(aws secretsmanager get-secret-value \
  --secret-id "myapp/database" \
  --query 'SecretString' \
  --output text | jq -r '.DATABASE_URL')
```

**Azure Key Vault:**
```bash
# Retrieve secret
export DATABASE_URL=$(az keyvault secret show \
  --vault-name "myapp-vault" \
  --name "database-url" \
  --query value \
  --output tsv)
```

**HashiCorp Vault:**
```bash
# Retrieve secret
export DATABASE_URL=$(vault kv get -field=database_url secret/myapp/database)
```

### Rotating Credentials

**Automated rotation script:**
```bash
#!/bin/bash
# rotate-credentials.sh

# 1. Generate new password
NEW_PASSWORD=$(openssl rand -base64 32)

# 2. Update in database
psql -h "$DB_HOST" -U postgres -c \
  "ALTER USER app_user WITH PASSWORD '$NEW_PASSWORD';"

# 3. Update secret manager
aws secretsmanager update-secret-value \
  --secret-id "myapp/database" \
  --secret-string "{\"DATABASE_URL\":\"postgresql://app_user:$NEW_PASSWORD@$DB_HOST:5432/myapp\"}"

# 4. Notify services to reload (optional)
# Could trigger a deployment or config reload

echo "Credentials rotated successfully"
```

**Schedule rotation:**
```bash
# Add to crontab
# Run monthly
0 2 1 * * /path/to/rotate-credentials.sh
```

## Audit Logging

### Database Audit

**PostgreSQL - Enable logging:**
```sql
-- Enable audit extension (requires superuser)
CREATE EXTENSION IF NOT EXISTS pgaudit;

-- Configure logging
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- Log queries > 1s
ALTER SYSTEM SET log_connections = on;
ALTER SYSTEM SET log_disconnections = on;
SELECT pg_reload_conf();
```

**MySQL - Enable logging:**
```ini
# my.cnf
[mysqld]
log-error = /var/log/mysql/error.log
general_log = 1
general_log_file = /var/log/mysql/general.log
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 1
```

### Application Audit

**Log all database operations:**
```markdown
Steps:
1. Log connection attempts (success/failure)
2. Log query execution with timing
3. Log data modifications
4. Store logs securely
5. Monitor for suspicious activity

Example log format:
[2024-01-15 10:30:45] QUERY user=app_user db=myapp duration=125ms
SELECT * FROM users WHERE id = '550e8400-e29b-41d4-a716--446655440000'
```

## Security Monitoring

### Detect Suspicious Activity

**Monitor for:**
- Failed authentication attempts
- Unusual query patterns
- Large data exports
- Access from new locations
- Query timeouts
- Connection spikes

**Example monitoring script:**
```bash
#!/bin/bash
# monitor-db-security.sh

# Check for failed connections
if grep -q "password authentication failed" /var/log/postgresql/postgresql.log; then
    echo "⚠️ Failed authentication attempts detected"
    # Send alert
fi

# Check for slow queries
if grep -q "duration: [5-9][0-9][0-9][0-9]ms" /var/log/postgresql/postgresql.log; then
    echo "⚠️ Slow queries detected"
    # Send alert
fi

# Check for unusual activity
PATTERN=$(tail -100 /var/log/postgresql/postgresql.log | grep -o "SELECT.*FROM.*WHERE" | sort | uniq -c | sort -rn | head -5)
if [ -n "$PATTERN" ]; then
    echo "Top queries:"
    echo "$PATTERN"
fi
```

## Compliance Considerations

### GDPR Compliance

**Data protection:**
```sql
-- Right to be forgotten
DELETE FROM users WHERE id = $1;

-- Data export
SELECT id, name, email FROM users WHERE id = $1;

-- Audit trail
INSERT INTO audit_log (user_id, action, timestamp)
VALUES ($1, 'data_export', NOW());
```

### PCI DSS Compliance

**Credit card data:**
```sql
-- Never store full card numbers
CREATE TABLE payments (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  card_last_four CHAR(4),  -- Only last 4 digits
  card_type VARCHAR(50),
  amount DECIMAL(10,2),
  created_at TIMESTAMP
);
```

## Security Checklist

### Pre-Production

- [ ] All credentials use environment variables
- [ ] SSL/TLS enabled and verified
- [ ] Database users have minimal privileges
- [ ] SQL injection prevention implemented
- [ ] Input validation on all queries
- [ ] Audit logging enabled
- [ ] Secrets stored in secure manager
- [ ] Network access restricted (VPN/private)
- [ ] Passwords meet complexity requirements
- [ ] Connection timeouts configured
- [ ] Query timeouts configured
- [ ] Rate limiting implemented
- [ ] Monitoring in place

### Ongoing

- [ ] Credentials rotated regularly
- [ ] Security patches applied
- [ ] Log monitoring active
- [ ] Access reviewed quarterly
- [ ] Penetration testing performed
- [ ] Backup encryption verified
- [ ] Disaster recovery tested

## Incident Response

### Credential Compromise

**Immediate actions:**
1. Rotate compromised credentials
2. Revoke active sessions
3. Review access logs
4. Notify stakeholders
5. Implement additional monitoring

**Example response:**
```bash
#!/bin/bash
# emergency-credential-rotation.sh

NEW_PASSWORD=$(openssl rand -base64 32)

# 1. Update database
psql -h "$DB_HOST" -U admin -c "ALTER USER app_user WITH PASSWORD '$NEW_PASSWORD';"

# 2. Update secrets manager
aws secretsmanager update-secret-value \
  --secret-id "myapp/database" \
  --secret-string "{\"DATABASE_URL\":\"postgresql://app_user:$NEW_PASSWORD@$DB_HOST:5432/myapp\"}"

# 3. Force restart of services
systemctl restart myapp-service

# 4. Log incident
echo "[$(date)] Credential compromise detected and remediated" >> /var/log/security/incidents.log
```

### Suspicious Activity

**Detection:**
- Monitor for data exfiltration
- Check for unauthorized queries
- Verify access patterns
- Review failed attempts

**Response:**
1. Isolate affected systems
2. Preserve evidence
3. Investigate root cause
4. Implement fixes
5. Update monitoring

## Best Practices Summary

### For Developers

1. **Never hardcode credentials** - Always use environment variables
2. **Enable SSL/TLS** - Never use unencrypted connections
3. **Use least privilege** - Database users should have minimal permissions
4. **Validate all inputs** - Prevent SQL injection
5. **Log security events** - Monitor for suspicious activity
6. **Rotate credentials** - Regular rotation prevents long-term exposure
7. **Test security** - Include security tests in CI/CD
8. **Document security** - Keep security documentation current

### For Operations

1. **Use secret managers** - AWS Secrets Manager, Azure Key Vault, etc.
2. **Implement monitoring** - Real-time security monitoring
3. **Regular audits** - Quarterly access reviews
4. **Patch management** - Keep database servers updated
5. **Backup encryption** - Encrypt all database backups
6. **Network segmentation** - Use VPCs, security groups
7. **Incident response** - Document and test procedures
8. **Compliance** - Follow GDPR, PCI DSS, etc.

## Conclusion

Database security requires:
- **Strong authentication** with environment variables
- **SSL/TLS encryption** for all connections
- **Least privilege access** with minimal user permissions
- **Input validation** to prevent SQL injection
- **Audit logging** for monitoring and compliance
- **Secret management** for credential storage
- **Regular rotation** of credentials and keys
- **Continuous monitoring** for suspicious activity

Follow these practices to ensure secure database integration in MCP-based plugins.