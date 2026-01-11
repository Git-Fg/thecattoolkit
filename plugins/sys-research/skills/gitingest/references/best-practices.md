# GitIngest Best Practices

## Context Hygiene (Anti-Bloat)

When ingesting repositories larger than 10 files or 50KB:

**DO NOT** stream directly to stdout/context:
```bash
# BAD - Pollutes context window
gitingest https://github.com/large/repo -o -
```

**DO** stream to a temporary file, then read specific sections:
```bash
# GOOD - Keeps context clean
gitingest https://github.com/large/repo -o .cattoolkit/context/repo_digest.txt
grep -A 20 "function_name" .cattoolkit/context/repo_digest.txt
```

## Filtering Strategy

Always apply filters to maximize signal-to-noise ratio:
1. **Exclude Lockfiles**: `-e "*.lock"`
2. **Exclude Assets**: `-e "*.png" -e "*.svg"`
3. **Target Source**: `-i "src/*"`
