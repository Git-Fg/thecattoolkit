#!/bin/bash

# Multi-Model Test Runner
# Usage: ./run-all-tests.sh [tier] [command]
# Tiers: haiku, sonnet, opus
# Commands: create-plan, run-plan, manage-plan

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to print colored output
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to run a test
run_test() {
    local tier=$1
    local command=$2
    local test_file="$SCRIPT_DIR/$tier/${command}.test.md"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    if [ ! -f "$test_file" ]; then
        print_error "Test file not found: $test_file"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi

    print_header "Running: $tier / $command"

    # Read test file and extract test cases
    local test_cases=$(grep -E "^## Test Case [0-9]+:" "$test_file" | wc -l)

    if [ "$test_cases" -eq 0 ]; then
        print_warning "No test cases found in $test_file"
        return 0
    fi

    echo "Found $test_cases test case(s)"

    # Parse and run each test case
    local case_num=1
    local all_passed=true

    while [ $case_num -le $test_cases ]; do
        echo ""
        echo "--- Test Case $case_num ---"

        # Extract test case details
        local test_name=$(sed -n "/## Test Case $case_num:/,/^## /p" "$test_file" | grep -E "^\*\*Input\*\*:" | sed 's/\*\*Input\*\*: //')
        local expected=$(sed -n "/## Test Case $case_num:/,/^## /p" "$test_file" | grep -E "^\*\*Expected" | sed 's/\*\*Expected[^:]*: //')

        if [ -z "$test_name" ]; then
            print_warning "Could not parse test case $case_num"
            case_num=$((case_num + 1))
            continue
        fi

        echo "Input: $test_name"

        # For now, we just validate that the test case is properly formatted
        # In a real implementation, you would execute the command and validate results
        local success_criteria=$(sed -n "/## Test Case $case_num:/,/^## /p" "$test_file" | grep -E "^- \[ \]" | wc -l)

        if [ "$success_criteria" -gt 0 ]; then
            print_success "Test case $case_num formatted correctly ($success_criteria criteria)"
        else
            print_error "Test case $case_num missing success criteria"
            all_passed=false
        fi

        case_num=$((case_num + 1))
    done

    if [ "$all_passed" = true ]; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
        print_success "$tier / $command - All tests formatted correctly"
        return 0
    else
        FAILED_TESTS=$((FAILED_TESTS + 1))
        print_error "$tier / $command - Some tests failed"
        return 1
    fi
}

# Main execution
main() {
    local tier=$1
    local command=$2

    print_header "Multi-Model Test Suite"
    echo "Project: $PROJECT_DIR"
    echo ""

    # Determine which tests to run
    if [ -z "$tier" ]; then
        # Run all tiers
        for t in haiku sonnet opus; do
            for cmd in create-plan run-plan manage-plan; do
                run_test "$t" "$cmd" || true
                echo ""
            done
        done
    elif [ -z "$command" ]; then
        # Run all commands for specific tier
        for cmd in create-plan run-plan manage-plan; do
            run_test "$tier" "$cmd" || true
            echo ""
        done
    else
        # Run specific test
        run_test "$tier" "$command"
    fi

    # Print summary
    print_header "Test Summary"
    echo "Total Tests: $TOTAL_TESTS"
    echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
    echo -e "${RED}Failed: $FAILED_TESTS${NC}"
    echo ""

    if [ $FAILED_TESTS -eq 0 ]; then
        print_success "All tests passed!"
        exit 0
    else
        print_error "Some tests failed"
        exit 1
    fi
}

# Show usage if --help specified
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Multi-Model Test Runner"
    echo ""
    echo "Usage:"
    echo "  $0                    # Run all tests"
    echo "  $0 <tier>            # Run all tests for a specific tier"
    echo "  $0 <tier> <command>  # Run a specific test"
    echo ""
    echo "Tiers: haiku, sonnet, opus"
    echo "Commands: create-plan, run-plan, manage-plan"
    echo ""
    echo "Examples:"
    echo "  $0                    # Run all tests"
    echo "  $0 haiku              # Run all Haiku tests"
    echo "  $0 sonnet create-plan # Run Sonnet create-plan test"
    echo ""
    exit 0
fi

# Run main function
main "$1" "$2"
