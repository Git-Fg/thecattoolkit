/// THIS GUIDE IS NOT THERE TO BE USED DIRECTLY BY THE MARKETPLACE ; BUT CONTAINS RELEVANT INFO ON "HOW DOES THIS WORK" AS WE HAVE TO ADMIT USERS WILL HAVE THEIR RULES CONFIGURED ; THEY MAY HAVE SPECIFIC SYSTEM INSTRUCTIONS ... AND GLOBAL LOGIC MUST NEVER INTERFER WITH IT IN A BAD WAY ///


# Rules (Project Configuration)

Rules files are specialized configuration documents that provide persistent, project-specific guidance to AI systems. They transform AI from generic assistants into specialized team members aligned with specific projects and workflows.

## Quick Reference

### What Rules Files Are

Rules files:
- **Persist across sessions**: Apply consistently over time
- **Encode project context**: Capture local knowledge and conventions
- **Guide behavior proactively**: Prevent issues before they occur
- **Evolve through iteration**: Improve through real-world usage

### What Rules Files Are Not

- **Static documentation**: They're active configuration, not passive docs
- **Generic best practices**: They're project-specific and contextual
- **One-time setup**: They require ongoing refinement and evolution
- **Replacement for communication**: They supplement, not replace, clear requirements

### Core Philosophy

**The Power of Specificity**: AI systems thrive on concrete, actionable guidance. The more specific your rules, the better the outcomes.

Example:
- BAD "Use good naming conventions"
- GOOD "Use camelCase for functions and PascalCase for components"

---

## Division I: Foundations

### Taxonomy and Classification

#### By Scope

| Scope | Location | Purpose | Duration |
|-------|----------|---------|----------|
| **Global** | `~/.claude/rules/*.md` | Personal preferences and universal guidelines | Long-term, evolves slowly |
| **Project** | `.claude/rules/*.md` | Team-shared conventions and project-specific knowledge | Aligned with project lifecycle |
| **Session** | Runtime | Temporary, experimental rules | Short-term |
| **Plugin** | `plugins/*/rules/*.md` | Plugin-specific constraints | Plugin lifecycle |

#### By Function

| Type | Purpose | Examples |
|------|---------|----------|
| **Behavioral** | Define how AI should act and respond | Communication style, error handling, decision-making |
| **Structural** | Specify project organization and conventions | File naming, directory structure, module boundaries |
| **Operational** | Define executable commands and workflows | Build commands, testing procedures, deployment processes |
| **Safety** | Establish boundaries and restrictions | Forbidden actions, approval requirements, risk mitigation |

### The Ten Universal Principles

Based on analysis of successful rules files across multiple platforms and projects:

#### 1. Specificity Over Generality

**Core Idea**: Concrete, specific rules produce better outcomes than general guidelines.

**Application**:
- Instead of "use good naming conventions," specify "use camelCase for functions and PascalCase for components"
- Instead of "follow our style," provide exact linting rules and formatting commands
- Instead of "be careful with production code," list specific files and directories to avoid

#### 2. Context Over Instruction

**Core Idea**: Rules should encode context about your project, not just commands.

**Application**:
- Explain *why* certain approaches are preferred
- Provide background on architectural decisions
- Include historical context for legacy code
- Describe business logic and constraints

#### 3. Actionability Over Description

**Core Idea**: Rules should enable concrete actions, not just provide information.

**Application**:
- Include specific commands to run
- Provide exact file paths and locations
- Specify exact versions and dependencies
- Offer concrete examples of correct implementation

#### 4. Safety First

**Core Idea**: Establish clear boundaries and restrictions to prevent unintended actions.

**Application**:
- Define what AI can do without approval
- List forbidden actions and sensitive areas
- Require confirmation for high-risk operations
- Implement gradual permission escalation

#### 5. Iterative Evolution

**Core Idea**: Rules files improve through usage and should evolve continuously.

**Application**:
- Start with minimal core rules
- Add rules based on observed failures
- Regularly review and refine existing rules
- Remove rules that become outdated or ineffective

#### 6. Layered Specificity

**Core Idea**: Use hierarchical rule systems to balance general and specific guidance.

