# Research & Prompting Anti-Patterns

A catalog of known pitfalls, mistakes, and red flags to avoid.

## Prompting Pitfalls

### 1. The "XML Soup"
**What**: Excessive or nested XML tags.
**Why**: Increases token cost and confuses the model's structural parsing.
**Prevention**: Limit to 15 flat tags. Use Markdown for content, XML only for containers.

### 2. Example Leakage
**What**: AI follows example content instead of instructions.
**Why**: Examples not properly isolated from the task instruction.
**Prevention**: Always wrap individual examples in flat `<example>` tags.

### 3. Vague Instructions
**What**: "Analyze this", "Check for bugs", "Be helpful".
**Why**: Lack of specific success criteria leads to generic, inconsistent output.
**Prevention**: Use specific action verbs and define exactly what "analysis" or "bugs" look like.

### 4. Over-Engineering
**What**: Adding 20 constraints and 10 examples for a simple task.
**Why**: Dilutes the attention of the model and risks hitting token limits.
**Prevention**: Start with Pure Markdown. Add complexity only where testing proves it's needed.

## Research Pitfalls

### 1. Scope Assumptions
**What**: Assuming evidence of absence is evidence of absence.
**Example**: "I didn't find a config file, so it doesn't exist."
**Prevention**: Explicitly verify all possible scopes (Global, Project, Local, Environment).

### 2. Deprecation Blindness
**What**: Relying on outdated documentation.
**Why**: Older docs (especially blogs/Q&A) often contradict current tool capabilities.
**Prevention**: Prioritize official docs and check "Updated" dates/Changelogs.

### 3. Single-Source Reliance
**What**: Basing critical claims on one source.
**Prevention**: Cross-reference multiple authoritative sources (Official Docs + GitHub Issues + Changelog).

### 4. Vagueness in Search
**What**: Poorly formulated queries like "How does X work?".
**Prevention**: Use specific, version-targeted queries like "{tool_name} v1.2 configuration example".

## Red Flags in AI Outputs

- **🚩 100% Success**: Every investigation perfectly succeeds (suspiciously clean).
- **🚩 Zero Citations**: Claims made without URLs or documentation references.
- **🚩 Binary Thinking**: "It is impossible" vs "It is the only way" without evidence.
- **🚩 Role Redefinition**: Forgetting the primary agent role in favor of a local prompt instruction.

## Concrete Anti-Pattern Examples

### Example 1: Generic Persona Definition

**❌ BAD:**
```markdown
You are a helpful AI assistant that helps users with various tasks.
```

**Why this fails:**
- Generic role provides no domain expertise
- No specific competencies defined
- No success criteria for evaluation

**✅ GOOD:**
```markdown
You are a **Senior PostgreSQL Database Administrator**.
Your goal is to optimize query performance without altering the underlying data schema unless absolutely necessary.

**Your Strengths:**
- Query plan analysis (EXPLAIN ANALYZE)
- Indexing strategies (B-Tree vs GIN/GiST)
- Vacuuming and maintenance configuration

**Success Criteria:**
- Reduced query execution time by >50%
- No degradation in write performance
- Zero downtime implementation
```

### Example 2: Missing Hard Boundaries

**❌ BAD:**
```markdown
You are a code reviewer. Review this code and provide feedback.
```

**Why this fails:**
- No explicit prohibition against making changes
- Model might modify files unintentionally
- No clear scope of review

**✅ GOOD:**
```markdown
You are a code reviewer for Claude Code.

**=== CRITICAL: READ-ONLY MODE - NO FILE MODIFICATIONS ===**
You are STRICTLY PROHIBITED from:
- Creating new files
- Modifying existing files
- Deleting files
- Running ANY commands that change system state

Your role is EXCLUSIVELY to analyze and review code. You do NOT have access to file editing tools.
```

### Example 3: XML Soup (Too Many Tags)

**❌ BAD:**
```markdown
<persona>You are a database expert</persona>
<success_criteria>Optimize queries</success_criteria>
<env><database>PostgreSQL</database><version>14</version></env>
<agent_persona type="Explore"><capability>Search files</capability></agent_persona>
<protocol><step>Analyze</step><step>Optimize</step></protocol>
<example><input>SELECT * FROM users</input><output>Optimized query</output></example>
```

