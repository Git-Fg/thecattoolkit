# Commands (Slash Commands)

Commands are the explicit interface of the plugin. These are **Instructions for Claude**, not messages for the user.

## 1. Anatomy (`commands/*.md`)

A command is a Markdown file with strict frontmatter.

```yaml
---
description: "Review security flaws"   # Mandatory.
argument-hint: "[file] [level]"        # UX: Guides autocompletion.
allowed-tools: ["Read", "Grep"]        # Security: Whitelist.
disable-model-invocation: true         # Control: Prevents model from calling it alone.
hide-from-slash-command-tool: "true"   # Visibility: Hide from menu.
---

# Prompt Body

Direct instruction to the AI.
```

## 2. Dynamic Syntax

Don't let Claude guess the context. Inject it.

### Bash Injection (`!`...``)
Executed by the shell before the prompt. "Fail Fast" pattern.

```markdown
Environment Check: !`test -f .env && echo "OK" || echo "MISSING"`

If MISSING, stop and notify the user.
```

### File Injection (`@`)
`@src/config.json` injects the file content.
*Warning:* In a plugin, `@./file` points to the plugin cache. For the user project, prefer passing the path as an argument.

## 3. Interaction Patterns

### The "Hybrid" Pattern (args vs questions)
Should you use arguments (`$1`) or ask questions?
*   **Rule:** Use arguments for power users (fast), use `AskUserQuestion` for exploration.
*   **Best Practice:** Check if `$1` is empty. If yes, trigger the Wizard.

```markdown
Project Type: !`[ -z "$1" ] && echo "ASK" || echo "$1"`

If Project Type is "ASK", call AskUserQuestion to get the user's preference.
```

## 4. The 5 Command Archetypes

Based on official plugins (`commit-commands`, `hookify`, `pr-review-toolkit`), here are the standard patterns.

### 1. The Wrapper ("The Runner")
**Example:** `commit-commands:clean_gone`
*   **Function:** Executes a complex deterministic log logic (Bash/Python) that is too risky for the LLM to hallucinate.
*   **Structure:**
    ```markdown
    Execute this script: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/clean.sh`.
    Analyze the output and summarize what was deleted.
    ```

### 2. The Wizard ("The Interactive Guide")
**Example:** `hookify:configure`
*   **Function:** Guides the user through complex configuration using the `AskUserQuestion` tool instead of 10 arguments.
*   **Technique:** The "Hybrid" Pattern (Check `$1`, if empty -> Ask).
*   **Structure:**
    ```markdown
    1. Analyze the project.
    2. Use `AskUserQuestion` to ask: "Which agent type?" (Radio button style).
    3. Generate the config based on the JSON response.
    ```

### 3. The Delegator ("The Agent Launcher")
**Example:** `pr-review-toolkit:review`
*   **Function:** A simple "Start Button" command that bootstraps a long-running Agent.
*   **Structure:**
    ```markdown
    Initiate a review using the `code-reviewer` agent.
    Pass context: !`git diff --name-only`.
    Use the `Task` tool to launch the agent.
    ```

### 4. The Scaffolder ("The Template Generator")
**Example:** `plugin-dev:create`
*   **Function:** Copies standard files from the plugin cache to the user's project.
*   **Technique:** Script using `${CLAUDE_PLUGIN_ROOT}` actions `cp`.
*   **Mechanism:**
    1.  Store templates in `my-plugin/assets/templates/`.
    2.  Write a script `scripts/scaffold.sh`:
        ```bash
        cp -r "${CLAUDE_PLUGIN_ROOT}/assets/templates/"* "${CLAUDE_PROJECT_DIR}/"
        ```
    3.  Command Prompt: "Run the scaffolding script: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/scaffold.sh`. Then ask the user for customization."

### 5. The Context Loader ("The Debugger")
**Example:** `/doctor` commands.
*   **Function:** Massively retrieves system info (Env vars, Node version, Git status) to "ground" the LLM before it answers.
*   **Structure:**
    ```markdown
    Context Analysis:
    - Node Version: !`node -v`
    - Git Status: !`git status`
    - Env Vars: !`printenv | grep MY_PLUGIN`
    Diagnose the configuration issues based on this data.
    ```

