# Hook Deployment Guide

## Overview

Hooks can be deployed in two ways:

1. **Dynamic Path Deployment (Recommended)** - Scripts use environment variables
2. **Static Path Deployment** - Scripts are copied to project with absolute paths

## Problem with Dynamic Paths

Using `${CLAUDE_PLUGIN_ROOT}` in hooks.json requires:
- Environment variable to be set in shell profile
- Plugin installation location to remain constant
- Variable to be available in all contexts

This creates deployment fragility:
- Hooks fail silently if variable not set
- MCP server crashes if variable not available
- Difficult to debug when environment differs

## Static Path Deployment (Solution)

The **Static Path Deployment** approach eliminates environment variable dependencies:

### Step 1: Copy Scripts to Project

```bash
# Create hooks directory
mkdir -p .cattoolkit/hooks/scripts

# Copy scripts from plugin to project
cp /path/to/plugins/guard-python/hooks/scripts/*.py .cattoolkit/hooks/scripts/
cp /path/to/plugins/guard-ts/hooks/scripts/*.js .cattoolkit/hooks/scripts/

# Set execute permissions
chmod +x .cattoolkit/hooks/scripts/*
```

### Step 2: Generate hooks.json with Absolute Paths

Create `.cattoolkit/hooks/hooks.json` with ABSOLUTE PATHS:

**For Python (guard-python):**
```json
{
  "description": "Guard hooks with static paths",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /absolute/path/to/project/.cattoolkit/hooks/scripts/protect-files.py",
            "timeout": 10000
          },
          {
            "type": "command",
            "command": "python3 /absolute/path/to/project/.cattoolkit/hooks/scripts/security-check.py",
            "timeout": 10000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /absolute/path/to/project/.cattoolkit/hooks/scripts/type-check-on-edit.py",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```

**For TypeScript (guard-ts):**
```json
{
  "description": "Guard hooks with static paths",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "node /absolute/path/to/project/.cattoolkit/hooks/scripts/protect-files.js",
            "timeout": 10000
          },
          {
            "type": "command",
            "command": "node /absolute/path/to/project/.cattoolkit/hooks/scripts/security-check.js",
            "timeout": 10000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "node /absolute/path/to/project/.cattoolkit/hooks/scripts/type-check.js",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

## Automated Deployment

Use the `/setup` command to automate deployment:

```bash
# Deploy guard-python hooks
/setup hooks guard-python

# Deploy guard-ts hooks
/setup hooks guard-ts
```

The setup command will:
1. Create `.cattoolkit/hooks/` directory
2. Copy scripts from plugin to project
3. Generate hooks.json with ABSOLUTE PATHS
4. Set execute permissions
5. Validate deployment

## Path Resolution

### For Python Hooks

Hook scripts use relative paths internally:

```python
# In protect-files.py
script_dir = Path(__file__).parent
hooks_dir = script_dir.parent  # hooks/
project_root = hooks_dir.parent  # .cattoolkit/
```

This allows scripts to find project files regardless of where they are deployed.

### For TypeScript Hooks

Hook scripts use similar pattern:

```javascript
// In protect-files.js
const scriptDir = path.dirname(__filename);
const hooksDir = path.dirname(scriptDir);
const projectRoot = path.dirname(hooksDir);
```

## Benefits of Static Deployment

✅ **No Environment Variables** - Hooks work without CLAUDE_PLUGIN_ROOT
✅ **Portable** - Project can be moved without reconfiguration
✅ **Reliable** - No silent failures from missing variables
✅ **Debuggable** - Clear error messages when paths are wrong
✅ **Secure** - Scripts are contained within project directory

## Migration from Dynamic to Static

If you previously used `${CLAUDE_PLUGIN_ROOT}`, migrate to static deployment:

1. Run `/setup hooks {plugin-name}` to deploy with static paths
2. Update your hooks.json to use absolute paths
3. Remove CLAUDE_PLUGIN_ROOT from shell profile (optional)
4. Test hooks with a sample edit operation

## Validation

After deployment, validate:

```bash
# Check scripts exist
ls -la .cattoolkit/hooks/scripts/

# Validate JSON
jq . .cattoolkit/hooks/hooks.json

# Test hooks
python3 manage-hooks/assets/scripts/hook-tester.py test .cattoolkit/hooks/hooks.json
```

## Troubleshooting

### Scripts Not Executing

```bash
# Check permissions
ls -la .cattoolkit/hooks/scripts/

# Fix permissions
chmod +x .cattoolkit/hooks/scripts/*
```

### Path Not Found

```bash
# Verify absolute paths in hooks.json
grep "command" .cattoolkit/hooks/hooks.json

# Test script manually
python3 .cattoolkit/hooks/scripts/protect-files.py
```

### JSON Invalid

```bash
# Check JSON syntax
jq . .cattoolkit/hooks/hooks.json

# Common issues:
# - Trailing commas
# - Unquoted keys
# - Missing quotes
```
