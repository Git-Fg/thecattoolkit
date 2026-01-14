# Skills (Procedural Memory)

Skills are libraries of know-how activated on demand. They allow Claude to become a domain expert through a **3-tier progressive disclosure architecture**.

## 1. The 3-Tier Loading Model

Skills use a filesystem-based architecture with three distinct loading levels:

### Level 1: Metadata (Discovery)
- **Location:** YAML frontmatter (`name`, `description`)
- **Cost:** Always loaded at startup (~100 tokens)
- **Purpose:** Agent's "SEO" for relevance detection
- **Optimization:** Use `disable-model-invocation: true` to shrink catalog
- **Content:** Name + Description only (max 1024 chars)

### Level 2: Instructions (Logic)
- **Location:** Main body of `SKILL.md`
- **Cost:** Loaded on activation
- **Limit:** <500 lines recommended
- **Purpose:** High-level router/onboarding guide
- **Structure:** Progressive disclosure - high-level overview first

### Level 3: Resources (Payload)
- **Location:** Files in `references/`, `scripts/`, `assets/`
- **Cost:** Zero context cost until accessed
- **Purpose:** Unlimited knowledge without token penalty
- **Pattern:** On-demand loading via explicit references
- **Organization:** Hub-and-spoke model (no nesting)

**Context Window Economics:**
- Tier 1: ~100 tokens (always in memory)
- Tier 2: ~500-2000 tokens (loaded when activated)
- Tier 3: Unlimited (loaded on-demand only)

**Progressive Disclosure Benefits:**
1. **Ultra-fast startup**: Only 100 tokens per skill loaded
2. **Efficient activation**: Detailed instructions only when needed
3. **Unlimited depth**: Zero-penalty access to comprehensive resources

### File Organization
```
skill-name/
├── SKILL.md (main instructions)
├── references/ (detailed documentation)
├── examples/ (ready-to-use code)
├── scripts/ (utility executables)
└── assets/ (templates, images)
```

## 1.5 Skills vs Other Customization Options

**Skills: Model-invoked expertise**
- Autonomous discovery
- Domain knowledge
- Complex workflows
- Used when: Claude needs to become an expert

**Slash Commands: User-invoked utilities**
- Explicit activation via `/`
- Session control
- Quick actions
- Used when: User wants direct control

**Subagents: Isolated execution**
- Parallel processing
- Context isolation
- Specialized tools
- Used when: Heavy processing or isolation needed

**MCP Servers: External capabilities**
- Tool invocation
- System integration
- API connections
- Used when: Need external services

**Decision Matrix:**

| Need | Use |
|:---|:---|
| Single capability, model-discovered | **SKILL** |
| Multi-skill orchestration, user-controlled | **COMMAND** |
| User interaction required | **COMMAND** |
| Isolation (>10 files) | **SKILL (context: fork)** |
| Runtime permission/tool scoping | **AGENT** |

## 1.6 Protocol-Based Skills (2026 Standard)

### The 2026 Philosophy Shift

**Protocol-Based (2026 Standard)**: Direct procedures without role-playing
- Structure: "Follow this X-step process"
- Focus: Actions, validation criteria, output formats
- Example: "Extract PDF text using pdfplumber. First open file, then extract text."

**Persona-Based (Deprecated)**: Narrative frame that wastes tokens
- Structure: "You are an expert who..."
- Focus: Role, motivation, background
- Example: "You are a PDF parsing specialist with 10 years of experience..."

