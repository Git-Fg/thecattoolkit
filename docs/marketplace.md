# Marketplace Configuration Guide

> **📘 Official Docs:** [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) - Official marketplace documentation
> **📘 Official Docs:** [Create plugins](https://code.claude.com/docs/en/plugins) - Official plugin creation guide
> **📘 Official Docs:** [Plugins reference](https://code.claude.com/docs/en/plugins-reference) - Complete technical specifications  
> **📖 Quick Reference:** See [CLAUDE.md](../CLAUDE.md#marketplace-configuration) for a summary.

Complete guide to The Cat Toolkit marketplace configuration and plugin distribution.

---

## Overview

The Cat Toolkit is distributed as a **Claude Code marketplace** - a catalog of plugins that users can discover and install. The marketplace configuration is defined in `.claude-plugin/marketplace.json` at the repository root.

---

## Marketplace Structure

**Location:** `.claude-plugin/marketplace.json` at repository root.

**Schema:**

| Field | Required | Description |
|:------|:---------|:------------|
| `name` | ✓ | Marketplace identifier (kebab-case) |
| `owner` | ✓ | Maintainer (`name` required, `email` optional) |
| `plugins` | ✓ | Array of plugin entries |
| `metadata.description` | | Brief description |
| `metadata.version` | | Semantic version |
| `metadata.pluginRoot` | | Base directory for relative paths |
| `metadata.keywords` | | Discovery keywords |
| `metadata.homepage` | | Homepage URL |
| `metadata.repository` | | Repository URL |
| `metadata.license` | | License identifier |

---

## Plugin Entry Configuration

| Field | Required | Type | Description |
|:------|:---------|:-----|:------------|
| `name` | ✓ | string | Plugin identifier (kebab-case) |
| `source` | ✓ | string\|object | Source location (relative path, GitHub repo, or git URL) |
| `strict` | | boolean | Require plugin.json (default: `true`) |
| `description` | | string | Brief description |
| `version` | | string | Semantic version |
| `author` | | object | Author (`name` required, `email` optional) |
| `repository` | | string | Repository URL |
| `license` | | string | SPDX license identifier |
| `category` | | string | Organization category |
| `tags` | | array | Searchable tags |
| `keywords` | | array | Discovery keywords |
| `commands` | | string\|array | Custom command paths |
| `agents` | | string\|array | Custom agent paths |
| `hooks` | | string\|object | Hook config or path |
| `mcpServers` | | string\|object | MCP config or path |
| `lspServers` | | string\|object | LSP config or path |

### Example Plugin Entry

```json
{
  "name": "sys-core",
  "source": "./plugins/sys-core",
  "description": "System Core - Infrastructure and Safety layer for plugin management, security auditing, and toolkit maintenance",
  "version": "1.0.2",
  "author": {
    "name": "Git-Fg"
  },
  "repository": "https://github.com/Git-Fg/thecattoolkit",
  "license": "MIT",
  "category": "infrastructure",
  "tags": ["security", "validation", "toolkit", "infrastructure", "safety"],
  "keywords": ["security", "audit", "validation", "toolkit", "infrastructure", "safety", "hooks", "scaffolding"],
  "strict": true
}
```

---

## Strict Mode & Plugin Source Types

**Strict Mode:**

| Mode | Behavior | Use When |
|:-----|:---------|:---------|
| `strict: true` (default) | Plugin must have `plugin.json`; marketplace fields merge/override | Plugins with complete manifest |
| `strict: false` | No `plugin.json` required; marketplace defines everything | Simple plugins defined in marketplace |

**Source Types:**

| Type | Format | Use When |
|:-----|:-------|:---------|
| **Relative Path** | `"./plugins/sys-core"` | Same repository as marketplace (Git only) |
| **GitHub** | `{"source": "github", "repo": "user/repo"}` | Separate repositories |
| **Git URL** | `{"source": "url", "url": "https://..."}` | GitLab, Bitbucket, self-hosted |

---

## Validation

**Commands:** `claude plugin validate .` (marketplace), `claude plugin validate ./plugins/plugin-name` (individual plugin).

**Requirements:**

| File | Required Fields | Notes |
|:-----|:---------------|:------|
| **marketplace.json** | `name`, `owner`, `plugins` | Plugin entries need `name` and `source` |
| **plugin.json** | `name` | Remove invalid fields (`capabilities`, `contributors`, `dependencies` in old schema) |

---

## Plugin.json Schema

### Required Fields

| Field | Type | Description |
|:-----|:-----|:------------|
| `name` | string | Plugin identifier (kebab-case, no spaces) |

### Standard Metadata Fields

| Field | Type | Description |
|:-----|:-----|:------------|
| `description` | string | Brief plugin description |
| `version` | string | Semantic version |
| `author` | object | Author info (`name` required, `email` optional) |
| `license` | string | SPDX license identifier |
| `homepage` | string | Plugin homepage URL |
| `repository` | string | Source code repository URL |
| `keywords` | array | Discovery keywords |

### Component Path Fields

| Field | Type | Description |
|:-----|:-----|:------------|
| `commands` | string\|array | Custom command paths |
| `agents` | string\|array | Custom agent paths |
| `skills` | string\|array | Custom skill paths |
| `hooks` | string\|object | Hook config or path |
| `mcpServers` | string\|object | MCP config or path |
| `lspServers` | string\|object | LSP config or path |

**Important:** Custom paths **supplement** default directories, they don't replace them.

---

## Version Management

### Marketplace Versioning

- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Update when:
  - **MAJOR**: Breaking changes to marketplace structure
  - **MINOR**: New plugins added, non-breaking schema changes
  - **PATCH**: Plugin updates, metadata changes

### Plugin Versioning

- Each plugin maintains its own version in `plugin.json`
- Marketplace entries can override plugin versions
- Version tracking enables:
  - Automatic updates via `/plugin marketplace update`
  - Dependency management
  - Change tracking

---

## Team Configuration

### Auto-Installation for Teams

Team admins can configure automatic marketplace installation via `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "cattoolkit": {
      "source": {
        "source": "github",
        "repo": "Git-Fg/thecattoolkit"
      }
    }
  },
  "enabledPlugins": {
    "sys-core@cattoolkit": {
      "scope": "project"
    },
    "sys-builder@cattoolkit": {
      "scope": "project"
    }
  }
}
```

When team members trust the repository folder, Claude Code will prompt them to install the marketplace.

---

## Installation Scopes

Plugins can be installed in different scopes:

| Scope | Location | Use Case |
|:------|:---------|:---------|
| **User** | `~/.claude/settings.json` | Personal use across all projects (default) |
| **Project** | `.claude/settings.json` | Team-shared plugins, committed to git |
| **Local** | `.claude/settings.local.json` | Personal overrides, gitignored |
| **Managed** | `managed-settings.json` | Admin-installed, read-only |

### Installation Examples

```bash
# User scope (default)
/plugin install sys-core@cattoolkit

# Project scope (team-shared)
/plugin install sys-core@cattoolkit --scope project

# Local scope (personal only)
/plugin install sys-core@cattoolkit --scope local
```

---

## Auto-Updates

The Cat Toolkit marketplace has auto-updates **disabled by default** (as a third-party marketplace).

### Enable Auto-Updates

1. Run `/plugin` to open plugin manager
2. Go to **Marketplaces** tab
3. Select `cattoolkit` marketplace
4. Choose **Enable auto-update**

When enabled, Claude Code will:
- Refresh marketplace data at startup
- Update installed plugins to latest versions
- Notify you if plugins were updated (restart recommended)

---

## Troubleshooting

| Issue | Solution |
|:------|:---------|
| **Marketplace not loading** | Verify `.claude-plugin/marketplace.json` exists, check URL accessibility, ensure repository is public/accessible |
| **Plugin installation failures** | Verify source URLs accessible, check plugin directories exist, ensure `plugin.json` exists (when `strict: true`) |
| **Validation errors** | Run `claude plugin validate .` (marketplace) or `claude plugin validate ./plugins/plugin-name` (plugin), remove invalid fields |
| **Files not found after installation** | Plugins copied to cache; external references won't work. Use symlinks or `${CLAUDE_PLUGIN_ROOT}` in hooks/MCP configs |
| **Plugin skills not appearing** | Clear cache: `rm -rf ~/.claude/plugins/cache`, restart Claude Code, reinstall plugin |

---

## Best Practices

1. **Use Semantic Versioning** - Follow MAJOR.MINOR.PATCH for both marketplace and plugins
2. **Include Comprehensive Metadata** - Add descriptions, categories, tags, and keywords for better discovery
3. **Validate Regularly** - Run `claude plugin validate` before committing changes
4. **Test Locally** - Test marketplace locally before pushing to repository
5. **Document Changes** - Update version numbers and changelogs when making changes
6. **Use Strict Mode** - Keep `strict: true` for plugins with their own plugin.json files
7. **Organize with Categories** - Use consistent categories across plugins
8. **Optimize Tags** - Use relevant tags for searchability without over-tagging

---

## Reference

- [Official Marketplace Documentation](https://code.claude.com/docs/en/plugin-marketplaces)
- [Plugin Reference](https://code.claude.com/docs/en/plugins-reference)
- [Discover Plugins Guide](https://code.claude.com/docs/en/discover-plugins)
