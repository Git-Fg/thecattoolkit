---
name: architecture
description: |
  System Architecture and Design Frameworks. MUST USE when designing new systems, analyzing existing architecture, or making architectural decisions. Provides comprehensive patterns, quality criteria, and ADR templates.
  <example>
  Context: User needs to design a new system
  user: "Design a real-time collaborative document editing service"
  assistant: "I'll load the architecture skill to perform comprehensive system design with pattern selection and ADR documentation."
  </example>
  <example>
  Context: User wants to analyze existing architecture
  user: "Analyze our microservices architecture for scalability issues"
  assistant: "I'll use the architecture skill to perform brownfield analysis and identify architectural improvements."
  </example>
  <example>
  Context: Architectural decision needed
  user: "Should we use microservices or monolith for our new API?"
  assistant: "I'll load the architecture skill to analyze the trade-offs and document the decision with an ADR."
  </example>
allowed-tools: Read Write Edit Glob Grep Bash TodoWrite
---

# Architecture Design & Analysis

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

