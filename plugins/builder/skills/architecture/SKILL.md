---
name: architecture
description: |
  System Architecture and Design Frameworks. MUST USE when designing new systems, analyzing existing architecture, or making architectural decisions.
  Keywords: system design, architecture analysis, scalability, technical decisions, ADR
context: fork
agent: architect
user-invocable: true
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, TodoWrite]
---

# Architecture Design & Analysis

## Operational Protocol
1. **Discovery**: Check for `.cattoolkit/planning/{project}/DISCOVERY.md`. If missing, execute discovery protocol.
2. **Analysis**: Apply appropriate workflow (Greenfield vs. Brownfield) based on requirements.
3. **Design**: Select patterns using architecture patterns and quality criteria.
4. **Documentation**: Create or update ADRs using ADR template.

## Core Principles
1. **Requirements-First**: Understand functional and non-functional requirements before selecting patterns
2. **Trade-off Awareness**: Every architectural decision has consequences; document them explicitly
3. **Evolutionary Design**: Design for change and incremental improvement

## Protocol Reference Index

### Discovery & Analysis
- **Protocol**: `references/discovery.md` - Deep discovery workflow (Context Mapping, Requirements, Environment)
- **Reference**: `references/quality-checklist.md` - Quality evaluation checklist
- **When to Apply**: MANDATORY before starting any design or analysis task to ensure 100% clarity.

### System Design (Greenfield)
- **Protocol**: `references/system-design.md` - Complete system design workflow
- **When to Apply**: New systems, major features, technology selection

### Architecture Decision Records
- **Template**: `references/adr-template.md` - ADR template and documentation standards
- **When to Apply**: Documenting significant architectural decisions

**ADR Creation Protocol:**
1. **Auto-increment**: Count existing ADR entries and add 1
2. **Append**: Add to bottom of ADR.md (never delete or modify old entries)
3. **File location**: `.cattoolkit/planning/{project-slug}/ADR.md`
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

## Architecture Patterns

Select appropriate patterns based on requirements. For detailed pattern descriptions and selection criteria, see `references/system-design.md`.

## Quality Criteria

Every architecture must address specific quality gates. For the comprehensive evaluation checklist, see `references/quality-checklist.md`.

