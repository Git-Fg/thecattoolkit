#!/bin/bash
# glue-detector.sh - Find glue code patterns in plugin structure

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
QUIET=false

[[ "${1:-}" == "--quiet" ]] && QUIET=true

log_info() { [[ "$QUIET" == "false" ]] && echo "$1"; }

cd "$ROOT_DIR"

echo "=== Glue Code Detection Report ==="
echo

# 1. Large Command Files (>10 lines that might be glue)
log_info "1. Large Command Files (>10 lines):"
find plugins/*/commands -name "*.md" -type f -not -path "*/references/*" -exec sh -c 'lines=$(wc -l < "$1"); if [ "$lines" -gt 10 ]; then echo "⚠️  $1 ($lines lines)"; fi' _ {} \; 2>/dev/null | sort
log_info ""

# 2. Agent Files with Excessive Delegation
log_info "2. Agent Files with Delegation Patterns:"
for file in plugins/*/agents/*.md; do
  if [ -f "$file" ]; then
    task_count=$(grep -c "Task(" "$file" 2>/dev/null || echo "0")
    task_count=$(echo "$task_count" | head -1)
    if [ -n "$task_count" ] && [ "$task_count" -gt 5 ] 2>/dev/null; then
      echo "⚠️  $file ($task_count Task calls)"
    fi
  fi
done
log_info ""

# 3. Commands that delegate to other commands
log_info "3. Command-to-Command Delegation:"
for file in plugins/*/commands/*.md; do
  if [ -f "$file" ] && grep -q "Skill(" "$file" 2>/dev/null; then
    echo "⚠️  $file (uses Skill tool)"
  fi
done
log_info ""

# 4. Skills referencing other skills via relative paths
log_info "4. Cross-Skill Coupling:"
grep -r "\.\./.*skill" plugins/*/skills/ 2>/dev/null | grep -v "the.*skill" | awk '{print "⚠️  " $0}' || true
log_info ""

# 5. Wrapper Agents (agents that just delegate)
log_info "5. Potential Wrapper Agents:"
for file in plugins/*/agents/*.md; do
  if [ -f "$file" ]; then
    task_count=$(grep -c "Task(" "$file" 2>/dev/null || echo "0")
    task_count=$(echo "$task_count" | head -1)
    content_lines=$(wc -l < "$file")
    if [ -n "$task_count" ] && [ "$task_count" -gt 5 ] 2>/dev/null && [ "$content_lines" -lt 50 ]; then
      echo "⚠️  $file (high delegation, minimal content)"
    fi
  fi
done
log_info ""

# 6. Commands with missing allowed-tools
log_info "6. Commands Missing Tool Restrictions:"
for file in plugins/*/commands/*.md; do
  if [ -f "$file" ] && ! grep -q "allowed-tools:" "$file"; then
    echo "⚠️  $file (no allowed-tools specified)"
  fi
done
log_info ""

# 7. Skills with execution logic (should be passive)
log_info "7. Skills with Execution Logic:"
grep -r "AskUserQuestion" plugins/*/skills/*.md 2>/dev/null | awk '{print "⚠️  " $0 " (skills should be passive)"}' || true
log_info ""

# 8. Glue Code Metrics Summary
log_info "8. Glue Code Metrics:"
total_commands=$(find plugins/*/commands -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
total_agents=$(find plugins/*/agents -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
total_skills=$(find plugins/*/skills -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
log_info "Total Commands: $total_commands"
log_info "Total Agents: $total_agents"
log_info "Total Skills: $total_skills"
log_info ""

echo "=== Detection Complete ==="
