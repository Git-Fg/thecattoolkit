# Command Patterns

## The Three Patterns

Commands follow one of three primary patterns based on their purpose and complexity.

## Pattern 1: Wrapper

**Purpose:** Simple shortcut to a single skill

**Use Case:**
- Quick access to commonly-used skills
- Semantic discovery is unreliable
- Zero-retention alias

**Structure:**
```yaml
---
description: "Quick shortcut for [skill purpose]"
allowed-tools: [Skill(skill-name)]
disable-model-invocation: true
---

# [Command Name] Shortcut

Invoke `skill-name` for [purpose].

**Goal:** [What the command accomplishes]

**Output:** [Expected result]
```

**Example:**
```yaml
---
description: "Quick code audit shortcut"
allowed-tools: [Skill(audit-security)]
disable-model-invocation: true
---

# Audit Shortcut

Invoke `audit-security` for immediate code vulnerability scan.

**Goal:** Scan codebase for security issues
**Output:** Security report with findings
```

## Pattern 2: Orchestrator

**Purpose:** Coordinate multiple skills or agents in sequence

**Use Case:**
- Multi-step workflows
- Complex procedures requiring multiple capabilities
- Sequential or parallel skill execution

**Structure:**
```yaml
---
description: "Execute [workflow description]"
allowed-tools: [Skill(a), Skill(b), Skill(c), Task]
---

# [Workflow Name]

Execute complete workflow:
1. **Step 1:** Invoke `skill-a` for [purpose]
2. **Step 2:** Delegate to `worker` agent for [task]
3. **Step 3:** Invoke `skill-c` for [verification]

**Constraint:** Do not ask for permission between steps unless the plan explicitly requires it.
```

**Example:**
```yaml
---
description: "Execute complete release workflow"
allowed-tools: [Skill(version-bump), Skill(testing), Skill(deploy)]
---

# Release Orchestrator

Execute complete release workflow:
1. **Version:** Bump version in package.json
2. **Test:** Run test suite
3. **Deploy:** Push to production

**Goal:** Release new version with validation
**Constraint:** Abort on test failure
```

## Pattern 3: Wizard

**Purpose:** Interactive workflow requiring user input

**Use Case:**
- Setup procedures
- Configuration workflows
- Multi-stage operations with decision points

**Structure:**
```yaml
---
description: "Interactive [wizard purpose]"
argument-hint: "Optional [parameter] description"
disable-model-invocation: true
---

# [Wizard Name]

Interactive wizard for [purpose].

## Phase 1: Gather Requirements

Use `AskUserQuestion` to collect:
- [Question 1]
- [Question 2]
- [Question 3]

## Phase 2: Execute

Based on user responses:
1. **Option A:** [Procedure A]
2. **Option B:** [Procedure B]
3. **Option C:** [Procedure C]

## Phase 3: Verify

Verify results and report completion.
```

**Example:**
```yaml
---
description: "Interactive project scaffolding"
argument-hint: "Optional template name"
disable-model-invocation: true
---

# Scaffold Wizard

Interactive wizard for creating new projects.

## Phase 1: Template Selection

Present available templates:
- **Minimal:** Basic structure only
- **Standard:** Include common tooling
- **Full:** Complete setup with all features

## Phase 2: Configuration

Gather project details:
- Project name
- Package manager preference
- TypeScript or JavaScript

## Phase 3: Generate

Create project structure based on selections.
```

## Pattern Selection Matrix

| Requirement | Best Pattern | Why |
|:------------|:-------------|:-----|
| Single skill access | Wrapper | Simplest, direct |
| Multi-skill coordination | Orchestrator | Sequential execution |
| User input needed | Wizard | Interactive |
| Human-only shortcut | Wrapper + `disable-model-invocation` | Zero retention |
| Complex decision tree | Wizard | Phased interaction |

## Anti-Patterns

**Avoid these:**

1. **Redundant Wrapper:** Command that just repeats skill description
   ```yaml
   # Bad
   description: "A command that does X"
   # Just invoke the skill directly instead
   ```

2. **Over-Orchestrating:** Commands for simple tasks
   ```yaml
   # Bad - single task, no orchestration needed
   description: "Read a file"
   # Use skill directly or rely on base capabilities
   ```

3. **Wizard without Questions:** Wizard pattern that doesn't use AskUserQuestion
   ```yaml
   # Bad
   description: "Interactive wizard"
   # But no AskUserQuestion in body
   # Should be Orchestrator instead
   ```
