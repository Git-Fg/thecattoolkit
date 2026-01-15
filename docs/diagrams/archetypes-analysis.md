# New Archetypes & Real-World Examples Analysis

Based on the 5 new rules added to the skills guide and comprehensive GitHub research (obra/superpowers, anthropics/claude-plugins-official, etc.), this document outlines recommended additions to the skills guide.

---

## Part 1: New Archetypes to Add

### Current State (4 Archetypes)
1. **Procedural** - Deterministic, repeatable processes
2. **Advisory** - Expertise and recommendations
3. **Generator** - Input→Output transformation
4. **Orchestrator** - Coordinate multiple capabilities

### Recommended New Archetypes

#### 5. Scenario-Driven Skill (NEW)

**Purpose:** Skills designed using TDD methodology, starting with usage scenarios before implementation.

**Pattern:** RED (Scenario) → GREEN (Implementation) → REFACTOR (Optimization)

**Key Characteristics:**
- Usage scenario written first (before any code/documentation)
- Expected behavior documented upfront
- Edge cases and constraints identified early
- Activation tested across models
- Description optimized for discoverability

**Use Cases:**
- Complex multi-step operations
- Skills that interact with other skills
- User-facing workflows with multiple paths

**Contrast with Procedural:**
- Procedural: "Here's the process"
- Scenario-Driven: "Here's the scenario, now implement the process"

#### 6. Evidence-Driven Skill (NEW)

**Purpose:** Skills that require file references, shell output, and grep results for every claim.

**Pattern:** Claim + Evidence (file:line or shell output)

**Key Characteristics:**
- Every claim includes file reference with line number
- Shell output pasted for validation evidence
- Grep results for search-based findings
- Qualifying language used only when evidence unavailable
- Claims are verifiable and reproducible

**Use Cases:**
- Security audits
- Code analysis
- Architecture reviews
- Performance investigations

**Examples from Research:**
```markdown
**Error Handling Issues:**
- `src/auth.py:45` - No error handling for network failures
- `src/db.py:120` - Missing exception for connection timeout

**Shell Output:**
```bash
$ pytest --cov=src
src/auth.py: 45% (missing: 23, 45, 67)
```
```

#### 7. State-Machine Skill (NEW)

**Purpose:** Skills with clear state transitions and cyclical workflows.

**Pattern:** RED → GREEN → REFACTOR → (repeat)

**Key Characteristics:**
- Explicit state transitions
- Cyclical or iterative process
- State persistence between cycles
- Clear entry/exit conditions
- Visual diagram documentation (DOT)

**Use Cases:**
- Iterative refinement processes
- Multi-stage workflows
- Feedback loops
- Optimization cycles

**Research Examples:**
- obra/superpowers: `test-driven-development` skill
- obra/superpowers: `writing-plans` skill
- obra/superpowers: `verification-before-completion` skill

#### 8. Subtask-Dispatching Skill (NEW)

**Purpose:** Skills that coordinate parallel subagents or subtasks.

**Pattern:** Dispatch → Wait → Aggregate → Return

**Key Characteristics:**
- Identifies independent subtasks
- Dispatches to subagents in parallel
- Aggregates results from multiple sources
- Handles failures gracefully
- Uses `context: fork` for isolation (NOT subagents)

**Use Cases:**
- Large-scale codebase analysis
- Multi-repository operations
- Parallel testing across environments
- Cross-domain validation

**Critical Distinction:**
- Use `context: fork` for isolation (3× token cost)
- AVOID spawning subagents (20k+ tokens + 1 quota)

#### 9. Diagram-First Skill (NEW)

**Purpose:** Skills where visual diagrams are the primary documentation, not supplementary.

**Pattern:** DOT diagram + Text alternative

**Key Characteristics:**
- Graphviz DOT diagram in `references/diagrams/`
- Diagram is primary documentation
- Text alternative provided for accessibility
- Diagram version-controlled (.dot files)
- Rendering to PNG/SVG for viewing

**Use Cases:**
- Complex workflows (>5 steps)
- Multi-system interactions
- State machines with branching
- Decision trees with multiple paths

---

## Part 2: Real-World Examples to Add

### Current Examples in Guide
1. **Procedural** - Database Migration
2. **Advisory** - Code Review
3. **Generator** - Test Creation (mentioned but not detailed)
4. **Orchestrator** - Multi-step Analysis (mentioned but not detailed)

