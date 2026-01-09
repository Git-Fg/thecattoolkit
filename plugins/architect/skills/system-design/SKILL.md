---
name: system-design
description: |
  Comprehensive System Architecture and Design.
  MUST USE when designing new systems, analyzing existing architecture, or making architectural decisions.
  Provides patterns, quality criteria, and ADR documentation.
  Keywords: system design, architecture, brownfield analysis, greenfield design, ADR
context: fork
agent: architect
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, TodoWrite
---

# Architecture Design & Analysis

## Operational Protocol
1. **Initialize**: Locate and read `.cattoolkit/planning/{project-slug}/DISCOVERY.md`. If missing, execute `references/discovery.md` protocol first.
2. **Analyze**: Apply the appropriate workflow (Greenfield vs. Brownfield) based on the input request.
3. **Design**: Select patterns and technologies using `references/system-design.md`.
4. **Verify**: Check design against `references/quality-checklist.md`.
5. **Document**: Create or update ADRs using `references/adr-template.md`.

## Workflow Selection

### Discovery & Analysis
- **Protocol**: `references/discovery.md`
- **When to Apply**: MANDATORY start for all tasks. Ensures 100% context clarity.

### System Design (Greenfield)
- **Protocol**: `references/system-design.md`
- **When to Apply**: New systems, major features, technology selection.

### Existing System Analysis (Brownfield)
- **Protocol**: `references/system-design.md` (See "Existing System Analysis" section)
- **When to Apply**: Refactoring, scalability audits, legacy migration.

## Architecture Decision Records (ADR)
**Location**: `.cattoolkit/planning/{project-slug}/ADR.md`
**Rule**: Append-only. Never modify existing decisions.
**Numbering**: Sequential (ADR-001, ADR-002...).

## Core Principles
1. **Requirements-First**: Functional/Non-functional reqs precede pattern selection.
2. **Trade-off Awareness**: Document "Why not X?" for every "We chose Y".
3. **Evolutionary Design**: Prioritize decoupled, changeable systems over perfect ones.

