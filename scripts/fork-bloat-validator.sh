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

echo "=== Fork-Bloat Validator (2026 Inline-First) ==="
echo "Checks for skills with 'context: fork' that may not need it"
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

has_tool() {
  local tools="$1"
  local tool="$2"
  echo "$tools" | grep -qE "\b${tool}\b" && return 0 || return 2
}

validate_skill() {
  local file="$1"
  local fm
  fm=$(extract_frontmatter "$file")

  # Check if skill has context: fork
  if has_yaml_key "$fm" "context"; then
    local context
    context=$(get_yaml_value "$fm" "context")
    if [[ "$context" == "fork" ]]; then
      local skill_name
      skill_name=$(get_yaml_value "$fm" "name")
      local allowed_tools=""
      if has_yaml_key "$fm" "allowed-tools"; then
        allowed_tools=$(get_yaml_value "$fm" "allowed-tools")
      fi

      # 2026 Inline-First Rule: If skill has context: fork but NO Task tool,
      # it's likely doing simple work that should be inline
      if ! echo "$allowed_tools" | grep -qE "\bTask\b"; then
        # Check if this is truly a complex task that needs isolation
        # If no Task tool and no agent binding, likely inline-eligible
        if ! has_yaml_key "$fm" "agent"; then
          log_warn "$file: Skill '$skill_name' has 'context: fork' but no 'Task' tool. 2026 Inline-First Rule: Tasks <10 files should use inline execution. Consider removing 'context: fork' unless strict isolation is required."
        fi
      fi

      # If has Task tool but not in allowed-tools list, it might be using Task implicitly
      # which is fine - but warn about explicit declaration
      if echo "$allowed_tools" | grep -qE "\bTask\b" && ! echo "$allowed_tools" | grep -qE "allowed-tools:"; then
        log_info "$file: Skill '$skill_name' uses 'Task' tool with 'context: fork'. This is appropriate for parallel agent delegation."
      fi
    fi
  fi
}

log_info "Validating Skill execution modes..."
while IFS= read -r -d '' file; do
  validate_skill "$file"
done < <(find plugins -name "SKILL.md" -type f -print0 2>/dev/null)

echo
if [[ "$EXIT_CODE" -eq 0 ]]; then
  log_info "No fork-bloat issues found. Skills follow 2026 Inline-First principles."
else
  echo "[SUMMARY] Fork-bloat warnings found. Review if skills can use inline execution for quota efficiency."
fi

exit "$EXIT_CODE"