### Recommended New Examples

#### Example 3: Scenario-Driven Skill - PDF Invoice Parser (NEW)

**Demonstrates:** TDD for Skills methodology

```yaml
---
name: extracting-pdf-invoices
description: "Extracts structured invoice data from PDF files. Use when user mentions invoices, PDF parsing, or extracting financial data. Handles multi-page invoices, varied layouts, and common edge cases. Do not use for PDF generation or editing."
allowed-tools: [Read, Bash, Write]
---

# PDF Invoice Extraction Skill

## RED Phase: Usage Scenario

**User Request:** "Can you extract data from these PDF invoices?"

**Expected Behavior:**
1. Skill activates on "invoices", "PDF parsing", "extracting financial data"
2. Validates PDF is text-based (not scanned images)
3. Extracts text using pdfplumber
4. Parses tables into structured JSON
5. Returns data with invoice_number, date, total, vendor_id

**Edge Cases:**
- Multi-page invoices
- Varied layouts
- Missing required fields
- Scanned/image-only PDFs (should reject)

**Constraints:**
- Text-based PDFs only (not OCR)
- Required fields: invoice_number, date, total, vendor_id
- Fallback: Use regex `INVOICE-\d+` pattern if table parsing fails

## GREEN Phase: Implementation

### Extraction Protocol

1. **Validate**: Check PDF is text-based
   ```bash
   pdffonts "$pdf_file" | grep -q "No fonts found"
   if [ $? -eq 0 ]; then
     echo "ERROR: Image-only PDF, OCR not supported"
     exit 1
   fi
   ```

2. **Extract**: Use pdfplumber for text + tables
   ```python
   import pdfplumber

   with pdfplumber.open(pdf_file) as pdf:
       text = pdf.pages[0].extract_text()
       tables = pdf.extract_tables()
   ```

3. **Parse**: Extract required fields
   ```python
   invoice_number = extract_invoice_number(text)
   date = extract_date(text)
   total = extract_total(tables[0])
   vendor_id = extract_vendor(text)
   ```

4. **Validate**: Output has required fields
   ```python
   required = ['invoice_number', 'date', 'total', 'vendor_id']
   assert all(field in output for field in required)
   ```

5. **Return**: Structured JSON
   ```python
   return json.dumps(output, indent=2)
   ```

## REFACTOR Phase: Optimization

**Test Activation:**
- ✅ Triggers on: "extract data from these PDF invoices"
- ✅ Triggers on: "parse these invoices"
- ✅ Triggers on: "extract financial data from PDF"
- ❌ Does NOT trigger on: "create PDF invoice"
- ❌ Does NOT trigger on: "edit invoice PDF"

**Description Optimization:**
- Added "handles multi-page invoices, varied layouts, and common edge cases"
- Added "Do not use for PDF generation or editing"
- Verified no workflow summarization

**Documentation Optimization:**
- Moved table parsing details to `references/table-methods.md`
- Kept core protocol in SKILL.md (<500 lines)
- Created `references/invoice-examples.md` with sample invoices

## Success Criteria Met
- [ ] Usage scenario written before implementation
- [ ] Description triggers on all test phrases
- [ ] Tested across 3 different invoice layouts
- [ ] Edge cases documented (image-only PDFs, missing fields)
- [ ] Follows Delta Standard (no PDF explanation)
- [ ] Validation checkpoints implemented
- [ ] Progressivedisclosure (details in references/)
```

**Why This Example Works:**
- Demonstrates complete TDD for Skills cycle
- Shows evidence-driven claims (bash commands, file references)
- Includes description optimization process
- Shows workflow without summarizing in description

---

#### Example 4: Evidence-Driven Skill - Security Auditor (NEW)

**Demonstrates:** Evidence-First Principle

```yaml
---
name: auditing-security
description: "Scans codebase for security vulnerabilities following OWASP Top 10. MUST Use when verifying security before deployment or conducting security audits. Do not use for performance optimization or code style checks."
allowed-tools: [Read, Grep, Glob]
---

# Security Audit Protocol

## Evidence-First Approach

This skill provides file references and line numbers for every claim. All vulnerabilities are verified with evidence.

## Audit Findings

### SQL Injection (3 files)

**File:** `src/auth/login.py:45`
```python
def authenticate(username, password):
    query = f"SELECT * FROM users WHERE username='{username}'"
    #                                           ^^^^^^^^ VULNERABLE
    cursor.execute(query)
