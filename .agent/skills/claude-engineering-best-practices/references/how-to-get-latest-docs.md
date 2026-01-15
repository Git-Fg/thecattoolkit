# How to Get Latest Documentation

This guide explains how to retrieve the most up-to-date information for volatile details that change frequently.

## Why Look Up Latest Docs?

Some details in Claude Code and Claude Dev change frequently:
- API field names in JSON schemas
- Command-line flags and options
- Hook event schemas (input/output structures)
- Plugin.json required/optional fields
- MCP protocol versions
- Tool permission lists
- Network domain blocklists

**Never hardcode these details** - always verify in the latest documentation.

## Source of Truth

### Claude Code (Terminal)
- **Master index**: `https://code.claude.com/docs/llms.txt`
- **Documentation base**: `https://code.claude.com/docs/en/`
- **Key files**:
  - Plugins reference: `plugins-reference.md`
  - Hooks: `hooks.md`
  - Sandboxing: `sandboxing.md`
  - Settings: `settings.md`

### Claude Dev (Platform)
- **Master index**: `https://platform.claude.com/docs/llms.txt` (or use `llms_claude_dev_code.txt`)
- **Documentation base**: `https://platform.claude.com/docs/en/`
- **Key files**:
  - Agent SDK: `agent-sdk/overview.md`
  - Tool use: `agents-and-tools/tool-use/overview.md`
  - Agent Skills: `agents-and-tools/agent-skills/overview.md`

## Standard Lookup Workflow

### Step 1: Find the URL

Use the llms.txt index to find the correct URL:

```bash
# For Claude Code docs
rg -n "pattern.*\.md" references/sources/llms_claude_code.txt

# For Claude Dev docs
rg -n "pattern.*\.md" references/sources/llms_claude_dev_code.txt
```

### Step 2: Fetch the Document

```bash
# Fetch the raw markdown
curl -sL "https://code.claude.com/docs/en/plugins-reference.md"

# Fetch and search for specific pattern
curl -sL "https://code.claude.com/docs/en/hooks.md" | rg -A 5 -B 5 "PreToolUse"
```

### Step 3: Extract Specific Information

```bash
# Extract just the schema section
curl -sL "URL.md" | rg -A 20 "## Schema"

# Extract field names
curl -sL "URL.md" | rg -o "\"fieldName\":\s*\"[^\"]+\"" | sort -u

# Extract code examples
curl -sL "URL.md" | rg -A 10 "```json"
```

## Common Lookup Patterns

### Plugin.json Schema

```bash
# Find the plugin reference URL
rg -n "plugins-reference" references/sources/llms_claude_code.txt

# Extract the schema
curl -sL "https://code.claude.com/docs/en/plugins-reference.md" | rg -A 30 "## Plugin manifest schema"

# Extract field details
curl -sL "https://code.claude.com/docs/en/plugins-reference.md" | rg -A 5 "Required fields"
```

### Hook Events

```bash
# Get hooks reference URL
rg -n "hooks\.md" references/sources/llms_claude_code.txt

# List all hook events
curl -sL "https://code.claude.com/docs/en/hooks.md" | rg "^### " | sed 's/^### //'

# Get specific event details
curl -sL "https://code.claude.com/docs/en/hooks.md" | rg -A 20 "^### PreToolUse"
```

### Agent SDK Hooks

```bash
# Get Agent SDK URL
rg -n "agent-sdk/overview" references/sources/llms_claude_dev_code.txt

# Find hook information
curl -sL "https://platform.claude.com/docs/en/agent-sdk/overview.md" | rg -A 10 "Hooks"

# Get full hooks reference
curl -sL "https://platform.claude.com/docs/en/agent-sdk/hooks.md" | rg -A 5 "PreToolUse\|PostToolUse"
```

### Tool Use Patterns

```bash
# Find tool use reference
rg -n "tool-use/overview" references/sources/llms_claude_dev_code.txt

# Extract tool examples
curl -sL "https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md" | rg -A 15 "## Tool use examples"
```

## Verification Rules

### Rule 1: Always Check Date

```bash
# Check if doc has been updated recently
curl -sL "URL.md" | rg -i "last updated|changelog" | head -5
```

### Rule 2: Cross-Reference Multiple Sources

```bash
# Verify info appears in multiple places
curl -sL "URL1.md" | rg "fieldName"
curl -sL "URL2.md" | rg "fieldName"
```

### Rule 3: Test in Safe Environment

Before implementing:
1. Create a minimal test case
2. Verify behavior matches documentation
3. Check for deprecation warnings

## Network Restrictions Handling

### If curl is Blocked

If network access is restricted:

1. **Check permissions**: Verify domain is in allowed list
   ```bash
   # In Claude Code settings
   "allowedDomains": ["code.claude.com", "platform.claude.com"]
   ```

2. **Use alternative tools**:
   - `WebFetch` MCP tool (if available)
   - Local cached copies in `references/sources/`

3. **Request permission**: Ask user to whitelist domain

4. **Fallback to local references**: Use files in `references/sources/` as last resort

### Sandbox Constraints

```bash
# Check if curl is allowed
rg -n "curl" ~/.claude/settings.json

