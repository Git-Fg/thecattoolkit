# Usage and Workflow

## Quick Start
1. **Intake** - Determine purpose (Do/Plan/Research/Refine)
2. **Generate** - Create prompt using purpose-specific templates
3. **Execute** - Run prompt with dependency-aware execution
4. **Validate** - Verify output and create summary

### Directory Structure
```
.prompts/
├── 001-topic-research/
│   ├── 001-topic-research.md     # Prompt
│   ├── topic-research.md         # Output
│   └── SUMMARY.md                # Human summary
├── 002-topic-plan/
│   ├── 002-topic-plan.md
│   ├── topic-plan.md
│   └── SUMMARY.md
```

## Usage Examples

### Create Research Prompt
```
/create-meta-prompt research authentication options for the app
```
**What it does:**
- Determines this is a Research task
- Scans for existing research files to reference
- Creates prompt with research-specific structure
- Saves to `.prompts/{number}-{topic}-research/`
- Executes with validation

### Create Planning Prompt
```
/create-meta-prompt plan the auth implementation approach
```
**What it does:**
- Detects existing auth-research.md
- Asks if it should reference the research
- Creates plan prompt with research context
- Runs after research completes

### Create Execution Prompt
```
/create-meta-prompt implement JWT authentication
```
**What it does:**
- References both research and plan
- Creates implementation prompt
- Includes verification steps