**Why Protocol Wins:**
- **Token efficiency**: 40-60% fewer tokens for same capability
- **Clarity**: Direct instructions vs. implied meaning through role
- **Maintainability**: Easier to update procedures vs. rewrite narratives
- **Composability**: Protocol A + Protocol B = workflow (personas don't compose)

### Protocol Structure Examples

**Example 1: Code Review Protocol**
```markdown
## Code Review Protocol

### Phase 1: Analysis
1. **Identify scope**: Files changed, lines affected
2. **Categorize changes**: Bug fix, feature, refactor, test
3. **Check patterns**: Look for anti-patterns in changed code

### Phase 2: Validation
1. **Security check**: OWASP Top 10 vulnerabilities
2. **Performance check**: N+1 queries, unnecessary loops
3. **Style check**: ESLint/Prettier compliance

### Output Format
```markdown
**Severity**: [Critical/High/Medium/Low]
**File**: `path/to/file`
**Line**: [number]
**Issue**: [description]
**Fix**: [specific remediation]
```
```

**Example 2: Data Processing Protocol**
```markdown
## Data Processing Protocol

### Step 1: Input Validation
- Verify file exists and is readable
- Check file format matches expected type
- Validate required columns/fields present

### Step 2: Transformation
- Apply business rules in sequence
- Handle edge cases with defaults
- Log transformations for audit trail

### Step 3: Output Verification
- Validate output schema
- Check record count matches expected
- Run data quality checks

### Error Handling
- Invalid input: Return specific error message
- Transform failure: Log and skip record
- Output error: Rollback and report
```

### Persona Structure (Deprecated) - DO NOT USE

**Example of Deprecated Style:**
```markdown
## DO NOT USE THIS PATTERN

### Persona
You are a Senior Code Reviewer with 15 years of experience in software engineering. You have a deep understanding of security vulnerabilities, performance optimization, and best practices...

### Your Approach
When reviewing code, you always:
- Think like a security expert
- Consider performance implications
- Apply industry best standards
```

**Why This Fails:**
- 150+ tokens of setup before any actual instruction
- Claude must infer procedures from vague "expert" description
- Difficult to update (need to maintain character consistency)
- Composes poorly (what happens when "experts disagree"?)

### Migration: Persona → Protocol

**Before (Persona - Deprecated):**
```markdown
## Persona
You are a database migration specialist with expertise in safe schema changes.

## Responsibilities
- Plan migrations carefully
- Always create backups
- Test migrations thoroughly
```

**After (Protocol - 2026 Standard):
```markdown
## Migration Protocol

### Phase 1: Planning
1. **Analyze changes**: Columns added/removed, indexes modified
2. **Create rollback plan**: SQL to revert changes
3. **Estimate duration**: Table size, index rebuild time

### Phase 2: Execution
1. **Create backup**: `pg_dump table_name > backup.sql`
2. **Run migration in transaction**:BEGIN; [migration SQL]; COMMIT;
3. **Verify**: Check row counts, run validation queries

### Phase 3: Rollback (if needed)
1. **Stop application**: Prevent new writes
2. **Restore backup**: `psql < backup.sql`
3. **Verify**: Data integrity check
```

### When Are Personas Acceptable?

**GOOD Acceptable Use Cases:**
- **Agent Configuration** (`agents/*.md`): Minimal setup for tool scoping
  ```yaml
  ---
  name: code-reviewer
  tools: [Read, Grep, Edit]
  ---
  # Code Reviewer Agent

  ## Purpose
  Configuration-only agent for scoped code review operations.
  ```
- **Human-Facing Documentation**: README files, tutorials (not for AI consumption)

**BAD Unacceptable Use Cases:**
- **SKILL.md files**: Use protocol format instead
- **Instructions meant for AI model**: Direct procedures preferred
- **Multi-step workflows**: Protocol structure composes better

### Quick Reference: Protocol vs Persona

| Aspect | Protocol (2026) | Persona (Deprecated) |
|:-------|:----------------|:---------------------|
| **Structure** | "Do X, then Y" | "You are a..." |
| **Token Cost** | 40-60% lower | High (narrative overhead) |
| **Maintainability** | Easy (direct edits) | Hard (character consistency) |
| **Composability** | Excellent (chaining) | Poor (conflicting roles) |
| **Validation** | Clear success criteria | Ambiguous ("expert judgment") |
| **Use in** | Skills, Commands | Agents (minimal), Docs |

**Remember**: 95% of the time, use Protocol-based skills. Only use persona language when writing for human readers, not for AI model consumption.

## 1.7 Skill Scope Matrix

**Criticality**: Cost of incorrect execution
- **High**: Migrations, security, compliance
- **Medium**: Reviews, analysis, generation
- **Low**: Brainstorming, creative tasks

**Variability**: Context change between executions
- **Low**: Standardized workflows
- **Medium**: Pattern-based tasks
- **High**: Creative/context-specific

**Autonomy**: Flexibility to grant
- **Low (Protocol)**: Exact steps
- **Medium (Guided)**: Patterns + adaptation
- **High (Heuristic)**: Broad principles

**Domain Boundary Test**: Users think of it as single operation.

## 2. The Delta Standard

Only add context Claude doesn't already have.

**Question every instruction:**
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

**Good Example** (50 tokens):
```markdown
## Extract PDF text

Use pdfplumber:

```python
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

Don't explain what PDFs are or how libraries work.
```

**Bad Example** (150 tokens):
```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common format that contains text, images, and other content. To extract text from a PDF, you'll need to use a library. There are many libraries available, but we recommend pdfplumber because it's easy to use...
```

**Why the Delta Standard Matters:**

The context window is a shared resource:
- System prompt (~10,000 tokens)
- Conversation history (~100,000 tokens)
- Other Skills' metadata (~N × 100 tokens)
- User's actual request (~5,000 tokens)

**Cost-Benefit Analysis:**
Every instruction you add displaces something else. Optimize for:
1. **Specific knowledge**: What Claude cannot infer
2. **Domain expertise**: Proprietary formats, internal workflows
3. **Edge cases**: Uncommon scenarios, error conditions

**What to Include:**
- ✓ Specific column mappings for proprietary formats
- ✓ Exact API endpoints or file paths
- ✓ Validation rules for critical operations
- ✓ Error handling for domain-specific issues

**What to Exclude:**
- ✗ General programming concepts
- ✗ How to use standard libraries
- ✗ Well-documented public APIs
- ✗ Obvious best practices

**The "Assumption Test":**
If you can reasonably assume Claude knows it from training, don't include it. If it's specific to your domain, do include it.

## 3. Autonomy Levels

Match specificity to task fragility and variability using the **Criticality + Variability Framework**:

### Protocol (Low Freedom)
Exact steps, no deviation. Use for:
- **High Criticality + Low Variability** operations
- Database migrations
- Security validations
- Compliance checks

**The Narrow Bridge Analogy**: One safe path through dangerous terrain.

**Example:**
```markdown
CRITICAL: Execute ONLY scripts/migrate.py
Do not modify flags
If fails with code 127, STOP
```

**When to Use:**
- Operation cost of error is high
- Standardized workflow exists
- Consistency is critical
- Exact sequence required

### Guided (Medium Freedom)
Pattern-based with adaptation. Use for:
- **High Criticality + High Variability** operations
- Code reviews
- Architectural guidance
- Analysis tasks

**The Scenic Route Analogy**: General direction provided, multiple valid paths.

**Example:**
```
Prioritize maintainability over cleverness
Follow criteria: 1) Readability, 2) Performance, 3) Security
```

**When to Use:**
- Pattern recognition needed
- Context-dependent decisions
- Expert judgment required
- Variation is expected

### Heuristic (High Freedom)
Broad principles, maximum flexibility. Use for:
- **Low Criticality + Any Variability** operations
- Creative tasks
- Brainstorming
- Innovation

**The Open Field Analogy**: Many valid paths, general guidance only.

**Example:**
```
Apply your expertise to identify important issues
Use judgment to prioritize findings
```

**When to Use:**
- Cost of error is low
- Creative solutions needed
- High context variation
- Innovation encouraged

**Decision Rules:**
- **High error cost** → Protocol/Guided
- **High context variation** → Guided/Heuristic
- **Well-defined approach** → Protocol
- **Requires judgment** → Heuristic

**The Autonomy Spectrum:**
```
Protocol ←─────────────→ Guided ←─────────────→ Heuristic
   ↓                      ↓                      ↓
