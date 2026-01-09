#!/bin/bash
# glue-detector.sh - Find glue code patterns in plugin structure

echo "=== Glue Code Detection Report ==="
echo

# 1. Large Command Files (>10 lines that might be glue)
echo "1. Large Command Files (>10 lines):"
find plugins/*/commands -name "*.md" -type f -exec sh -c 'lines=$(wc -l < "$1"); if [ "$lines" -gt 10 ]; then echo "⚠️  $1 ($lines lines)"; fi' _ {} \; | sort
echo

# 2. Agent Files with Excessive Delegation
echo "2. Agent Files with Delegation Patterns:"
for file in plugins/*/agents/*.md; do
  if [ -f "$file" ]; then
    task_count=$(grep -c "Task(" "$file" 2>/dev/null || echo "0")
    task_count=$(echo "$task_count" | head -1)
    if [ -n "$task_count" ] && [ "$task_count" -gt 5 ] 2>/dev/null; then
      echo "⚠️  $file ($task_count Task calls)"
    fi
  fi
done
echo

# 3. Commands that delegate to other commands
echo "3. Command-to-Command Delegation:"
for file in plugins/*/commands/*.md; do
  if [ -f "$file" ] && grep -q "Skill(" "$file" 2>/dev/null; then
    echo "⚠️  $file (uses Skill tool)"
  fi
done
echo

# 4. Skills referencing other skills via relative paths
echo "4. Cross-Skill Coupling:"
grep -r "\.\./.*skill" plugins/*/skills/ 2>/dev/null | grep -v "the.*skill" | awk '{print "⚠️  " $0}'
echo

# 5. Wrapper Agents (agents that just delegate)
echo "5. Potential Wrapper Agents:"
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
echo

# 6. Commands with missing allowed-tools
echo "6. Commands Missing Tool Restrictions:"
for file in plugins/*/commands/*.md; do
  if [ -f "$file" ] && ! grep -q "allowed-tools:" "$file"; then
    echo "⚠️  $file (no allowed-tools specified)"
  fi
done
echo

# 7. Skills with execution logic (should be passive)
echo "7. Skills with Execution Logic:"
grep -r "AskUserQuestion" plugins/*/skills/*.md 2>/dev/null | awk '{print "⚠️  " $0 " (skills should be passive)"}'
echo

# 8. Glue Code Metrics Summary
echo "8. Glue Code Metrics:"
total_commands=$(find plugins/*/commands -name "*.md" -type f | wc -l)
total_agents=$(find plugins/*/agents -name "*.md" -type f | wc -l)
total_skills=$(find plugins/*/skills -name "*.md" -type f | wc -l)
echo "Total Commands: $total_commands"
echo "Total Agents: $total_agents"
echo "Total Skills: $total_skills"
echo

echo "=== Detection Complete ==="

