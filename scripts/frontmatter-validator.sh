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
log_warn() { echo "[WARNING] $1"; }
log_error() { echo "[CRITICAL] $1"; EXIT_CODE=1; }

echo "=== Frontmatter Validator ==="
echo

cd "$ROOT_DIR"

VALID_TOOLS="Read|Write|Edit|Glob|Grep|Bash|Task|AskUserQuestion|Skill"
VALID_MODELS="sonnet|opus|haiku|inherit|claude-sonnet|claude-opus|claude-haiku"
VALID_PERMISSION_MODES="default|acceptEdits|dontAsk|bypassPermissions|plan|ignore"

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

validate_skill() {
  local file="$1"
  local fm
  fm=$(extract_frontmatter "$file")
  local skill_dir skill_dirname
  skill_dir=$(dirname "$file")
  skill_dirname=$(basename "$skill_dir")
  
  local name
  name=$(get_yaml_value "$fm" "name")
  if [[ -z "$name" ]]; then
    log_error "$file: Missing required field 'name'"
  elif [[ ! "$name" =~ ^[a-z0-9-]+$ ]]; then
    log_error "$file: name '$name' must be lowercase with hyphens only"
  elif [[ ${#name} -gt 64 ]]; then
    log_error "$file: name '$name' exceeds 64 characters"
  elif [[ "$name" != "$skill_dirname" ]]; then
    log_warn "$file: name '$name' should match directory name '$skill_dirname'"
  fi
  
  if ! has_yaml_key "$fm" "description"; then
    log_error "$file: Missing required field 'description'"
  else
    if echo "$fm" | grep -qE "description: [|>]"; then
      log_error "$file: description MUST be single-line (no '|' or '>' multi-line syntax)"
    fi
    
    local desc
    desc=$(get_yaml_value "$fm" "description")
    if [[ ${#desc} -gt 1024 ]]; then
      log_warn "$file: description exceeds 1024 characters"
    fi
    
    local first_line
    first_line=$(echo "$desc" | head -1)
    if [[ -n "$first_line" ]] && [[ ! "$first_line" =~ ^[\"\']?(USE|MUST|SHOULD) ]]; then
      log_info "$file: Consider starting description with trigger (USE when...) for better discovery"
    fi
  fi
  
  if has_yaml_key "$fm" "context"; then
    local context
    context=$(get_yaml_value "$fm" "context")
    if [[ "$context" != "fork" ]]; then
      log_error "$file: context must be 'fork' if specified (got: '$context')"
    fi
  fi
  
  if has_yaml_key "$fm" "agent"; then
    if ! has_yaml_key "$fm" "context"; then
      log_warn "$file: 'agent' field only valid with 'context: fork'"
    fi
  fi
  
  if has_yaml_key "$fm" "user-invocable"; then
    local user_inv
    user_inv=$(get_yaml_value "$fm" "user-invocable")
    if [[ "$user_inv" == "true" ]]; then
      log_warn "$file: Redundant default 'user-invocable: true' (defaults to true, omit this)"
    fi
  fi
  
  if has_yaml_key "$fm" "allowed-tools"; then
    local tools
    tools=$(get_yaml_value "$fm" "allowed-tools")
    if [[ "$tools" =~ Skill\( ]]; then
      if [[ ! "$tools" =~ Skill\([a-z0-9-]+\) ]]; then
        log_warn "$file: Skill() syntax might be malformed in allowed-tools"
      fi
    fi
  fi
  
  if has_yaml_key "$fm" "hooks"; then
    local hooks_content
    hooks_content=$(awk '/^hooks:/{f=1;next} /^[a-z-]+:/{if(f)f=0} f' "$file")
    if echo "$hooks_content" | grep -qE "^\s+(SessionStart|UserPromptSubmit|PermissionRequest|Notification|SubagentStop|SessionEnd|PreCompact):"; then
      log_error "$file: Skill hooks only support PreToolUse, PostToolUse, Stop events"
    fi
  fi
}

validate_command() {
  local file="$1"
  local fm
  fm=$(extract_frontmatter "$file")
  
  if ! has_yaml_key "$fm" "description"; then
    log_error "$file: Missing required field 'description'"
  fi
  
  if has_yaml_key "$fm" "model"; then
    log_warn "$file: Hardcoded 'model' field (keep components generalistic, omit model)"
  fi
}

validate_agent() {
  local file="$1"
  local fm
  fm=$(extract_frontmatter "$file")
  local agent_name
  agent_name=$(basename "$file" .md)
  
  if has_yaml_key "$fm" "name"; then
    local name
    name=$(get_yaml_value "$fm" "name")
    if [[ "$name" != "$agent_name" ]]; then
      log_warn "$file: name '$name' should match filename '$agent_name'"
    fi
  fi
  
  if ! has_yaml_key "$fm" "description"; then
    log_error "$file: Missing required field 'description'"
  fi
  
  if has_yaml_key "$fm" "model"; then
    log_warn "$file: Hardcoded 'model' field (keep components generalistic, omit model)"
  fi
}

log_info "Validating Skill frontmatter..."
while IFS= read -r -d '' file; do
  validate_skill "$file"
done < <(find plugins -name "SKILL.md" -type f -print0 2>/dev/null)

log_info "Validating Command frontmatter..."
while IFS= read -r -d '' file; do
  validate_command "$file"
done < <(find plugins/*/commands -name "*.md" -type f -not -path "*/references/*" -print0 2>/dev/null)

log_info "Validating Agent frontmatter..."
while IFS= read -r -d '' file; do
  validate_agent "$file"
done < <(find plugins/*/agents -name "*.md" -type f -not -path "*/references/*" -print0 2>/dev/null)

echo
if [[ "$EXIT_CODE" -eq 0 ]]; then
  log_info "No critical frontmatter issues found."
else
  echo "[SUMMARY] Critical issues found. Exit code: $EXIT_CODE"
fi

exit "$EXIT_CODE"
