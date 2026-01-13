---
description: "Collaboratively architect a plan with deep requirements gathering."
argument-hint: "<project description>"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, Skill(managing-project-plans), Skill(architecting-project-plans), AskUserQuestion]
disable-model-invocation: true
---

# Create Plan (Interactive)

## Quick Reference
- **Usage**: `/sys-builder:create-plan-interactive "Description of what to build"`
- **Purpose**: Deep discovery, clarification questions, collaborative planning
- **Returns**: Plan files with 100% clarity on requirements
- **When to Use**: Complex projects with ambiguities or unclear requirements

## Table of Contents
1. [Overview](#overview)
2. [Quick Start](#quick-start) (Get clarity in 4 phases)
3. [Detailed Protocol](#detailed-protocol) (Complete workflow)
4. [Clarification Menu](#clarification-menu) (Question templates)
5. [Examples](#examples) (Common scenarios)
6. [Reference](#reference) (Technical details)

## Overview (Expandable)

This command achieves **100% clarity** on requirements before writing any plan files.

**Workflow:**
1. **Deep Discovery** → Investigate codebase thoroughly
2. **Question Burst** → Ask structured clarification questions
3. **Architecture** → Create plan based on clarified requirements
4. **Validation** → Validate plan with user before task generation

**Key Features:**
- Structured "Clarification Menu" with 3 options per question
- Your recommendation marked as [RECOMMENDED]
- Waits for user selection before proceeding
- Ideal for complex projects where ambiguity could derail execution

**Uses Skills:**
- `managing-project-plans` - Templates and standards
- `architecting-project-plans` - Investigation and synthesis methodology

## Quick Start

```bash
# For complex projects
/sys-builder:create-plan-interactive "Build a web app with authentication"
```

**Four Phases:**
1. **Discovery** → I investigate your codebase
2. **Questions** → I ask clarifying questions
3. **Architecture** → I create the plan
4. **Validation** → You review and approve

**Result:** Plan with 100% clarity, no ambiguities

## Detailed Protocol

### Phase 1: Deep Discovery
**Goal:** Understand technical context completely

**Process:**
1. **Scan Project Structure**
   ```bash
   Glob: package.json, requirements.txt, Cargo.toml, go.mod
   Glob: README.md, *.md, docs/*
   Glob: src/**/*, lib/**/*, app/**/*
   ```

2. **Analyze Dependencies**
   ```bash
   Read: package.json
   Read: requirements.txt or pyproject.toml
   Read: Cargo.toml or go.mod
   ```

3. **Review Documentation**
   ```bash
   Read: README.md
   Read: ARCHITECTURE.md (if exists)
   Read: docs/* (if exists)
   ```

4. **Identify Patterns**
   ```bash
   Grep: "class \|function \|const "
   Grep: "import \|from "
   Grep: "test\|spec"
   ```

**Output:** Complete technical context

### Phase 2: The Question Burst
**Goal:** Eliminate all ambiguities

**Process:**
1. **Analyze Requirements**
   - Parse user requirements
   - Compare against codebase state
   - Identify ambiguities

2. **Present Clarification Menu**
   - Use `AskUserQuestion` tool
   - Present 3 options per ambiguity
   - Mark recommendation as [RECOMMENDED]
   - Wait for selection

**Example Question Burst:**
```
🔍 Clarification Needed: Tech Stack
You said "build a web app" but I found package.json with React.

[RECOMMENDED] React + TypeScript + Vite
  - Matches existing codebase
  - Modern, fast development
  - Strong TypeScript support

  Option B: Vue.js + JavaScript
  - Simpler learning curve
  - Less boilerplate

  Option C: Vanilla JavaScript
  - No dependencies
  - More manual work
```

**Wait** for user selection before proceeding.

### Phase 3: Architecture
**Goal:** Create plan with 100% clarity

**Process:**
1. **Synthesize Requirements**
   - User requirements + discovery findings
   - Clarified answers from questions
   - Technical constraints identified

2. **Create Plan Files**
   - Use `managing-project-plans` templates
   - Apply `architecting-project-plans` methodology
   - Generate BRIEF.md, ROADMAP.md

3. **STOP for Validation**
   - Present complete plan
   - Ask: "Does this plan capture your requirements correctly?"
   - Wait for approval

### Phase 4: Task Generation
**Goal:** Create detailed, actionable tasks

**Process:**
1. **Generate Phase Plans**
   - Create `phases/XX-name/XX-XX-PLAN.md` files
   - Each phase: 2-3 actionable tasks
   - Tasks are atomic and verifiable

2. **Validate Task Quality**
   - Each task has Scope, Action, Verify, Done
   - Success criteria are measurable
   - Dependencies are explicit

## Clarification Menu

### Common Question Categories

#### Tech Stack
**When:** User mentions technology without specificity
**Example:**
```
🔍 Clarification Needed: Frontend Framework
You mentioned "frontend" but didn't specify framework.

[RECOMMENDED] Continue with {existing_framework}
  - Matches existing codebase
  - Consistent architecture
  - Less complexity

  Option B: {alternative_framework}
  - Better for {specific_use_case}
  - Pros: {pros}
  - Cons: {cons}

  Option C: {third_option}
  - Best for {specific_use_case}
  - Pros: {pros}
  - Cons: {cons}
```

#### Architecture
**When:** Unclear about system design
**Example:**
```
🔍 Clarification Needed: System Architecture
You mentioned "API" but unclear about scope.

[RECOMMENDED] REST API with Express.js
  - Standard HTTP methods
  - JSON responses
  - Integrates with existing React frontend

  Option B: GraphQL API
  - Flexible queries
  - Strong typing
  - Better for complex data relationships

  Option C: Server-Side Rendering (SSR)
  - SEO-friendly
  - Faster initial load
  - Good for content-heavy sites
```

#### Database
**When:** Data storage requirements unclear
**Example:**
```
🔍 Clarification Needed: Database
You mentioned "store user data" but didn't specify database.

[RECOMMENDED] Continue with {existing_db}
  - Already configured
  - Matches existing patterns
  - Reduces complexity

  Option B: PostgreSQL
  - ACID compliant
  - Scalable
  - Good for relational data

  Option C: MongoDB
  - Flexible schema
  - Good for evolving requirements
  - Better for unstructured data
```

#### Authentication
**When:** Security requirements need clarification
**Example:**
```
🔍 Clarification Needed: Authentication Method
You mentioned "login" but didn't specify authentication.

[RECOMMENDED] Email/Password + JWT
  - Simple to implement
  - Industry standard
  - Works with existing user model

  Option B: OAuth (Google, GitHub)
  - No password management
  - Better UX
  - Requires OAuth setup

  Option C: Multi-Factor Authentication
  - More secure
  - Better for sensitive data
  - Additional complexity
```

#### Deployment
**When:** Deployment strategy unclear
**Example:**
```
🔍 Clarification Needed: Deployment Platform
You mentioned "deploy" but didn't specify platform.

[RECOMMENDED] Continue with {existing_platform}
  - Already configured
  - Matches current setup
  - Faster deployment

  Option B: Docker + Kubernetes
  - Highly scalable
  - Cloud-native
  - Better for microservices

  Option C: Serverless (Vercel/Netlify)
  - Pay-per-use
  - Auto-scaling
  - Good for static sites
```

### Question Writing Guidelines

**Structure:**
```markdown
🔍 Clarification Needed: {Category}
{description of ambiguity>

[RECOMMENDED] {Recommended Option}
  - {Reason 1}
  - {Reason 2}
  - {Reason 3}

  Option B: {Option B Name}
  - {Pros/cons}

  Option C: {Option C Name}
  - {Pros/cons}
```

**Best Practices:**
- ✓ Present 3 options maximum
- ✓ Mark recommendation as [RECOMMENDED]
- ✓ Explain rationale for recommendation
- ✓ Wait for user selection
- ✓ Don't proceed until all questions answered

## Examples

### Example 1: New React App
```bash
/sys-builder:create-plan-interactive "Build a task management app"
```
**Questions Asked:**
- Frontend: React + TypeScript or Vue?
- Backend: Node.js/Express or Python/Django?
- Database: PostgreSQL or MongoDB?
- Auth: Email/password or OAuth?

### Example 2: Adding to Existing Project
```bash
/sys-builder:create-plan-interactive "Add payment processing to Django app"
```
**Questions Asked:**
- Payment Provider: Stripe or PayPal?
- Integration: Separate service or in-app?
- Testing: Full E2E or unit tests only?

### Example 3: Complex Microservice
```bash
/sys-builder:create-plan-interactive "Build a real-time chat system"
```
**Questions Asked:**
- Protocol: WebSockets or Server-Sent Events?
- Message Broker: Redis or RabbitMQ?
- Scaling: Horizontal or Vertical?
- Storage: In-memory or Persistent?

## Reference

### File Structure Created
```
.cattoolkit/plan/{project-slug}/
├── BRIEF.md           # Clarified requirements
├── DISCOVERY.md       # Deep discovery findings
├── ROADMAP.md         # Phase overview
├── QUESTIONS.md        # Clarification Q&A
└── phases/
    ├── 01-foundation/
    │   └── 01-01-PLAN.md
    ├── 02-core/
    │   └── 02-01-PLAN.md
    └── 03-enhancement/
        └── 03-01-PLAN.md
```

### Skills Used
| Skill | Purpose | When |
|-------|---------|------|
| managing-project-plans | Templates, schemas | Plan creation |
| architecting-project-plans | Investigation, synthesis | Discovery phase |

### Question Categories Checklist
**Ask Questions For:**
- [ ] Technology stack choices
- [ ] Architecture patterns
- [ ] Database selection
- [ ] Authentication method
- [ ] Deployment platform
- [ ] Testing strategy
- [ ] Performance requirements
- [ ] Security requirements
- [ ] Scalability needs
- [ ] Integration points

**Don't Ask For:**
- Preferences already stated clearly
- Details derivable from context
- Questions with obvious answers
- Things that don't matter to success

### Validation Criteria
**Plan is Complete When:**
- [ ] All ambiguities resolved
- [ ] User approves BRIEF.md
- [ ] User approves ROADMAP.md
- [ ] Phase plans are detailed
- [ ] Success criteria are measurable

### Differences from create-plan
| Aspect | create-plan | create-plan-interactive |
|--------|-------------|------------------------|
| Discovery | Automated | Deep + Manual |
| Questions | None | Structured burst |
| Clarity | 80% | 100% |
| Speed | Faster | Slower (but thorough) |
| Use Case | Clear requirements | Ambiguous requirements |

### When to Use Which
**Use create-plan when:**
- Requirements are clear
- Time is limited
- Simple project
- Well-understood domain

**Use create-plan-interactive when:**
- Requirements are ambiguous
- Complex project
- Multiple stakeholders
- Unclear technical choices
- Need 100% clarity

### Error Handling
**If investigation fails:**
- Note limitations in discovery
- Ask more questions
- Proceed with best judgment

**If questions unclear:**
- Rephrase questions
- Provide examples
- Ask for clarification

**If user doesn't answer:**
- Mark assumptions in plan
- Proceed with recommendation
- Note assumptions in BRIEF.md

### Next Steps After Interactive Planning
**Execute Plan:**
```bash
/sys-builder:run-plan
```

**Refine Further:**
```bash
/sys-builder:manage-plan "add clarification to phase 2"
```

**View Clarifications:**
```bash
cat .cattoolkit/plan/{project-slug}/QUESTIONS.md
```
