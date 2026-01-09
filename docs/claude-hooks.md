# Claude Code Hooks & Architecture

> [!IMPORTANT]
> The hooks in this toolkit are designed specifically for **Claude Code** and rely on the `${CLAUDE_PLUGIN_ROOT}` environment variable.

## Reference Architecture

The Cat Toolkit uses a "Reference Architecture" pattern for hooks, meaning:
1.  **No Deployment:** Hook scripts are NOT copied to your project.
2.  **Direct Execution:** Claude executes scripts directly from its internal plugin cache.
3.  **Variable Resolution:** The `hooks.json` configuration uses `${CLAUDE_PLUGIN_ROOT}` to find the scripts.

### How it works

When you install a plugin (e.g., `claude plugin install @cattoolkit/guard-python`), Claude reads the `hooks.json` manifest.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/plugins/guard-python/hooks/scripts/protect-files.py\""
      }
    ]
  }
}
```

- When Claude runs, it automatically injects `CLAUDE_PLUGIN_ROOT` pointing to where the plugin is cached.
- The command resolves to something like: `python3 "/Users/username/.claude/plugins/cache/guard-python/hooks/scripts/protect-files.py"`.

## Compatibility

| Environment | Status | Notes |
| :--- | :--- | :--- |
| **Claude Code** | ✅ Fully Supported | Hooks fire automatically. |
| **Other MCP Clients** | ⚠️ Limited | Marketplace commands work, but hooks (automation/safety) will NOT fire. |

## Security

Running code from the plugin cache has security implications. We mitigate this by:
1.  **Read-Only Plugin Dir:** Scripts are forbidden from writing to `${CLAUDE_PLUGIN_ROOT}` via `is_safe_write()`.
2.  **Project-Only Writes:** Wrappers only allow file modifications within your allowed Project Root.
3.  **Quoted Paths:** All paths in `hooks.json` are quoted to prevent argument injection via spaces in paths.

## Troubleshooting

If hooks are not firing:
1.  Ensure you are using **Claude Code**.
2.  Check that the plugin is installed: `claude plugin list`.
3.  Verify `hooks.json` syntax (valid JSON, quoted paths).
