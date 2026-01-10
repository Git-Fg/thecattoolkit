# Bootstrap Protocol

The Bootstrap Protocol is the Emergency Safe Mode for the Cat Toolkit. It is designed to break circular dependencies and restore core functionality when AI-driven repair tools fail.

## When to use Bootstrap

Invoke `/bootstrap` when:
1. `/heal` or `/build` fails with a Python traceback (e.g., in `hook-tester.py`).
2. The `plugin-expert` agent is hallucinating or looping.
3. Core management skills (like `manage-hooks`) are corrupted.
4. You need to reset the system to a last known good state without agent interference.

## Recovery Decision Tree

1. **Specific File Corruption?**
   - → Use `git checkout HEAD -- <path>` or `/bootstrap <path>`.
2. **Major Meta-Plugin Drift?**
   - → Use `/bootstrap plugins/meta`.
3. **Catastrophic "AI Hallucination" State?**
   - → Use `/bootstrap --hard 1` to revert the last commit.
4. **Local Repository Corrupted?**
   - → Use `/bootstrap --remote plugins/meta`.

## Manual Recovery (Agent-less)

If Claude Code is unable to execute even basic commands, use the standalone script from your terminal:

```bash
./plugins/meta/skills/manage-healing/assets/scripts/bootstrap.sh soft
```

## Safety Mechanisms

- **Deterministic:** Uses pure git (no model reasoning required for the actual restore).
- **Vector Pattern:** Runs in the main conversation context to preserve diagnostic visibility.
- **Zero Dependencies:** Does not rely on Python, Node.js, or any plugin-specific logic beyond basic Bash.