# Or check in project settings
rg -n "curl" .claude/settings.json
```

If curl is blocked and domain is not allowed:
- Document the limitation
- Use local reference files
- Mark details as "requires verification"

## Decision Matrix

| Situation | Action |
|-----------|--------|
| curl succeeds, returns 200 | Use fetched data, cite source |
| curl succeeds, but domain not in whitelist | Document limitation, use local refs |
| curl fails (network error) | Use local refs, mark as "needs update" |
| curl fails (403/permission) | Request domain whitelist, use local refs |
| curl times out | Retry once, then use local refs |

## Best Practices

### Do's
- ✅ Always fetch latest docs for volatile details
- ✅ Verify field names, schemas, flags
- ✅ Check for deprecation notices
- ✅ Cross-reference multiple sources
- ✅ Document when docs were fetched
- ✅ Cache results if network is slow

### Don'ts
- ❌ Never hardcode version-specific details
- ❌ Don't assume fields are required (verify)
- ❌ Don't skip verification "to save time"
- ❌ Don't use cached docs older than 1 month
- ❌ Don't implement based on outdated info

## Quick Reference

### Most Common Lookups

```bash
# Plugin.json required fields
curl -sL "https://code.claude.com/docs/en/plugins-reference.md" | rg -A 10 "Required fields"

# Hook event schemas
curl -sL "https://code.claude.com/docs/en/hooks.md" | rg -A 20 "PreToolUse Input"

# Agent SDK hooks
curl -sL "https://platform.claude.com/docs/en/agent-sdk/hooks.md" | rg -A 10 "PreToolUse\|PostToolUse"

# Tool permissions
curl -sL "https://platform.claude.com/docs/en/agent-sdk/permissions.md" | rg -A 5 "allowed_tools\|permission_mode"

# Sandbox domains
curl -sL "https://code.claude.com/docs/en/sandboxing.md" | rg -A 10 "domain|network"
```

### Emergency Fallbacks

If you cannot fetch docs:

1. Use local index files in `references/sources/`
2. Search existing thematic files in `references/claude-*/`
3. Mark uncertain details with ⚠️ notation
4. Recommend manual verification

## Examples

### Example 1: Verifying Plugin.json Fields

```bash
# Find URL
$ rg -n "plugins-reference" references/sources/llms_claude_code.txt
39:https://code.claude.com/docs/en/plugins-reference.md

# Fetch and extract
$ curl -sL "https://code.claude.com/docs/en/plugins-reference.md" | rg -A 30 "## Plugin manifest schema"

# Verify required vs optional
$ curl -sL "URL" | rg -E "Required fields|Optional fields" -A 20
```

### Example 2: Checking Hook Event Schema

```bash
# Find URL
$ rg -n "hooks\.md" references/sources/llms_claude_code.txt
22:https://code.claude.com/docs/en/hooks.md

# Get event list
$ curl -sL "https://code.claude.com/docs/en/hooks.md" | rg "^### "
PreToolUse
PostToolUse
Notification
UserPromptSubmit
Stop
SubagentStop
PreCompact
SessionStart
SessionEnd

# Get specific event details
$ curl -sL "URL" | rg -A 30 "^### PreToolUse"
```

### Example 3: Agent SDK Permissions

```bash
# Find URL
$ rg -n "agent-sdk/permissions" references/sources/llms_claude_dev_code.txt

# Extract permission modes
$ curl -sL "URL" | rg -A 10 "permission_mode"
```

## Maintenance

### Monthly Checks
- Review frequently-used URLs for updates
- Update local llms.txt files if needed
- Check for deprecated features

### When Changes Detected
1. Update relevant thematic reference files
2. Note the change in the file header
3. Update lookup commands if URLs changed
4. Alert users of breaking changes

Remember: **Accuracy > Speed**. Taking 30 seconds to verify can save hours of debugging.

---

## Official Documentation Links

### Master Indexes
- **Claude Code Documentation Index**: https://code.claude.com/docs/llms.txt
- **Claude Dev Platform Documentation Index**: https://platform.claude.com/docs/llms.txt

### Key Reference Documents
- **Claude Code Plugin Components**: https://code.claude.com/docs/en/plugins-reference.md
- **Claude Code Hooks**: https://code.claude.com/docs/en/hooks.md
- **Claude Code Sandboxing**: https://code.claude.com/docs/en/sandboxing.md
- **Claude Code Settings**: https://code.claude.com/docs/en/settings.md
- **Agent SDK Overview**: https://platform.claude.com/docs/en/agent-sdk/overview.md
- **Agent Skills**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md
- **Tool Use**: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md

### Verification
This guide was last verified against the official documentation on 2026-01-13. Always check the latest docs for current information.
