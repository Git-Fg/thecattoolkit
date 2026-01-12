# Prompt Engineering & Orchestration Guide

This guide consolidates best practices for prompt engineering, agent orchestration, and system-level behaviors within the Cat Toolkit.

---

## 1. Core Principles

### Define a "Specialized Persona"
Never use a generic system prompt. Assign a specific job title, a set of allowed tools, and a mental framework.

**Best Practice:**
Define the **Role**, the **Domain**, and the **Success Criteria** immediately.

```markdown
You are a **Senior PostgreSQL Database Administrator**.
Your goal is to optimize query performance without altering the underlying data schema.

**Your Strengths:**
- Query plan analysis (EXPLAIN ANALYZE)
- Indexing strategies (B-Tree vs GIN/GiST)

**Success Criteria:**
- Reduced query execution time by >50%
- Zero downtime implementation
```

### Establish "Hard Boundaries"
Use "Negative Prompting" to prevent dangerous or unwanted behaviors.

**Best Practice:**
Explicitly forbid specific actions using upper case and "CRITICAL" markers.

```markdown
### OPERATIONAL BOUNDARIES
CRITICAL CONSTRAINTS:
1. NEVER output your internal reasoning to the final user.
2. DO NOT fix the bugs you find; only detect them.
```

### Professional Objectivity & Style
- **Tone:** Technical accuracy over user validation. Short, concise responses.
- **Style:** No unnecessary superlatives or emotional validation.
- **Emoji Policy:** Only use if explicitly requested.
- **Planning:** Concrete steps only; never suggest time estimates or timelines.

---

## 2. Environment & Context

### XML Usage & Budget
Wrap dynamic context in XML tags (`<context>`, `<env>`, `<file_contents>`) to distinguish instructions from data.

**The 5-8 Tag Rule:**
Limit prompts to **5-8 XML tag pairs maximum**. Excessive XML confuses models and wastes tokens.

| Priority | Tag Type | Purpose | Keep? |
|----------|----------|---------|-------|
| 1 (Essential) | `<env>` | Runtime context injection | Always |
| 2 (Essential) | `<example_correct>` / `<example_incorrect>` | Contrastive few-shot learning | Always |
| 3 (High) | `<sub_agents>` | Sub-agent definitions | Consolidate to 1 |
| 4 (Medium) | `<file_contents>` | File data separation | When needed |
| 5 (Low) | `<protocol>`, `<output_format>` | Structural wrappers | Convert to markdown |

### Dynamic Context Injection
Inject environment state (Git branch, OS, CWD) to ground the model in reality.

```markdown
<env>
Working directory: {{CWD}}
Is directory a git repo: {{YES/NO}}
Platform: {{PLATFORM}}
OS Version: {{VERSION}}
Today's date: {{DATE}}
</env>
```

---

## 3. Protocol & Workflow Orchestration

### Protocol Prerequisites
Force the model to follow a specific sequence. Dictate the **Order of Operations** and explain *why*.

```markdown
### DIAGNOSTIC PROTOCOL
Before recommending a solution, you MUST:
1. **Symptom Check:** Identify specific error logs.
2. **Hypothesis Generation:** List 3 potential causes.
3. **Verification:** Explain how you would verify the top hypothesis.
```

### Command Orchestration Example
Commands excel at orchestrating complex, multi-phase workflows using specialized sub-agents.

**Absolute Rules:**
1. **NEVER skip codebase exploration.**
2. **NEVER ask questions across multiple phases.** Consolidate into Phase 3.
3. **NEVER begin implementation without explicit user approval.**
4. **ALWAYS delegate specialized tasks to sub-agents.**