**Application**:
- Global rules for universal preferences
- Project rules for team conventions
- Subdirectory rules for specialized contexts
- Local rules for individual workflows

#### 7. Concrete Examples Over Abstract Rules

**Core Idea**: Real code examples are more valuable than written descriptions.

**Application**:
- Point to specific files demonstrating good patterns
- Include actual code snippets showing correct implementation
- Reference working examples of complex patterns
- Call out files to avoid and explain why

#### 8. Command-Centric Design

**Core Idea**: Make executable commands a first-class element of rules systems.

**Application**:
- Include exact commands with full flags and options
- Provide file-scoped commands for efficiency
- Specify when to use different commands
- Include validation and testing procedures

#### 9. Clear Boundaries and Permissions

**Core Idea**: Explicitly define what AI can and cannot do.

**Application**:
- Use three-tier permission system: Always/Ask First/Never
- Define specific files and directories to avoid
- Specify approval requirements for sensitive actions
- Document escalation procedures for uncertainty

#### 10. Team Alignment Through Rules

**Core Idea**: Rules files should encode team knowledge and align team practices.

**Application**:
- Commit shared rules to version control
- Use rules to onboard new team members
- Align rules with team workflows and tools
- Create consistency through shared conventions

---

## Division II: Core Components

### Essential Elements

#### 1. The Do's and Don'ts Foundation

Every effective rules file should begin with explicit do's and don'ts.

**Structure**:
```markdown
### Do
- [Specific positive action with exact details]
- [Another specific positive action]
- [Tool/version-specific requirement]

### Don't
- [Specific negative action to avoid]
- [Another specific negative action]
- [Tool/version restriction]
```

**Characteristics of Good Do's and Don'ts**:
- **Nitpicky specificity**: The more precise, the better
- **Version awareness**: Include exact versions and dependencies
- **Tool-specific guidance**: Reference specific tools and libraries
- **Pattern focus**: Emphasize recurring patterns over one-off issues

**Example**:
```markdown
### Do
- use MUI v3. make sure your code is v3 compatible
- use emotion `css={{}}` prop format
- use mobx for state management with `useLocalStore`
- default to small components. prefer focused modules over god components

### Don't
- do not hard code colors
- do not use `div`s if we have a component already
- do not add new heavy dependencies without approval
```

#### 2. Command Reference

Include specific, executable commands that AI can run to validate and build the project.

**Structure**:
```markdown
### Commands

# Type checking
npm run tsc --noEmit [path/to/file]

# Formatting
npm run prettier --write [path/to/file]

# Linting
npm run eslint --fix [path/to/file]

# Testing
npm run test [path/to/file.test]

# Building
npm run build

Note: [When to use each command]
```

**Best Practices**:
- **File-scoped commands**: Enable efficient validation of single files
- **Complete commands**: Include full commands with all flags
- **Usage guidance**: Explain when to use each command
- **Efficiency focus**: Prefer fast, scoped commands over slow, global ones

#### 3. Safety and Permissions

Define clear boundaries for AI actions using a three-tier permission system.

**Structure**:
```markdown
### Safety and Permissions

Allowed without prompt:
- [Specific low-risk actions]
- [Safe read operations]
- [Safe validation commands]

Ask first:
- [Moderate-risk actions]
- [Structural changes]
- [Dependency modifications]

Never:
- [High-risk actions]
- [Production modifications]
- [Sensitive data access]
```

**Permission Tiers**:

1. **Always Allowed** (Low Risk)
   - Read operations
   - Static analysis
   - File-scoped validation
   - Code formatting

2. **Ask First** (Moderate Risk)
   - File creation/modification
   - Dependency changes
   - Configuration updates
   - Build operations

3. **Never Allowed** (High Risk)
   - Production deployments
   - Secret access
   - Destructive operations
   - System-level changes

#### 4. Project Structure Guidance

Provide strategic pointers to help AI understand project organization.

**Structure**:
```markdown
### Project Structure
- [Directory description with purpose]
- [Key files and their purposes]
- [Architectural patterns to follow]
- [Legacy areas to avoid]
```

