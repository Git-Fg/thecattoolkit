#!/usr/bin/env python3
"""
Evaluate Stop Hook
Replaces the bloated LLM prompt hook with a deterministic check.
Legacy prompt logic was: "Is this a meaningful end? Has context been used?"

Current logic:
- Defaults to APPROVE (allow stop)
- Can be extended to check for dirty state or uncommitted changes
"""

import sys
import json
import os


def main():
    # In the future, we can add logic to check for uncommitted changes
    # or active tasks tokens.
    # For now, we allow the user/system to stop when requested.

    result = {
        "decision": "allow",
        "message": "Session stop approved by deterministic evaluator",
    }

    print(json.dumps(result))


if __name__ == "__main__":
    main()