"Execute exactly       "Follow patterns       "Use principles
 what I say"          and adapt"            and decide"
```

## 4. The Four Universal Archetypes

### 1. Procedural Skill
**Purpose:** Deterministic, repeatable processes
- **Pattern:** Exact steps, validation gates, idempotent operations
- **Examples:** Migrations, security scans, compliance checks
- **Key Characteristics:**
  - Exact sequence of operations
  - Machine-verifiable success criteria
  - Idempotent (can run multiple times safely)
  - Low variance in execution

### 2. Advisory Skill
**Purpose:** Provide expertise and recommendations
- **Pattern:** Heuristic principles, contextual adaptation, domain knowledge
- **Examples:** Code reviews, architectural guidance, best practices
- **Key Characteristics:**
  - Domain expertise applied to context
  - Flexible adaptation to variations
  - Human judgment integration
  - Higher variance in approaches

### 3. Generator Skill
**Purpose:** Create structured outputs from inputs
- **Pattern:** Template-driven, validation-enhanced, iterative refinement
- **Examples:** Document generation, test creation, report formatting
- **Key Characteristics:**
  - Input → Output transformation
  - Template-based consistency
  - Validation checkpoints
  - Iterative improvement loops

### 4. Orchestrator Skill
**Purpose:** Coordinate multiple capabilities and workflows
- **Pattern:** Explicit dependencies, pipeline sequencing, state management
- **Examples:** Multi-step analysis, compound workflows, cross-domain tasks
- **Key Characteristics:**
  - Multi-step workflows
  - Dependency management
  - State persistence
  - Cross-domain coordination

### 4.1 Common Anti-Patterns

#### The Mega-Skill Anti-Pattern
**Problem:** Multiple unrelated domains in one skill
```markdown
BAD: "PDF processing and report generation and data visualization"
```

**Why It Fails:**
- Poor activation (unclear purpose)
- Context bloat (everything loaded)
- Inconsistent behavior
- Hard to maintain

**Solution:** Atomic boundaries + pipeline orchestration
```markdown
GOOD: "Parse PDF invoices" (Skill 1) → "Generate financial reports" (Skill 2)
```

#### The Vague Trigger Anti-Pattern
**Problem:** Generic descriptions
```yaml
BAD: description: "Helps with documents"
```

**Why It Fails:**
- Unreliable activation
- False positives
- Poor user experience

**Solution:** Specific triggers + negative constraints
```yaml
GOOD: description: "Extracts data from PDF invoices. Use when parsing invoice documents. Do not use for PDF creation or editing."
```

#### The Instruction Bloat Anti-Pattern
**Problem:** Explaining known concepts
```markdown
BAD: "To extract text, you first open the file using the pdfplumber library..."
```

**Why It Fails:**
- Context overflow
- Reduced activation
- Token waste

**Solution:** Delta standard + progressive disclosure
```markdown
GOOD: "Use pdfplumber.open(file).pages[0].extract_text()"
```

#### The Validation Anti-Pattern
**Problem:** No upfront completeness checks
```markdown
BAD: "Just execute the migration and hope it works"
```

**Why It Fails:**
- Cascading errors
- Unrecoverable failures
- Data corruption

**Solution:** Validation-first + machine-verifiable checks
```markdown
GOOD:
1. Validate: Check schema compatibility
2. Backup: Create rollback point
3. Execute: Run migration with validation
4. Verify: Confirm data integrity
```

## 4.2 Isolation Strategies (Fork vs Agents)

### WARNING The Subagent Crisis (2026)

**CRITICAL WARNING:** Subagents are almost always a mistake for pure isolation.

**The Cost Reality:**
- **Startup Cost:** ~20,000-25,000 tokens (System prompt + CLAUDE.md + Context)
- **Hidden Cost:** Consumes 1 "Prompt" quota (Z.AI/Subscription models), unlike tool calls.
- **Latency:** Full re-initialization of the environment.

### 1. Context Fork (`context: fork`)
**The Standard for Isolation.**
- **Mechanism:** Runs a Skill in a temporary, isolated process.
- **Cost:** ~3× inline token cost (significantly cheaper than subagent).
- **Use Case:** Heavy file operations, parallel processing, keeping main context clean.
- **Configuration:**
  ```yaml
  context: fork
  agent: <optional-custom-agent>
  ```

### 2. Subagents (Legacy/Specialized)
**Use ONLY when:**
- You need a persistent "Persona" or specific toolset (Agent configuration).
- The task requires a fundamentally different "Brain" (System Prompt).

**Skills-Subagent Relationship:**
- Subagents DO NOT inherit Skills automatically.
- Must explicitly inject via `skills: []` field.

**Example:**
```markdown
# In subagent definition
skills: [analyzer, builder, tester]  # Explicit injection
```

### When to Use Subagents
**Use Subagents When:**
- Need context isolation (protecting main conversation)
- Parallel processing required
- Heavy processing (>10 files)
- Need different tool access than main agent
- Long-running operations

**Use Skills When:**
- Adding domain expertise
- Providing guidance/standards
- Single-step operations
- Shared context acceptable

## 5. Configuration & Isolation



### Frontmatter Options

**Required Fields:**
- **`name`**: Regex `^[a-z][a-z0-9-]{2,49}$` (lowercase, hyphens, 3-50 chars)
- **`description`**: Max 1024 chars, 3rd person only

**Optional Fields:**
- **`allowed-tools: [Read]`**: Sandboxes the Skill (read-only)
- **`user-invocable: false`**: Hides from user menu (internal usage)
- **`disable-model-invocation: true`**: Removes from model catalog, prevents auto-selection
- **`license`**: Short format recommended
- **`compatibility`**: Environment requirements (max 500 chars)
- **`metadata`**: Arbitrary key-value pairs

### Permission Management

**The Least Privilege Principle:**
```markdown
# Good: Minimal tool access
allowed-tools: [Read, Bash]

