# Examples: Planning with Files in Action

This document provides real-world examples of the Planning with Files workflow in action.

## Example 1: Research Task - Morning Exercise Benefits

**User Request:** "Research the benefits of morning exercise and write a summary"

### Loop 1: Create Plan
```bash
Write task_plan.md
```

**task_plan.md:**
```markdown
# Task Plan: Morning Exercise Benefits Research

## Goal
Create a research summary on the benefits of morning exercise with scientific backing.

## Phases
- [x] Phase 1: Create this plan ✓
- [ ] Phase 2: Search and gather scientific sources
- [ ] Phase 3: Analyze and synthesize findings
- [ ] Phase 4: Create comprehensive summary
- [ ] Phase 5: Review and finalize

## Key Questions
1. What are the documented physical health benefits?
2. What mental health benefits have been studied?
3. What does recent research (2020-2025) show?
4. Are there any potential drawbacks?

## Expected Deliverable
- morning_exercise_summary.md (2-3 pages)
- Key statistics and study citations
- Actionable recommendations

## Status
**Currently in Phase 1** - Plan created, ready to research
```

### Loop 2: Research
```bash
# Always read the plan first
Read task_plan.md

# Gather information
WebSearch "morning exercise benefits scientific studies 2024"
WebSearch "exercise timing metabolism research"
Write notes.md

# Update progress
Edit task_plan.md
```

**notes.md:**
```markdown
# Notes: Morning Exercise Benefits

## Scientific Sources

### Study 1: Exercise Timing and Metabolism
- Journal: Cell Metabolism, 2024
- Key finding: Morning exercise increases fat oxidation by 20%
- Sample size: 30 participants
- Duration: 8 weeks

### Study 2: Mental Health and Exercise Timing
- Journal: Psychology of Sport and Exercise, 2024
- Key finding: Morning exercise improved mood scores by 15%
- Also improved sleep quality
- Sample size: 150 participants

### Study 3: Consistency in Exercise
- Journal: Sports Medicine, 2023
- Key finding: Morning exercise created more consistent routines
- Participants 3x more likely to stick to schedule
- Related to reduced decision fatigue

## Physical Benefits
- Increased fat oxidation
- Improved metabolism throughout day
- Better glucose control
- Enhanced muscle growth

## Mental Benefits
- Improved mood (15% increase in positive affect)
- Reduced anxiety
- Better focus and concentration
- More energy throughout day

## Potential Drawbacks
- Very early exercise may impact sleep if too intense
- Requires earlier bedtime
- Gym may be crowded at peak hours

## Questions to Investigate
- What time of morning is optimal?
- How long should sessions be?
- What types of exercise work best?
```

**Updated task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Create this plan ✓
- [x] Phase 2: Search and gather scientific sources ✓
- [ ] Phase 3: Analyze and synthesize findings
- [ ] Phase 4: Create comprehensive summary
- [ ] Phase 5: Review and finalize

## Errors Encountered
- None so far

## Status
**Currently in Phase 3** - Synthesizing research findings into structured summary
```

### Loop 3: Synthesize
```bash
Read task_plan.md
Read notes.md
Write morning_exercise_summary.md
Edit task_plan.md
```

**morning_exercise_summary.md:**
```markdown
# The Science-Backed Benefits of Morning Exercise

## Executive Summary

Recent scientific research (2023-2024) demonstrates significant physical and mental health benefits of morning exercise. Studies show 20% increase in fat oxidation, 15% improvement in mood scores, and 3x better adherence to workout routines compared to evening exercise.

## Physical Health Benefits

### Metabolism Enhancement
- **Fat Oxidation**: 20% increase in fat burning throughout the day
- **Glucose Control**: Better blood sugar regulation
- **Metabolic Rate**: Elevated for 6-8 hours post-exercise

### Research Evidence
Study from Cell Metabolism (2024) with 30 participants over 8 weeks showed consistent improvements in metabolic markers.

## Mental Health Benefits

### Mood and Mental Well-being
- **Positive Affect**: 15% increase in mood scores
- **Anxiety Reduction**: Measurable decrease in anxiety levels
- **Sleep Quality**: Paradoxically improved despite earlier wake time

### Cognitive Benefits
- Enhanced focus and concentration
- Improved decision-making throughout day
- Reduced decision fatigue

