# Subagent Prompt Writing Guide

## Key Insight

Subagent prompts should be task-specific, not generic. They define a specialized role with clear focus areas, workflows, and constraints.

**Structure**: Most agents use **Pure Markdown** (`## Role`, `## Workflow`, `## Constraints`). Add XML tags only when complexity genuinely requires it.

## Pure Markdown Default

**Start with Pure Markdown.** This is what the actual agents in this codebase use, and it works well for most cases.

### Simple Agent Example (Default Pattern)

```yaml
---
name: text-summarizer
description: Summarizes text content. Use for quick overview of documents.
tools: Read
---

## Role

You are a concise text summarizer focusing on key points.

## Focus Areas

- Main ideas and themes
- Critical details
- Actionable insights

## Workflow

1. Read the content
2. Identify main points
3. Summarize in 3-5 bullet points

## Success Criteria

- Summary captures essential information
- Bullet points are scannable
- Key details preserved
```

This pattern handles the vast majority of agent use cases effectively.

## When to Add XML Tags

Add XML tags only when you have a genuine need that Markdown cannot address:

### Valid XML Use Cases

**Multi-phase state tracking:**
```xml
<phase>
<context>
[current phase context]
</context>
<task>
[what to do in this phase]
</task>
</phase>
```

**Critical safety constraints:**
```xml
<constraints>
<mandatory>
[hard requirements that must never be violated]
</mandatory>
</constraints>
```

**Complex decision trees:**
```xml
<decision-tree>
<condition name="condition-1">
[path when condition-1 is true]
</condition>
<condition name="condition-2">
[path when condition-2 is true]
</condition>
</decision-tree>
```

### When NOT to Use XML

❌ **Don't use XML for:**
- Simple lists (use Markdown)
- Basic structure (Markdown headings work fine)
- Single workflow (just use Markdown)
- Personal preferences ("I prefer to...")
- Unnecessary complexity

## YAML Frontmatter

### Required Fields

```yaml
---
name: agent-name          # lowercase-with-hyphens
description: ...           # What the agent does + when to use
---
```

### Optional Fields

```yaml
---
name: agent-name
description: ...
tools: Read, Write, Edit  # Optional: restrict tools
skills: [skill-a, skill-b] # Optional: related skills
model: sonnet             # Optional: sonnet/opus/haiku/inherit
---
```

### Description Standards

**Formula:** `{Role}. MUST/PROACTIVELY USE when {trigger condition}`

**Examples:**
```
description: System Maintainer. MUST USE when auditing, creating, or fixing AI components (agents, skills, commands, hooks).
description: Security specialist. PROACTIVELY USE when analyzing code for vulnerabilities or reviewing authentication systems.
description: Performance optimizer. CONSULT for database tuning, caching strategies, or profiling slow code.
```

## System Prompt Structure

### Recommended Sections

**1. Role** (Required)
- Who the agent is
- What it specializes in
- Core identity

**2. Constraints** (Recommended)
- Hard rules (NEVER/MUST/ALWAYS)
- Boundaries and scope
- Safety requirements

**3. Focus Areas** (Recommended)
- What to prioritize
- Key concerns
- Important aspects

**4. Workflow** (Optional)
- Step-by-step process
- How to approach tasks
- Methodology

**5. Output Format** (Optional)
- How to structure results
- Required sections
- Formatting rules

**6. Success Criteria** (Optional)
- How to know when done
- Completion markers
- Quality standards

**7. Validation** (Optional)
- How to verify work
- Checkpoints
- Self-review

## Core Principles

### Be Specific

**❌ Generic:**
```
You are a helpful assistant that helps with coding.
```

**✅ Specific:**
```
You are a React component refactoring specialist. You focus on converting class components to hooks, optimizing re-renders, and improving component performance.
```

### Use Clear Structure

**✅ Markdown headings work well:**
```markdown
## Role
[Description of who the agent is]

## Constraints
- NEVER modify test files
- ALWAYS preserve component API
- MUST follow React hooks rules

## Workflow
1. Analyze current component
2. Identify refactoring opportunities
3. Convert to functional component with hooks
4. Verify functionality
```

### Task-Specific Instructions

**Tailor to the specific domain:**
- Don't create generic "helper" agents
- Focus on particular expertise
- Include domain-specific knowledge
- Reference specific technologies/frameworks

### Intelligence Rules

**Simple agents** (single focused task):
- Use role + constraints minimum
- Example: api-researcher, test-runner

**Medium agents** (multi-step process):
- Add workflow, output format, success criteria
- Example: api-researcher, documentation-generator

**Complex agents** (research + generation + validation):
- Add all sections including validation, examples
- Example: mcp-api-researcher, comprehensive-auditor

## Writing Effective Prompts

### Core Principles

**1. Use strong modal verbs:**
- MUST, NEVER, ALWAYS, DO, DON'T
- Creates clear boundaries
- Prevents scope creep

**2. Include specific triggers:**
- "when working with SKILL.md files"
- "for database validation tasks"
- "to create REST APIs"

**3. Define success criteria:**
- How to know when done
- Measurable outcomes
- Quality standards

**4. Provide examples:**
- Show desired output format
- Demonstrate expectations
- Clarify ambiguous instructions

### Description Field Optimization

**For automatic routing, include:**

**Keywords** users would naturally say:
```
"audit our agents"
→ description: MUST USE when auditing agent configurations
```

**Domain terms:**
```
"security review"
→ description: Security specialist for vulnerability assessment
```

**Action triggers:**
```
"create a plan"
→ description: Strategic planning for project execution
```

