# Agent Skills — Progressive Disclosure Pattern

Agent Skills demonstrate the **progressive disclosure** pattern: load information in stages based on need.

## Core Concept

### What Skills Provide
- **Domain expertise**: Specialized knowledge and workflows
- **Reusable capabilities**: Create once, use automatically
- **Context efficiency**: Don't repeat instructions
- **Composability**: Combine skills for complex tasks

### Progressive Disclosure Architecture
```
Level 1: Metadata (~100 tokens)
  ↓
Level 2: Instructions (<5k tokens)
  ↓
Level 3: Resources (unlimited via bash)
```

## Three-Tier Pattern

### Level 1: Metadata (Always Loaded)
**Purpose**: Discovery and trigger matching
**Token cost**: ~100 tokens per skill
**Content**: YAML frontmatter

```yaml
---
name: code-reviewer
description: Automated code quality and security reviews. Use for reviewing code changes, checking security vulnerabilities, and suggesting improvements.
---
```

**What Claude uses**:
- Knows skill exists
- Decides when to trigger
- Matches description to user request

### Level 2: Instructions (Loaded on Trigger)
**Purpose**: Procedural knowledge and workflows
**Token cost**: <5k tokens
**Content**: SKILL.md body

```markdown
# Code Reviewer

## Quick Start
Use this skill to review code changes:

```
/code-reviewer --scan-changed-files
/code-reviewer --full-audit
/code-reviewer --security-scan
```

## When to Use
- Before committing code
- During code review process
- When checking for security issues

## How It Works
1. Scans changed files
2. Runs static analysis
3. Checks for common vulnerabilities
4. Suggests improvements

## Examples
Example 1: Review current changes
```
/code-reviewer --scan-changed-files
```

Example 2: Full security audit
```
/code-reviewer --security-scan --verbose
```
```

**What Claude uses**:
- Step-by-step guidance
- Best practices
- Example patterns
- When/why to use

### Level 3: Resources (As Needed)
**Purpose**: Reference materials, scripts, data
**Token cost**: Effectively unlimited
**Content**: Bundled files accessed via bash

```
code-reviewer/
├── SKILL.md (instructions)
├── reference.md (detailed docs)
├── scripts/
│   ├── scan-changes.sh
│   ├── security-check.sh
│   └── format-report.sh
├── templates/
│   └── review-report.md
└── examples/
    └── sample-findings.json
```

**What Claude uses**:
- Executes scripts: `bash scan-changes.sh`
- Reads specific files: `cat template.md`
- Runs checks: `./security-check.sh`
- **Code never enters context**, only outputs

**Why this matters**:
- Scripts can be complex (hundreds of lines) without consuming tokens
- Reference docs can be comprehensive without affecting context
- Examples can be extensive for lookup

## Skill Structure

### Required Files
```
skill-name/
└── SKILL.md  # Required: YAML frontmatter + instructions
```

### Optional Files
```
skill-name/
├── SKILL.md
├── reference.md       # Detailed docs
├── examples.md        # More examples
├── scripts/          # Executable helpers
│   ├── script1.sh
│   └── script2.py
├── templates/        # File templates
├── data/            # Reference data
└── assets/          # Images, etc.
```

### SKILL.md Format

#### Required Frontmatter
```yaml
---
name: skill-name
description: Brief description of what this skill does and when to use it
---
```

**Field requirements**:
- `name`: Max 64 chars, lowercase, numbers, hyphens only
- `description`: Max 1024 chars, clear when to use

#### Body Structure
```markdown
# Skill Name

## Quick Start
[Brief examples - 2-3 most common use cases]

## When to Use
[When to trigger this skill]

## How It Works
[High-level workflow]

## Examples
[Concrete examples with expected inputs/outputs]

## Advanced Usage
[For complex scenarios - optional]

## See Also
[References to other skills/resources]
```

## Common Patterns

