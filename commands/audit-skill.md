---
description: Audit skill for YAML compliance, pure XML structure, progressive disclosure, and best practices
argument-hint: <skill-path>
---

<objective>
Invoke the skill-auditor subagent to audit the skill(s) at $ARGUMENTS for compliance with Agent Skills best practices.

This ensures skills follow proper structure (pure XML, required tags, progressive disclosure) and effectiveness patterns.
This ensures referenced files follow proper structure and effectiveness patterns. This ensures files from the Skill(s) folder are properly integrated and referenced with relative path within the Skill(s) markdown file.

</objective>

<process>
1. Invoke skill-auditor subagent
2. 
2. Check for the $ARGUMENTS files related to the skill(s) and list all relative path from subfolder(s)/subfile(s). Pass skill(s) path: $ARGUMENTS and the relatives paths of files from the skill(s) folder
3. Subagent will read updated best practices (including pure XML structure requirements)
4. Subagent evaluates XML structure quality, required/conditional tags, anti-patterns and all the relevant files from the meta skill
5. Review detailed findings with file:line locations, compliance scores, and recommendations
</process>

<success_criteria>
- Subagent invoked successfully
- Arguments passed correctly to subagent
- Audit includes XML structure evaluation
- Audit include actionable sugestions
</success_criteria>
