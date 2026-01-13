# The Universal Engineering Standard for Agent Skills

## Executive Summary

**Good Skills are concise, well-structured, and tested with real usage.**

This guide provides practical authoring decisions to help you write Skills that Claude can discover and use effectively.

### Core Principles

#### 1. Concise is Key

The context window is a shared resource. Your Skill shares the context window with:
- The system prompt
- Conversation history
- Other Skills' metadata
- The user's actual request

**Progressive Disclosure Architecture**: Skills use a 3-tier loading system:
- **Tier 1** (Metadata): Always loaded at startup (~100 tokens)
- **Tier 2** (Instructions): Loaded on activation (<500 lines)
- **Tier 3** (Resources): Loaded on-demand (zero context cost)

**The Delta Standard**: Only add context Claude doesn't already have.

Question every instruction:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

**Good example** (50 tokens):
```markdown
## Extract PDF text

Use pdfplumber:

```python
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

Don't explain what PDFs are or how libraries work.
```

**Bad example** (150 tokens):
```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common format that contains text, images, and other content. To extract text from a PDF, you'll need to use a library. There are many libraries available, but we recommend pdfplumber because it's easy to use...
```

The concise version assumes Claude's existing knowledge.

#### 2. Set Appropriate Degrees of Freedom

Match specificity to task fragility and variability.

**High Freedom** (text-based guidance):
- Multiple valid approaches
- Context-dependent decisions
- Heuristic principles guide approach

**Medium Freedom** (pseudocode/scripts with parameters):
- Preferred pattern exists
- Acceptable variation
- Configuration affects behavior

**Low Freedom** (specific scripts, minimal parameters):
- Operations are fragile
- Consistency is critical
- Exact sequence required

**The Narrow Bridge Analogy**:
- **Narrow bridge with cliffs**: One safe path. Use exact instructions (low freedom). Example: database migrations.
- **Open field**: Many valid paths. Give general direction (high freedom). Example: code reviews.

#### 3. Match Autonomy to Task Characteristics

Use the **Criticality + Variability** framework:

**High Criticality + Low Variability → Low Autonomy (Protocol)**
- Exact steps, no deviation
- Example: Security validations

**High Criticality + High Variability → Medium Autonomy (Guided)**
- Pattern-based with adaptation
- Example: Code reviews

**Low Criticality + Any Variability → High Autonomy (Heuristic)**
- Broad principles, maximum flexibility
- Example: Creative tasks

#### 4. Design for Discovery

Skills are **model-invoked**, not user-called. The description field is the agent's "SEO."

**Description Formula**: Capability + Trigger + Negative Constraint

**Example**:
```yaml
description: Extracts raw text and tabular data from .pdf files. Use when user mentions parsing, scraping, or converting PDF invoices. Do not use for PDF generation, editing, or image-to-PDF conversion.
```

**Optimization Rules**:
1. Use specific triggers: "parsing PDF invoices" > "working with PDFs"
2. Use gerunds: "parsing", "analyzing", "extracting"
3. Include context anchoring: specific file types, use cases
4. State clear exclusions: what NOT to use it for
5. Third-person voice only: "Extracts data..." never "I can help..."

#### 5. Architecture: Progressive Disclosure

**Filesystem-as-Context Model**: Skills are directory structures, not prompts.

**Hub-and-Spoke Structure**:
- SKILL.md is the central hub
- All references one level deep
- No daisy-chaining (A.md → B.md)

**Atomic Unit Principle**:
- One domain per Skill
- Users think of it as single operation
- Example: "Analyze PDF invoices" (one Skill), not "Process PDFs and generate reports" (two Skills)

---

## Division 1: Architectural Foundations

### 1.1 The 3-Tier Loading Model

Every Skill must respect three levels:

**Level 1: Metadata (Discovery)**
- YAML frontmatter (`name`, `description`)
- Always loaded at startup
- Ultra-lightweight (~100 tokens)
- Agent's "SEO" for relevance detection

**Level 2: Instructions (Logic)**
- Main body of SKILL.md
- Loaded on activation
- <500 lines recommended
- High-level router/onboarding guide

**Level 3: Resources (Payload)**
- Files in `references/`, `scripts/`, `assets/`
- Zero context cost until accessed
- Unlimited potential knowledge
- On-demand loading via Read/Execute

### 1.2 Skills vs Other Customization Options

**Skills**: Model-invoked expertise
- Autonomous discovery
- Domain knowledge
- Complex workflows

**Slash Commands**: User-invoked utilities
- Explicit activation
- Session control
- Quick actions

**Subagents**: Isolated execution
- Parallel processing
- Context isolation
- Specialized tools

**MCP Servers**: External capabilities
- Tool invocation
- System integration
- API connections

### 1.3 Skill Scope Matrix

**Criticality**: Cost of incorrect execution
- High: Migrations, security, compliance
- Medium: Reviews, analysis, generation
- Low: Brainstorming, creative tasks

**Variability**: Context change between executions
- Low: Standardized workflows
- Medium: Pattern-based tasks
- High: Creative/context-specific

**Autonomy**: Flexibility to grant
- Low (Protocol): Exact steps
- Medium (Guided): Patterns + adaptation
- High (Heuristic): Broad principles

**Domain Boundary Test**: Users think of it as single operation.

---

## Division 2: Metadata & Discovery

### 2.1 Complete YAML Frontmatter Specification

#### Required Fields

**`name`** (Max 64 chars)
- Lowercase + hyphens only
- No consecutive hyphens
- No start/end hyphens
- Matches directory name

**`description`** (Max 1024 chars)
- Capability + Trigger + Negative Constraint
- Specific keywords for matching
- Third-person voice only

#### Optional Fields

**`allowed-tools`**: Tool access restriction
**`user-invocable`**: Slash menu visibility (default: true)
**`license`**: Short format recommended
**`compatibility`**: Environment requirements (max 500 chars)
**`metadata`**: Arbitrary key-value pairs

### 2.2 Trigger Optimization

**Formula**: What + When + What NOT

**Good**: "Extracts text from PDFs when user mentions parsing invoices. Do not use for PDF creation."

**Bad**: "Helps with documents."

**Rules**:
1. Specific over generic
2. Action-oriented language
3. Context anchoring
4. Clear exclusions
5. Third-person only

---

## Division 3: Instruction Engineering

### 3.1 The Delta Standard

Only provide context Claude cannot infer.

**Negative**: Explaining what PDFs are or how `import` works
**Positive**: Specific column mappings for proprietary formats

### 3.2 Autonomy Levels

**Protocol (Low Freedom)**:
```
CRITICAL: Execute ONLY scripts/migrate.py
Do not modify flags
If fails with code 127, STOP
```

**Guided (Medium Freedom)**:
```
Prioritize maintainability over cleverness
Follow criteria: 1) Readability, 2) Performance, 3) Security
```

**Heuristic (High Freedom)**:
```
Apply your expertise to identify important issues
Use judgment to prioritize findings
```

**Decision Rules**:
- High error cost → Protocol/Guided
- High context variation → Guided/Heuristic
- Well-defined approach → Protocol
- Requires judgment → Heuristic

### 3.3 Conditional Workflow

Use explicit branching to prevent mode confusion:

```markdown
## Modification Workflow
1. Determine task:
   - **New File?** → Follow [Creation Guide](references/creation.md)
   - **Update File?** → Follow [Update Guide](references/update.md)
