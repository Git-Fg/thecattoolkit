# Architecture & Philosophy

This guide details the technical foundations of Claude Code plugins. Understanding these mechanisms is essential before creating content, as they dictate portability and security rules.

## 1. Philosophy: Standalone vs Plugin

Claude Code offers two extension modes. Choosing the right one is the first architectural decision.

| Feature | Standalone Mode | Plugin Mode |
|:---|:---|:---|
| **Location** | `.claude/` (project root) | `.claude-plugin/` + dedicated structure |
| **Identification** | `/command` (direct) | `/plugin:command` (namespaced) |
| **Scope** | Current project only | Global (installed in user cache) |
| **Versioning** | None (Project Git) | SemVer (via `plugin.json`) |
| **Dependencies** | Project dependencies | Isolated (manual management) |
| **Usage** | Prototyping, Project scripts | Distribution, Reusable tools |

**The Winning Strategy:** Always start in Standalone to iterate quickly. Migrate to a Plugin only when the tool is stable and ready for distribution.

## 2. Installation Model (The Cache)

Unlike a classic project, **Claude Code does not execute your plugin "in place"**.

1.  **Copy:** Upon installation, all plugin content is recursively copied into a **secure cache** (e.g., `~/.claude/plugins/cache/v1/...`).
2.  **Execution:** The runtime executes from this cache.
3.  **Read-Only:** This cache folder must be considered **read-only**.
    *   ❌ `echo "log" >> ./logs.txt` (High risk: overwritten on update, unpredictable permissions).
    *   ✅ `echo "log" >> /tmp/my-plugin.log` or `${CLAUDE_PROJECT_DIR}/.claude/tmp/`.

### Implications for Paths (`../`)
Any relative reference going up to a parent (`../libs`) will fail because the parent folder does not exist in the cache.
*   **Solution:** Everything the plugin needs must be *inside* it. Use *internal* symlinks if necessary.

### Dependency Management
There is no automatic `npm install` or `pip install`.
*   **Zero-Dep Strategy (Recommended):** Standard Bash/Python scripts.
*   **Bundled Strategy:** Commit `node_modules` or `vendor` (if architecture compatible).
*   **Global Check Strategy:** Verify tool presence at start of script (`command -v jq || exit 1`).

## 3. Filesystem Structure

The structure is strict to enable auto-discovery.

```text
my-plugin/
├── .claude-plugin/           # METADATA ONLY
│   └── plugin.json           # Manifest
├── commands/                 # Commands (Root)
│   ├── deploy.md             # -> /my-plugin:deploy
│   └── db/                   # -> /my-plugin:db:...
├── agents/                   # Agents
│   └── code-reviewer.md
├── skills/                   # Skills
│   └── git-mastery/
│       ├── SKILL.md
│       └── references/
├── hooks/                    # Hooks & Scripts
│   ├── hooks.json
│   └── scripts/
├── .mcp.json                 # MCP Config
├── .lsp.json                 # LSP Config
└── assets/                   # Templates, Images
```

**Fatal Error:** NEVER put `commands/` or `agents/` inside `.claude-plugin/`.

## 4. Manifest Configuration (`plugin.json`)

The `plugin.json` file is the brain. Beyond metadata, it controls deep behavior.

### Output Styles (`outputStyles`)
This field points to a directory of Markdown files that define "Personas" or formatting instructions.
```json
"outputStyles": "./assets/styles/"
```
*   **Mechanism:** When the user selects a style (e.g., "Concise"), the content of `./assets/styles/concise.md` is **injected into the System Prompt**.
*   **Usage:** Create styles for different expertise levels (e.g., `teacher.md`, `expert.md`).

## 4. Configuration Hierarchy

Your plugin is the lowest class citizen. The user is always right.

**Priority Order (Strongest to Weakest):**
1.  **Managed** (Enterprise Policy)
2.  **CLI Args** (`--flag`)
3.  **Local** (`.claude/settings.local.json`)
4.  **Project** (`.claude/settings.json`)
5.  **User** (`~/.claude/settings.json`)
6.  **Plugin** (Your `plugin.json` / defaults)

**Impact:** Name your components uniquely (`myplugin-style`) to avoid being accidentally overwritten by global user config.

## 5. Development Tips

### Testing & Cache Clearing
Since plugins are cached, changes aren't always immediate.
*   **Force Reinstall:** `/plugin install local-plugin@v1.0.1`
*   **Nuke Cache:** `rm -rf ~/.claude/plugins/cache` (The "Turn it off and on again" of plugin dev).

### Multi-Plugin Loading
To test interactions between two local plugins:
`claude --plugin-dir ./plugin-a --plugin-dir ./plugin-b`
