# Example: Validate Commit Messages

Ensure that git commit messages follow the Conventional Commits specification.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if this is a git commit command: $ARGUMENTS\n\nIf it's a git commit, validate the message follows conventional commits format (feat|fix|docs|refactor|test|chore): description\n\nIf invalid format: {\"decision\": \"block\", \"reason\": \"Commit message must follow conventional commits\"}\nIf valid or not a commit: {\"decision\": \"approve\", \"reason\": \"ok\"}"
          }
        ]
      }
    ]
  }
}
```