```
**Fix:** Use parameterized queries with `?` placeholders

**File:** `src/api/users.py:123`
```python
user_id = request.args['id']
query = f"SELECT * FROM profiles WHERE id={user_id}"
#                                       ^^^^^^^ VULNERABLE
cursor.execute(query)
```
**Fix:** Use `cursor.execute("SELECT * FROM profiles WHERE id=?", (user_id,))`

**File:** `src/db/queries.py:67`
```python
def get_user(email):
    return db.query(f"SELECT * FROM users WHERE email = '{email}'")
    #                                             ^^^^^ VULNERABLE
```
**Fix:** Use ORM parameter binding: `db.query("SELECT * FROM users WHERE email = ?", (email,))`

### XSS Vulnerabilities (2 files)

**File:** `src/web/render.py:89`
```python
def render_page(content):
    return f"<div>{content}</div>"
    #         ^^^^^^^^ VULNERABLE (unsanitized input)
```
**Fix:** Escape HTML entities: `return f"<div>{escape(content)}</div>"`

**File:** `src/views/comments.py:234`
```python
comment = request.form['comment']
html = f"<p>{comment}</p>"
#      ^^^^^^^ VULNERABLE
return render(html)
```
**Fix:** Use `bleach.clean()` or `markdown.markdown()` with sanitization

### Hardcoded Secrets (4 instances)

**Shell Output:**
```bash
$ grep -r "api_key\|secret\|password" src/ --include="*.py" | grep -v "test"
src/config.py:12:API_KEY = "sk-1234567890abcdef"
src/config.py:15:DATABASE_URL = "postgres://user:pass123@localhost/db"
src/utils/auth.py:45:SECRET_KEY = "supersecretkey123"
src/utils/payment.py:78:STRIPE_KEY = "sk_live_51Hz..."
```

**Fix Required:**
- Move to environment variables
- Use `.env` file with `.gitignore`
- Rotate exposed keys immediately

## Validation Evidence

**Test Results:**
```bash
$ python -m pytest tests/test_security.py
==================== FAILURES ====================
____________________ test_sql_injection ____________________
tests/test_security.py:23: AssertionError: Expected 401 but got 200
____________________ test_xss_protection ____________________
tests/test_security.py:45: AssertionError: Unsanitized HTML detected

==================== 2 failed, 8 passed in 3.42s ====================
```

**Static Analysis:**
```bash
$ bandit -r src/
Run started:2024-01-15 10:23:45.123456

>> Issue: [B608:hardcoded_sql_expressions]
   Severity: HIGH
   Confidence: MEDIUM
   Location: src/auth/login.py:45
   More Info: https://bandit.readthedocs.io/en/latest/plugins/b608_hardcoded_sql_expressions.html

>> Issue: [B703:django_mark_safe]
   Severity: MEDIUM
   Confidence: HIGH
   Location: src/web/render.py:89

Results found 9 issues, 2 HIGH severity, 4 MEDIUM severity
```

## Severity Classification

**CRITICAL** (Fix Immediately):
- SQL injection in authentication flows
- Hardcoded production secrets
- Command injection vulnerabilities

**HIGH** (Fix Within 24h):
- XSS vulnerabilities in user-facing pages
- Insecure deserialization
- Authentication bypass

**MEDIUM** (Fix Within Sprint):
- Missing input validation
- Insecure direct object references
- Insufficient logging

## Remediation Priority

1. **sql-injection** (3 files) - CRITICAL
   - Impact: Full database access
   - Fix: Parameterized queries everywhere

2. **hardcoded-secrets** (4 instances) - CRITICAL
   - Impact: System compromise
   - Fix: Environment variables + key rotation

3. **xss-vulnerabilities** (2 files) - HIGH
   - Impact: User session hijacking
   - Fix: HTML escaping + sanitization
```

**Why This Example Works:**
- Every claim has file:line evidence
- Shell output included for verification
- Grep results shown for secrets
- Test failures documented
- Severity classification with evidence

---

#### Example 5: State-Machine Skill - Iterative Refinement (NEW)

**Demonstrates:** TDD RED→GREEN→REFACTOR cycle with visual diagram