### Pattern 1: Simple Command Skill
```yaml
---
name: deploy-app
description: Deploy application to specified environment
---

# Deploy

## Quick Start
/deploy --env production
/deploy --env staging --dry-run

## When to Use
- Deploying new versions
- Rolling back deployments
- Checking deployment status

## How It Works
1. Validates environment
2. Runs pre-deploy checks
3. Executes deployment
4. Verifies deployment
5. Reports results

## Examples
Deploy to production:
```
/deploy --env production
```

Dry run (no changes):
```
/deploy --env staging --dry-run
```

Rollback:
```
/ploy --rollback --version 1.2.3
```
```

### Pattern 2: Analysis Skill
```yaml
---
name: security-audit
description: Comprehensive security audit of code changes
---

# Security Audit

## Quick Start
/security-audit --changed-files
/security-audit --full-scan

## When to Use
- Before code reviews
- Security compliance checks
- Vulnerability assessment

## How It Works
1. Scans changed files
2. Identifies security patterns
3. Checks against OWASP guidelines
4. Generates findings report

## Examples
Audit changed files:
```
/security-audit --changed-files
```

Full codebase scan:
```
/security-audit --full-scan --verbose
```

## Scripts Used
See `scripts/security-check.sh` for implementation details.
```

### Pattern 3: Multi-Tool Skill
```yaml
---
name: data-pipeline
description: Build, test, and deploy data processing pipelines
---

# Data Pipeline

## Quick Start
/pipeline build --source s3://bucket/data
/pipeline test --pipeline-id 123
/pipeline deploy --pipeline-id 123 --env prod

## When to Use
- Creating data pipelines
- Testing transformations
- Deploying to production

## How It Works
1. Validates pipeline configuration
2. Builds pipeline artifacts
3. Runs tests
4. Deploys to environment

## Examples
Build from S3:
```
/pipeline build --source s3://bucket/data --format parquet
```

Test pipeline:
```
/pipeline test --pipeline-id 123 --sample-data 1000
```

## Advanced Usage
See `reference.md` for:
- Custom transformations
- Advanced testing strategies
- Monitoring and alerting

## Resources
- `scripts/build.sh`: Build logic
- `scripts/test.sh`: Testing framework
- `templates/`: Pipeline templates
```

## Best Practices

### 1. Keep Level 1 Minimal
```yaml
# Good: Short, specific
description: "Security audit of code changes. Use before code reviews."

# Bad: Too verbose
description: "This skill performs comprehensive security audits of code changes including static analysis, dependency checking, OWASP compliance validation, and vulnerability scanning. It can be used before code reviews, after pulling new changes, or as part of CI/CD pipelines. The skill supports multiple languages and frameworks..."
```

### 2. Level 2 Should Be Actionable
```markdown
# Good: Specific steps
## How It Works
1. Run security scanner
2. Check for OWASP top 10
3. Validate dependencies
4. Generate report

# Bad: Vague
## How It Works
The skill analyzes code for security issues and provides recommendations.
```

### 3. Provide Concrete Examples
```markdown
# Good
## Examples
Audit changed files:
```
/security-audit --changed-files
```

# Bad
## Examples
Use the skill to audit your code.
```

### 4. Scripts Are Execute-Only
```bash
# scripts/security-check.sh
#!/bin/bash
# This script runs security checks
# Code never enters context, only outputs

echo "Running security audit..."

# Check for hardcoded secrets
if grep -r "password\s*=" . 2>/dev/null; then
    echo "WARNING: Hardcoded passwords found"
    exit 1
fi

echo "Security check complete"
exit 0
```

### 5. Progressive Disclosure
```markdown
# Good: Layered information
## Quick Start
[2-3 simple examples]

## Examples
[More detailed examples]

## Advanced Usage
[Link to reference.md]

## See Also
[Link to other skills]
```

## Anti-Patterns (Avoid)

