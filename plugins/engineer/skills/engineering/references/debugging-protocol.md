# 6-Phase Debugging Protocol

1. **Capture**: Get the raw error log. Never paraphrase errors.
2. **Analyze**: Trace the stack backwards from crash point.
3. **Hypothesize**: "I believe X is causing Y because Z."
4. **Test**: Prove the hypothesis with a minimal repro.
5. **Fix**: Apply the minimal change required.
6. **Verify**: Run the repro case and regression suite.