**Best Practices**:
- **Strategic pointers**: Guide AI to important files and directories
- **Purpose explanation**: Explain the "why" behind structure
- **Pattern reference**: Point to files demonstrating good patterns
- **Legacy warnings**: Identify areas to avoid or treat carefully

---

## Division III: Structure and Organization

### Hierarchical Organization

Rules files should be organized hierarchically to balance comprehensiveness with manageability.

**Global Level** (`~/.claude/rules/*.md`):
```markdown
# Global Developer Preferences

## General Rules
- [Universal preferences]
- [Personal coding standards]
- [Tool preferences]

## Code Quality
- [Quality standards]
- [Naming conventions]
- [Documentation requirements]

## Git Workflow
- [Commit conventions]
- [Branch strategies]
- [Review processes]
```

**Project Level** (`.claude/rules/*.md`):
```markdown
# [Project Name] Rules
[Project description]

## Tech Stack
- Framework: [specific versions]
- Language: [specific versions]
- Dependencies: [key dependencies]

## Project Structure
[Directory structure with descriptions]

## Commands
[Project-specific commands]

## Code Standards
[Project-specific standards]

## Safety
[Project-specific safety rules]
```

**Plugin Level** (`plugins/*/rules/*.md`):
```markdown
# [Plugin Name] Constraints

## Plugin-Specific Rules
- [Constraints for this plugin]
- [Required patterns]
- [Forbidden actions]
```

### Content Flow and Sequencing

Order content strategically to maximize effectiveness:

1. **Opening Summary**: Project name, description, tech stack
2. **Quick Reference**: Commands, file locations, key files
3. **Core Rules**: Do's, don'ts, safety, standards
4. **Detailed Guidance**: Examples, patterns, workflows
5. **Appendices**: Extended documentation, references

---

## Division IV: Content Design Patterns

### Pattern 1: Example-Driven

**Structure**:
```markdown
### [Topic] Examples

GOOD **Good Examples**
- [Reference to specific good file]: [Why it's good]
- [Another good example]: [What to learn]

BAD **Bad Examples**
- [Reference to specific bad file]: [Why it's problematic]
- [Another bad example]: [What to avoid]

**Learning**: [Key takeaway for AI to remember]
```

### Pattern 2: Command-First

**Structure**:
```markdown
### [Operation] Commands

# [Purpose]
[full command with all flags]

# [Alternative purpose]
[alternative command]

**When to use**: [Specific guidance]
**Validation**: [How to verify success]
```

### Pattern 3: Boundary-Definition

**Structure**:
```markdown
### [Topic] Boundaries

🟢 **Always Allowed**
- [Specific allowed actions]
- [Safe operations]

🟡 **Ask First**
- [Moderate-risk actions]
- [Situations requiring confirmation]

🔴 **Never Allowed**
- [Forbidden actions]
- [High-risk operations]

**Escalation Path**: [What to do when uncertain]
```

### Pattern 4: Pattern-Capture

**Structure**:
```markdown
### [Common Task] Pattern

**When**: [When to apply this pattern]
**Pattern**: [Generic pattern description]
**Example**: [Specific file demonstrating pattern]
**Pitfalls**: [Common mistakes to avoid]

**Code Template**:
```[language]
[Template code]
```
```

---

## Division V: Advanced Strategies

### Multi-Level Rule Architecture

Complex projects benefit from layered rules systems:

**Level 1: Global Rules** (`~/.claude/rules/*.md`)
- Personal preferences
- Universal coding standards
- Tool preferences
- Communication styles

**Level 2: Project Rules** (`.claude/rules/*.md`)
- Team-shared conventions
- Project-specific standards
- Architecture patterns
- Workflow processes

**Level 3: Plugin Rules** (`plugins/*/rules/*.md`)
- Plugin-specific constraints
- Required patterns
- Integration requirements

### Conflict Resolution

When rules conflict across levels, use clear resolution strategies:

**Priority Order**:
1. Plugin rules (highest priority - most specific)
2. Project rules
3. Global rules (lowest priority - most general)

