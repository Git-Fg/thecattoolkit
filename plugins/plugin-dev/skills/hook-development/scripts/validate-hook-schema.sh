#!/bin/bash
# Hook Schema Validator
# Validates hooks.json configuration for structure, syntax, and best practices

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Usage
show_usage() {
  cat <<EOF
Usage: $0 <path/to/hooks.json>

Validates hook configuration file for:
  - Valid JSON syntax
  - Required fields presence
  - Hook type validity (command/prompt)
  - Matcher patterns
  - Timeout value ranges
  - Prompt-based hook event compatibility
  - Best practices (paths, etc.)

Examples:
  $0 hooks/hooks.json
  $0 -v hooks/hooks.json
  $0 --strict hooks/hooks.json

Options:
  -h, --help       Show this help message
  -v, --verbose    Show detailed validation output
  --strict         Enable strict validation mode
  --no-warnings    Treat warnings as errors
EOF
  exit 0
}

# Parse arguments
VERBOSE=false
STRICT=false
NO_WARNINGS=false

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help)
      show_usage
      ;;
    -v|--verbose)
      VERBOSE=true
      shift
      ;;
    --strict)
      STRICT=true
      shift
      ;;
    --no-warnings)
      NO_WARNINGS=true
      shift
      ;;
    -*)
      echo "Unknown option: $1" >&2
      show_usage
      ;;
    *)
      break
      ;;
  esac
done