# Bad: Unrestricted access
# (omitted allowed-tools = full access)
```

**Permission Cascade:**
```
Main Agent → Subagent (override) → Skill (temporary)
```

**Security Model Comparison:**

| Aspect | Skills (`allowed-tools`) | Agents (`tools`) |
|:-------|:-------------------------|:-----------------|
| **Purpose** | Temporary restriction | Persistent allowlist |
| **If omitted** | No restriction | **Inherits ALL tools** (security risk) |
| **Security model** | Least privilege during task | Least privilege by default |

**Common Permission Sets:**

```yaml
# Read-only analysis
allowed-tools: [Read, Grep, Glob]

# File operations
allowed-tools: [Read, Write, Bash]

# Full access (use sparingly)
allowed-tools: [Read, Write, Bash, Edit, Glob, Grep, Skill, WebFetch]
```

### Context Forking
- **Purpose:** Protect main context from massive logs or file reads
- **Usage:** Define in agents/ with explicit skill injection
- **Rule:** Sub-agents do not inherit skills automatically
- **Cost:** ~20k+ tokens (avoid unless necessary)

**When to Use:**
- Massive file operations (>100 files)
- Long-running processes
- Need separate tool access
- Protect main context from noise

**When Not to Use:**
- Simple operations (<10 files)
- Need shared context
- Available in current context

## 5.1 Testing & Validation

### Model-Specific Testing

**Test Across Model Types:**

**Haiku** (fast, economical)
- Question: Does the Skill provide enough guidance?
- Expectation: Clear, concise instructions
- Common issue: Too little context

**Sonnet** (balanced)
- Question: Is the Skill clear and efficient?
- Expectation: Good balance of detail and brevity
- Common issue: Redundant information

**Opus** (powerful reasoning)
- Question: Does the Skill avoid over-explaining?
- Expectation: Trust model's reasoning ability
- Common issue: Too much hand-holding

**Cross-Model Compatibility:**
What works for Opus might need more detail for Haiku. Aim for instructions that work well across all models.

### Success Metrics

**Activation Rate**: Percentage of appropriate activations
- Target: >80% for well-designed skills
- Measure: Count relevant activations vs. total invocations

**Success Rate**: Percentage of successful task completions
- Target: >90% for mature skills
- Measure: Completed tasks vs. attempted tasks

**Context Efficiency**: Information density vs. capability ratio
- Target: Minimal tokens for maximum capability
- Measure: Tokens used / tasks completed

**User Satisfaction**: Qualitative feedback
- Target: Positive user reports
- Measure: User feedback, adoption rate

### Validation Framework

**Theoretical Validation Process:**

1. **Principle Identification**: What universal truth does this demonstrate?
   - Is this based on established engineering principles?
   - Does it align with known best practices?

2. **Pattern Recognition**: How does this align with known archetypes?
   - Procedural, Advisory, Generator, or Orchestrator?
   - Protocol, Guided, or Heuristic autonomy?

3. **Anti-Pattern Check**: Does this avoid known failure modes?
   - Mega-skill anti-pattern?
   - Vague trigger anti-pattern?
   - Instruction bloat anti-pattern?

4. **Theoretical Grounding**: What scientific principles support this?
   - Cognitive load theory?
   - Information theory?
   - Systems design principles?

5. **Cross-Platform Validation**: Does this hold across implementations?
   - Works on all Claude models?
   - Framework-agnostic approach?
   - Portable across platforms?

### Machine-Verifiable Validation

**Objective Checks:**
```markdown
✓ Description follows Capability + Trigger + Negative pattern
✓ Autonomy level matches task characteristics
✓ Resources organized hub-and-spoke (no nesting)
✓ Scripts return JSON-over-stdout for validation
✓ Allowed-tools set to minimum required
```

**Automated Validation:**
```bash
# Run toolkit analyzer
uv run scripts/toolkit-analyzer.py

# Fix common issues
uv run scripts/toolkit-analyzer.py --fix
```

## 6. Trigger Optimization (The SEO Formula)

**Format:** What + When + What NOT

**Formula Structure:**
```
Capability (what it does) + Trigger (when to use) + Negative Constraint (what NOT to use for)
```

**Example:**
```yaml
description: Extracts raw text and tabular data from .pdf files. Use when user mentions parsing, scraping, or converting PDF invoices. Do not use for PDF generation, editing, or image-to-PDF conversion.
```

### Optimization Rules

1. **Specific over Generic**
   - ✓ Good: "parsing PDF invoices"
   - ✗ Bad: "working with PDFs"

2. **Action-Oriented Language**
   - ✓ Good: "parsing", "analyzing", "extracting", "validating"
   - ✗ Bad: "helps with", "useful for"

3. **Context Anchoring**
   - ✓ Good: ".pdf files", "CSV data", "JSON APIs"
   - ✗ Bad: "documents", "data", "files"

4. **Clear Exclusions**
   - ✓ Good: "Do not use for PDF creation or editing"
   - ✗ Bad: (omitted)

5. **Third-Person Voice Only**
   - ✓ Good: "Extracts data...", "Processes files..."
   - ✗ Bad: "I can help you...", "I will extract..."

### Trigger Phrase Examples

**Data Processing:**
```yaml
# Good
"Parses CSV data when user mentions importing spreadsheets"
"Converts JSON to CSV when working with data transformation"

