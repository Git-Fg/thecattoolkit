# Discovery Protocol

## Overview

The Discovery Protocol is a systematic approach to investigating existing codebases and understanding project context before creating plans.

## Phase 1: Project Scanning

### 1.1 Structure Analysis

**Goal:** Understand the physical organization of the codebase

**Commands:**
```bash
# Count total files
find . -type f -not -path '*/.*' | wc -l

# Count lines of code (LOC)
find . -type f -name "*.py" -o -name "*.js" -o -name "*.ts" | xargs wc -l

# Find largest files
find . -type f -exec ls -lh {} + | sort -k5 -hr | head -20

# Directory structure (depth 3)
find . -type d -maxdepth 3 | head -30
```

**Key Metrics:**
- Total files count
- Code-to-config ratio
- Test coverage (if tests exist)
- Documentation presence

### 1.2 Dependency Analysis

**Goal:** Identify technology stack and external dependencies

**File Patterns:**
- Node.js: `package.json`, `yarn.lock`, `pnpm-lock.yaml`
- Python: `requirements.txt`, `pyproject.toml`, `poetry.lock`
- Go: `go.mod`, `go.sum`
- Rust: `Cargo.toml`, `Cargo.lock`
- Java: `pom.xml`, `build.gradle`
- PHP: `composer.json`, `composer.lock`

**Analysis Steps:**
1. **Read dependency files**
   - Runtime dependencies (not devDependencies)
   - Version constraints
   - Major/minor version patterns

2. **Identify Frameworks**
   ```bash
   # React/Vue/Angular
   grep -r "react\|vue\|angular" package.json

   # Python frameworks
   grep -r "django\|flask\|fastapi\|pytest" requirements.txt

   # ORMs/databases
   grep -r "sequelize\|prisma\|typeorm\|sqlalchemy" package.json
   ```

3. **Build Tools**
   ```bash
   # Bundlers
   ls -la | grep -E "vite|webpack|rollup|parcel"

   # Linters/formatters
   grep -E "eslint|prettier|black|ruff" package.json
   ```

### 1.3 Documentation Review

**Goal:** Understand project from existing docs

**Files to Check:**
- `README.md` - Main entry point
- `CONTRIBUTING.md` - Development process
- `ARCHITECTURE.md` or `docs/` - Technical docs
- `CHANGELOG.md` or `HISTORY.md` - Change tracking
- `LICENSE` - Legal constraints

**Review Checklist:**
- [ ] Purpose and scope clearly defined?
- [ ] Setup instructions present?
- [ ] Architecture described?
- [ ] API documentation available?
- [ ] Contributing guidelines clear?

### 1.4 Code Pattern Analysis

**Goal:** Understand coding conventions and patterns

**Search Patterns:**

```bash
# Naming conventions
grep -r "^class " --include="*.py" --include="*.js" --include="*.java" .
grep -r "^def \|^function " --include="*.py" --include="*.js" .

# Design patterns
grep -r "singleton\|factory\|observer" --include="*.py" --include="*.js" .

# Architecture style
grep -r "MVC\|MVVM\|flux\|redux" --include="*.py" --include="*.js" .

# Testing patterns
find . -name "*test*" -o -name "*spec*" | wc -l
grep -r "test\|it\|describe" --include="*.test.js" --include="*.spec.js" .
```

**Pattern Categories:**
1. **Structure:** How code is organized
2. **Naming:** Conventions for variables, functions, classes
3. **Patterns:** Design patterns in use
4. **Architecture:** Overall architectural style
5. **Testing:** Test strategy and coverage

## Phase 2: Context Analysis

### 2.1 Environment Detection

**Goal:** Understand deployment and runtime environment

**OS Compatibility:**
```bash
# Check shebang lines
grep -r "^#!/" --include="*.py" --include="*.js" . | head -10

# Check for OS-specific code
grep -r "win32\|darwin\|linux" --include="*.py" --include="*.js" .

# Docker presence
ls -la | grep -i docker
find . -name "Dockerfile*" -o -name "docker-compose.yml"
```

**Runtime Requirements:**
```bash
# Node.js version
node --version 2>/dev/null || echo "Node.js not found"

# Python version
python --version 2>/dev/null || python3 --version 2>/dev/null || echo "Python not found"

# Other runtimes
go version 2>/dev/null || echo "Go not found"
java -version 2>/dev/null || echo "Java not found"
```

### 2.2 Database & Services

**Goal:** Identify data layer and external services

**Database Detection:**
```bash
# Search for database connections
grep -r "mongodb\|mysql\|postgres\|sqlite\|redis" --include="*.py" --include="*.js" .

# ORM patterns
grep -r "sequelize\|prisma\|sqlalchemy\|mongoose" package.json

# Configuration files
find . -name "*.env*" -o -name "config.*" | head -10
```

**External Services:**
```bash
# API keys/tokens (check .env files)
find . -name ".env*" -exec cat {} \; 2>/dev/null | grep -E "API_KEY\|TOKEN\|SECRET"

# Service integrations
grep -r "stripe\|aws\|gcp\|azure\|sendgrid" --include="*.py" --include="*.js" .
```

