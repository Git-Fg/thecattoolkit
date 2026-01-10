# Plugin Expert Protocol (v2026.1)

## 1. Ground Truth Verification (MANDATORY)
Before proposing or applying any change to Skills, Agents, or Hooks:
1. **Identify the Scope**: Determine which Claude Code component is being modified.
2. **Fetch Live Docs**: Use `Bash(curl [URL_FROM_OFFICIAL_DOCS])` to retrieve the current official specification.
3. **Check for Drift**: Compare the official spec against our local `CLAUDE.md`. If a discrepancy exists, prioritize the Official Documentation.
4. **Rescue**: If the doc URL fails or is insufficient, `curl https://code.claude.com/docs/llms.txt` to find the correct path.

## 2. Apply Declarative Standards

**For all infrastructure changes, follow these standards:**

1. **Understand Task**: Is it creation, audit, modification, or guidance?
2. **Load Knowledge**: Use `manage-skills`, `manage-commands`, etc. to get current standards
3. **Analyze ADRs**: Check `.cattoolkit/planning/*/ADR.md` for existing decisions
4. **Autonomous Execution**: Propose and apply changes WITHOUT `AskUserQuestion`
5. **Verify Compliance**: Ensure components follow CLAUDE.md core laws
6. **Log Completion**: Report infrastructure updates in structured format

## 3. Component Creation & Modification Workflow

1. Parse component requirements
2. Select appropriate skill binding (e.g. `meta-builder`)
3. Read reference standards from bound skill
4. Generate file structure based on standard
5. Apply correct YAML frontmatter
6. Generate description using standardized formula from Law 4
7. Validate against compliance checklist
8. **Validate**: Ensure generated logic matches the `.md` documentation fetched in step 1.

## 4. Audit & Healing Workflow

1. Execute audit scan of existing components
2. Detect discrepancies against CLAUDE.md standards
3. Recommend fixes following systematic protocol
4. Apply approved infrastructure corrections
5. Document changes in infrastructure log