```yaml
---
name: refactoring-code
description: "Applies structured refactoring cycles to improve code quality. PROACTIVELY Use when improving existing code, reducing complexity, or paying down technical debt. Do not use for new feature development or bug fixes."
allowed-tools: [Read, Grep, Edit, Bash]
---

# Code Refinement Cycle

## The Three-State Machine

```dot
digraph refinement_cycle {
    rankdir=TB;
    node [shape=box, style=filled, fontname="Arial-12"];

    RED [fillcolor="#ffcccc", label="RED\nIdentify Issue"];
    GREEN [fillcolor="#ccffcc", label="GREEN\nApply Fix"];
    REFACTOR [fillcolor="#ccccff", label="REFACTOR\nOptimize"];
    VERIFY [label="Verify Fix\nStill Pass?"];

    RED -> GREEN;
    GREEN -> VERIFY;
    VERIFY -> REFACTOR [label="Yes"];
    REFACTOR -> VERIFY [label="Re-test"];
    VERIFY -> RED [label="No\nNew Issue"];
}
```

**See:** [references/refinement-cycle.dot](references/refinement-cycle.dot)

## State Transitions

### RED State: Identify Issue

**Entry:** Code smells detected, complexity high, or technical debt identified

**Actions:**
1. Measure complexity: `radon cc src/ -a`
2. Find duplication: `jscpd src/`
3. Identify smell: `prospector src/`

**Evidence Required:**
```bash
$ radon cc src/auth.py -a
src/auth.py:F43 authenticate - A (1.2)
src/auth.py:F78 validate_user - B (3.8)
```

**Exit Condition:** Issue identified with evidence

### GREEN State: Apply Fix

**Entry:** Issue identified in RED state

**Actions:**
1. Apply smallest fix that addresses issue
2. Run tests to verify no regression
3. Commit with descriptive message

**Example Fix:**
```python
# BEFORE (complexity A)
def authenticate(user, passw, remember=False, timeout=30):
    if user and passw:
        if remember:
            if timeout:
                # ... 15 nested levels
```

```python
# AFTER (complexity B)
def authenticate(user, password, remember=False, timeout=30):
    if not user or not password:
        return False

    session = create_session(user, timeout)
    if remember:
        session.extend()
    return session.validate()
```

**Exit Condition:** Fix applied, tests pass

### REFACTOR State: Optimize

**Entry:** GREEN state complete, looking for next issue

**Actions:**
1. Consider broader design improvements
2. Extract common patterns
3. Improve naming/structure

**Question:** "Can this be further simplified without changing behavior?"

**Exit Condition:** No more improvements found OR complexity acceptable

### VERIFY State: Check Still Passes

**Entry:** REFACTOR state complete

**Actions:**
1. Run full test suite
2. Verify no behavioral changes
3. Check complexity improved

**Evidence Required:**
```bash
$ pytest tests/ -v
======================== 156 passed in 12.34s =========================

$ radon cc src/auth.py -a
src/auth.py:F43 authenticate - B (2.1)  # Improved from A
```

**Decision:**
- **YES** (tests pass): Return to REFACTOR or exit
- **NO** (tests fail): Return to GREEN state

## State Persistence

**Track state in `_refinement_state.md`:**
```markdown
# Refinement State

**Current State:** REFACTOR
**Last Issue:** Duplicate session creation logic
**Last Action:** Extracted `create_session()` helper
**Tests Status:** PASS (156/156)
**Next Step:** Check for more duplication

**History:**
- RED → GREEN → VERIFY → REFACTOR (current)
```

## When to Exit

**Exit Conditions:**
- Complexity acceptable (all files < C)
- No more duplications found
- Tests passing
- No clear improvements remaining

**Return to:** RED state (look for next issue or move to next file)
```

**Why This Example Works:**
- Shows complete state machine with DOT diagram
- Evidence-driven (bash output, file references)
- State persistence with `_state.md`
- Clear exit conditions
- Visual diagram as primary documentation

---

#### Example 6: Subtask-Dispatching Skill - Parallel Analysis (NEW)

**Demonstrates:** `context: fork` for parallel execution

