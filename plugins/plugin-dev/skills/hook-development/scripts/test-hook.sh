#!/bin/bash
# Hook Testing Helper
# Tests individual hook scripts or prompt hooks with sample input
# Measures execution time and validates output

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Usage
show_usage() {
  cat <<EOF
Usage: $0 [options] <hook-script|prompt-text> <test-input.json>

Tests a hook with sample input and shows detailed results.

Options:
  -h, --help              Show this help message
  -v, --verbose           Show detailed execution information
  -t, --timeout N         Set timeout in seconds (default: 60)
  --create-sample TYPE     Generate sample test input for event type
  --show-templates         Show available event templates
  --dry-run              Show what would be tested without executing
  --json                  Output results in JSON format

Arguments:
  hook-script             Path to hook script (bash file)
                          OR prompt text (if using --prompt flag)
  test-input.json         Path to test input JSON file

Examples:
  # Test a command hook script
  $0 scripts/validate-write.sh test-input.json

  # Test with verbose output
  $0 -v -t 30 scripts/validate-bash.sh write-input.json

  # Create sample input
  $0 --create-sample PreToolUse > test-input.json

  # Test prompt hook directly
  $0 --prompt "Validate file write safety" test-input.json

Event Types for --create-sample:
  PreToolUse, PostToolUse, Stop, SubagentStop
  UserPromptSubmit, SessionStart, SessionEnd
  Notification
EOF
  exit 0
}

# Parse arguments
VERBOSE=false
TIMEOUT=60
CREATE_SAMPLE=""
SHOW_TEMPLATES=false
DRY_RUN=false
OUTPUT_JSON=false
IS_PROMPT_HOOK=false

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help)
      show_usage
      ;;
    -v|--verbose)
      VERBOSE=true
      shift
      ;;
    -t|--timeout)
      TIMEOUT="$2"
      shift 2
      ;;
    --create-sample)
      CREATE_SAMPLE="$2"
      shift 2
      ;;
    --show-templates)
      SHOW_TEMPLATES=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --json)
      OUTPUT_JSON=true
      shift
      ;;
    --prompt)
      IS_PROMPT_HOOK=true
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

if [ "$SHOW_TEMPLATES" = true ]; then
  cat <<EOF
Available Event Templates:

1. PreToolUse
   - Triggered before tool execution
   - Fields: tool_name, tool_input, tool_result

2. PostToolUse
   - Triggered after tool completion
   - Fields: tool_name, tool_input, tool_result

3. Stop
   - Triggered when agent considers stopping
   - Fields: reason, transcript_path

4. SubagentStop
   - Triggered when subagent completes
   - Fields: reason, transcript_path

5. UserPromptSubmit
   - Triggered when user submits prompt
   - Fields: user_prompt

6. SessionStart
   - Triggered when session begins
   - Fields: session_id, cwd

7. SessionEnd
   - Triggered when session ends
   - Fields: session_id, cwd

8. Notification
   - Triggered on notifications
   - Fields: notification_type, message

Use: $0 --create-sample <EventType> > test-input.json
EOF
  exit 0
fi

if [ -n "$CREATE_SAMPLE" ]; then
  create_sample_input "$CREATE_SAMPLE"
  exit 0
fi