# Bad
"Works with data"
"Helps with files"
```

**Code Analysis:**
```yaml
# Good
"Analyzes TypeScript code for type safety violations"
"Reviews pull requests for security vulnerabilities"

# Bad
"Helps with code"
"Useful for development"
```

**Document Processing:**
```yaml
# Good
"Extracts text from PDF invoices using OCR"
"Converts Markdown to HTML when generating documentation"

# Bad
"Processes documents"
"Works with text"
```

### Negative Constraints Examples

**Essential Exclusions:**
```yaml
# Prevent misuse
"Do not use for PDF creation, only parsing"
"Do not use for security scanning, only performance analysis"

# Prevent conflicts
"Do not use when user explicitly requests manual review"
"Do not use for encrypted or password-protected files"
```

**Anti-Competition:**
```yaml
# Prevent overlap with other skills
"Do not use when sql skill is available"
"Do not use when user asks for general advice"

# Scope boundaries
"Do not use for multi-file projects, only single files"
"Do not use for real-time processing, only batch operations"
```

### The SEO Mindset

Think of descriptions as **search engine optimization** for AI:

1. **Keywords**: Specific technical terms
2. **Intent Matching**: What users actually say
3. **Negative SEO**: Prevent irrelevant matches
4. **Semantic Precision**: Exact match to capability

**Example Evolution:**
```yaml
# v1.0: Too generic
description: "Helps with PDF processing"

# v1.5: Better, still vague
description: "Extracts text from PDF files"

# v2.0: Optimized
description: "Extracts raw text and tabular data from PDF invoices. Use when user mentions parsing invoices or extracting structured data from PDFs. Do not use for PDF creation, editing, or image-only PDFs."
```

### Testing Your Triggers

**Activation Test:**
- Will Claude correctly identify when to use this skill?
- Are the trigger phrases natural and common?

**Exclusion Test:**
- Will Claude avoid using this for inappropriate tasks?
- Are negative constraints clear and specific?

**Competition Test:**
- Does this skill compete with others unnecessarily?
- Are boundaries clearly defined?

## 6.1 Security & Safety Patterns

### Permission Management

**The Least Privilege Principle:**
- Restrict tools to minimum required
- Use allowlists, not denylists
- Validate before execution

**Permission Design Patterns:**

```yaml
# Read-only analysis (safest)
allowed-tools: [Read, Grep, Glob]

# File operations with care
allowed-tools: [Read, Bash]

# Full access (dangerous, use sparingly)
allowed-tools: [Read, Write, Bash, Edit, Glob, Grep, Skill]
```

### Hook System Patterns

**Common Hook Applications:**

**Security Hooks:**
```markdown
- Block dangerous operations (rm -rf, format disk)
- Validate file paths (prevent directory traversal)
- Check permissions before write operations
```

**Logging Hooks:**
```markdown
- Create audit trails for sensitive operations
- Log all destructive actions
- Track skill activations for debugging
```

**Authorization Hooks:**
```markdown
- Role-based access control
- Environment-specific restrictions
- API key validation
```

**Tool Interception:**
```markdown
- Redirect operations to safe alternatives
- Validate inputs before execution
- Sanitize outputs before display
```

### Validation-First Safety

**Pre-Execution Validation:**

```markdown
## Security Validation Workflow
1. **Validate Inputs**: Check file paths, permissions, environment
2. **Check Permissions**: Verify allowed-tools covers operations
3. **Validate Environment**: Confirm required tools/resources available
4. **Create Checkpoint**: Save state before destructive operations
```

**Machine-Verifiable Checks:**

```python
# scripts/validate_security.py
def validate_operation():
    # Check file paths are safe
    assert not path_contains_parent_refs(file_path)

    # Verify permissions
    assert has_required_permissions(operation)

    # Check environment
    assert all_tools_available(required_tools)

    return {"status": "valid", "checks_passed": True}
```

**Reversible Planning:**
```markdown
# Always create rollback points
1. Create backup before destructive operations
2. Validate backup integrity
3. Execute operation with validation
4. Verify success before cleanup
```

### Common Security Pitfalls

**Over-Permissive Skills:**
```yaml
# Bad: No restrictions
# (omitted allowed-tools)

# Good: Minimal access
allowed-tools: [Read, Grep]
```

**Unvalidated Inputs:**
```markdown
# Bad: Blind execution
Execute scripts/unsafe_operation.py --input {user_input}

# Good: Validate first
Validate input format
Check permissions
Execute only if validation passes
```

**Missing Rollback:**
```markdown
# Bad: Irreversible operations
1. Delete files
2. Done

