---
name: manage-skills
description: The Authority on Skill Architecture. MUST CONSULT when creating, auditing, or refactoring skills to ensure compliance with architectural standards, naming conventions, and directory structure.
allowed-tools: Read Write Edit
---

# Skill Management Authority

## Knowledge Base

### 1. Shared Standards
**File:** [shared-standards.md](references/shared-standards.md)
**Contains:** Common principles, integration patterns, and anti-patterns for all management skills.

### 2. Communication & Prompts
**File:** [standards-communication.md](references/standards-communication.md)
**Contains:** The Triangle Prompt Pattern, XML/Markdown usage, Handoff protocols.

### 3. Security
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
| [shared-standards.md](references/shared-standards.md) | Common standards for all management skills |
| [standards-communication.md](references/standards-communication.md) | Triangle Prompt pattern, XML/Markdown usage, handoff protocols |
| [standards-security.md](references/standards-security.md) | Background execution, tool permissions, path traversal |
| (Consult `CLAUDE.md`) | Core architecture and quality gates |