## XML/Markdown Decision Framework

### Use Pure Markdown When:

✅ **Simple, linear workflows**
- Single path through task
- No complex state tracking
- Clear step-by-step process

✅ **Standard structure needed**
- Role, constraints, workflow sections
- No complex decision trees
- Basic organization

✅ **Most agent types:**
- Research agents
- Analysis agents
- Simple execution agents

### Use Hybrid XML/Markdown When:

⚠️ **Multi-phase workflows**
- Distinct phases with different contexts
- State must be tracked across phases
- Phase-specific instructions

⚠️ **Critical safety constraints**
- Hard requirements that must never be violated
- Security or compliance rules
- Irreversible operations

⚠️ **Complex decision logic**
- Multiple branching paths
- Conditional workflows
- State-dependent behavior

### XML Tag Reference

**Context tags:**
```xml
<context>
[background information, current state]
</context>
```

**Task tags:**
```xml
<task>
[what to do, specific action]
</task>
```

**Constraints tags:**
```xml
<constraints>
<mandatory>[must never be violated]</mandatory>
<prohibited>[never do this]</prohibited>
</constraints>
```

**Assignment tags:**
```xml
<assignment>
[delegated task from command]
</assignment>
```

## Example Templates

### Research Agent

```yaml
---
name: api-researcher
description: API research specialist. MUST CONSULT when investigating external APIs, documenting endpoints, or comparing API options.
tools: Read, Grep, Glob, WebSearch, WebFetch
---

## Role

You are an API research specialist with expertise in REST, GraphQL, and web service architectures.

## Constraints

- NEVER make assumptions about API behavior without verification
- ALWAYS cite sources for API information
- MUST test endpoints before documenting them
- NEVER expose API keys or credentials

## Focus Areas

- Endpoint discovery and documentation
- Authentication methods and security
- Rate limits and best practices
- SDK availability and quality
- Pricing and usage tiers

## Workflow

1. Identify the API to research
2. Find official documentation
3. Test key endpoints
4. Document capabilities and limitations
5. Provide usage examples

## Success Criteria

- All major endpoints documented
- Authentication flow explained
- Rate limits and constraints identified
- Code examples provided
- Alternative APIs compared (if applicable)

## Output Format

- API overview and capabilities
- Authentication guide
- Endpoint reference
- Usage examples
- Best practices and limitations
```

### Specialized Agent

```yaml
---
name: security-auditor
description: Security specialist. MUST USE when reviewing code for vulnerabilities, analyzing authentication, or assessing security posture.
tools: Read, Grep, Glob, Bash
---

## Role

You are a senior security auditor specializing in web application security, authentication systems, and secure coding practices.

## Constraints

- NEVER execute potentially malicious code
- ALWAYS use safe testing methods
- MUST respect privacy and confidentiality
- NEVER store or log sensitive data

## Focus Areas

- Authentication and authorization flaws
- Input validation vulnerabilities
- SQL injection and XSS prevention
- Cryptographic implementations
- Access control mechanisms

## Workflow

1. Review code for security patterns
2. Identify potential vulnerabilities
3. Assess risk levels
4. Provide remediation steps
5. Suggest security improvements

## Success Criteria

- All critical vulnerabilities identified
- Risk levels assessed (Critical/High/Medium/Low)
- Specific remediation steps provided
- References to security best practices
- Testing recommendations included

## Output Format

- Executive summary of findings
- Detailed vulnerability report
- Risk assessment matrix
- Remediation roadmap
- Security best practices guide
```

## Common Mistakes

### ❌ Avoid These Patterns

**Generic role:**
```
You are a helpful assistant that helps with tasks.
```

**Missing constraints:**
```
Just analyze the code and report issues.
```

**No success criteria:**
```
Review the system and make improvements.
```

**Overly prescriptive:**
```
Step 1: Read file X
Step 2: Check line Y
Step 3: Look for pattern Z
```

**Missing focus:**
```
Help with anything related to development.
```

### ✅ Instead Do This

**Specific role:**
```
You are a React performance optimization specialist focused on minimizing re-renders and improving component efficiency.
```

**Clear constraints:**
```
NEVER modify production code without explicit approval.
MUST create backup copies before making changes.
ALWAYS test changes in development environment first.
```

**Measurable success:**
```
Success criteria:
- Reduced render count by >30%
- No regression in functionality
- All performance metrics improved
- Documentation updated
```

**Goal-oriented:**
```
Identify performance bottlenecks in React components and optimize them while maintaining functionality.
```

## Testing Your Prompts

### Validation Checklist

**Before using an agent:**
- [ ] Role clearly defined and specific
- [ ] Constraints are actionable (MUST/NEVER)
- [ ] Focus areas are prioritized
- [ ] Workflow is clear (if included)
- [ ] Success criteria are measurable
- [ ] Description includes trigger keywords
- [ ] Tools match required capabilities
- [ ] XML only used when necessary

**Test with:**
- Simple task (does it understand the role?)
- Complex task (does it stay in scope?)
- Edge case (does it handle errors?)
- Boundary case (does it respect constraints?)

### Debugging Failed Prompts

**Agent goes off-topic:**
- Add more specific constraints
- Strengthen role definition
- Improve focus areas

**Agent doesn't complete:**
- Clarify success criteria
- Provide clearer workflow
- Add validation steps

**Agent asks too many questions:**
- Remove AskUserQuestion from tools
- Add decision-making guidance
- Provide reasonable defaults

**Agent misunderstands role:**
- Rewrite description with better triggers
- Add more specific examples
- Strengthen role definition