# Good: Reversible
1. Create backup
2. Validate backup
3. Execute operation
4. Verify success
5. Cleanup backup (only if successful)
```

### Best Practices Checklist

**Before Deployment:**
- [ ] Minimal tool access granted
- [ ] All destructive operations validated
- [ ] Rollback points created
- [ ] Audit logging enabled
- [ ] Error messages sanitized
- [ ] Path traversal prevented
- [ ] Input validation implemented
- [ ] Permission checks automated

**During Execution:**
- [ ] Pre-flight checks pass
- [ ] Progress checkpoints created
- [ ] Failures isolated and recoverable
- [ ] Logs contain sufficient detail

**After Completion:**
- [ ] State verified
- [ ] Rollback points cleaned up (if successful)
- [ ] Audit log complete
- [ ] Success metrics recorded

## 7. State Anchoring & Validation

### State Management
```markdown
# State
- [x] Step 1: Backup
- [ ] Step 2: Transform
**Last Checkpoint:** SUCCESS
```

**Requirements:**
1. Atomic checkpoints
2. Idempotent operations
3. Progress visibility
4. Failure isolation

### Validation-First Architecture
```markdown
## Document Processing Workflow
1. **Plan**: Create changes.json
2. **Validate**: Run scripts/validate_changes.py
3. **Execute**: Apply changes if validation passes
4. **Verify**: Run scripts/verify_output.py
```

**Use for:**
- Batch operations
- Destructive operations
- Complex workflows
- High-stakes tasks

## 8. The 12-Point QA Checklist

Before deploying any skill, verify:

### Practical Validation Checklist
- [ ] **Description Format**: Contains 3rd person Capability + Trigger + Negative Constraint?
- [ ] **Trigger Optimization**: Specific gerunds and context anchoring included?
- [ ] **Negative Constraints**: Clear exclusions for what NOT to use for?
- [ ] **Name Compliance**: Excludes "anthropic" and "claude", matches directory?
- [ ] **Hub-and-Spoke**: References are 1-level deep, no nesting?
- [ ] **TOC Present**: Table of contents for reference files >100 lines?
- [ ] **User Invocation**: `user-invocable` appropriately set for utility skills?
- [ ] **State Persistence**: `_state.md` artifact mandated where needed?
- [ ] **Script Output**: Scripts return JSON-over-Stdout for validation?
- [ ] **File Outputs**: All outputs directed to CWD/Tmp (not Skill directory)?
- [ ] **Minimal Permissions**: `allowed-tools` set to minimum required set?
- [ ] **Asset Integrity**: Checksums included for critical assets?
- [ ] **Sub-agent Specification**: Explicit agent type specified in forks?

### Theoretical Validation Checklist

**Universal Success Patterns:**
- [ ] **Domain Encapsulation**: Clear, single mental model?
- [ ] **Autonomy Alignment**: Level matches task characteristics (Protocol/Guided/Heuristic)?
- [ ] **Trigger Precision**: Specific trigger phrases for reliable activation?
- [ ] **Context Efficiency**: 3-tier model minimizes overhead?
- [ ] **Validation Strategy**: Validation loops for high-risk operations?
- [ ] **Resource Organization**: Domain-based organization enables selective loading?
- [ ] **Error Prevention**: Destructive operations protected by validation?
- [ ] **State Management**: Persistent artifacts enable recovery?

### The QA Workflow

**Phase 1: Self-Assessment**
```markdown
1. Read description: Would you know when to use this?
2. Check triggers: Specific enough for reliable activation?
3. Review autonomy: Appropriate for task criticality?
4. Validate permissions: Minimal access granted?
```

**Phase 2: Machine Validation**
```bash
# Run automated checks
uv run scripts/toolkit-analyzer.py

# Fix common issues
uv run scripts/toolkit-analyzer.py --fix
```

**Phase 3: Cross-Model Testing**
```markdown
1. Test with Haiku: Is guidance sufficient?
2. Test with Sonnet: Is balance optimal?
3. Test with Opus: Is it avoiding over-explanation?
```

**Phase 4: User Testing**
```markdown
1. Deploy to staging environment
2. Monitor activation rate
3. Track success rate
4. Gather user feedback
5. Iterate based on data
```

### Success Criteria

**Activation Rate**: >80% for well-designed skills
- Measure: Relevant activations / total invocations
- Fix: Improve trigger specificity if low

**Success Rate**: >90% for mature skills
- Measure: Completed tasks / attempted tasks
- Fix: Add validation or improve instructions

**Context Efficiency**: Minimal tokens for maximum capability
- Measure: Tokens used / tasks completed
- Fix: Apply Delta Standard more aggressively

**User Satisfaction**: Positive qualitative feedback
- Measure: User reports and adoption rate
- Fix: Iterate based on user needs

### Common QA Failures

**Vague Triggers (40% of new skills)**
```yaml
# FAIL
description: "Helps with documents"

# PASS
description: "Extracts text from PDF invoices. Use when parsing invoice documents. Do not use for PDF creation."
```

**Over-Permissive Tools (30% of new skills)**
```yaml
# FAIL
# allowed-tools omitted (full access)

# PASS
allowed-tools: [Read, Grep]  # minimal required
```

**Mega-Skills (20% of new skills)**
```markdown
# FAIL
"PDF processing and report generation and data visualization"

# PASS
"Parse PDF invoices" (atomic skill)
```

**Missing Validation (10% of new skills)**
```markdown
# FAIL
"Just execute the migration"

# PASS
1. Validate: Check schema compatibility
2. Backup: Create rollback point
3. Execute: Run migration with validation
4. Verify: Confirm data integrity
```

## 9. Architecture: Hub-and-Spoke

**Filesystem-as-Context Model:**
- SKILL.md is the central hub
- All references one level deep
- No daisy-chaining (A.md → B.md)

**Atomic Unit Principle:**
- One domain per Skill
- Users think of it as single operation
- Example: "Analyze PDF invoices" (one Skill), not "Process PDFs and generate reports" (two Skills)

## 10. Concrete Examples & Use Cases

### Example 1: Procedural Skill - Database Migration

**Scenario:** Safe database schema migration with rollback capability

```yaml
---
name: migrate-database-schema
description: Executes database schema migrations with automatic rollback on failure. Use when user mentions updating database structure or applying schema changes. Do not use for data migrations, only schema changes.
allowed-tools: [Bash, Read]
user-invocable: false
---
```

```markdown
## Database Migration Protocol

**CRITICAL:** This is a Protocol-level skill. Execute EXACTLY as specified.

### State Management
```markdown
# State
- [ ] Step 1: Pre-flight validation
- [ ] Step 2: Create backup
- [ ] Step 3: Validate backup
- [ ] Step 4: Execute migration
- [ ] Step 5: Verify integrity
- [ ] Step 6: Cleanup (if successful)
**Last Checkpoint:** READY
```

