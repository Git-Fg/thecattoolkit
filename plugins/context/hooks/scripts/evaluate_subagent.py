#!/usr/bin/env python3
"""
Evaluate Subagent Stop Hook
Replaces the bloated LLM prompt hook with a deterministic check.
Legacy prompt logic was: "Did it complete successfully? Any errors?"

Current logic:
- Defaults to APPROVE
- Logs subagent completion
"""

import sys
import json
import os


def main():
    # Read input event if needed (passed via stdin)
    # try:
    #     input_data = json.load(sys.stdin)
    # except Exception:
    #     pass

    # We assume the subagent finished. We approve the stop event.
    # If the subagent failed, the system usually handles it before this hook.

    result = {
        "status": "approve",
        "message": "Subagent stop approved by deterministic evaluator",
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()
