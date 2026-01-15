# Tool Prompt Template

> **Description:** {Brief description of what the tool does}

> **Instructions:**
> - {Instruction 1}
> - {Instruction 2}
> - {Instruction 3}

**When NOT to use:** {When this tool should not be used}

**When to use:** {When this tool should be used}

**Inputs:** {What parameters are required}

**Outputs:** {What the tool returns}

<example_correct>
{Example of correct tool usage}
</example_correct>

<example_incorrect>
{Example of incorrect tool usage}
**Reasoning:** {Why this is incorrect}
</example_incorrect>

## Protocol-Specific Templates

### For Multi-Step Tools

**MANDATORY PREREQUISITE - THIS IS A HARD REQUIREMENT**
You MUST {prerequisite step} BEFORE {main action}.

**Why:** {Explanation of why this is necessary}

**Flow:**
1. {Step 1}
2. {Step 2} (**REQUIRED**)
3. {Step 3}

### For Specialized Tools

**Domain:** {Specific domain (e.g., Database, API, CLI)}
**Expertise:** {What the tool excels at}

Your role is to {primary function}.

### For Interactive Tools

**Usage:**
- {Usage pattern 1}
- {Usage pattern 2}
- {Usage pattern 3}

**Error Handling:**
- If {error condition}, then {action}
- If {error condition}, then {action}
