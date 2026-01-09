---
name: manage-skills
description: The Authority on Skill Architecture. MUST CONSULT when creating, auditing, or refactoring skills to ensure compliance with architectural standards, naming conventions, and directory structure.
allowed-tools: Read Write Edit
---

# Skill Management Authority

## Essential Principles

1. **Passive Knowledge**: Skills never ask questions. They provide standards and templates for autonomous execution.
2. **Atomic Independence**: Skills do not depend on specific Commands. They are self-contained libraries of knowledge.
3. **Progressive Disclosure**: SKILL.md < 500 lines; detailed standards live in `references/`.
4. **Intelligence > Process**: Trust the model to determine execution steps based on standards and templates.

## Knowledge Base

### 1. Communication & Envelopes
**File:** [standards-communication.md](references/standards-communication.md)
**Contains:** The Envelope Pattern, XML/Markdown usage, Handoff protocols.

### 2. Security
**File:** [standards-security.md](references/standards-security.md)
**Contains:** Background execution rules, Tool permissions.

## Working Examples

Ready-to-use patterns:

- **[router-pattern.md](examples/router-pattern.md)** - Code analysis router demonstrating delegator pattern

## Asset Library

### Templates (`assets/templates/`)
Production-grade templates for skill scaffolding:

| Template | Use Case |
|----------|----------|
| `standard-skill.md` | Single-workflow skills (Minimal/Task) |
| `router-pattern.md` | Complex skills with 4+ workflows |
| `progressive-disclosure.md` | Skills requiring references/ subdirectory |
| `reference-file.md` | Reference document formatting |

### References (`references/`)
Consolidated standards and documentation:

| Reference | Purpose |
|-----------|---------|
| [standards-communication.md](references/standards-communication.md) | Envelope pattern, XML/Markdown usage, handoff protocols |
| [standards-security.md](references/standards-security.md) | Background execution, tool permissions, path traversal |
| (Consult `CLAUDE.md`) | Core architecture and quality gates |

## Integration Points

### With Commands
Commands provide the **orchestration layer**:
- Define goals and inject context
- Handle user interaction (Vector phase)
- Delegate to agents using Envelope pattern (Triangle phase)
- Validate and present results

### With Agents
Agents provide the **execution layer**:
- Load skills for domain expertise
- Apply declarative standards autonomously
- Execute without asking questions (Triangle pattern)
- Use intelligence to determine "How" based on "What" and "Rules"

### With Other Skills
Skills are **self-contained libraries**:
- No cross-skill dependencies via relative paths
- Use natural language references
- Trust agent to load multiple skills
- Each skill is independently useful
