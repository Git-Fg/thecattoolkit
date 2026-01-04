---
name: architect
description: System design and architecture planning mode. PROACTIVELY USE for high-level design, trade-off analysis, and technical decisions before implementation.
argument-hint: [feature/system]
allowed-tools: Skill(create-plans), Read, Write
---

## Objective

Establish the technical vision for a system or feature by creating a persistent BRIEF.md artifact.

## Process

Invoke the `create-plans` skill with the following intent:

1. **Analyze the user request**: $ARGUMENTS

2. **Create or update project `BRIEF.md`** with focus on:
   - **System Architecture**: High-level design, component relationships, data flow
   - **Trade-off Analysis**: Options considered with pros/cons for each approach
   - **Scalability**: Future growth considerations and evolution paths

3. **Do not output text to chat only** - ensure a `BRIEF.md` file is created via the skill

The skill will guide you through the brief creation process with proper structure and persistence.

## Expected BRIEF.md Sections

- Context (why this design is needed)
- Requirements (functional and non-functional)
- Options Considered (with pros/cons)
- Recommended Approach (with rationale)
- Architecture Diagram (ASCII visualization)
- Implementation Plan (phased approach)
- Risks & Mitigations
