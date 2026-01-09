# Prompt Engineer Protocol

## 1. Parse Markdown Prompt

**Extract from prompt:**
- `# Context`: The background information and requirements
- `# Assignment`: What type of prompt to create/optimize

**Log receipt:**
```
[PROMPT-ENGINEER] Received Markdown prompt (isolated context)
- Context: [brief description]
- Assignment: [prompt task]
- Type: [single-prompt | meta-prompt | optimization]
```

## 2. Load Skill Knowledge

**Action:** Read the appropriate skill resources based on task:

For prompt creation:
Load the prompt-library skill templates and prompt-engineering skill patterns

For optimization:
Load the prompt-engineering skill techniques and optimization references

**Identify:**
- The specific template or pattern needed
- Step-by-step methodology for application
- Best practices and optimization techniques
- Output structure requirements

## 3. Apply Prompt Engineering

**For Single Prompts:**
1. Analyze the task requirements thoroughly

2. Apply the **Upgrade Path Protocol**:
   - Start with **Markdown First** (default)
   - Upgrade to **Hybrid XML/Markdown** ONLY if "Complexity Triggers" are met:
     - **Data Isolation:** >50 lines of raw data
     - **Constraint Weight:** Rules that MUST NEVER be broken
     - **Internal Monologue:** Complex reasoning requiring Chain-of-Thought
3. Select appropriate pattern from prompt-engineering skill
3. Apply the template from prompt-library skill
4. Optimize using techniques from prompt-engineering skill
5. Add concrete examples where helpful

**For Meta-Prompts:**
1. Design the chain structure (Research → Plan → Do → Refine)
2. Apply templates from prompt-library skill for each stage
3. Define dependencies between stages
4. Add YAML frontmatter and SUMMARY.md
5. Validate chain integration

**For Optimization:**
1. Analyze current prompt strengths and weaknesses
2. Apply optimization framework from prompt-engineering skill
3. Iterate with improvements
4. Document changes and reasoning

## 4. Structure Output

**Follow template structure from skills:**
- Use appropriate template from prompt-library/assets/templates/
- Apply **Signal-to-Noise Rule** for format decision
- Use XML tags (Max 15) ONLY for semantic envelopes
- Never nest XML tags
- Include concrete examples

## 5. Write Output to File

**Output locations:**
- Single prompts: `.cattoolkit/prompts/{number}-{name}.md`
- Prompt chains: `.cattoolkit/chains/{number}-{topic}/`
- Meta-prompts: `.cattoolkit/generators/{purpose}.md`
- Optimized prompts: Same location as original with `.v2` suffix or overwrite

**Validation:**
- Verify structure follows template
- Ensure XML tag limits respected
- Confirm examples are concrete and helpful
- Check for clarity and effectiveness

## 6. Log Completion

**Log success:**
```
[PROMPT-ENGINEER] Prompt engineering complete
- Type: [single | meta-prompt | optimization]
- Output: [file path]
- Key feature: [one-line summary]
```

**Report to orchestrator:**
Return a summary message with:
- Prompt type created/optimized
- Key features or improvements
- Location of output file(s)
