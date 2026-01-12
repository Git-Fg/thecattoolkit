# Anti-Patterns

Common mistakes when creating skills and how to avoid them.

## Architecture Anti-Patterns

### 1. Workflow Router Pattern

**❌ Wrong**: Making skills execute multi-step workflows

```markdown
name: deploy-app
description: "Deploys applications to production with validation"

## Workflow:
1. Build the application
2. Run tests
3. Deploy to staging
4. Run integration tests
5. Deploy to production

This is a COMMAND, not a SKILL!
```

**✅ Correct**: Skills provide knowledge, commands orchestrate

```markdown
name: deployment-strategy
description: "Expert guidance on deployment patterns. Use when designing deployment strategies."

## Deployment Patterns:
- Blue-green deployments
- Canary releases
- Rolling deployments
- Feature flags

When you need to deploy: Use a COMMAND that delegates to this skill for guidance.
```

**Why**: Skills are knowledge bases, not workflow executors. Commands handle orchestration.

---

### 2. All-in-One File

**❌ Wrong**: Everything in SKILL.md (> 1000 lines)

```markdown
SKILL.md (1500 lines):
## Section 1: Introduction
## Section 2: Getting Started
## Section 3: Basic Concepts
## Section 4: Intermediate Topics
## Section 5: Advanced Techniques
## Section 6: Expert Tips
## Section 7: API Reference
## Section 8: Examples
## Section 9: Troubleshooting
## Section 10: Best Practices
```

**✅ Correct**: Progressive disclosure

```markdown
SKILL.md (200 lines):
## Quick start
## Core concepts
## Common patterns

See [references/progressive-disclosure.md](references/progressive-disclosure.md) for advanced topics.
See [references/templates-usage.md](references/templates-usage.md) for complete template guide.
```

**Why**: Progressive disclosure reduces token cost and improves load time.

---

### 3. Unnecessary Forking

**❌ Wrong**: Fork context for < 10 files

```markdown
---
context: fork
---
```

**✅ Correct**: Use inline skill for small scopes

```markdown
---
# No context specified = inline
---
```

**Why**: Fork costs 3× more than inline. Only fork for >10 files or isolation needs.

---

## Naming Anti-Patterns

### 4. Wrong Name Format

**❌ Wrong**:
- `CreateHooks` (PascalCase)
- `create_hooks` (snake_case)
- `createhooks` (no separator)
- `create hooks` (spaces)

**✅ Correct**:
- `create-hooks` (kebab-case)
- `pdf-processor`
- `csv-validator`

**Why**: Naming convention enforcement prevents conflicts and ensures consistency.

---

### 5. Poor Name Choices

**❌ Wrong**:
- `my-skill` (too generic)
- `do-thing` (unclear purpose)
- `complex-workflow-processor` (too long, workflow in name)

**✅ Correct**:
- `pdf-processor` (clear purpose)
- `csv-validator` (specific capability)
- `security-audit` (knowledge domain)

**Why**: Names should clearly indicate capability or domain.

---

## Description Anti-Patterns

### 6. Vague Descriptions

**❌ Wrong**:
```yaml
description: "A skill for helping with code."
description: "Useful tools and features."
description: "Do things better."
```

**✅ Correct**:
```yaml
description: "Processes CSV files with validation. Use when working with tabular data."
description: "Enforces coding standards. Use when committing code."
```

**Why**: Descriptions enable intent-based discovery. Be specific.

---

### 7. First Person

**❌ Wrong**:
```yaml
description: "I help you process CSV files."
description: "You should use me when validating data."
```

**✅ Correct**:
```yaml
description: "Processes CSV files with validation. Use when working with tabular data."
```

**Why**: Always use third person for consistency and portability.

---

### 8. Missing Trigger Conditions

**❌ Wrong**:
```yaml
description: "Processes CSV files."
```

**✅ Correct**:
```yaml
description: "Processes CSV files with validation. Use when working with tabular data."
```

**Why**: "Use when" clause helps users discover skills by intent.

---

## Structure Anti-Patterns

### 9. Broken Links

**❌ Wrong**:
```
Broken link patterns:
  - File doesn't exist
  - Wrong directory path
  - Incorrect file case
```

**✅ Correct**:
```
Correct link patterns:
  - Direct reference: references/existing-file.md
  - Valid example: examples/simple-skill-example.md
```

**Why**: Broken links confuse users and fail validation.