if [ $# -ne 2 ]; then
  echo "Error: Missing required arguments" >&2
  echo ""
  show_usage
fi

HOOK_TARGET="$1"
TEST_INPUT="$2"

# Validate inputs
if [ "$IS_PROMPT_HOOK" = false ] && [ ! -f "$HOOK_TARGET" ]; then
  echo -e "${RED}❌ Error: Hook script not found: $HOOK_TARGET${NC}" >&2
  exit 1
fi

if [ ! -f "$TEST_INPUT" ]; then
  echo -e "${RED}❌ Error: Test input file not found: $TEST_INPUT${NC}" >&2
  exit 1
fi

# Validate timeout
if ! [[ "$TIMEOUT" =~ ^[0-9]+$ ]] || [ "$TIMEOUT" -lt 1 ]; then
  echo -e "${RED}❌ Error: Invalid timeout value: $TIMEOUT${NC}" >&2
  exit 1
fi

# Create sample input function
create_sample_input() {
  local event_type="$1"

  case "$event_type" in
    PreToolUse)
      cat <<'EOF'
{
  "session_id": "test-session-123",
  "transcript_path": "/tmp/test-transcript.txt",
  "cwd": "/tmp/test-project",
  "permission_mode": "ask",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/tmp/test-project/test.txt",
    "content": "Test file content"
  },
  "context": {
    "project_type": "nodejs",
    "user_id": "test-user"
  }
}
EOF
      ;;
    PostToolUse)
      cat <<'EOF'
{
  "session_id": "test-session-123",
  "transcript_path": "/tmp/test-transcript.txt",
  "cwd": "/tmp/test-project",
  "permission_mode": "ask",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/tmp/test-project/test.js",
    "content": "console.log('test');"
  },
  "tool_result": {
    "success": true,
    "message": "File written successfully"
  }
}
EOF
      ;;
    Stop|SubagentStop)
      cat <<'EOF'
{
  "session_id": "test-session-123",
  "transcript_path": "/tmp/test-transcript.txt",
  "cwd": "/tmp/test-project",
  "permission_mode": "ask",
  "hook_event_name": "Stop",
  "reason": "Task appears complete",
  "context": {
    "tasks_completed": ["task1", "task2"],
    "files_modified": ["src/index.js"]
  }
}
EOF
      ;;
    UserPromptSubmit)
      cat <<'EOF'
{
  "session_id": "test-session-123",
  "transcript_path": "/tmp/test-transcript.txt",
  "cwd": "/tmp/test-project",
  "permission_mode": "ask",
  "hook_event_name": "UserPromptSubmit",
  "user_prompt": "Create a new component for user authentication"
}
EOF
      ;;
    SessionStart)
      cat <<'EOF'
{
  "session_id": "test-session-123",
  "transcript_path": "/tmp/test-transcript.txt",
  "cwd": "/tmp/test-project",
  "permission_mode": "ask",
  "hook_event_name": "SessionStart",
  "context": {
    "project_path": "/tmp/test-project",
    "project_type": "nodejs"
  }
}
EOF
      ;;
    SessionEnd)
      cat <<'EOF'
{
  "session_id": "test-session-123",
  "transcript_path": "/tmp/test-transcript.txt",
  "cwd": "/tmp/test-project",
  "permission_mode": "ask",
  "hook_event_name": "SessionEnd",
  "context": {
    "session_duration": 3600,
    "tools_used": ["Read", "Write", "Bash"]
  }
}
EOF
      ;;
    Notification)
      cat <<'EOF'
{
  "session_id": "test-session-123",
  "transcript_path": "/tmp/test-transcript.txt",
  "cwd": "/tmp/test-project",
  "permission_mode": "ask",
  "hook_event_name": "Notification",
  "notification_type": "permission_prompt",
  "message": "Requesting permission to run bash command",
  "severity": "info"
}
EOF
      ;;
    *)
      echo "Unknown event type: $event_type" >&2
      echo "Valid types: PreToolUse, PostToolUse, Stop, SubagentStop, UserPromptSubmit, SessionStart, SessionEnd, Notification" >&2
      exit 1
      ;;
  esac
}

# Validate JSON
validate_json() {
  local json_file="$1"
  if ! jq empty "$json_file" 2>/dev/null; then
    echo -e "${RED}❌ Error: Test input is not valid JSON${NC}" >&2
    return 1
  fi
  return 0
}

