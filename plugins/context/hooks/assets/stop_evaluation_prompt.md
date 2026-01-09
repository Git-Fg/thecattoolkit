You are evaluating if Claude should stop working.

Analyze the session:
1. Is this a meaningful end of work session?
2. Has context been actively used (files edited, commands run)?
3. Is this a logout/pause or natural completion?

Extract your decision and reason into this EXACT XML structure:

<decision>
<approve>true</approve>
<reason>Brief explanation of why this session should/shouldn't stop</reason>
</decision>

CRITICAL REQUIREMENTS:
- You MUST include the <decision> tags in your response
- The <approve> tag must contain exactly "true" or "false"
- You may add explanation before or after the XML tags
- The XML tags must be present for the system to work correctly

Example format:
[Your analysis here]
<decision>
<approve>false</approve>
<reason>This session has active context usage and meaningful work</reason>
</decision>
[Additional context if needed]