```

---

## Division 4: Resource Management

### 4.1 Reference Structuring

**TOC Requirement**: Files >100 lines need table of contents

**Organization Principles**:
- Functional domains over feature organization
- Minimize cross-references
- Self-contained files

### 4.2 Zero-Context Pattern

**Loading Strategy**:
1. Zero-cost awareness (agent knows resources exist)
2. On-demand loading (specific resources only)
3. Selective consumption (minimal relevant portions)

**Implementation**:
- Large datasets: Store in resources/, load subsets
- API docs: Complete specs available, read relevant sections
- Code examples: Bundle extensively, reference specifically

---

## Division 5: Skills-Subagent Interaction

### 5.1 Built-in Subagent Types

**Explore**: Fast, read-only, file discovery
**Plan**: Research agent, read-only, inheritance model
**General-purpose**: Complex tasks, all tools, inheritance

### 5.2 Skills-Subagent Relationship

**Skills**: Add knowledge to current conversation
**Subagents**: Run in separate context with own tools

**Key Principles**:
- Skills provide guidance/standards
- Subagents provide isolation/different tools
- Subagents don't inherit Skills
- Must explicitly inject via `skills` field

---

## Division 6: Workflow & State Management

### 6.1 State Anchoring

**The Ephemeral Context Problem**: Context windows are temporary.

**State Anchoring Strategy**:
```markdown
# State
- [x] Step 1: Backup
- [ ] Step 2: Transform
**Last Checkpoint:** SUCCESS
```

**Requirements**:
1. Atomic checkpoints
2. Idempotent operations
3. Progress visibility
4. Failure isolation

### 6.2 Pipeline Sequencing

**Dependency Graph Principle**:
```markdown
# Sequence
1. **Analyze**: Run xlsx tool, verify file exists
2. **Present**: Run pptx tool, charts MUST match Step 1 data
```

**Design Rules**:
- Unidirectional dependencies
- Parallel execution for independent steps
- Define data contracts
- Stop on errors

### 6.3 Validation-First Architecture

**Three-Phase Validation**:
1. Plan: Verify plan is well-formed
2. Pre-execution: Check prerequisites
3. Post-execution: Verify outputs

**Example**:
```markdown
## Document Processing Workflow
1. **Plan**: Create changes.json
2. **Validate**: Run scripts/validate_changes.py
3. **Execute**: Apply changes if validation passes
4. **Verify**: Run scripts/verify_output.py
```

**Use for**:
- Batch operations
- Destructive operations
- Complex workflows
- High-stakes tasks

---

## Division 7: Universal Skill Archetypes

### 7.1 The Four Archetypes

#### Procedural Skill
- **Purpose**: Deterministic, repeatable processes
- **Pattern**: Exact steps, validation gates, idempotent operations
- **Examples**: Migrations, security scans, compliance checks

#### Advisory Skill
- **Purpose**: Provide expertise and recommendations
- **Pattern**: Heuristic principles, contextual adaptation, domain knowledge
- **Examples**: Code reviews, architectural guidance, best practices

#### Generator Skill
- **Purpose**: Create structured outputs from inputs
- **Pattern**: Template-driven, validation-enhanced, iterative refinement
- **Examples**: Document generation, test creation, report formatting

#### Orchestrator Skill
- **Purpose**: Coordinate multiple capabilities and workflows
- **Pattern**: Explicit dependencies, pipeline sequencing, state management
- **Examples**: Multi-step analysis, compound workflows, cross-domain tasks

### 7.2 Anti-Patterns

**Mega-Skill Anti-Pattern**:
- Problem: Multiple unrelated domains
- Failure: Poor activation, context bloat, inconsistency
- Solution: Atomic boundaries + pipeline orchestration

**Vague Trigger Anti-Pattern**:
- Problem: Generic descriptions
- Failure: Unreliable activation, false positives
- Solution: Specific triggers + negative constraints

**Instruction Bloat Anti-Pattern**:
- Problem: Explaining known concepts
- Failure: Context overflow, reduced activation
- Solution: Delta standard + progressive disclosure

**Validation Anti-Pattern**:
- Problem: No upfront completeness checks
- Failure: Cascading errors, unrecoverable failures
- Solution: Validation-first + machine-verifiable checks

---

## Division 8: Testing & Validation

### 8.1 Model-Specific Testing

**Test Across Model Types**:
- **Haiku** (fast, economical): Does the Skill provide enough guidance?
- **Sonnet** (balanced): Is the Skill clear and efficient?
- **Opus** (powerful reasoning): Does the Skill avoid over-explaining?

**Cross-Model Compatibility**:
What works for Opus might need more detail for Haiku. Aim for instructions that work well across all models.

### 8.2 Success Metrics

**Activation Rate**: Percentage of appropriate activations
**Success Rate**: Percentage of successful task completions
**Context Efficiency**: Information density vs. capability ratio
**User Satisfaction**: Qualitative feedback

### 8.3 Validation Framework

**Theoretical Validation Process**:
1. Principle Identification: What universal truth does this demonstrate?
2. Pattern Recognition: How does this align with known archetypes?
3. Anti-Pattern Check: Does this avoid known failure modes?
4. Theoretical Grounding: What scientific principles support this?
5. Cross-Platform Validation: Does this hold across implementations?

---

## Division 9: Security & Safety

### 9.1 Permission Management

**Least Privilege Principle**:
- Restrict tools to minimum required
- Use allowlists, not denylists
- Validate before execution

### 9.2 Hook System Patterns

**Common Hook Applications**:
- Security: Block dangerous operations
- Logging: Create audit trails
- Authorization: Role-based access
- Tool Interception: Redirect operations

### 9.3 Validation-First Safety

**Pre-Execution Validation**:
- Validate inputs before processing
- Check permissions before execution
- Verify environment readiness

**Machine-Verifiable Checks**:
- Scripts provide objective validation
- Clear error messages
- Reversible planning

---

## Division 10: Quality Assurance

### 10.1 The 12-Point QA Checklist

1. [ ] Description contains 3rd person Capability + Trigger?
2. [ ] Negative constraints defined?
3. [ ] Name excludes "anthropic" and "claude"?
4. [ ] References are 1-level deep (Hub-and-Spoke)?
5. [ ] TOC present for long reference files?
6. [ ] `user-invocable` set for utility skills?
7. [ ] `_state.md` artifact mandated for persistence?
8. [ ] Scripts return JSON-over-Stdout?
9. [ ] All file outputs directed to CWD/Tmp (not Skill dir)?
10. [ ] `allowed-tools` set to minimum required set?
11. [ ] Checksums included for critical assets?
12. [ ] Sub-agent forks specify an agent type?

### 10.2 Theoretical Validation Checklist

**Universal Success Patterns**:
- [ ] Domain Encapsulation: Clear, single mental model?
- [ ] Autonomy Alignment: Level matches task characteristics?
- [ ] Trigger Optimization: Specific trigger phrases included?
- [ ] Context Efficiency: 3-tier model minimizes overhead?
- [ ] Validation Strategy: Validation loops for high-risk ops?
- [ ] Resource Organization: Domain-based organization?
- [ ] Error Prevention: Destructive ops protected by validation?

---

## Division 11: Advanced Patterns

### 11.1 Progressive Disclosure Implementation

**Content Type Separation**:
- **Instructions**: Flexible markdown guidance
- **Code**: Executable scripts for deterministic operations
- **Resources**: Reference materials for factual lookup

**File Organization**:
```
skill-name/
├── SKILL.md (main instructions)
├── references/ (detailed documentation)
├── examples/ (ready-to-use code)
├── scripts/ (utility executables)
└── assets/ (templates, images)
```

### 11.2 Context Efficiency Theory

**Information Density Optimization**:
- Discovery phase: ~100 tokens for semantic matching
- Activation phase: <500 lines for procedural knowledge
- Execution phase: Unlimited capability without context penalty

**Context Window Economics**:
Challenge each instruction:
- Does Claude need this explanation?
- Can Claude infer this?
- Does this justify its token cost?

### 11.3 Cross-Platform Success Factors

Skills that succeed across platforms consistently demonstrate:

1. **Semantic Precision**: Specific, action-oriented trigger language
2. **Context Efficiency**: 3-tier loading minimizes overhead
3. **Validation Emphasis**: Multiple layers prevent cascades
4. **Domain Focus**: Narrow, deep expertise
5. **State Management**: Persistent artifacts enable recovery
6. **Autonomy Alignment**: Instruction style matches task
7. **Resource Organization**: Domain-based enables selective loading

---

## Conclusion

Effective Skills follow universal principles:

1. **Concise**: Respect the context window
2. **Structured**: Use progressive disclosure
3. **Tested**: Validate across models and use cases
4. **Focused**: One domain, clear boundaries
5. **Discoverable**: Optimized for model invocation

The framework-agnostic approach ensures Skills work across any agent platform while maintaining consistent quality and effectiveness.