```yaml
---
name: analyzing-codebase-parallel
description: "Orchestrates parallel codebase analysis across multiple dimensions. Use when user mentions full audit, comprehensive analysis, or cross-domain review. Dispatches independent analyses in parallel using context fork."
allowed-tools: [Read, Grep, Glob, Bash, Skill, Edit]
context: fork
---

# Parallel Codebase Analysis

## Architecture: Fork-Based Parallelism

**Key Decision:** Use `context: fork` NOT subagents

**Why Fork:**
- Cost: ~3× inline token cost
- Subagent cost: 20k+ tokens + 1 prompt quota
- Parallel execution without quota overhead
- Clean context isolation

## Dispatch Matrix

| Analysis Type | Fork Instance | Resources | Output |
|:--------------|:---------------|:----------|:-------|
| Security | fork-1 | security-analyzer skill | `findings/security.md` |
| Performance | fork-2 | performance-analyzer skill | `findings/performance.md` |
| Architecture | fork-3 | architecture-analyzer skill | `findings/architecture.md` |
| Quality | fork-4 | quality-analyzer skill | `findings/quality.md` |
| Dependencies | fork-5 | dependency-analyzer skill | `findings/dependencies.md` |

## Dispatch Protocol

### Phase 1: Discovery

**Identify Independent Analyses:**
```bash
# Find all Python files
find src/ -name "*.py" > targets.txt
```

**Determine Parallelism:**
- Security scan: All files (independent)
- Performance check: All files (independent)
- Architecture: Component-based (independent modules)
- Quality: Per-file (independent)
- Dependencies: Graph-based (independent subgraphs)

### Phase 2: Parallel Dispatch

```bash
# Fork 1: Security Analysis
cat > /tmp/fork-1-input.json << EOF
{
  "analysis_type": "security",
  "targets": "@targets.txt",
  "output": "findings/security.md"
}
EOF

# Fork 2: Performance Analysis
cat > /tmp/fork-2-input.json << EOF
{
  "analysis_type": "performance",
  "targets": "@targets.txt",
  "output": "findings/performance.md"
}
EOF

# Launch all forks in parallel
for i in {1..5}; do
  claude --context fork --input /tmp/fork-${i}-input.json &
done
wait  # Wait for all forks
```

### Phase 3: Aggregation

**Collect Results:**
```markdown
## Comprehensive Analysis Results

### Security Analysis
[Content from findings/security.md]

### Performance Analysis
[Content from findings/performance.md]

### Architecture Analysis
[Content from findings/architecture.md]

### Quality Analysis
[Content from findings/quality.md]

### Dependencies Analysis
[Content from findings/dependencies.md]

### Cross-Cutting Findings

**Critical Issues (across multiple dimensions):**
- `src/auth.py:45` - SQL injection (Security) + Performance (N+1 query)
- `src/utils/cache.py:123` - Race condition (Security) + Architecture (thread safety)

**Recommended Action Plan:**
1. Fix SQL injection in authentication (Security CRITICAL)
2. Add caching layer (Performance)
3. Refactor cache for thread safety (Architecture)
```

## Error Handling

**If Fork Fails:**
```bash
# Check fork exit status
for i in {1..5}; do
  if [ ! -f "findings/analysis-${i}.md" ]; then
    echo "WARNING: Fork ${i} failed, using fallback"
    # Run simplified analysis inline
    analyze_fallback "analysis-${i}" > "findings/analysis-${i}.md"
  fi
done
```

## Cost Comparison

**Subagent Approach (WRONG):**
- 5 subagents × 20k tokens = 100k tokens
- 5 prompts = 5 quota consumption
- Total: 100k tokens + 5 quota

**Fork Approach (CORRECT):**
- 5 forks × 3× inline cost = 15× tokens
- No quota consumption
- Total: ~15k tokens (85% savings)

## Output Artifacts

**`_analysis_summary.md`:**
```markdown
# Codebase Analysis Summary

**Analysis Date:** 2024-01-15
**Files Analyzed:** 142 Python files
**Analyses Run:** 5 (parallel)
**Total Time:** 3.2 minutes

## Findings Summary
- Critical: 3 issues
- High: 12 issues
- Medium: 28 issues
- Low: 45 issues

## Artifacts Generated
- findings/security.md
- findings/performance.md
- findings/architecture.md
- findings/quality.md
- findings/dependencies.md
- _analysis_summary.md (this file)
```
```

**Why This Example Works:**
- Demonstrates `context: fork` vs subagent decision
- Shows cost comparison (85% token savings)
- Complete dispatch protocol with error handling
- Evidence-based (bash commands, file references)
- Output artifact structure