❌ **Monolithic SKILL.md**: Everything in one file
❌ **Missing examples**: No concrete usage patterns
❌ **No scripts**: Everything in instructions (consumes tokens)
❌ **Too verbose at Level 1**: Overly long descriptions
❌ **Missing metadata**: No YAML frontmatter
❌ **No progression**: Same info at all levels
❌ **Hardcoded paths**: Scripts with relative paths
❌ **Complex bash in context**: Scripts should be external files

## Skill Composition

### Combining Skills
Skills can reference each other:
```markdown
## See Also
- `security-audit`: For security checks
- `code-reviewer`: For quality review
- `deploy-app`: For deployment
```

### Skill Chains
```
User Request
  ↓
Skill A (triggered)
  ↓
Skill B (called by A)
  ↓
Skill C (called by B)
  ↓
Result
```

## Skill Lifecycle

### In Claude Code
1. Skills discovered from `.claude/skills/` directories
2. Metadata loaded at startup
3. SKILL.md loaded when triggered
4. Scripts executed via bash
5. Cleaned up when done

### In Agent SDK
```python
options = ClaudeAgentOptions(
    allowed_tools=["Skill", "Read", "Bash"]
)
# Skills auto-discovered from .claude/skills/
```

### In Claude API
```python
options = ClaudeAgentOptions(
    container={
        "skill_ids": ["code-reviewer", "security-audit"],
        "codeExecutionEnabled": True
    }
)
```

## Security Considerations

### 1. Trust Source
- Only use skills from trusted sources
- Audit skill code before use
- Review scripts for security issues

### 2. Permission Scope
- Skills run with user's permissions
- Can read/write files user can access
- Can execute commands user can run

### 3. Network Access
- Skills can make network requests
- Follow user's network permissions
- Can be restricted by sandbox

### 4. Audit Everything
```bash
# In scripts
echo "Security audit started: $(date)" >> /tmp/audit.log
echo "Files scanned: $FILE_COUNT" >> /tmp/audit.log
```

## Debugging Skills

### Enable Debug Mode
```bash
claude --debug
# Shows: skill loading, execution, errors
```

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Skill not loading | Missing SKILL.md | Add SKILL.md to skill directory |
| Metadata not showing | Invalid YAML | Validate YAML frontmatter |
| Scripts failing | Not executable | `chmod +x script.sh` |
| Paths broken | Relative paths | Use absolute or env vars |
| Context too large | No scripts | Move code to scripts/ |

### Testing Skills
```bash
# Test script directly
bash scripts/security-check.sh

# Test in Claude Code
/code-reviewer --test-mode

# Debug mode
claude --debug
```

## Distribution

### Local (Claude Code)
```
.claude/skills/
├── skill-name/
│   └── SKILL.md
└── another-skill/
    └── SKILL.md
```

### Package for Sharing
```
my-skills/
├── code-reviewer/
│   ├── SKILL.md
│   └── scripts/
├── security-audit/
│   ├── SKILL.md
│   └── scripts/
└── README.md
```

## Volatile Details (Look Up)

These change frequently:
- Exact field names in YAML frontmatter
- SKILL.md format requirements
- Available tools in different environments
- Platform-specific constraints

**Always verify**: Use latest documentation for current requirements.

## Resources

### Official Skills
- PowerPoint (pptx)
- Excel (xlsx)
- Word (docx)
- PDF (pdf)

### Community Skills
- GitHub: Search "claude skills"
- npm: @anthropic-ai/claude-skills

---

## Official Documentation Links

- **Agent Skills Overview**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md
- **Agent Skills Quickstart**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart
- **Agent Skills Best Practices**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- **Skills in Claude Code**: https://code.claude.com/docs/en/skills
- **Agent SDK Skills**: https://platform.claude.com/docs/en/agent-sdk/skills.md
- **Agent Skills Cookbook**: https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction

### Verification
Last verified: 2026-01-13