### 2.3 Security Analysis

**Goal:** Identify security considerations

**Security Patterns:**
```bash
# Authentication
grep -r "jwt\|oauth\|bcrypt\|passlib" --include="*.py" --include="*.js" .

# HTTPS/TLS
grep -r "https\|ssl\|tls" --include="*.py" --include="*.js" .

# Input validation
grep -r "validator\|sanitize\|escape" --include="*.py" --include="*.js" .

# Security headers
grep -r "cors\|csrf\|xss" --include="*.py" --include="*.js" .
```

**Configuration Files:**
```bash
# Check for security configs
ls -la | grep -E "\.env\|security\|auth"

# Permissions
find . -type f -name "*.pem" -o -name "*.key" -o -name "*.crt"
```

## Phase 3: Requirement Synthesis

### 3.1 User Requirement Mapping

**Input Analysis:**
1. Parse user requirements
2. Extract functional needs
3. Identify non-functional requirements
4. Note constraints and preferences

**Mapping Process:**
```
User Requirement → Codebase Reality → Gap/Opportunity

Example:
User: "Add user authentication"
Reality: "Has user table but no auth logic"
Gap: "Need to implement auth middleware + login flow"
Opportunity: "Can leverage existing user model"
```

### 3.2 Constraint Identification

**Categories:**
1. **Technical Constraints**
   - Framework versions
   - Database limitations
   - Performance requirements
   - Compatibility needs

2. **Business Constraints**
   - Timeline
   - Budget
   - Stakeholder requirements
   - Compliance needs

3. **Environmental Constraints**
   - Deployment platform
   - Scale requirements
   - Integration points
   - Security policies

### 3.3 Success Criteria Definition

**Criteria Framework:**
- **Specific:** Clear and unambiguous
- **Measurable:** Quantifiable where possible
- **Achievable:** Realistic given constraints
- **Relevant:** Aligned with user goals
- **Time-bound:** Has a deadline or phase

**Examples:**
```markdown
# Good Success Criteria
✅ User can register with email/password
✅ User can login and receive JWT token
✅ JWT expires after 24 hours
✅ Passwords are hashed with bcrypt

# Bad Success Criteria
✅ Make authentication better
✅ Add user login
✅ Improve security
```

## Discovery Output

### DISCOVERY.md Template

```markdown
# Discovery Report: {project-name}

**Date:** {YYYY-MM-DD}
**Scope:** {What was analyzed}

## Project Overview
**Purpose:** {What the project does}
**Scale:** {X files, Y lines of code}
**Maturity:** {New/Active/Mature/Legacy}

## Technology Stack

### Runtime
- **Language:** {Python/Node.js/Go/etc.}
- **Version:** {version}
- **Package Manager:** {pip/npm/cargo/etc.}

### Frameworks
- **Primary:** {React/Django/FastAPI/etc.}
- **Secondary:** {Express/Flask/etc.}

### Databases
- **Primary:** {PostgreSQL/MongoDB/etc.}
- **Cache:** {Redis/Memcached}
- **ORM:** {Sequelize/SQLAlchemy/etc.}

### Tools
- **Build:** {Vite/Webpack/etc.}
- **Test:** {Jest/Pytest/etc.}
- **Lint:** {ESLint/Black/etc.}

## Architecture
**Style:** {MVC/Microservices/Monolith/etc.}
**Structure:** {How code is organized}
**Patterns:** {Design patterns in use}

## Code Quality
**Testing:** {Coverage %, test framework}
**Documentation:** {README quality, API docs}
**Conventions:** {Naming, formatting, style}

## Dependencies
**Count:** {X dependencies}
**Outdated:** {Y outdated dependencies}
**Vulnerabilities:** {Z known vulnerabilities}

## Environment
**OS:** {Linux/macOS/Windows}
**Docker:** {Yes/No}
**Cloud:** {AWS/GCP/Azure/None}

## Security
**Auth:** {JWT/OAuth/Passport/etc.}
**HTTPS:** {Enforced/Optional}
**Validation:** {Library used}

## Key Findings
1. {Finding 1}
2. {Finding 2}
3. {Finding 3}

## Constraints
1. {Technical constraint}
2. {Business constraint}
3. {Environmental constraint}

## Opportunities
1. {Improvement opportunity}
2. {Feature opportunity}
3. {Refactor opportunity}

## Recommendations
1. {Actionable recommendation}
2. {Actionable recommendation}
3. {Actionable recommendation}
```

## Quick Reference

### Discovery Checklist
- [ ] Project structure analyzed
- [ ] Dependencies cataloged
- [ ] Documentation reviewed
- [ ] Code patterns identified
- [ ] Environment detected
- [ ] Security assessed
- [ ] Constraints documented
- [ ] Opportunities noted
- [ ] DISCOVERY.md created

### Red Flags
- ⚠️ No tests
- ⚠️ Outdated dependencies
- ⚠️ No documentation
- ⚠️ Inconsistent patterns
- ⚠️ Security vulnerabilities
- ⚠️ Hardcoded secrets
- ⚠️ No CI/CD