---

#### Example 7: Description Pattern Comparison (NEW)

**Demonstrates:** Cat Toolkit vs. obra/superpowers patterns

```yaml
---
# Pattern A: Cat Toolkit Standard
name: validating-tdd
description: "Provides Universal Standard for Test-Driven Development. PROACTIVELY Use when writing code, debugging, or implementing features. Modes available: debug, review, refactor. Enforces RED-GREEN-REFACTOR cycle."
allowed-tools: [Read, Write, Bash, Edit]
---

# TDD Validation Protocol

## When to Use

**MUST Use when:**
- Writing any production code
- Debugging test failures
- Implementing features or bugfixes

**Modes:**
- **debug** - Investigate test failures
- **review** - Validate test coverage
- **refactor** - Improve code with tests as safety net

## Protocol

1. **RED**: Write failing test first
2. **GREEN**: Write minimal code to pass
3. **REFACTOR**: Improve with tests as safety net
```

```yaml
---
# Pattern B: obra/superpowers Standard
name: extracting-pdf-invoices
description: "Extracts structured invoice data from PDF files. Use when user mentions invoices, PDF parsing, or extracting financial data. Handles multi-page invoices, varied layouts, and common edge cases. Do not use for PDF generation, editing, or image-only PDFs."
allowed-tools: [Read, Bash, Write]
---

# PDF Invoice Extraction Protocol

## When to Use

**Use when:**
- Parsing invoice documents
- Extracting financial data from PDFs
- Converting invoice PDFs to structured data

**Do NOT use when:**
- Creating PDF files
- Editing or modifying existing PDFs
- Processing image-only or scanned PDFs (no text layer)

## Protocol

1. Validate PDF is text-based
2. Extract text using pdfplumber
3. Parse tables into structured data
4. Return JSON with required fields
```

## Pattern Comparison

| Aspect | Cat Toolkit (Pattern A) | obra/superpowers (Pattern B) |
|:-------|:------------------------|:-------------------------------|
| **Modality Markers** | MUST, PROACTIVELY, SHOULD | None (simple triggers) |
| **Operational Modes** | Explicit (debug, review, refactor) | Implicit (single operation) |
| **Use Case** | Internal toolkit infrastructure | User-facing/portable tools |
| **Trigger Language** | "PROACTIVELY Use when..." | "Use when..." |
| **Workflow in Description** | Sometimes (modes listed) | Never (causes skip bug) |
| **Distribution** | Cat Toolkit only | Marketplace compatible |

## Decision Guide

**Choose Cat Toolkit Pattern (A) when:**
- Multiple operational modes exist
- Critical/compliance scope (MUST use cases)
- Internal toolkit infrastructure
- Explicit invocation guidance needed

**Choose obra/superpowers Pattern (B) when:**
- Single-mode operation
- User-facing/portable skill
- Marketplace distribution intended
- Simple discovery needed

## Hybrid Pattern (Advanced)

For complex skills with modes AND marketplace intent:

```yaml
description: "Orchestrates comprehensive codebase analysis across security, performance, and architecture. PROACTIVELY Use when conducting full audits or multi-dimensional reviews. Do not use for single-file analysis or quick checks. Supports modes: security-only, performance-only, full-audit."
```

**Structure:**
1. Capability: "Orchestrates comprehensive codebase analysis..."
2. Modality: "PROACTIVELY Use when..." (internal guidance)
3. Trigger: "...conducting full audits..." (SEO discovery)
4. Negative: "Do not use for single-file..." (exclusion)
5. Modes: "Supports modes: ..." (operational flexibility)
```

**Why This Example Works:**
- Side-by-side comparison of both patterns
- Clear decision guide
- Hybrid pattern for complex cases
- Demonstrates both are VALID (not competition)
```

**Why This Example Works:**
- Shows both patterns are VALID (not "better/worse")
- Clear decision matrix for choosing
- Hybrid pattern for complex use cases
- Resolves confusion from research findings

---

## Part 3: Recommended Additions to Skills Guide

### Add New Section: "## 4.1 Extended Archetypes"

**Location:** After Section 4 (Four Universal Archetypes)

**Content:**
- Scenario-Driven Skill (TDD for Skills)
- Evidence-Driven Skill (Evidence-First)
- State-Machine Skill (Cyclical workflows)
- Subtask-Dispatching Skill (Parallel fork-based)
- Diagram-First Skill (Visual documentation)

