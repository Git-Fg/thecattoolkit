# Workflow: Dependency Audit

## Purpose
Deep analysis of third-party libraries, versions, and security implications.

## Process

### Step 1: Extract Dependencies
Read the dependency definition files:
- **Node**: `package.json`
- **Python**: `requirements.txt` or `pyproject.toml`
- **Go**: `go.mod`
- **Rust**: `Cargo.toml`

### Step 2: Categorize
Group dependencies by purpose:
- **Core Framework**: (React, Django, Spring)
- **Data**: (Prisma, SQLAlchemy, Mongoose)
- **Utilities**: (Lodash, Pandas, Zod)
- **Dev/Build**: (TypeScript, ESLint, Pytest, Webpack)

### Step 3: Version Check
Identify if core dependencies are current or legacy.
- *Check*: Are major versions outdated? (e.g., React 16 vs 18, Python 2 vs 3)

### Step 4: Report
Generate a dependency matrix:

```markdown
# Dependency Audit

## Core Stack
- [Name]: [Version] ([Status: Current/Legacy])

## Infrastructure
- Database drivers: [List]
- Cloud SDKs: [List]

## Tooling
- Testing: [List]
- Linting: [List]

## Observations
- [Note on potential conflicts or outdated packages]
- [Note on heavy dependencies that might affect performance]
```

## Success Criteria
- [ ] Primary framework identified with version
- [ ] Dependencies categorized by function
- [ ] Legacy/Outdated risks flagged