if [ $# -eq 0 ]; then
  echo "Error: Missing required argument" >&2
  echo ""
  show_usage
fi

HOOKS_FILE="$1"

if [ ! -f "$HOOKS_FILE" ]; then
  echo -e "${RED}❌ Error: File not found: $HOOKS_FILE${NC}" >&2
  exit 1
fi

echo -e "${BLUE}🔍 Validating hooks configuration: $HOOKS_FILE${NC}"
echo ""

# Validation state
ERRORS=0
WARNINGS=0

# Helper functions
log_error() {
  echo -e "${RED}❌ $1${NC}" >&2
  ((ERRORS++))
}

log_warning() {
  echo -e "${YELLOW}⚠️  $1${NC}" >&2
  ((WARNINGS++))
}

log_info() {
  if [ "$VERBOSE" = true ]; then
    echo -e "${BLUE}ℹ️  $1${NC}" >&2
  fi
}

log_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

# Check 1: Valid JSON syntax
echo "Checking JSON syntax..."
if ! jq empty "$HOOKS_FILE" 2>/dev/null; then
  log_error "Invalid JSON syntax"
  if [ "$VERBOSE" = true ]; then
    jq . "$HOOKS_FILE" 2>&1 | head -20 >&2
  fi
else
  log_success "Valid JSON syntax"
fi

# Check 2: Root structure
echo ""
echo "Checking root structure..."
VALID_EVENTS=("PreToolUse" "PostToolUse" "UserPromptSubmit" "Stop" "SubagentStop" "SessionStart" "SessionEnd" "PreCompact" "Notification")

# Check if hooks.json has "hooks" wrapper (plugin format) or direct events (settings format)
if jq -e '.hooks' "$HOOKS_FILE" >/dev/null 2>&1; then
  log_info "Plugin format detected (has 'hooks' wrapper)"

  # Validate wrapper
  if jq -e '.hooks | type == "object"' "$HOOKS_FILE" >/dev/null 2>&1; then
    log_success "Valid 'hooks' wrapper structure"
  else
    log_error "'hooks' field must be an object"
  fi

  # Get events from inside wrapper
  EVENTS=$(jq -r '.hooks | keys[]' "$HOOKS_FILE" 2>/dev/null || echo "")
else
  log_info "Settings format detected (direct events)"

  # Get events from root
  EVENTS=$(jq -r 'keys[]' "$HOOKS_FILE" 2>/dev/null || echo "")
fi

if [ -z "$EVENTS" ]; then
  log_warning "No hook events found"
else
  log_success "Hook events found: $(echo "$EVENTS" | tr '\n' ' ')"
fi

# Validate each event
for event in $EVENTS; do
  VALID_EVENT=false
  for valid_event in "${VALID_EVENTS[@]}"; do
    if [ "$event" = "$valid_event" ]; then
      VALID_EVENT=true
      break
    fi
  done

  if [ "$VALID_EVENT" = false ]; then
    log_warning "Unknown event type: '$event' (valid: ${VALID_EVENTS[*]})"
  fi
done

# Check 3: Validate each hook definition
echo ""
echo "Validating individual hook definitions..."

if [ -z "$EVENTS" ]; then
  log_error "No events to validate"
else
  for event in $EVENTS; do
    log_info "Validating event: $event"

    # Get hook array path
    if jq -e '.hooks' "$HOOKS_FILE" >/dev/null 2>&1; then
      HOOK_PATH=".hooks.\"$event\""
    else
      HOOK_PATH=".\"$event\""
    fi

    hook_count=$(jq -r "$HOOK_PATH | length" "$HOOKS_FILE" 2>/dev/null || echo "0")

    if [ "$hook_count" = "0" ] || [ "$hook_count" = "null" ]; then
      log_warning "Event '$event' has no hooks defined"
      continue
    fi

    log_success "Event '$event' has $hook_count hook(s)"

    # Validate each hook in the array
    for ((i=0; i<hook_count; i++)); do
      log_info "  Validating hook #$((i+1)) in event '$event'"

      # Check matcher exists
      matcher=$(jq -r "$HOOK_PATH[$i].matcher // empty" "$HOOKS_FILE" 2>/dev/null || echo "")

      if [ -z "$matcher" ] || [ "$matcher" = "null" ]; then
        log_error "  Event '$event' hook #$((i+1)): Missing 'matcher' field"
        continue
      fi

      log_success "  Hook #$((i+1)): Valid matcher: '$matcher'"

      # Check hooks array exists
      hooks=$(jq -r "$HOOK_PATH[$i].hooks // empty" "$HOOKS_FILE" 2>/dev/null || echo "")

      if [ -z "$hooks" ] || [ "$hooks" = "null" ]; then
        log_error "  Event '$event' hook #$((i+1)): Missing 'hooks' array"
        continue
      fi

      # Check hooks is array
      if ! jq -e "$HOOK_PATH[$i].hooks | type == \"array\"" "$HOOKS_FILE" >/dev/null 2>&1; then
        log_error "  Event '$event' hook #$((i+1)): 'hooks' must be an array"
        continue
      fi

      hook_array_count=$(jq -r "$HOOK_PATH[$i].hooks | length" "$HOOKS_FILE" 2>/dev/null || echo "0")

      if [ "$hook_array_count" = "0" ]; then
        log_warning "  Event '$event' hook #$((i+1)): Empty hooks array"
        continue
      fi

      log_success "  Hook #$((i+1)): Has $hook_array_count hook definition(s)"

      # Validate each hook definition in the array
      for ((j=0; j<hook_array_count; j++)); do
        log_info "    Validating hook definition #$((j+1))"

        # Check type field
        hook_type=$(jq -r "$HOOK_PATH[$i].hooks[$j].type // empty" "$HOOKS_FILE" 2>/dev/null || echo "")

        if [ -z "$hook_type" ] || [ "$hook_type" = "null" ]; then
          log_error "    Event '$event' hook #$((i+1)) definition #$((j+1)): Missing 'type' field"
          continue
        fi

        # Validate type
        if [ "$hook_type" != "command" ] && [ "$hook_type" != "prompt" ]; then
          log_error "    Event '$event' hook #$((i+1)) definition #$((j+1)): Invalid type '$hook_type' (must be 'command' or 'prompt')"
          continue
        fi

        log_success "    Hook definition #$((j+1)): Valid type: '$hook_type'"

        # Type-specific validation
        if [ "$hook_type" = "command" ]; then
          # Check command field
          command=$(jq -r "$HOOK_PATH[$i].hooks[$j].command // empty" "$HOOKS_FILE" 2>/dev/null || echo "")

          if [ -z "$command" ]; then
            log_error "    Command hook definition #$((j+1)): Missing 'command' field"
          else
            log_success "    Command hook definition #$((j+1)): Has command: '${command:0:50}...'"

            # Check for hardcoded paths
            if [[ "$command" == /* ]] && [[ "$command" != *'\${CLAUDE_PLUGIN_ROOT}'* ]]; then
              log_warning "    Command hook definition #$((j+1)): Hardcoded absolute path detected. Consider using \${CLAUDE_PLUGIN_ROOT} for portability"
            fi

            # Check if script file exists (if relative path)
            if [[ "$command" != http* ]] && [[ "$command" != https* ]]; then
              script_path=$(echo "$command" | sed 's/^bash\s*//' | sed 's/\${CLAUDE_PLUGIN_ROOT}/./g' | awk '{print $1}')
              if [ -n "$script_path" ] && [ ! -f "$script_path" ] && [ ! -x "$script_path" ]; then
                log_warning "    Command hook definition #$((j+1)): Script file not found or not executable: $script_path"
              fi
            fi
          fi
        elif [ "$hook_type" = "prompt" ]; then
          # Check prompt field
          prompt=$(jq -r "$HOOK_PATH[$i].hooks[$j].prompt // empty" "$HOOKS_FILE" 2>/dev/null || echo "")

          if [ -z "$prompt" ]; then
            log_error "    Prompt hook definition #$((j+1)): Missing 'prompt' field"
          else
            prompt_length=${#prompt}
            log_success "    Prompt hook definition #$((j+1)): Has prompt ($prompt_length chars)"

            # Check prompt-based hook compatibility with event
            if [ "$event" != "Stop" ] && [ "$event" != "SubagentStop" ] && [ "$event" != "UserPromptSubmit" ] && [ "$event" != "PreToolUse" ]; then
              log_warning "    Prompt hook definition #$((j+1)): Prompt hooks may not be fully supported on event '$event' (best supported on: Stop, SubagentStop, UserPromptSubmit, PreToolUse)"
            fi

            # Check prompt length (very long prompts might be problematic)
            if [ "$prompt_length" -gt 2000 ]; then
              log_warning "    Prompt hook definition #$((j+1)): Very long prompt ($prompt_length chars). Consider shortening."
            fi
          fi
        fi

        # Check timeout field (optional)
        timeout=$(jq -r "$HOOK_PATH[$i].hooks[$j].timeout // empty" "$HOOKS_FILE" 2>/dev/null || echo "")

        if [ -n "$timeout" ] && [ "$timeout" != "null" ]; then
          # Validate timeout is a number
          if ! [[ "$timeout" =~ ^[0-9]+$ ]]; then
            log_error "    Hook definition #$((j+1)): Timeout must be a number, got '$timeout'"
          elif [ "$timeout" -lt 5 ]; then
            log_warning "    Hook definition #$((j+1)): Timeout ($timeout seconds) is very low. Recommended: 5-10s minimum"
          elif [ "$timeout" -gt 600 ]; then
            log_warning "    Hook definition #$((j+1)): Timeout ($timeout seconds) is very high. Recommended: Maximum 600s (10 minutes)"
          elif [ "$hook_type" = "command" ] && [ "$timeout" -gt 60 ]; then
            log_warning "    Hook definition #$((j+1)): Command hook timeout ($timeout seconds) is high. Recommended: 60s maximum"
          elif [ "$hook_type" = "prompt" ] && [ "$timeout" -gt 30 ]; then
            log_warning "    Hook definition #$((j+1)): Prompt hook timeout ($timeout seconds) is high. Recommended: 30s maximum"
          else
            log_success "    Hook definition #$((j+1)): Valid timeout: ${timeout}s"
          fi
        else
          # Provide default timeout recommendations
          if [ "$hook_type" = "command" ]; then
            log_info "    Hook definition #$((j+1)): No timeout specified (recommended: 60s for command hooks)"
          else
            log_info "    Hook definition #$((j+1)): No timeout specified (recommended: 30s for prompt hooks)"
          fi
        fi
      done
    done
  done
fi

# Check 4: Best practices validation
echo ""
echo "Checking best practices..."

# Check for duplicate events
ALL_EVENTS=$(jq -r 'keys[]' "$HOOKS_FILE" 2>/dev/null || echo "")
if [ -n "$ALL_EVENTS" ]; then
  DUPLICATES=$(echo "$ALL_EVENTS" | sort | uniq -d)
  if [ -n "$DUPLICATES" ]; then
    log_warning "Duplicate event definitions found: $DUPLICATES"
  else
    log_success "No duplicate event definitions"
  fi
fi

# Check for empty hooks arrays
for event in $EVENTS; do
  if jq -e ".hooks.\"$event\" | length == 0" "$HOOKS_FILE" >/dev/null 2>&1; then
    log_warning "Event '$event' has an empty hooks array"
  fi
done 2>/dev/null || true

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Validation Summary${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
  echo -e "${GREEN}✅ All checks passed!${NC}"
  echo ""
  echo "Your hooks configuration is valid and follows best practices."
  exit 0
elif [ $ERRORS -eq 0 ]; then
  echo -e "${YELLOW}⚠️  Validation passed with $WARNINGS warning(s)${NC}"
  echo ""
  if [ "$NO_WARNINGS" = true ]; then
    echo "Treating warnings as errors (--no-warnings flag set)"
    exit 1
  else
    echo "Consider fixing these warnings for better configuration."
    exit 0
  fi
else
  echo -e "${RED}❌ Validation failed${NC}"
  echo ""
  echo -e "${RED}Errors: $ERRORS${NC}"
  echo -e "${YELLOW}Warnings: $WARNINGS${NC}"
  echo ""
  echo "Please fix the errors above before using this configuration."
  exit 1
fi