### Add New Section: "## 10.1 Real-World Examples"

**Location:** Expand Section 10 (Concrete Examples)

**New Examples to Add:**
1. **Example 3:** Scenario-Driven Skill (PDF Invoice Parser with full TDD cycle)
2. **Example 4:** Evidence-Driven Skill (Security Auditor with file references)
3. **Example 5:** State-Machine Skill (Refinement Cycle with DOT diagram)
4. **Example 6:** Subtask-Dispatching Skill (Parallel Analysis with fork comparison)
5. **Example 7:** Description Pattern Comparison (Cat Toolkit vs. obra/superpowers)

### Add New Section: "## 11. Decision Matrix"

**Location:** After Section 10 (Concrete Examples)

**Content:**
- How to choose between 9 archetypes
- When to use Cat Toolkit vs. obra/superpowers description patterns
- Fork vs. Subagent decision tree
- When to use diagrams vs. text-only documentation

---

## Part 4: Implementation Priority

### High Priority (Add Immediately)
1. **Evidence-Driven Skill Example** - Demonstrates Section 2.1 (Evidence-First)
2. **Description Pattern Comparison** - Clarifies Section 6.2.1
3. **Scenario-Driven Skill Example** - Demonstrates Section 5.2 (TDD for Skills)

### Medium Priority (Add Soon)
4. **State-Machine Skill Example** - Demonstrates visual diagram usage (Section 9.5)
5. **Subtask-Dispatching Skill Example** - Demonstrates `context: fork` decision (Section 4.2)

### Low Priority (Add Later)
6. **Extended Archetypes Section** - Formalize new archetypes
7. **Decision Matrix Section** - Cross-reference all patterns

---

## Part 5: Key Insights from Research

### From obra/superpowers (23k stars)

1. **Gerund-based naming** (`writing-skills`, `executing-plans`)
2. **TDD for Skills is fundamental** - Not optional, core methodology
3. **Visual diagrams everywhere** - DOT files in every complex skill
4. **Evidence-First is default** - Every claim backed by file reference
5. **Protocol over persona** - No role-playing, just procedures

### From Cat Toolkit

1. **Modality markers** (MUST, PROACTIVELY, SHOULD) - Unique to Cat Toolkit
2. **3-tier loading model** - Progressive disclosure architecture
3. **Hub-and-spoke** - Flat file structure
4. **Fork over subagents** - Token efficiency principle
5. **Delta Standard** - Only document what Claude doesn't know

### From anthropics/claude-plugins-official (3.8k stars)

1. **Simple description pattern** - "Use when..." without workflow
2. **Example-plugin structure** - SKILL.md + references/ + scripts/
3. **Agent as config-only** - No persona in agent files
4. **Skills as procedures** - Not workers, not identities

---

## Part 6: Real-World Example Template

**Template for adding new examples to skills guide:**

```markdown
### Example X: [Archetype] - [Descriptive Name]

**Demonstrates:** [Which new rule this shows]

**Scenario:** [One sentence description]

```yaml
---
name: example-skill-name
description: "[Trigger-optimized description]"
allowed-tools: [list]
---
```

```markdown
# Skill Name

## [Red/Yellow/Green Phase if TDD]

### Evidence Section
**File:** path/to/file:line
```python
code snippet
```

### Diagram
```dot
digraph example {
    // DOT diagram
}
```

### Protocol
1. Step 1
2. Step 2
3. Step 3

**Why This Works:**
- Demonstrates [specific rule]
- Shows evidence-driven approach
- Includes visual diagram
```
```

---

## Summary

The skills guide should be enhanced with:

1. **5 New Archetypes:** Scenario-Driven, Evidence-Driven, State-Machine, Subtask-Dispatching, Diagram-First

2. **5 New Real-World Examples:** PDF Parser (TDD), Security Auditor (Evidence), Refinement Cycle (State-Machine), Parallel Analysis (Fork), Description Comparison (Pattern Decision)

3. **2 New Sections:** Extended Archetypes (4.1), Decision Matrix (11)

4. **Cross-References:** Link new examples to new rules (Section 2.1, 5.2, 6.2, 6.2.1, 9.5)

This ensures the guide demonstrates all 5 new rules with concrete, actionable examples.
