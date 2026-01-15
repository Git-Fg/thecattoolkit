---
name: designing-architecture
description: "Applies system architecture and design frameworks for software systems. Provides discovery protocols, system design workflows, architecture decision records (ADRs), and quality evaluation criteria. PROACTIVELY Use when designing new systems, analyzing existing architecture, or making architectural decisions. Do not use for project plan state management, task execution, or phase coordination."
allowed-tools: [Read, Write, Edit, Glob, Grep, TodoWrite]
---

# Architecture Design & Analysis

## Core Purpose

Provides architectural methodology for system design and analysis:

1. **Discovery**: Analyze existing systems and gather requirements
2. **System Design**: Apply design frameworks for new systems
3. **Architecture Patterns**: Select appropriate patterns based on requirements
4. **Decision Records**: Document significant architectural decisions via ADRs
5. **Quality Evaluation**: Assess architecture quality using comprehensive criteria

## Core Principles

1. **Requirements-First**: Understand functional and non-functional requirements before selecting patterns
2. **Trade-off Awareness**: Every architectural decision has consequences; document them explicitly
3. **Evolutionary Design**: Design for change and incremental improvement

## Protocol Reference Index

### Discovery & Analysis
- **Protocol**: `references/discovery.md` - Deep discovery workflow (Context Mapping, Requirements, Environment)
- **Protocol**: `references/codebase-discovery.md` - Quick codebase exploration
- **Reference**: `references/quality-checklist.md` - Quality evaluation checklist
- **When to Apply**: MANDATORY before starting any design or analysis task to ensure 100% clarity.

### System Design (Greenfield)
- **Protocol**: `references/system-design.md` - Complete system design workflow
- **When to Apply**: New systems, major features, technology selection

### Architecture Patterns
- **Reference**: `references/architecture-patterns.md` - Design patterns guide
- **When to Apply**: Selecting patterns based on requirements

### Architecture Decision Records
- **Template**: `references/adr-template.md` - ADR template and documentation standards
- **When to Apply**: Documenting significant architectural decisions

**ADR Creation Protocol:**
1. **Auto-increment**: Count existing ADR entries and add 1
2. **Append**: Add to bottom of ADR.md (never delete or modify old entries)
3. **File location**: `.cattoolkit/plan/{project-slug}/ADR.md`
4. **Numbering**: Sequential (ADR-001, ADR-002, etc.)
5. **Append-Only Rule**: Never delete, modify, or reorder entries

**When to Create ADR:**
- Technology stack changes (frameworks, databases)
- Major architectural patterns (auth strategy, state management)
- Breaking API changes (protocol changes, data format changes)
- Infrastructure additions (caching, message queues)
- Significant refactors (directory structure, module organization)

## Workflow Selection

**Protocol Chain:**
1. **Discovery**: ALWAYS start with `references/discovery.md` to gather context.
2. **Analysis/Design**: Based on discovery results:
   - **Greenfield (New System)**: Follow `references/system-design.md`.
   - **Brownfield (Existing System)**: Perform mapping and refactoring analysis.
3. **Documentation**: Document all outcomes with ADRs and diagrams.

## Quality Criteria

Every architecture must address specific quality gates. For the comprehensive evaluation checklist, see `references/quality-checklist.md`.

**Note**: For project plan state management and task execution, use `managing-plans` skill.
