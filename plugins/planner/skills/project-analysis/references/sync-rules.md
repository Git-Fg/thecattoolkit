# Workflow: Sync Rules

## Required Reading
- `references/quick-scan.md` - For understanding current project state

## Process

### Step 1: Locate AI Rule Files

Search for AI rule/configuration files in the project:

```bash
# Find common AI rule files
find . -maxdepth 3 -name "CLAUDE.md" -o -name ".cursorrules" -o -name "AI_RULES.md" -o -name "codegen.yml" 2>/dev/null | grep -v node_modules | grep -v ".git"

# List root directory to identify project-specific rule files
ls -la | grep -E "(\.md$|\.yml$|\.yaml$|\.json$)"
```

**Note locations of all rule files found.**

### Step 2: Analyze Current Project State

Perform a quick-scan of the project to understand the current tech stack and structure:

```bash
# Quick project overview
ls -F

# Identify entry points and configuration
find . -maxdepth 2 -not -path '*/.*' -not -path './node_modules*' -not -path './venv*' | head -20
```

**Read key files:**
- `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml` (tech stack)
- `README.md` (first 50 lines for project description)
- Configuration files (`docker-compose.yml`, `Dockerfile`, etc.)

### Step 3: Compare Rules Against Reality

For each rule file found, analyze discrepancies:

**Check these common outdated references:**

1. **Tech Stack References**
   - Does the rule file mention specific technologies?
   - Are those technologies actually present in the project?
   - Are there technologies in the project that the rules don't mention?

2. **File Structure**
   - Does the rules file reference paths that no longer exist?
   - Are there new directories/patterns not covered in the rules?

3. **Commands/Workflows**
   - Are build/run commands in the rules still accurate?
   - Do deployment/ci-cd references match actual configuration?

4. **Tool-Specific Instructions**
   - Do linting/formatting commands match package.json scripts?
   - Are testing frameworks mentioned correctly?

### Step 4: Generate Sync Report

Create a comprehensive report:

```markdown
# AI Rules Sync Report

## Rule Files Audited
- `CLAUDE.md` - [status: up-to-date/outdated]
- `.cursorrules` - [status: up-to-date/outdated]

## Current Project State
- **Language**: [e.g., TypeScript]
- **Framework**: [e.g., Next.js 14]
- **Key Dependencies**: [list main packages]

## Discrepancies Found

### 1. [Category]
**Issue**: [Description]
**Current Reality**: [What the project actually has]
**Recommendation**: Update rule file to [specific change]

### 2. [Category]
**Issue**: [Description]
**Current Reality**: [What the project actually has]
**Recommendation**: Update rule file to [specific change]

## Priority Changes Needed
1. **High**: [Critical updates that affect AI behavior]
2. **Medium**: [Important but not critical]
3. **Low**: [Nice-to-have improvements]

## Next Steps
- Review the proposed changes
- Update rule files with recommended modifications
- Test that updated rules produce expected behavior
```

## Success Criteria
- [ ] All AI rule files located and analyzed
- [ ] Current project state documented
- [ ] Discrepancies identified and categorized
- [ ] Specific recommendations provided for each issue
- [ ] Report includes both problems and solutions
