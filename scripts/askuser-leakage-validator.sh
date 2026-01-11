#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
QUIET=false
EXIT_CODE=0

usage() {
  echo "Usage: $0 [--quiet]"
  echo "  --quiet  Only output critical errors"
  exit 0
}

[[ "${1:-}" == "--help" ]] && usage
[[ "${1:-}" == "--quiet" ]] && QUIET=true

log_info() { [[ "$QUIET" == "false" ]] && echo "[INFO] $1"; }
log_warn() { echo "[WARNING] $1"; EXIT_CODE=1; }
log_error() { echo "[CRITICAL] $1"; EXIT_CODE=1; }

echo "=== AskUser-Leakage Validator (2026 Autonomous Agent Standards) ==="
echo "Checks for agents with 'permissionMode: acceptEdits' that have 'AskUserQuestion' in tools"
echo

cd "$ROOT_DIR"

extract_frontmatter() {
  local file="$1"
  awk '/^---$/{if(f){exit}else{f=1;next}} f' "$file"
}

get_yaml_value() {
  local content="$1"
  local key="$2"
  echo "$content" | grep -E "^${key}:" | sed -E "s/^${key}:[[:space:]]*//" | head -1
}

has_yaml_key() {
  local content="$1"
  local key="$2"
  echo "$content" | grep -qE "^${key}:" && return 0 || return 1
}

validate_agent() {
  local file="$1"
  local fm
  fm=$(extract_frontmatter "$file")
  local agent_name
  agent_name=$(basename "$file" .md)

  # Check if agent has permissionMode: acceptEdits
  if has_yaml_key "$fm" "permissionMode"; then
    local perm_mode
    perm_mode=$(get_yaml_value "$fm" "permissionMode")

    if [[ "$perm_mode" == "acceptEdits" ]] || [[ "$perm_mode" == "bypassPermissions" ]]; then
      # Check if agent has tools specified
      if has_yaml_key "$fm" "tools"; then
        local tools
        tools=$(get_yaml_value "$fm" "tools")

        # Check if AskUserQuestion is in tools list
        if echo "$tools" | grep -qE "\bAskUserQuestion\b"; then
          log_error "$file: Agent '$agent_name' has 'permissionMode: $perm_mode' with 'AskUserQuestion' in tools. 2026 Autonomous Agent Rule: Execution-phase workers MUST NOT have AskUserQuestion. Only planning-phase coordinators (director-type) should use AskUserQuestion."
        fi
      else
        # No tools specified - inherits all tools including AskUserQuestion
        # If permissionMode is acceptEdits or bypassPermissions, this is a worker
        # Workers should not have AskUserQuestion
        if [[ "$perm_mode" == "acceptEdits" ]]; then
          log_warn "$file: Agent '$agent_name' has 'permissionMode: acceptEdits' but no 'tools' whitelist specified. Agent inherits ALL tools including 'AskUserQuestion'. 2026 Standard: Worker agents must explicitly exclude AskUserQuestion from their tools whitelist."
        fi
      fi
    fi

    # Additional check: agent description patterns for worker vs coordinator
    local description
    if has_yaml_key "$fm" "description"; then
      description=$(get_yaml_value "$fm" "description")

      # If agent is a worker (has "worker" in description or name)
      if [[ "$agent_name" =~ worker ]] || [[ "$description" =~ [Ww]orker ]]; then
        if has_yaml_key "$fm" "tools"; then
          local tools
          tools=$(get_yaml_value "$fm" "tools")
          if echo "$tools" | grep -qE "\bAskUserQuestion\b"; then
            log_error "$file: Agent '$agent_name' is identified as a worker but has 'AskUserQuestion' in tools. Workers execute autonomously without user interaction."
          fi
        fi
      fi

      # If agent is a director/coordinator, AskUserQuestion is acceptable
      if [[ "$agent_name" =~ director ]] || [[ "$agent_name" =~ coordinator ]] || [[ "$description" =~ [Dd]irector ]] || [[ "$description" =~ [Cc]oordinator ]]; then
        log_info "$file: Agent '$agent_name' is a coordinator-type agent. AskUserQuestion is acceptable for planning-phase coordination."
      fi
    fi
  fi
}

log_info "Validating Agent tool configurations..."
while IFS= read -r -d '' file; do
  validate_agent "$file"
done < <(find plugins/*/agents -name "*.md" -type f -not -path "*/references/*" -print0 2>/dev/null)

echo
if [[ "$EXIT_CODE" -eq 0 ]]; then
  log_info "No AskUser-leakage issues found. Agents follow 2026 autonomous execution standards."
else
  echo "[SUMMARY] AskUser-leakage violations found. Worker agents must not have AskUserQuestion for autonomous execution."
fi

exit "$EXIT_CODE"
