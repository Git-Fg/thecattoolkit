### 1. Define a "Specialized Persona" (Not just "Helpful Assistant")
The tool never uses a generic system prompt. It assigns a specific job title, a set of allowed tools, and a mental framework.

**From the Source (`Agent Architect` prompt):**
> *"You are an elite AI agent architect... Your expertise lies in translating user requirements into precisely-tuned agent specifications..."*

**Best Practice:**
Define the **Role**, the **Domain**, and the **Success Criteria** immediately.

**Example Prompt:**
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

---

### 2. Establish "Hard Boundaries" (Negative Constraints)
The tool uses "Negative Prompting" extensively to prevent dangerous behaviors. The "Explore" agent is a prime example of this—it is psychologically "sandbox" by the prompt before it is technically sandboxed by the code.

**From the Source (`Explore Agent` prompt):**
> *"=== CRITICAL: READ-ONLY MODE - NO FILE MODIFICATIONS ===*
> *You are STRICTLY PROHIBITED from:*
> *- Creating new files*
> *- Modifying existing files*
> *- Running ANY commands that change system state"*

**Best Practice:**
Do not just ask the model to do X; explicitly forbid it from doing Y, Z, and Q. Use upper case and "CRITICAL" markers.

**Example Prompt:**
```markdown
### OPERATIONAL BOUNDARIES
You are in **Audit Mode**.

CRITICAL CONSTRAINTS:
1. NEVER output your internal reasoning to the final user; only output the JSON result.
2. DO NOT fix the bugs you find. You are a detector, not a fixer.
3. DO NOT invent URLs. If a URL is not present in the source text, output null.
```

---

### 3. Inject Dynamic Context via XML Tags (Parsimoniously)
The tool injects the environment state (Git branch, OS, CWD) into every request. This grounds the model in reality.

**From the Source (`Main Loop` prompt):**
> *"Here is useful information about the environment... <env> Working directory: /src... Is directory a git repo: Yes... </env>"*

**Best Practice:**
Wrap dynamic context in XML tags (`<context>`, `<env>`, `<file_contents>`). This helps the model distinguish between your instructions and the data it needs to process.

> [!IMPORTANT]
> **Limit to 5-8 XML tag pairs maximum.** Excessive XML confuses some LLMs and increases token count. See Section 7 for prioritization.

**Example Prompt:**
```markdown
I need you to write a unit test for the following component.

<env>
Framework: React 18
Testing Library: Vitest + React Testing Library
TypeScript: Strict Mode
</env>

<file_contents filename="UserProfile.tsx">
export const UserProfile = ({ user }) => <div>{user.name}</div>;
</file_contents>

Please write the test file.
```

---

### 4. Enforce "Protocol Prerequisites" (Chain of Thought)
The tool forces the model to follow a specific sequence of operations before taking action. The MCP (Model Context Protocol) prompt is the best example: it forces the model to read a schema before calling a tool.

**From the Source (`MCP tool` prompt):**
> *"MANDATORY PREREQUISITE... You MUST call 'mcp-tool info' BEFORE ANY 'mcp-tool call'. Why this is non-negotiable: Tool schemas NEVER match your expectations."*

**Best Practice:**
If a task is complex, dictate the **Order of Operations**. Explicitly tell the model *why* it must follow this order to prevent "lazy" guessing.

**Example Prompt:**
```markdown
### DIAGNOSTIC PROTOCOL
Before recommending a solution, you MUST follow this sequence:

1. **Symptom Check:** specificy exactly which error logs you are analyzing.
2. **Hypothesis Generation:** List 3 potential causes.
3. **Verification:** Explain how you would verify the top hypothesis.

ONLY after these 3 steps are complete may you propose a code fix.
```

---

### 5. Use XML-Structured Few-Shot Examples
The tool avoids vague examples. It uses `<example>` and `<bad-example>` tags to demonstrate exactly how the model should (and should not) behave.

**From the Source (`Bash` tool prompt):**
> *<bad-example>*
> *User: Use the slack tool*
> *Assistant: [Calls slack/search directly]*
> *WRONG - You must call mcp-tool info for ALL tools before making ANY call*
> *</bad-example>*