**Rules**:
- Use Unix paths (`/` not `\`)
- Direct references only (no A→B→C chains)
- Match exact case
- No relative paths

---

### 10. Deep Linking Chains

**❌ Wrong**:
```
SKILL.md:
See step-one
references/step-one.md:
For details, see step-two
references/step-two.md:
Finally, see step-three
```

**✅ Correct**:
```
SKILL.md:
See references/step-one.md directly
See references/step-two.md directly
See references/step-three.md directly
```

**Why**: Direct links are clearer and don't require following chains.

---

### 11. No Structure

**❌ Wrong**:
```
skill/
└── SKILL.md (random text, no sections)
```

**✅ Correct**:
```
skill/
├── SKILL.md (structured with sections)
├── references/ (organized by topic)
├── examples/ (step-by-step)
└── assets/ (templates)
```

**Why**: Structure helps users find information quickly.

---

## Implementation Anti-Patterns

### 12. Caller Assumptions

**❌ Wrong**:
```markdown
"You have been tasked with creating hooks."
"Use the /create-hooks command."
"When called from a command..."
```

**✅ Correct**:
```markdown
"Hooks are event-driven automation."
"To create hooks, follow this workflow..."
"For hook examples, see references/examples.md"
```

**Why**: Skills are discovered by intent, not called procedurally. Don't assume caller.

---

### 13. Cross-Plugin Hardlinks

**❌ Wrong**:
```
See ../../other-plugin/docs/guide.md
Run script: ../other-plugin/scripts/helper.sh
```

**✅ Correct**:
```
See other plugin documentation for cross-plugin workflows.
For hook validation, use validation scripts in your plugin.
```

**Why**: Hard links create tight coupling and break portability.

---

### 14. Over-Engineering

**❌ Wrong**:
```markdown
---
name: csv-processor-advanced-v2
description: "Advanced CSV processing with configurable options, extensible plugins, custom validators, streaming support, and enterprise features."
context: fork
allowed-tools: [Read, Write, Edit, Grep, Bash, WebFetch, WebSearch, Task]
user-invocable: true
---
```

**✅ Correct**:
```markdown
---
name: csv-processor
description: "Processes CSV files with validation. Use when working with tabular data."
---
```

**Why**: Start simple. Add complexity only when needed.

---

### 15. Interactive Intake

**❌ Wrong**:
```markdown
## Intake
1. Ask the user what they want to do
2. Ask for the file path
3. Ask for the desired output format
```

**✅ Correct**:
```markdown
## Intake
1. Infer intent from conversation history and user prompt
2. If arguments are missing, use smart defaults or infer from open files
3. ONLY ask if critical information is missing and cannot be inferred
```

**Why**: Skills should be smart and autonomous. Interactive logic ("ask user") breaks the flow and treats the user like a data entry clerk.

---

### 16. Redundant README

**❌ Wrong**:
```
my-skill/
├── SKILL.md
└── README.md  <-- Delete this!
```

**✅ Correct**:
```
my-skill/
└── SKILL.md
```

**Why**: `SKILL.md` is the authoritative entry point for a skill. Adding a `README.md` creates ambiguity about which file the agent should read and often leads to duplicated or out-of-sync documentation. `README.md` belongs at the **Project** or **Plugin** root, not in individual skill directories.

---

## Anti-Pattern Quick Reference

| Anti-Pattern | Symptom | Fix |
|--------------|---------|-----|
| Workflow Router | Multi-step process | Move to COMMAND |
| All-in-One File | SKILL.md > 500 lines | Use references/ |
| Unnecessary Fork | < 10 files, fork context | Remove context |
| Wrong Format Name | PascalCase, snake_case | Use kebab-case |
| Vague Description | Generic "helpful" text | Be specific with capability |
| First Person | "I/you" in description | Use third person |
| Missing Triggers | No "Use when" | Add trigger conditions |
| Broken Links | 404 errors | Use direct Unix paths |
| Deep Linking | A→B→C chains | Direct references |
| Caller Assumptions | "You have been tasked" | Remove caller assumptions |
| Cross-Plugin Links | `../other-plugin/` | Remove hard links |
| Over-Engineering | Too many features | Start simple |
| Interactive Intake | "Ask the user..." | Infer from context |
| Redundant README | `skill/README.md` | Use `SKILL.md` only |

---

## Detection

**Automated detection**:
```bash
# Run all validations
uv run scripts/validate-all.py ./my-skill/

# Check token budget
uv run scripts/check-token-budget.py ./my-plugin/
```

**Manual review checklist**:
- [ ] Name follows kebab-case format
- [ ] Description has capability + trigger
- [ ] SKILL.md < 500 lines
- [ ] All links work
- [ ] No caller assumptions
- [ ] No workflow execution
- [ ] Progressive structure
- [ ] No cross-plugin links
- [ ] No interactive intake "Ask user" loops
- [ ] No `README.md` inside skill folder

---

## Recovery

If you've created an anti-pattern:

1. **Identify the pattern** → See table above
2. **Refactor incrementally** → Don't rewrite everything
3. **Validate frequently** → Run scripts after each change
4. **Test the result** → Ensure it still works

**Example refactor**: Workflow Router → Knowledge Provider

**Before**:
```markdown
name: deploy-app
## Steps:
1. Build...
2. Test...
3. Deploy...
```

**After**:
```markdown
name: deployment-guide
## Patterns:
- Blue-green
- Canary
- Rolling...
```

Move the actual deployment to a COMMAND.

---

## Prevention

**Best practices**:
1. Start with template matching your complexity
2. Run validation scripts early and often
3. Get feedback before publishing
4. Keep it simple initially
5. Add complexity only when needed

**Remember**:
- Skills = Knowledge
- Commands = Orchestration
- Agents = Delegation

Choose the right primitive for the job.