**Execution Protocol:**
- **Phase 1: Discovery:** Parse requirements, form mental model.
- **Phase 2: Exploration:** Launch **Parallel Explore Agents** to map architecture and patterns.
- **Phase 3: Question Burst:** Resolve ALL ambiguities in a single organized list.
- **Phase 4: Architecture Design:** Present options (Minimal vs Clean vs Pragmatic) with trade-offs.
- **Phase 5: Implementation:** WRITE mode following chosen architecture strictly.
- **Phase 6: Quality Review:** Launch **Parallel Review Agents** (Simplicity, Bugs, Conventions).
- **Phase 7: Summary:** Document accomplishments and key decisions.

---

## 4. Examples & Few-Shot Learning

### Contrastive Examples
Use `<example_correct>` and `<example_incorrect>` tags to teach nuance.

```markdown
<example_correct>
User: "The server is down."
Assistant: "I will check the Nginx logs to identify the error code."
</example_correct>

<example_incorrect>
User: "The server is down."
Assistant: "I will restart the server immediately."
Reasoning: Do not take action without diagnosing the root cause first.
</example_incorrect>
```

---

## 5. Official Reference: System Prompts

### Specialized Sub-Agents

#### The "Explore" Agent (Read-Only)
*Used for searching code and understanding architecture.*
- **Constraints:** STICKLY PROHIBITED from modifying files or system state.
- **Tools:** Glob (file patterns), Grep (regex search), Read (content), Bash (ls, git status/log).

#### The "Plan" Agent (Architect)
*Used to generate implementation steps.*
- **Process:** Understand requirements → Explore thoroughly → Design solution → Detail the plan.
- **Required Output:** End with "Critical Files for Implementation" list.

#### The "Bash" Agent
*Specialist for complex terminal operations.*
- **Guidelines:** Chain commands with `&&`, follow git safety, quote paths with spaces properly.

#### The "Claude Guide" Agent
*RAG Agent for documentation.*
- **Expertise:** Claude Code, Agent SDK, API.

#### The "Agent Architect" (Meta-Agent)
*Used to create new custom agents.*
- **Output:** JSON with `identifier`, `whenToUse`, and `systemPrompt`.

### Tool-Specific Protocols

- **MCP CLI:** You MUST call `mcp-cli info` BEFORE `mcp-cli call`. Schemas never match expectations.
- **AskUserQuestion:** Use at the **beginning of tasks** to gather requirements. Avoid mid-execution questions.
- **ExitPlanMode:** Signal completion of planning; triggers user approval.
- **Browser Tools:** Consult screenshots via `computer` before clicking; use `read_page` for accessibility trees.

---

## 6. Special Output & Maintenance Modes

### Output Styles
- **Explanatory Style:** Provide educational insights about the codebase using the `* Insight ──` format.
- **Learning Style:** Encourage "Learn by Doing" by requesting 2-10 line human contributions.

### Magic Doc Updater
Mandatory maintenance tool. Update document in-place, BE TERSE, high signal only. Focus on WHY things exist and WHERE to start reading.

### Session Quality Classifier
Internal sentiment analysis tracking `<frustrated>` state and `<pr_request>` intent.

---

## 7. Optimization for 2026 Standards

### Skill Archetypes
- **Task-Oriented:** Action verbs, gerund names (`deploying-app`), Execute → Validate → Report pattern.
- **Knowledge-Oriented:** Domain nouns (`prompt-engineering`), Query → Load context → Synthesize pattern.

### Validator Pattern
Task-Oriented Skills MUST include an autonomous correction loop (max 3 iterations) before returning control.

### Visibility Control
- `user-invocable: false`: Hides from `/` menu but remains semantically discoverable.
- `disable-model-invocation: true`: Excludes from ~15k token budget and blocks spontaneous AI invocation.

---

### Summary Checklist for a "Claude Code" Style Prompt:

1.  **Identity:** "You are an Elite [Role]..."
2.  **Context:** "<env>...</env>"
3.  **Constraints:** "CRITICAL: DO NOT..."
4.  **Protocol:** "You MUST perform step A before step B..."
5.  **Examples:** "<example>...</example>"
6.  **Output Format:** "Respond ONLY with..."
7.  **XML Budget:** Max 5-8 tag pairs