**Best Practice:**
Provide "Contrastive Examples." Show a "Good" interaction and a "Bad" interaction. This teaches the model the nuance of your requirements.

**Example Prompt:**
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

---

### 6. The "Plan Mode" Workflow (State Machines)
The tool switches the model into a "Plan Mode" where it cannot execute code, only write to a `PLAN.md`. This separates "Thinking" from "Doing."

**From the Source (`Plan Mode` prompt):**
> *"Phase 1: Initial Understanding... Phase 2: Design... Phase 4: Final Plan... This is the only file you are allowed to edit."*

**Best Practice:**
For complex tasks, create a **Phased Workflow**. Ask the model to output a plan to a specific artifact (like a scratchpad or a `<thinking>` block) before it attempts to generate the final output.

**Example Prompt:**
```markdown
### EXECUTION PHASES

**Phase 1: Analysis**
Read the provided CSV data. Identify outliers and missing values. Output your findings in a <analysis> tag.

**Phase 2: Strategy**
Based on Phase 1, determine the best imputation method for missing values.

**Phase 3: Code Generation**
Write the Python Pandas code to clean the dataset based on the Phase 2 strategy.
```

---

### Summary Checklist for a "Claude Code" Style Prompt:

1.  **Identity:** "You are an Elite [Role]..."
2.  **Context:** "<env>...</env>"
3.  **Constraints:** "CRITICAL: DO NOT..."
4.  **Protocol:** "You MUST perform step A before step B..."
5.  **Examples:** "<example>...</example>"
6.  **Output Format:** "Respond ONLY with..."
7.  **XML Budget:** Max 5-8 tag pairs

---

### 7. Parsimonious XML Usage (LLM Compatibility)

Not all LLMs handle XML equally well. Excessive or nested XML tags can confuse models, increase token consumption, and reduce prompt portability.

**The 5-8 Tag Rule:**
Limit your prompt to **5-8 XML tag pairs maximum**. Prioritize tags by semantic value.

**XML Tag Priority Matrix:**

| Priority | Tag Type | Purpose | Keep? |
|----------|----------|---------|-------|
| 1 (Essential) | `<env>` | Runtime context injection | Always |
| 2 (Essential) | `<example_correct>` / `<example_incorrect>` | Contrastive few-shot learning | Always |
| 3 (High) | `<sub_agents>` or `<agent_persona>` | Sub-agent definitions | Consolidate to 1 |
| 4 (Medium) | `<file_contents>` | File data separation | When needed |
| 5 (Low) | `<protocol>`, `<output_format>` | Structural wrappers | Convert to markdown |

**What to Convert to Markdown:**
- `<persona>` → **Bold header**
- `<success_criteria>` → **Numbered list**
- `<protocol>` → Steps listed directly
- `<output_format>` → Inline code block or table
- `<prerequisites>` → Checkbox list

**Bad (11+ tag pairs):**
```markdown
<persona>...</persona>
<success_criteria>...</success_criteria>
<env>...</env>
<agent_persona type="Explore">...</agent_persona>
<protocol>...<agent_dispatch>...</agent_dispatch>...</protocol>
<example_correct>...</example_correct>
<example_incorrect>...</example_incorrect>
<agent_persona type="Plan">...<output_format>...</output_format>...</agent_persona>
```

**Good (6 tag pairs):**
```markdown
**Your Strengths:** [markdown list]
**Success Criteria:** [markdown list]

<env>...</env>

<sub_agents>
[All agent personas consolidated here]
</sub_agents>

<example_correct>...</example_correct>
<example_incorrect>...</example_incorrect>
```

**Why This Matters:**
- **GPT-4/GPT-4o:** Handles XML well, but nested tags reduce attention efficiency
- **Claude:** Native XML support, but excessive nesting still wastes tokens
- **Gemini:** Less reliable XML parsing; simpler is better
- **Llama/Mistral:** Variable XML support; flat structures work best