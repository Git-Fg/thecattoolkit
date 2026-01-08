# Command Patterns Reference

Verified patterns from official Claude Code documentation, now organized in the `examples/` directory.

## Git Workflow Patterns

| Pattern | Example File | Description |
|---------|--------------|-------------|
| **Commit with Context** | [git-commit-full.md](../examples/git-commit-full.md) | Full context from status, diff, and logs |
| **Simple Commit** | [git-commit-simple.md](../examples/git-commit-simple.md) | Minimalist commit command |
| **Git Only** | [git-only.md](../examples/git-only.md) | Restricted to git operations only |

## Code Analysis Patterns

| Pattern | Example File | Description |
|---------|--------------|-------------|
| **Performance Opt** | [performance-optimization.md](../examples/performance-optimization.md) | Analyze and optimize performance |
| **Security Review** | [security-review.md](../examples/security-review.md) | Scan for vulnerabilities |
| **File Analysis** | [file-analysis.md](../examples/file-analysis.md) | Analyze specific file argument |
| **Read-Only Analysis** | [read-only-analysis.md](../examples/read-only-analysis.md) | Safe analysis (no write permissions) |

## Issue Tracking Patterns

| Pattern | Example File | Description |
|---------|--------------|-------------|
| **Fix Issue** | [fix-issue.md](../examples/fix-issue.md) | Fix issue #ID with workflow |
| **PR Review** | [review-pr.md](../examples/review-pr.md) | Review PR with priority and assignment |

## File Operation Patterns

| Pattern | Example File | Description |
|---------|--------------|-------------|
| **File Reference** | [reference-file.md](../examples/reference-file.md) | Review file using @ syntax |
| **Compare Files** | [compare-files.md](../examples/compare-files.md) | Diff two files |

## Thinking-Only Patterns

| Pattern | Example File | Description |
|---------|--------------|-------------|
| **Deep Analysis** | [deep-analysis.md](../examples/deep-analysis.md) | First-principles analysis |
| **Strategic Planning** | [strategic-planning.md](../examples/strategic-planning.md) | Plan implementation strategy |

## Bash Execution Patterns

| Pattern | Example File | Description |
|---------|--------------|-------------|
| **Project Health** | [project-health.md](../examples/project-health.md) | Dynamic environment loading |
| **Deployment Gate** | [deploy-gate.md](../examples/deploy-gate.md) | Conditional execution based on tests |
| **Project Checks** | [project-checks.md](../examples/project-checks.md) | Restricted specific bash commands |

## Workflow Patterns

| Pattern | Example File | Description |
|---------|--------------|-------------|
| **Feature Workflow** | [feature-workflow.md](../examples/feature-workflow.md) | Plan -> Implement -> Verify -> Commit |
| **Fix Performance** | [fix-performance.md](../examples/fix-performance.md) | Analyze -> Fix (Chained) |
| **Hybrid Workflow** | [hybrid-workflow.md](../examples/hybrid-workflow.md) | Foreground review + Background analysis |

## Background Execution Patterns

| Pattern | Example File | Description |
|---------|--------------|-------------|
| **Background Agent** | [background-agent.md](../examples/background-agent.md) | Single background task |
| **Parallel Fan-Out** | [parallel-fan-out.md](../examples/parallel-fan-out.md) | Multiple parallel agents |
| **Staged Workflow** | [staged-background.md](../examples/staged-background.md) | Sequential background stages |