# Parse test input for reporting
parse_test_input() {
  local input_file="$1"
  jq -r '
    "Event: " + (.hook_event_name // "unknown") +
    "\nTool: " + (.tool_name // "N/A") +
    "\nSession: " + (.session_id // "unknown")
  ' "$input_file"
}

# Run the hook
run_hook() {
  local hook_target="$1"
  local test_input="$2"

  if [ "$IS_PROMPT_HOOK" = true ]; then
    # For prompt hooks, we simulate the behavior
    local prompt_text="$hook_target"
    local input_data=$(cat "$test_input")

    if [ "$VERBOSE" = true ]; then
      echo -e "${CYAN}Prompt Hook Test${NC}"
      echo "Prompt: $prompt_text"
      echo ""
      echo "Input Data:"
      echo "$input_data" | jq .
      echo ""
    fi

    # Simulate prompt hook (we can't actually run it without Claude Code)
    echo -e "${YELLOW}ℹ️  Note: Prompt hooks cannot be tested directly without Claude Code${NC}" >&2
    echo -e "${YELLOW}   This is a command hook testing tool${NC}" >&2
    echo ""
    echo "To test prompt hooks, use this test input in Claude Code with debug mode:"
    echo "  claude --debug"
    echo ""
    echo "Prompt to use:"
    echo "  $prompt_text"
    echo ""
    echo "Sample input saved to: $test_input"

    return 0
  else
    # For command hooks, run the actual script
    if [ ! -x "$hook_target" ]; then
      echo -e "${YELLOW}⚠️  Warning: Hook script is not executable${NC}" >&2
      echo -e "${YELLOW}   Attempting to run with bash...${NC}" >&2
    fi

    # Run the hook with timeout
    start_time=$(date +%s%N)

    set +e
    output=$(timeout "$TIMEOUT" bash -c "cat '$test_input' | '$hook_target'" 2>&1)
    exit_code=$?
    set -e

    end_time=$(date +%s%N)
    duration=$(( (end_time - start_time) / 1000000 ))  # Convert to milliseconds

    echo "$output"
    return $exit_code
  fi
}

# Analyze results
analyze_results() {
  local exit_code="$1"
  local duration="$2"
  local output="$3"

  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  if [ "$OUTPUT_JSON" = true ]; then
    # JSON output format
    jq -n \
      --arg exit_code "$exit_code" \
      --arg duration "$duration" \
      --argjson output "$output" \
      '{
        exit_code: ($exit_code | tonumber),
        duration_ms: ($duration | tonumber),
        output: $output,
        success: ($exit_code == 0 or $exit_code == 2)
      }'
    return
  fi

  echo -e "${BLUE}Test Results:${NC}"
  echo ""
  echo -e "Exit Code: ${exit_code}"
  echo -e "Duration: ${CYAN}${duration}ms${NC}"
  echo ""

  case $exit_code in
    0)
      echo -e "${GREEN}✅ Hook approved/succeeded${NC}"
      ;;
    2)
      echo -e "${RED}🚫 Hook blocked/denied${NC}"
      ;;
    124)
      echo -e "${RED}⏱️  Hook timed out after ${TIMEOUT}s${NC}"
      ;;
    *)
      echo -e "${YELLOW}⚠️  Hook returned unexpected exit code: $exit_code${NC}"
      ;;
  esac

  echo ""
  echo "Output:"
  if [ -n "$output" ]; then
    echo "$output"
    echo ""

    # Try to parse as JSON
    if echo "$output" | jq empty 2>/dev/null; then
      echo "Parsed JSON output:"
      echo "$output" | jq .
    fi
  else
    echo "(no output)"
  fi

  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  if [ $exit_code -eq 0 ] || [ $exit_code -eq 2 ]; then
    echo -e "${GREEN}✅ Test completed successfully${NC}"
    return 0
  else
    echo -e "${RED}❌ Test failed${NC}"
    return 1
  fi
}

# Main execution
echo -e "${BLUE}🧪 Testing Hook${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$IS_PROMPT_HOOK" = true ]; then
  echo -e "${CYAN}Hook Type: ${GREEN}Prompt Hook${NC}"
else
  echo -e "${CYAN}Hook Type: ${GREEN}Command Hook${NC}"
  echo "Script: $HOOK_TARGET"
fi

echo "Input: $TEST_INPUT"
echo "Timeout: ${TIMEOUT}s"
echo ""

if [ "$VERBOSE" = true ]; then
  echo "Test Input Details:"
  parse_test_input "$TEST_INPUT"
  echo ""
fi

if [ "$DRY_RUN" = true ]; then
  echo -e "${YELLOW}ℹ️  Dry run mode - not executing hook${NC}"
  exit 0
fi

# Validate test input
if ! validate_json "$TEST_INPUT"; then
  exit 1
fi

# Run the hook
echo -e "${CYAN}▶️  Running hook...${NC}"
echo ""

output=$(run_hook "$HOOK_TARGET" "$TEST_INPUT")
exit_code=$?

# Calculate duration
duration=0  # Will be set by run_hook

# Analyze and display results
analyze_results "$exit_code" "$duration" "$output"
final_exit_code=$?

echo ""

if [ $final_exit_code -eq 0 ]; then
  echo -e "${GREEN}✓ Hook test passed${NC}"
else
  echo -e "${RED}✗ Hook test failed${NC}"
fi

exit $final_exit_code