### Execution Workflow
1. **Validate**: Run `scripts/validate_migration.py`
   - Check database connectivity
   - Verify schema compatibility
   - Confirm no conflicting migrations

2. **Backup**: Create rollback point
   - Run `scripts/create_backup.py`
   - Store backup metadata in `_state.md`

3. **Execute**: Apply migration
   - Run `scripts/migrate.py`
   - Monitor for errors
   - Stop immediately on failure

4. **Verify**: Confirm success
   - Run `scripts/verify_migration.py`
   - Check data integrity
   - Confirm schema changes applied

### Rollback Procedure
If verification fails:
1. Restore from backup: `scripts/restore_backup.py`
2. Verify restoration: `scripts/verify_restoration.py`
3. Report failure with diagnostic data
```

**Why This Works:**
- Protocol-level (Low Freedom): Exact steps, no deviation
- Validation-first: Checks before execution
- State management: Checkpoints for recovery
- Idempotent: Safe to run multiple times

### Example 2: Advisory Skill - Code Review

**Scenario:** Architectural guidance with expert judgment

```yaml
---
name: review-architecture
description: Provides architectural guidance and code review recommendations. Use when user mentions code review, architecture analysis, or design decisions. Do not use for security audits or performance optimization.
allowed-tools: [Read, Grep, Glob]
user-invocable: true
---
```

```markdown
## Architectural Review Framework

**Autonomy Level:** Guided (Medium Freedom)

### Review Criteria (in order of priority)

1. **Maintainability** (40% weight)
   - Code readability and documentation
   - Modular design and separation of concerns
   - Naming conventions and consistency

2. **Architecture** (30% weight)
   - Design pattern appropriateness
   - Component coupling and cohesion
   - Abstraction layers and interfaces

3. **Scalability** (20% weight)
   - Performance implications
   - Resource usage patterns
   - Growth accommodation

4. **Best Practices** (10% weight)
   - Language-specific conventions
   - Testing coverage and quality
   - Error handling patterns

### Review Process
1. **Scan**: Use grep to identify potential issues
   - Look for anti-patterns
   - Find complexity hotspots
   - Identify missing tests

2. **Analyze**: Apply criteria framework
   - Prioritize findings by impact
   - Consider context and constraints
   - Validate against project goals

3. **Recommend**: Provide actionable guidance
   - Specific improvement suggestions
   - Justification for each recommendation
   - Priority levels (Critical, Important, Suggestion)

### Output Format
```markdown
## Architectural Review: {Component/Module}

### Summary
- Overall Grade: [A-F]
- Critical Issues: {count}
- Recommendations: {count}

### Findings

#### Critical (Fix Before Merge)
- {Issue}: {Explanation} → {Recommendation}

#### Important (Address Soon)
- {Issue}: {Explanation} → {Recommendation}

#### Suggestions (Nice to Have)
- {Issue}: {Explanation} → {Recommendation}

### Positive Aspects
- {What works well}
```

**Why This Works:**
- Guided autonomy: Expert judgment applied to context
- Structured approach: Clear criteria and weights
- Actionable output: Specific recommendations with priorities
- Balanced perspective: Recognizes positives, not just problems
```

### Example 3: Generator Skill - Test Creation

**Scenario:** Generate test suites from code analysis

```yaml
---
name: generate-tests
description: Generates comprehensive test suites from source code. Use when user mentions creating tests, test coverage, or unit testing. Do not use for integration tests or end-to-end testing.
allowed-tools: [Read, Grep, Glob, Write]
user-invocable: true
---
```

```markdown
## Test Generation Framework

**Autonomy Level:** Guided (Medium Freedom)

### Input Analysis
1. **Identify Test Targets**
   - Scan for functions/methods without tests
   - Prioritize by complexity and criticality
   - Map dependencies and imports

2. **Determine Test Strategy**
   - Unit tests for pure functions
   - Mock tests for external dependencies
   - Integration points for complex modules

### Generation Pattern
```markdown
# For each function/method:

1. **Edge Case Tests**
   - Null/empty inputs
   - Boundary values
   - Invalid inputs

2. **Happy Path Tests**
   - Typical successful inputs
   - Expected output validation

3. **Negative Tests**
   - Error conditions
   - Exception handling
   - Failure scenarios
```

### Template Structure
```python
# {test_file_name}.py
import pytest
from {module} import {target}

class Test{Target}:
    """Test suite for {target}"""

    def test_{function}_success(self):
        """Test {function} with valid inputs"""
        # Arrange
        {setup_code}

        # Act
        result = {function}({inputs})

        # Assert
        assert result == {expected}

    def test_{function}_edge_case(self):
        """Test {function} with edge case"""
        # Test implementation

    def test_{function}_error(self):
        """Test {function} error handling"""
        # Test implementation
```

### Validation
1. **Syntax Check**: Verify generated tests compile
2. **Coverage Check**: Ensure target functions tested
3. **Quality Check**: Validate test descriptions and structure

**Why This Works:**
- Generator pattern: Template-driven with validation
- Structured output: Consistent test organization
- Quality assurance: Multiple validation layers
- Iterative improvement: Can regenerate based on feedback
```

### Example 4: Orchestrator Skill - Multi-Step Analysis

**Scenario:** Coordinate analysis across multiple domains

```yaml
---
name: analyze-codebase
description: Orchestrates comprehensive codebase analysis across multiple dimensions. Use when user mentions full code review, comprehensive analysis, or codebase audit. Do not use for single-file analysis or specific issues.
allowed-tools: [Read, Grep, Glob, Bash, Skill]
user-invocable: true
---
```

```markdown
## Codebase Analysis Orchestration

**Autonomy Level:** Guided (Medium Freedom)

