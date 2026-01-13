---
name: architecting-project-plans
description: "Actively investigates codebases, synthesizes requirements, and creates comprehensive project plans. Use when creating plans from user requirements and codebase discovery."
context: fork
---

# Architecting Project Plans: Intelligence Layer

## Core Purpose

**Active Intelligence:** This skill investigates codebases, synthesizes requirements, and creates comprehensive project plans.

It answers: "WHAT should we build?" and "HOW should we approach it?"

## Integration Pattern

This skill **uses** `managing-project-plans` for:
- File system standards (BRIEF, ROADMAP, PHASE schemas)
- Templates (in managing-project-plans/assets/templates/)
- Validation rules

This skill **provides**:
- Auto-discovery workflow logic
- Codebase analysis patterns
- Requirement synthesis algorithms
- Plan architecture methodology

## Discovery Protocol

### Phase 1: Project Scanning
**Goal:** Understand the existing codebase structure

**Tools Used:** `Glob`, `Bash`, `Read`

**Actions:**
1. **Scan Project Structure**
   ```bash
   # Count total files
   find . -type f -not -path '*/.*' | wc -l

   # Find configuration files
   Glob pattern: package.json, pyproject.toml, requirements.txt, Cargo.toml, go.mod
   ```

2. **Analyze Dependencies**
   - Read package.json, requirements.txt, etc.
   - Identify frameworks (React, Vue, Django, FastAPI, etc.)
   - Note build tools (Vite, Webpack, Make, etc.)
   - Check for databases, message queues, cache layers

3. **Review Documentation**
   - Read existing README files
   - Check for architecture docs
   - Review code comments for patterns
   - Identify existing conventions

**Output:** `.cattoolkit/plan/{project-slug}/DISCOVERY.md`

### Phase 2: Context Analysis
**Goal:** Understand project context and constraints

**Tools Used:** `Read`, `Grep`, `Bash`

**Actions:**
1. **Codebase Patterns**
   - Search for recurring patterns: `Grep pattern: "class \|function \|const "`
   - Identify architectural style: MVC, microservices, monolith, etc.
   - Note naming conventions
   - Check for tests: `find . -name "*test*" -o -name "*spec*"`

2. **Brownfield Analysis**
   - Existing features: What works?
   - Known issues: What breaks?
   - Technical debt: What needs fixing?
   - Migration requirements: What must change?

3. **Environment Detection**
   - OS compatibility: Linux, macOS, Windows?
   - Runtime: Node.js, Python, Go, Java?
   - Package managers: npm, pip, cargo, maven?

**Output:** Context profile with constraints and opportunities

### Phase 3: Requirement Synthesis
**Goal:** Combine user input with codebase analysis

**Inputs:**
- User requirements (from command arguments)
- Discovery findings (from Phase 1)
- Context analysis (from Phase 2)

**Process:**
1. **Map Requirements to Reality**
   - User wants X, codebase has Y → Gap analysis
   - User wants X, framework supports Y → Integration strategy
   - User wants X, no existing support → New implementation

2. **Identify Constraints**
   - Technical: Framework limitations, dependency conflicts
   - Business: Timeline, budget, stakeholder requirements
   - Environmental: Deployment platform, scale requirements

3. **Generate Success Criteria**
   - Measurable outcomes
   - Testable conditions
   - Acceptance criteria

**Output:** Synthesized requirements document

## Plan Architecture Methodology

### Breaking Down Work
**Principle:** Tasks should be atomic, verifiable, and independent

**Task Creation Pattern:**
```markdown
### Task N: {action-verb}-{object}
**Scope:** {specific files or directories}
**Action:** {imperative description of what to do}
**Verify:** {how to confirm it worked}
**Done:** {acceptance criteria}
```

**Task Granularity:**
- **Too Big:** Takes more than 2-3 hours
- **Too Small:** Can be combined with another task
- **Just Right:** 30-90 minutes, clear success criteria

### Phase Structure
**Pattern:** Foundation → Core → Enhancement → Polish

1. **Foundation Phase**
   - Setup, configuration, scaffolding
   - Dependencies, environment setup
   - Basic structure creation

2. **Core Phase**
   - Primary functionality implementation
   - Core features that deliver value
   - Main business logic

3. **Enhancement Phase**
   - Additional features
   - Performance optimizations
   - Extended capabilities

4. **Polish Phase**
   - UI/UX improvements
   - Documentation
   - Final testing and cleanup

### Dependency Management
**Rules:**
1. No circular dependencies
2. Explicit dependencies in ROADMAP.md
3. Foundation phases before core phases
4. Independent tasks can run in parallel

## Synthesis Algorithms

### Algorithm 1: Greenfield Planning
**When:** New project, no existing codebase

**Steps:**
1. Analyze user requirements
2. Select technology stack (React + TypeScript + Vite, etc.)
3. Define success criteria
4. Create foundation → core → enhancement → polish phases
5. Generate atomic tasks

### Algorithm 2: Brownfield Integration
**When:** Adding to existing codebase

**Steps:**
1. Discovery protocol (Phase 1-2)
2. Map requirements to existing patterns
3. Identify integration points
4. Create migration + enhancement phases
5. Define compatibility requirements

### Algorithm 3: Feature Addition
**When:** Adding specific feature to existing system

**Steps:**
1. Analyze existing feature patterns
2. Follow established conventions
3. Create feature-specific tasks
4. Define integration tests
5. Document new patterns

### Algorithm 4: Refactoring
**When:** Improving existing code

**Steps:**
1. Analyze current architecture
2. Identify pain points
3. Design target architecture
4. Create migration tasks
5. Define rollback strategy

## Plan Creation Workflow

### Using Managing-Project-Plans Standards

1. **Create BRIEF.md**
   - Use `managing-project-plans` template
   - Fill in objective, success criteria, constraints
   - Include current state (for Brownfield)

2. **Create ROADMAP.md**
   - Use `managing-project-plans` template
   - Define phases using methodology above
   - Set explicit dependencies
   - Add phase summaries

3. **Create Phase Plans**
   - Use `managing-project-plans` template
   - Create atomic tasks per phase
   - Add verification criteria
   - Include handoff protocol

4. **Validate Structure**
   - Check file naming
   - Verify status codes
   - Confirm dependencies
   - Apply validation rules

## Quick Reference

### Discovery Checklist
- [ ] Project structure scanned
- [ ] Dependencies analyzed
- [ ] Documentation reviewed
- [ ] Code patterns identified
- [ ] Environment detected
- [ ] Context documented

### Synthesis Checklist
- [ ] Requirements mapped to reality
- [ ] Constraints identified
- [ ] Success criteria defined
- [ ] Phases structured
- [ ] Tasks atomicized
- [ ] Dependencies explicit

### Plan Creation Checklist
- [ ] BRIEF.md created (template)
- [ ] ROADMAP.md created (template)
- [ ] Phase plans created (template)
- [ ] Structure validated
- [ ] Dependencies checked

## References

**See:**
- `references/discovery-protocol.md` - Detailed discovery workflow
- `references/synthesis-algorithms.md` - Requirement synthesis patterns
- `references/integration-patterns.md` - How to use managing-project-plans
- `managing-project-plans` skill - Standards and templates