**Resolution Strategies**:
- **Explicit Override**: Clearly mark conflicting rules
- **Scope Limitation**: Restrict rules to specific contexts
- **Temporal Hierarchy**: Use most specific and recent rules
- **Documentation**: Explain conflicts and resolutions

### Evolution Strategy

Rules should evolve systematically:

1. **Observation**: Identify issues or gaps
2. **Hypothesis**: Propose rule changes
3. **Experimentation**: Test in low-risk contexts
4. **Evaluation**: Assess effectiveness
5. **Integration**: Incorporate successful changes
6. **Documentation**: Record changes and rationale

---

## Division VI: Safety and Boundaries

### Risk Assessment Framework

Categorize actions by risk level to define appropriate safety measures:

**Low Risk** (Always Allowed):
- Read operations
- Static analysis
- Code formatting
- File-scoped validation

**Medium Risk** (Ask First):
- File creation/modification
- Dependency updates
- Configuration changes
- Build operations

**High Risk** (Never or Explicit Approval):
- Production deployments
- Secret access
- Destructive operations
- System modifications

### Permission Escalation

Define clear escalation paths for uncertain situations:

```markdown
### When Uncertain

1. **Ask Clarifying Questions**
   - Request specific requirements
   - Seek confirmation on approach
   - Identify missing context

2. **Propose Small Plans**
   - Break large tasks into smaller steps
   - Suggest incremental approaches
   - Offer alternative solutions

3. **Create Draft PRs**
   - Share work-in-progress
   - Request feedback before finalizing
   - Enable collaborative refinement

**Never**: Make large speculative changes without confirmation
```

---

## Division VII: Maintenance and Evolution

### The Living Document Model

Treat rules files as evolving systems:

**Continuous Improvement**:
- Monitor AI behavior and outcomes
- Identify patterns in failures or successes
- Update rules based on observations
- Validate changes through testing

**Change Management**:
- Track rule changes over time
- Maintain change history
- Communicate updates to team
- Measure impact of changes

### Refinement Process

Systematic approach to rule refinement:

1. **Collect Observations**
   - Monitor AI interactions
   - Track common mistakes
   - Identify gaps in guidance

2. **Analyze Patterns**
   - Categorize issues by type
   - Identify root causes
   - Assess rule effectiveness

3. **Propose Changes**
   - Design rule improvements
   - Consider trade-offs
   - Plan implementation

4. **Test Changes**
   - Apply to limited scope
   - Monitor results
   - Gather feedback

5. **Integrate Successes**
   - Roll out effective changes
   - Update documentation
   - Communicate improvements

### Version Control for Rules

Treat rules files like code:

- **Commit Changes**: Track all modifications
- **Branch Strategies**: Experiment safely
- **Code Reviews**: Evaluate rule changes
- **Documentation**: Explain rationale
- **Rollback**: Revert ineffective changes

---

## Quick Reference Checklist

### Rules File Design Checklist

**Before finalizing a rules file, verify:**

**Structure**
- [ ] Clear opening summary with project context
- [ ] Explicit do's and don'ts section
- [ ] Complete command reference
- [ ] Safety and permissions defined

**Content**
- [ ] Specific, actionable rules
- [ ] Concrete examples provided
- [ ] Context and rationale included
- [ ] File paths and locations specified

**Safety**
- [ ] Permission tiers clearly defined
- [ ] Escalation paths documented
- [ ] Risk assessment framework applied
- [ ] Forbidden actions listed

**Maintenance**
- [ ] Version controlled
- [ ] Change tracking enabled
- [ ] Review cycle established
- [ ] Team alignment verified

### Common Anti-Patterns

**BAD The Vague Rule**
- Problem: "Write clean code"
- Solution: "Use functional components with hooks"

**BAD The Missing Context**
- Problem: "Don't use X"
- Solution: "Don't use X because it causes Y issue. Use Z instead."

**BAD The Outdated Rule**
- Problem: Rules that no longer reflect current practices
- Solution: Regular review and update cycle

**BAD The Over-Specified Rule**
- Problem: Too many rules making it hard to navigate
- Solution: Hierarchical organization with clear scoping

**BAD The Contradictory Rule**
- Problem: Rules that conflict with each other
- Solution: Clear priority order and conflict resolution