### Analysis Pipeline
```markdown
# State
- [ ] Step 1: Project structure analysis
- [ ] Step 2: Dependency analysis
- [ ] Step 3: Code quality scan
- [ ] Step 4: Security review
- [ ] Step 5: Performance analysis
- [ ] Step 6: Generate comprehensive report
**Last Checkpoint:** READY
```

### Pipeline Sequence
1. **Structure Analysis** (Subagent: Explore)
   - Map project architecture
   - Identify key components
   - Document file organization

2. **Dependency Review** (Skill: dependency-analyzer)
   - Check for outdated packages
   - Identify security vulnerabilities
   - Validate version compatibility

3. **Quality Scan** (Skill: code-quality)
   - Analyze complexity metrics
   - Identify code smells
   - Review test coverage

4. **Security Audit** (Skill: security-scanner)
   - Check for common vulnerabilities
   - Validate input sanitization
   - Review authentication/authorization

5. **Performance Review** (Skill: performance-analyzer)
   - Identify bottlenecks
   - Review algorithm efficiency
   - Check resource usage

6. **Synthesis** (This skill)
   - Aggregate findings
   - Prioritize recommendations
   - Generate action plan

### Coordination Strategy
- **Data Contracts**: Each step outputs standardized artifacts
- **Dependency Management**: Later steps consume earlier outputs
- **Error Isolation**: Failures don't cascade
- **Progress Tracking**: State file tracks completion

**Why This Works:**
- Orchestrator pattern: Coordinates multiple capabilities
- Explicit dependencies: Clear data flow
- State persistence: Recovery from interruptions
- Parallel execution: Independent steps run concurrently
```

### Example 5: Complete Skill File Structure

**Example Directory:**
```
pdf-parser/
├── SKILL.md
├── references/
│   ├── extraction-methods.md
│   ├── error-handling.md
│   └── supported-formats.md
├── scripts/
│   ├── extract_text.py
│   ├── extract_tables.py
│   └── validate_output.py
└── assets/
    ├── templates/
    │   └── extraction-report.md
    └── examples/
        └── sample-invoices/
```

**Example SKILL.md:**
```markdown
# PDF Text Extraction

Extracts text and tabular data from PDF files using domain-specific optimization.

## When to Use
- Parsing invoice documents
- Extracting structured data from reports
- Converting PDF content to markdown

## Supported Formats
- Text-based PDFs (not scanned images)
- Tables with clear borders
- Standard fonts (not custom/crafted)

## Usage Pattern
1. **Identify**: Confirm PDF is text-based
2. **Extract**: Run extraction script
3. **Validate**: Check output quality
4. **Format**: Convert to target format

## Validation
Always run `scripts/validate_output.py` after extraction.

## Limitations
- Cannot process scanned/image-only PDFs
- Complex layouts may require manual review
- Custom fonts may reduce accuracy

See [references/supported-formats.md](references/supported-formats.md) for details.
```

**Why This Structure Works:**
- Hub-and-spoke: SKILL.md central, resources 1-level deep
- Progressive disclosure: Overview first, details on demand
- Self-contained: All resources linked from hub
- Validated: Scripts for quality assurance
```

### Common Patterns Summary

| Pattern | Use When | Key Characteristics | Example |
|:--------|:---------|:-------------------|:--------|
| **Protocol** | High risk, low variance | Exact steps, validation gates | Database migration |
| **Guided** | Medium risk, pattern-based | Criteria, weights, judgment | Code review |
| **Heuristic** | Low risk, high variance | Principles, flexibility | Brainstorming |
| **Generator** | Template-driven output | Templates, validation | Test generation |
| **Orchestrator** | Multi-step workflows | Dependencies, coordination | Full analysis |

## 11. Conclusion: Key Takeaways

### Universal Success Principles

1. **Concise**: Respect the context window
   - Apply the Delta Standard ruthlessly
   - Question every instruction
   - Optimize for information density

2. **Structured**: Use progressive disclosure
   - 3-tier loading model
   - Hub-and-spoke architecture
   - Atomic domain boundaries

3. **Tested**: Validate across models and use cases
   - Cross-model compatibility
   - Machine-verifiable checks
   - User feedback loops

4. **Focused**: One domain, clear boundaries
   - Avoid mega-skill anti-pattern
   - Specific trigger optimization
   - Clear negative constraints

5. **Discoverable**: Optimized for model invocation
   - SEO-optimized descriptions
   - Third-person voice
   - Action-oriented language

### The Framework-Agnostic Approach

The Universal Engineering Standard ensures Skills work across any agent platform:
- **Anthropic Claude**: Native support
- **Z.AI Routing**: Full compatibility
- **Custom Implementations**: Framework-independent
- **Future Platforms**: Extensible design

### Final Checklist

Before deploying any skill, verify:
- [ ] Description follows Capability + Trigger + Negative pattern
- [ ] Autonomy level matches task characteristics
- [ ] Resources organized hub-and-spoke
- [ ] Validation-first approach implemented
- [ ] Permissions minimized
- [ ] Cross-model tested
- [ ] User feedback plan established

### Next Steps

1. **Build**: Use these patterns to create new skills
2. **Validate**: Apply the QA checklist rigorously
3. **Test**: Deploy to staging environment
4. **Iterate**: Improve based on real usage data
5. **Share**: Contribute patterns back to the community
### Cross-Platform Success Factors

Skills that succeed across platforms consistently demonstrate:

1. **Semantic Precision**: Specific, action-oriented trigger language
2. **Context Efficiency**: 3-tier loading minimizes overhead
3. **Validation Emphasis**: Multiple layers prevent cascades
4. **Domain Focus**: Narrow, deep expertise
5. **State Management**: Persistent artifacts enable recovery
6. **Autonomy Alignment**: Instruction style matches task
7. **Resource Organization**: Domain-based enables selective loading
