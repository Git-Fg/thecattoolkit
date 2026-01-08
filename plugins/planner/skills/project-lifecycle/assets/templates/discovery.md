# Discovery Findings Template

## MANDATORY USAGE

**YOU MUST USE THIS TEMPLATE** when creating `.cattoolkit/planning/{project-slug}/DISCOVERY.md`.

**Scoped Folder:** ALWAYS use scoped project folder `{project-slug}` (e.g., `user-auth-system`)

**Related Files:**
- `@.cattoolkit/planning/{project-slug}/BRIEF.md` - Project brief
- `@.cattoolkit/planning/{project-slug}/ROADMAP.md` - Project roadmap

## Discovery Document Structure

```markdown
# Discovery Findings: [Project Name]

**Date:** YYYY-MM-DD
**Discovery Phase:** [Phase name or number]
**Plan Type:** [Lite / Standard]

## Executive Summary

[2-3 sentences summarizing what was discovered and the direction forward]

## Project Understanding

### Problem Space
[What problem are we solving?]

### Current State (if applicable)
[For brownfield projects - describe existing system]

### Key Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## Findings

### Technical Architecture
[Current or proposed architecture understanding]

### Dependencies & Constraints
- [Dependency 1]
- [Constraint 1]

### Risks Identified
- [Risk 1] → [Mitigation strategy]
- [Risk 2] → [Mitigation strategy]

### Opportunities
- [Opportunity 1]
- [Opportunity 2]

## Decisions Made

1. **[Decision]** - Rationale: [Why this decision was made]

2. **[Decision]** - Rationale: [Why this decision was made]

## Questions Resolved

| Question | Answer | Notes |
|----------|--------|-------|
| [Question 1] | [Answer] | [Context] |
| [Question 2] | [Answer] | [Context] |

## Questions Remaining

| Question | Impact | Decision Needed By |
|----------|--------|-------------------|
| [Question 1] | [High/Med/Low] | [Phase/Date] |
| [Question 2] | [High/Med/Low] | [Phase/Date] |

## Recommendations

### Immediate Actions
- [ ] [Action 1]
- [ ] [Action 2]

### Future Considerations
- [Consideration 1]
- [Consideration 2]

## Context Sources

**Files Analyzed:**
- [File 1]
- [File 2]

**Stakeholder Input:**
- [Source 1]
- [Source 2]

**External Research:**
- [Research 1]
- [Research 2]

---

**Status:** ✅ Discovery Complete
**Next Phase:** [Brief / Roadmap / Plan Author]
**Created by:** [Agent Name]
**Last Updated:** YYYY-MM-DD
```

## MANDATORY Guidelines

**Content Requirements:**
- MUST capture ALL findings from discovery phase
- MUST document decisions and rationale
- MUST identify risks and opportunities
- MUST track resolved and remaining questions
- MUST provide clear recommendations

**Structure Requirements:**
- MUST use this exact template structure
- MUST be self-contained (no external context needed)
- MUST use @ references for any file context
- MUST be concise but comprehensive (under 200 lines)

**Workflow Integration:**
- Created AFTER Requirements Gathering phase
- BEFORE Plan Author is invoked
- Serves as truth source for planning
- Referenced in @BRIEF.md if needed

## Discovery vs Brief

**DISCOVERY.md captures:**
- The process and findings
- What was learned during analysis
- Decisions made and why
- Questions and answers

**BRIEF.md captures:**
- The project definition
- Success criteria
- Constraints and scope
- User-facing narrative

Both are created during planning, but DISCOVERY.md is the "how we got here" and BRIEF.md is "where we're going."
