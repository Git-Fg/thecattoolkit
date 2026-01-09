You are evaluating if a subagent task completed successfully.

Check:
1. Was the subagent performing context operations (scribe agent, context management)?
2. Did it complete its task successfully?
3. Any errors that need addressing?

Extract your evaluation into this EXACT XML structure:

<evaluation>
<complete>true</complete>
<reason>Brief explanation of completion status</reason>
</evaluation>

CRITICAL REQUIREMENTS:
- You MUST include the <evaluation> tags in your response
- The <complete> tag must contain exactly "true" or "false"
- You may add explanation before or after the XML tags
- The XML tags must be present for the system to work correctly

Example format:
[Your analysis here]
<evaluation>
<complete>true</complete>
<reason>Scribe agent successfully created handoff document</reason>
</evaluation>
[Additional context if needed]
