---
name: project-analysis
description: |
  This skill provides architecture discovery capabilities for new codebases, including structure mapping, tech stack identification, and pattern recognition. It serves as the standard for "Ground Truth" generation.
  <example>
  Context: User starts working on new codebase
  user: "How does this project work?"
  assistant: "I'll load the project-analysis skill to map the architecture."
  </example>
  <example>
  Context: User needs tech stack identification
  user: "What technologies are we using?"
  assistant: "I'll use the project-analysis skill to identify the tech stack."
  </example>
  <example>
  Context: Syncing AI rules with project
  user: "Audit our AI rules against current project"
  assistant: "I'll delegate to the project-analysis skill for rules synchronization."
  </example>
allowed-tools: Read Glob Grep Bash
---

# Architecture Discovery Guide

## Core Principles

### 1. Breadth Before Depth
Always establish the high-level structure (directories, entry points, configuration) before diving into implementation details of specific files.

### 2. Evidence-Based
Don't guess the tech stack. Verify it by checking configuration files (`package.json`, `go.mod`, `pyproject.toml`, `Dockerfile`, etc.).

### 3. Pattern Recognition
Look for naming conventions (Controllers, Services, Hooks) and structural patterns (Monorepo, Clean Architecture) to infer intent.

## Discovery Protocols

### Quick Overview
- **Standard**: `references/quick-scan.md`
- **Purpose**: Fast 3-step project identification
- **When to Use**: Starting work on new codebase, initial onboarding
- **Output**: Structure, stack, and basic purpose

### Architecture Mapping
- **Standard**: `references/architecture-map.md`
- **Purpose**: Deep dive into system design patterns
- **When to Use**: Understanding system design, data flow, component relationships
- **Output**: Architecture diagram, key components, design patterns

### Dependency Audit
- **Standard**: `references/dependency-audit.md`
- **Purpose**: Detailed analysis of dependencies and versions
- **When to Use**: Security audits, upgrade planning, maintenance
- **Output**: Dependency graph, version analysis, security implications

### AI Rules Sync
- **Standard**: `references/sync-rules.md`
- **Purpose**: Audit AI rule files against current project state
- **When to Use**: Ensuring AI guidelines match current project practices
- **Output**: Gap analysis, recommendations for alignment

## Reference Materials

- **Tech Stack Signatures**: `references/tech-stack-signatures.md` - Heuristics for identifying languages and frameworks

## Discovery Checklist

**Phase 1: Project Structure**
- [ ] Identify entry points (main, index, app files)
- [ ] Map directory structure and organization
- [ ] Identify configuration files
- [ ] Note build/deployment scripts

**Phase 2: Technology Stack**
- [ ] Verify language from file extensions
- [ ] Check dependency files (package.json, go.mod, requirements.txt, etc.)
- [ ] Identify framework from structure
- [ ] Note database/ORM patterns
- [ ] Identify testing framework

**Phase 3: Architecture Patterns**
- [ ] Identify architectural style (MVC, Clean Architecture, etc.)
- [ ] Map component relationships
- [ ] Identify data flow patterns
- [ ] Note naming conventions
- [ ] Document design patterns in use