## Routine Adherence

### The Consistency Factor
Perhaps the most significant finding: Participants were **3x more likely** to maintain their exercise routine when scheduled in the morning.

**Why?**
- Fewer scheduling conflicts
- Reduced decision fatigue (work day hasn't started)
- Better sleep hygiene (earlier bedtime)
- Energy boost for the day ahead

## Optimal Timing and Approach

### Best Time
- 6:00 AM - 9:00 AM window appears most effective
- Allows time for post-exercise shower and breakfast
- Aligns with natural circadian rhythm

### Recommended Duration
- 30-45 minutes optimal
- Can be split into two sessions if needed

### Exercise Types
- Any consistent activity works
- Studies included: running, weight training, cycling, yoga
- Individual preference matters most

## Potential Drawbacks and Solutions

| Drawback | Solution |
|----------|----------|
| Early wake time | Gradual adjustment (15 min earlier per week) |
| Gym crowds | 7-8 AM optimal window, less crowded |
| Sleep impact | No intense exercise within 2 hours of bedtime |

## Actionable Recommendations

1. **Start Gradually**: Begin with 20-minute sessions
2. **Set Alarm Earlier**: Even on weekends to maintain rhythm
3. **Prepare Night Before**: Lay out clothes, pre-workout snack
4. **Choose Enjoyable Activities**: Consistency > intensity
5. **Track Benefits**: Journal energy/mood to see improvements

## Conclusion

The scientific evidence strongly favors morning exercise for both physical and mental health benefits, with the added advantage of significantly better adherence to workout routines. The key is gradual implementation and focusing on consistency rather than intensity.

## Sources
- Cell Metabolism, 2024: "Exercise Timing and Metabolic Health"
- Psychology of Sport and Exercise, 2024: "Morning Exercise and Mental Well-being"
- Sports Medicine, 2023: "Exercise Routine Adherence Patterns"
```

**Updated task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Create this plan ✓
- [x] Phase 2: Search and gather scientific sources ✓
- [x] Phase 3: Analyze and synthesize findings ✓
- [x] Phase 4: Create comprehensive summary ✓
- [ ] Phase 5: Review and finalize

## Deliverable Created
- morning_exercise_summary.md (comprehensive, 2 pages)
- Includes scientific citations
- Actionable recommendations
- Statistics and study references

## Status
**Currently in Phase 5** - Final review complete, ready to deliver
```

### Loop 4: Deliver
```bash
Read task_plan.md
Read morning_exercise_summary.md
# Verify all phases complete ✓
# Task ready to deliver!
```

---

## Example 2: Bug Fix Task - Authentication Login Bug

**User Request:** "Fix the login bug in the authentication module"

### Initial Plan
```bash
Write task_plan.md
```

**task_plan.md:**
```markdown
# Task Plan: Fix Login Bug

## Goal
Identify and fix the authentication bug preventing successful login.

## Phases
- [x] Phase 1: Understand bug report ✓
- [ ] Phase 2: Locate and examine authentication code
- [ ] Phase 3: Reproduce the bug
- [ ] Phase 4: Identify root cause
- [ ] Phase 5: Implement fix
- [ ] Phase 6: Test and verify
- [ ] Phase 7: Update documentation

## Bug Report Details
- User: Cannot log in after password reset
- Error: "Invalid credentials" even with correct password
- Frequency: Affects ~10% of users
- Recent change: Password reset flow modified last week

## Key Questions
1. What specific error message appears?
2. Which authentication endpoint is failing?
3. What changed in the password reset flow?
4. How can we reproduce reliably?

## Status
**Currently in Phase 2** - Examining authentication code
```

### Investigation Phase
```bash
Read task_plan.md
Glob "**/auth/*.ts"
Read src/auth/login.ts
Bash "npm run dev"  # Start dev server
Edit task_plan.md
```

**Updated task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Understand bug report ✓
- [x] Phase 2: Locate and examine authentication code ✓
- [ ] Phase 3: Reproduce the bug
- [ ] Phase 4: Identify root cause
- [ ] Phase 5: Implement fix
- [ ] Phase 6: Test and verify
- [ ] Phase 7: Update documentation

## Code Examination Findings
- Found: src/auth/login.ts (main login handler)
- Found: src/auth/validate.ts (validation logic)
- Error: TypeError: Cannot read property 'token' of undefined
- Location: validate.ts line 47

## Key Questions - Updated
1. ✓ What error: TypeError in validate.ts
2. ✓ Endpoint: POST /api/auth/login
3. ✓ Changed: Password reset now uses different token format
4. Need to reproduce to confirm hypothesis

## Status
**Currently in Phase 3** - Attempting to reproduce the bug
```

### Bug Reproduction
```bash
Read task_plan.md
Bash "npm test auth.test.js"
Write bug_reproduction.md
Edit task_plan.md
```

**bug_reproduction.md:**
```markdown
# Bug Reproduction Log

## Steps to Reproduce
1. User resets password via email link
2. User clicks email link
3. New password set successfully
4. User attempts login with new password
5. Error: "Invalid credentials"

## Expected Behavior
User should be able to login with new password

## Actual Behavior
TypeError: Cannot read property 'token' of undefined

## Environment
- Node.js: v18
- Browser: Chrome 120
- Test Date: 2026-01-11

## Additional Notes
- Works fine for existing users who haven't reset
- New users can register and login normally
- Password reset confirmation works
- Issue occurs AFTER reset, during login
```

**Updated task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Understand bug report ✓
- [x] Phase 2: Locate and examine authentication code ✓
- [x] Phase 3: Reproduce the bug ✓
- [ ] Phase 4: Identify root cause
- [ ] Phase 5: Implement fix
- [ ] Phase 6: Test and verify
- [ ] Phase 7: Update documentation

## Root Cause Hypothesis
Password reset changes token format from JWT to HMAC
validate.ts still expects JWT structure
Need to check token validation logic

## Errors Encountered
- [2026-01-11] TypeError in validate.ts line 47: user object undefined
  → Root cause: token format mismatch
  → Resolution: Update validation to handle both formats

## Status
**Currently in Phase 4** - Root cause identified, implementing fix
```

### Fix Implementation
```bash
Read task_plan.md
Read src/auth/validate.ts
Edit src/auth/validate.ts
Bash "npm test auth.test.js"
Edit task_plan.md
```

**Updated task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Understand bug report ✓
- [x] Phase 2: Locate and examine authentication code ✓
- [x] Phase 3: Reproduce the bug ✓
- [x] Phase 4: Identify root cause ✓
- [x] Phase 5: Implement fix ✓
- [ ] Phase 6: Test and verify
- [ ] Phase 7: Update documentation

## Fix Applied
File: src/auth/validate.ts
- Added compatibility check for token format
- Support both JWT and HMAC tokens
- Backwards compatible with existing tokens
- Added validation for new format

## Test Results
- ✓ All existing tests pass
- ✓ New test for password reset flow passes
- ✓ Manual testing successful

## Status
**Currently in Phase 6** - Comprehensive testing complete
```

### Final Verification
```bash
Read task_plan.md
Bash "npm run test:integration"
Write bug_fix_report.md
Edit task_plan.md
```

**bug_fix_report.md:**
```markdown
# Bug Fix Report: Authentication Login Issue

## Summary
Successfully fixed authentication bug affecting users after password reset.

## Root Cause
Password reset flow changed token format from JWT to HMAC, but validation logic still expected JWT structure, causing TypeError.

## Solution
Updated `src/auth/validate.ts` to:
1. Detect token format (JWT vs HMAC)
2. Use appropriate validation method
3. Maintain backwards compatibility
4. Add comprehensive error handling

## Files Modified
- src/auth/validate.ts (added token format detection)
- tests/auth.test.js (added password reset flow test)

## Testing
- ✓ All existing unit tests pass
- ✓ New integration test passes
- ✓ Manual testing with password reset flow successful
- ✓ Regression testing: no other auth flows affected

## Verification Steps
1. Create test account
2. Reset password via email
3. Login with new password
4. Result: ✅ Success, no errors

## Deployment
Ready for production deployment.
```

**Final task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Understand bug report ✓
- [x] Phase 2: Locate and examine authentication code ✓
- [x] Phase 3: Reproduce the bug ✓
- [x] Phase 4: Identify root cause ✓
- [x] Phase 5: Implement fix ✓
- [x] Phase 6: Test and verify ✓
- [x] Phase 7: Update documentation ✓

## Final Status
✅ **COMPLETE** - Bug fixed, tested, and documented
```

---

## Example 3: Feature Development - Dark Mode Toggle

**User Request:** "Add a dark mode toggle to the settings page"

### Initial Plan
```bash
Write task_plan.md
```

**task_plan.md:**
```markdown
# Task Plan: Dark Mode Toggle Implementation

## Goal
Add functional dark mode toggle to settings page with persistent theme switching.

## Phases
- [x] Phase 1: Create plan ✓
- [ ] Phase 2: Research existing theme system
- [ ] Phase 3: Design implementation approach
- [ ] Phase 4: Implement toggle component
- [ ] Phase 5: Add theme switching logic
- [ ] Phase 6: Test across components
- [ ] Phase 7: Polish UI/UX
- [ ] Phase 8: Test and document

## Key Questions
1. Does existing theme system exist?
2. What CSS approach is used (CSS-in-JS, custom properties, etc.)?
3. Where should toggle be placed in settings?
4. How to persist user preference?

## Expected Deliverable
- Dark mode toggle in settings page
- Smooth theme transitions
- Persistent preference (localStorage)
- Works across all components

## Status
**Currently in Phase 2** - Researching existing theme infrastructure
```

### Research Phase
```bash
Read task_plan.md
Glob "**/*theme*"
Glob "**/*dark*"
Glob "**/*style*"
Read src/styles/theme.ts
Write notes.md
Edit task_plan.md
```

**notes.md:**
```markdown
# Notes: Dark Mode Implementation Research

## Existing Theme System
Found: src/styles/theme.ts
- Uses: CSS custom properties (--primary-color, etc.)
- Current: Light theme only
- Good foundation for adding dark theme

## Implementation Approach Decision
Option A: Add dark theme properties
- Create: src/styles/dark-theme.ts
- Use: CSS custom properties for dark colors
- Update: All components to use CSS variables

Option B: CSS-in-JS styled-components
- More control per component
- Requires refactoring existing code
- More complex

Chosen: Option A (CSS custom properties)
Rationale: Minimal refactoring, maintainable, consistent

## Files to Modify
1. src/styles/theme.ts - Add dark theme CSS variables
2. src/components/Settings/Toggle.tsx - Create toggle
3. src/hooks/useTheme.ts - Create theme hook
4. src/App.tsx - Wrap with ThemeProvider

## Design Decisions
- Toggle position: Settings page, top section
- Theme persistence: localStorage key 'theme'
- Default: System preference (prefers-color-scheme)
- Transition: 0.3s ease for smooth switching
```

**Updated task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Create plan ✓
- [x] Phase 2: Research existing theme system ✓
- [x] Phase 3: Design implementation approach ✓
- [ ] Phase 4: Implement toggle component
- [ ] Phase 5: Add theme switching logic
- [ ] Phase 6: Test across components
- [ ] Phase 7: Polish UI/UX
- [ ] Phase 8: Test and document

## Implementation Approach
Using CSS custom properties (Option A)
- Minimal refactoring needed
- Consistent across components
- Easy to maintain

## Files to Modify
1. src/styles/theme.ts - Add dark theme
2. src/components/Settings/Toggle.tsx - New component
3. src/hooks/useTheme.ts - New hook
4. src/App.tsx - Wrap with provider

## Errors Encountered
- None so far

## Status
**Currently in Phase 4** - Building toggle component
```

### Implementation Phase
```bash
Read task_plan.md
Read src/styles/theme.ts
Edit src/styles/theme.ts
Write src/hooks/useTheme.ts
Write src/components/Settings/ThemeToggle.tsx
Edit task_plan.md
```

**Updated task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Create plan ✓
- [x] Phase 2: Research existing theme system ✓
- [x] Phase 3: Design implementation approach ✓
- [x] Phase 4: Implement toggle component ✓
- [x] Phase 5: Add theme switching logic ✓
- [ ] Phase 6: Test across components
- [ ] Phase 7: Polish UI/UX
- [ ] Phase 8: Test and document

## Implementation Progress
✓ Created dark theme CSS variables
✓ Built ThemeToggle component
✓ Implemented useTheme hook
✓ Added localStorage persistence
✓ Integrated with existing theme system

## Status
**Currently in Phase 6** - Testing theme across all components
```

### Testing and Refinement
```bash
Read task_plan.md
Bash "npm run dev"
Read src/App.tsx
Edit src/styles/theme.ts  # Fix transition issue
Edit task_plan.md
```

**Final Implementation Status:**
```markdown
## Phases
- [x] Phase 1: Create plan ✓
- [x] Phase 2: Research existing theme system ✓
- [x] Phase 3: Design implementation approach ✓
- [x] Phase 4: Implement toggle component ✓
- [x] Phase 5: Add theme switching logic ✓
- [x] Phase 6: Test across components ✓
- [x] Phase 7: Polish UI/UX ✓
- [x] Phase 8: Test and document ✓

## Final Status
✅ **COMPLETE** - Dark mode toggle fully implemented and tested

## Deliverables
- ✓ Dark mode toggle in settings
- ✓ Smooth theme transitions (0.3s)
- ✓ Persistent preference (localStorage)
- ✓ Works across all components
- ✓ Follows system preference by default
```

---

## Example 4: Error Recovery Pattern

### Scenario: API Goes Down Mid-Task

**Context:** Building a dashboard that fetches data from an external API

### Initial Plan
```bash
Write task_plan.md
```

**task_plan.md:**
```markdown
# Task Plan: Build Sales Dashboard

## Goal
Create real-time sales dashboard with data visualization.

## Phases
- [x] Phase 1: Create plan ✓
- [ ] Phase 2: Set up project structure
- [ ] Phase 3: Fetch data from API
- [ ] Phase 4: Build visualization components
- [ ] Phase 5: Add real-time updates
- [ ] Phase 6: Test and polish

## API Details
- Endpoint: https://api.sales.company.com/v1/sales
- Authentication: API key in header
- Update frequency: Every 30 seconds

## Status
**Currently in Phase 3** - Fetching data from API
```

### API Failure Occurs
```bash
Read task_plan.md
Read src/api/sales.ts
Bash "curl https://api.sales.company.com/v1/sales"
```

**Error Encountered:**
```
curl: (7) Failed to connect to api.sales.company.com port 443: Connection refused
```

### Error Logging and Recovery
```bash
Edit task_plan.md
```

**Updated task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Create plan ✓
- [x] Phase 2: Set up project structure ✓
- [ ] Phase 3: Fetch data from API (BLOCKED - API down)
- [ ] Phase 4: Build visualization components
- [ ] Phase 5: Add real-time updates
- [ ] Phase 6: Test and polish

## Errors Encountered
- [2026-01-11 14:32] API connection failed: api.sales.company.com unreachable
  → Connection refused (API may be down)
  → Status: Investigating alternative approaches

## Recovery Plan
1. Check API status page
2. If down, create mock data for development
3. Build components with mock data
4. Return to API integration when service restored

## Status
**Currently in Phase 3** - API unavailable, implementing mock data approach
```

### Creating Mock Data
```bash
Read task_plan.md
Write src/data/mockSales.ts
Edit src/api/sales.ts  # Use mock if API fails
Edit task_plan.md
```

**Updated task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Create plan ✓
- [x] Phase 2: Set up project structure ✓
- [x] Phase 3: Fetch data from API (IMPLEMENTED - with fallback) ✓
- [ ] Phase 4: Build visualization components
- [ ] Phase 5: Add real-time updates
- [ ] Phase 6: Test and polish

## Recovery Actions
✓ Created realistic mock sales data
✓ Implemented fallback in sales.ts API client
✓ Dashboard now works with or without API
✓ Progress not blocked by API downtime

## Status
**Currently in Phase 4** - Building visualization components with mock data
```

### Success Despite Obstacle
```bash
Read task_plan.md
Read src/components/Dashboard.tsx
Edit task_plan.md
```

**Final task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Create plan ✓
- [x] Phase 2: Set up project structure ✓
- [x] Phase 3: Fetch data from API (IMPLEMENTED - with fallback) ✓
- [x] Phase 4: Build visualization components ✓
- [x] Phase 5: Add real-time updates ✓
- [x] Phase 6: Test and polish ✓

## Final Status
✅ **COMPLETE** - Dashboard fully functional

## Key Learnings
- Fallback strategies prevent blockers
- Mock data enables parallel development
- Error recovery built resilience into the system
- API downtime didn't impact timeline

## Errors Overcome
- [2026-01-11] API downtime → Implemented mock data fallback
- Result: Development continued uninterrupted
```

**Lesson:** Logging errors in the plan file and documenting recovery actions transforms obstacles into learning opportunities and ensures progress continues.

---

## The Read-Before-Decide Pattern

### When to Use It

After many tool calls (20+), before any major decision:

```bash
# Context has grown, original goals may be fuzzy
[20 tool calls have happened...]
[Working on component X...]
[But what was the original goal?]

→ Read task_plan.md  # This refreshes goals in attention!
→ Now continue with fresh understanding
```

### Why It Works

1. **Attention Window**: Re-reading brings goals back into recent context
2. **Context Refresh**: 15-20 lines of plan vs 500 lines of history
3. **Goal Alignment**: Ensures decisions align with original objectives
4. **Progress Tracking**: See exactly where you are

### Example in Action

**Without Read-Before-Decide:**
```
[Working on data validation...]
[Building custom validator...]
[Adding TypeScript types...]
[User: "How's the login feature coming?"]
Claude: "...login feature? I was working on data validation."
[Context drifted - original goal forgotten]
```

**With Read-Before-Decide:**
```
[Read task_plan.md]
# Goal: "Implement user authentication system"
# Phase 3: Login functionality
# Currently: Working on data validation for login form

[Continue working with fresh context]
Claude: "I'm in Phase 3 - building login validation."
[Goal remains clear and focused]
```

### When to Re-Read

**Re-read when:**
- Starting a new component or feature
- Making design/architecture decisions
- Feeling uncertain about current state
- Switching between different aspects of work
- After 20-30 tool calls
- Before asking user questions

**Don't re-read for:**
- Quick file edits
- Simple searches
- Immediate next steps in same phase
- Following established patterns

### Quick Reference

```bash
# Before major decisions:
Read task_plan.md

# Before design choices:
Read task_plan.md
Read notes.md

# When feeling lost:
Read task_plan.md

# After interruption:
Read task_plan.md
```

## Advanced Pattern: Multi-Stream Research

### Organizing Parallel Research

When researching multiple related topics:

```bash
Write task_plan.md
Write notes.md
```

**task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Create plan ✓
- [ ] Phase 2: Research multiple topics
  - [ ] Topic A: [Status]
  - [ ] Topic B: [Status]
  - [ Topic C: [Status]
- [ ] Phase 3: Synthesize findings
- [ ] Phase 4: Create deliverable

## Research Streams
### Stream A: Technology Trends
- Focus: Latest developments
- Target: 5 sources

### Stream B: Best Practices
- Focus: Proven methodologies
- Target: 3 sources

### Stream C: Case Studies
- Focus: Real-world examples
- Target: 4 sources
```

**notes.md:**
```markdown
# Notes: Multi-Topic Research

## Stream A: Technology Trends
### Source 1
- Finding: [Detail]
- Source: [Citation]

### Source 2
- Finding: [Detail]
- Source: [Citation]

## Stream B: Best Practices
### Practice 1
- Description: [Detail]
- Source: [Citation]

## Stream C: Case Studies
### Case 1
- Company: [Name]
- Approach: [Detail]
- Results: [Detail]
```

**Updated task_plan.md:**
```markdown
## Phases
- [x] Phase 1: Create plan ✓
- [x] Phase 2: Research multiple topics ✓
  - [x] Topic A: Technology trends (5 sources) ✓
  - [x] Topic B: Best practices (3 sources) ✓
  - [x] Topic C: Case studies (4 sources) ✓
- [ ] Phase 3: Synthesize findings
- [ ] Phase 4: Create deliverable

## Research Complete
- Total: 12 sources across 3 streams
- Ready to synthesize into cohesive deliverable
```

## Conclusion

These examples demonstrate the power of Planning with Files:

1. **Structure**: Clear phases and checkboxes provide direction
2. **Persistence**: Work survives interruptions
3. **Recovery**: Errors become learning, not blockers
4. **Clarity**: Re-reading keeps goals fresh in attention
5. **Progress**: Visible advancement through phases

The pattern scales from simple research tasks to complex development workflows, always providing a foundation of clarity and organization.