**Why this fails:**
- 7 nested XML tags (exceeds 5-8 rule)
- Simple content wrapped in XML unnecessarily
- Difficult to parse and maintain

**✅ GOOD:**
```markdown
You are a **PostgreSQL Database Administrator**.
Your expertise lies in query optimization and performance tuning.

**Your Strengths:**
- Query plan analysis (EXPLAIN ANALYZE)
- Indexing strategies
- Performance monitoring

**Success Criteria:**
- Reduced query execution time by >50%
- Zero downtime implementation

<env>
Database: PostgreSQL 14
</env>

<example_correct>
User: "Optimize this query"
Assistant: "I'll analyze the query plan..."
</example_correct>
```

### Example 4: Scattered Questions

**❌ BAD:**
```markdown
[During implementation]
"One more question — should we add logging here?"
[Later during review]
"Also, what about error handling?"
```

**Why this fails:**
- Questions break user flow
- Information loss between phases
- Wastes time revisiting completed work

**✅ GOOD:**
```markdown
**=== CRITICAL: THIS IS THE ONLY QUESTION-ASKING PHASE ===**

1. Compile ALL questions from earlier phases into a single organized list:
   - Edge Cases:
     1. Should the feature handle concurrent requests?
     2. What happens when the user session expires?

   - Integration:
     3. Should this integrate with the notification system?
     4. Do we need admin override capability?

2. Present questions in numbered, categorized format
3. WAIT for complete answers before proceeding
```

### Example 5: Vague Protocol Prerequisites

**❌ BAD:**
```markdown
Use the MCP tool to access the API.
```

**Why this fails:**
- No prerequisite checking
- Tool schemas never match expectations
- May fail unexpectedly

**✅ GOOD:**
```markdown
**MANDATORY PREREQUISITE - THIS IS A HARD REQUIREMENT**
You MUST call `mcp-cli info <server>/<tool>` BEFORE ANY `mcp-cli call <server>/<tool>`.

**Why:** MCP tool schemas never match expectations. Even tools with pre-approved permissions require schema checks.

**Flow:**
1. `mcp-cli tools` (Discover)
2. `mcp-cli info <tool>` (Check Schema - **REQUIRED**)
3. `mcp-cli call <tool>` (Execute)
```

### Example 6: Missing Contrastive Examples

**❌ BAD:**
```markdown
Here are some examples of good code:
[Code examples]
```

**Why this fails:**
- No contrast to show what's wrong
- Doesn't teach nuance
- Examples might be ignored

**✅ GOOD:**
```markdown
<example_correct>
User: "The server is down."
Assistant: "I see the server is unresponsive. I will check the Nginx logs to identify the error code."
</example_correct>

<example_incorrect>
User: "The server is down."
Assistant: "I will restart the server immediately."
Reasoning: Do not take action without diagnosing the root cause first.
</example_incorrect>
```

### Example 7: No Approval Gates

**❌ BAD:**
```markdown
"I'll start implementing now with some improvements I think would be better."
```

**Why this fails:**
- Premature implementation wastes resources
- User may not approve the approach
- Violates user ownership of decisions

**✅ GOOD:**
```markdown
**=== CRITICAL: REQUIRES EXPLICIT USER APPROVAL ===**

**MANDATORY PREREQUISITE — VERIFY BEFORE STARTING:**
- [ ] User has explicitly selected an architecture approach
- [ ] All Phase 3 questions have been answered
- [ ] Codebase mental model is complete

1. Confirm explicit user approval to proceed
2. Implement following the chosen architecture EXACTLY
3. Do not deviate from selected approach
```

## Verification Checklist
- [ ] Are examples isolated?
- [ ] Is XML minimal and flat?
- [ ] Are claims cited with URLs?
- [ ] Have all scopes been checked?
- [ ] Is the version relevance confirmed?
- [ ] Does the persona have specific domain expertise?
- [ ] Are hard boundaries explicitly defined?
- [ ] Are questions consolidated into a single phase?
- [ ] Are protocol prerequisites mandatory?
- [ ] Are contrastive examples provided?
- [ ] Are approval gates explicitly required?
