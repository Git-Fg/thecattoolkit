# Command Creation Standards

## 1. Structural Patterns

### Ultra-Minimalist (Default)
```yaml
---
description: {Brief, human-friendly description}
argument-hint: [{optional argument description}]
---
{One-line instruction}
```

### Structured (Multi-step)
```markdown
## Objective
{Goal description}

## Process
1. {Step 1}
2. {Step 2}

## Success Criteria
- {Result 1}
```

## 2. XML vs Markdown Matrix

| Use Case | Recommended Format |
|----------|--------------------|
| Default structure | Markdown |
| Machine-parsed routing | `<routing>` (Table) |
| Intent Analysis | `<intent_analysis>` |
| Strict Constraints | `<constraints>` |

## 3. Description Specifications

- **Formula**: `{Action Verb} + {Context/Trigger}`
- **Required Keywords**:
  - `MUST`: Critical operations.
  - `PROACTIVE`: Recommended workflows.
  - `CONSULT`: Reference expertise.

## 4. User-Centric Wrappers

- **Condition**: Command delegates to `Skill` or `Task` tools.
- **Requirement**: `disable-model-invocation: true` in frontmatter.
- **Goal**: Prevent AI from programmatically calling what it can already do via tools.
