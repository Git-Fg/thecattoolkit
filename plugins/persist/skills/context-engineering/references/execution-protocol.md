# Scribe Time-Server Protocol

## 1. Parse Request

**Extract from prompt:**
- `Request Type`: The context operation type (summarize-session, create-handoff, purge-context, archive-session)
- `Context`: The background information, parameters, and file locations
- `Priority`: Operation priority level

**Log receipt:**
```
[SCRIBE] Time-Server request received (isolated context)
- Request Type: [operation-type]
- Context Files: [paths-to-read]
- Priority: [level]
- Expected Output: [handoff-update]
- Hook System: Active (auto-load, auto-log, auto-compact)
```

**IMPORTANT - Hook System Integration:**
The context system now uses passive hooks for automatic management:
- SessionStart: Auto-loads plan and scratchpad (no initialization needed)
- PostToolUse: Auto-logs all Edit/Write/Bash operations
- PreCompact: Auto-compacts memory via compact_memory.py script

Your operations work with this existing infrastructure - do not duplicate hook functionality.

## 2. Load Skill Knowledge

**Action:** Read the appropriate context-engineering skill resources based on request type:

For session summary:
```
Read: context-engineering skill - references/session-summary.md
Read: context-engineering skill - templates/handoff.md
```

For handoff creation:
```
Read: context-engineering skill - references/handoff-protocol.md
Read: context-engineering skill - templates/handoff.md
```

For context purge/archive:
```
Read: context-engineering skill - references/scratchpad-maintenance.md
```

**Identify:**
- The specific workflow required
- Template structures needed
- File operations to perform
- Output format requirements

## 3. Execute Context Operation

### 3a: For Session Summarization
1. **Read Context Files**:
   - Read `.cattoolkit/context/scratchpad.md` (includes Recent Actions from hooks)
   - Read `.cattoolkit/context/todos.md`
   - Read `.cattoolkit/context/context.log` (recent raw actions)
   - Read `.cattoolkit/context/checkpoints/*.md` (auto-created by PreCompact hook)
   - _Note: Optionally check builder project status via `.cattoolkit/planning/{project}/PLAN.md`_

2. **Analyze Context**:
   - Count entries and estimate tokens
   - Assess context health across four dimensions
   - Identify key decisions and progress

3. **Generate Summary**:
   - Create session summary following template from session-summary.md
   - Calculate health score (Completeness, Relevance, Freshness, Conciseness)
   - Generate recommendations based on health score

4. **Write Outputs**:
   - Write summary to `.cattoolkit/context/session-summary-{timestamp}.md`
   - Write metrics to `.cattoolkit/context/session-metrics.json`
   - Update `.cattoolkit/context/context.log`
   - Update `.cattoolkit/context/todos.md`

### 3b: For Handoff Creation
1. **Pre-Handoff Checkpoint**:
   - Create checkpoint following handoff-protocol.md
   - Capture current state snapshot

2. **Compile Handoff Document**:
   - Gather all context data
   - Generate comprehensive handoff.md
   - Create tool-specific handoffs (claude.md, cursor.md)
   - Validate handoff quality

3. **Archive Context** (if requested):
   - Create session archive
   - Clean context files for next session

4. **Write Outputs**:
   - Main handoff: `.cattoolkit/context/handoff.md`
   - Tool handoffs: `.cattoolkit/context/handoff-{tool}.md`
   - Checkpoint: `.cattoolkit/context/checkpoints/{timestamp}-handoff-prep.md`
   - Archive: `.cattoolkit/context/archives/session-{timestamp}.tar.gz`
   - Summary: `.cattoolkit/context/handoff-summary.txt`

### 3c: For Context Purge
1. **Analyze Context Size**:
   - Read scratchpad.md and calculate size
   - Identify old entries to archive

2. **Archive Strategy**:
   - Move old entries to checkpoint
   - Keep recent entries in scratchpad
   - Create clean scratchpad

3. **Execute Purge**:
   - Create archive of old entries
   - Write cleaned scratchpad
   - Update context.log

### 3d: For Archive Session
1. **Gather Session Data**:
   - Read all context files
   - Collect metrics and summaries

2. **Create Archive**:
   - Package all session files
   - Create metadata file
   - Store in archives directory

3. **Generate Archive Report**:
   - Document archived content
   - List archive location
   - Update context.log

## 4. Update Handoff.md with Results

**For all operations**, update `.cattoolkit/context/handoff.md` with relevant results as per skill templates.

## 5. Exit Cleanly

**Time-Server pattern complete:**
Request processed in isolated context, results written to handoff.md, ready for main thread to continue.
