# Performance Optimization

## Timeout Guidelines

| Operation Type | Timeout | Examples |
|---------------|---------|----------|
| **Fast** | 5-10s | File existence checks, simple regex |
| **Standard** | 30s | Git operations, linting, formatting |
| **Complex** | 60s | Build processes, large file operations |

## Optimization Strategies

### 1. Minimize Hook Execution

- Use matchers to filter specific tools only
- Avoid wildcard matchers when possible
- Cache expensive operations

### 2. Fast File Operations

```bash
# Fast existence check
[ -f "$file_path" ] && echo "exists" || echo "missing"

# Use test operators
[ -r "$file_path" ] && [ -w "$file_path" ] && echo "readable and writable"
```

### 3. Parallel Execution

Hooks run in parallel. Design them to be independent:

```json
{
  "matcher": "Write",
  "hooks": [
    {
      "type": "command",
      "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/check1.sh",
      "timeout": 10
    },
    {
      "type": "command",
      "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/check2.sh",
      "timeout": 10
    }
  ]
}
```

Both checks run simultaneously.

### 4. Caching

For expensive operations, cache results:

```bash
cache_file="/tmp/hook_cache_$(echo "$1" | md5sum | cut -d' ' -f1)"

if [ -f "$cache_file" ] && [ $(find "$cache_file" -mtime -1 2>/dev/null) ]; then
  cat "$cache_file"
  exit 0
fi

# Expensive operation
result=$(expensive_operation)

# Cache result
echo "$result" > "$cache_file"
echo "$result"
```

## Common Performance Issues

### Issue: Slow File I/O

**Solution:** Use efficient tools

```bash
# Slow
cat large_file.txt | grep pattern

# Fast
grep pattern large_file.txt
```

### Issue: Too Many Hooks

**Solution:** Consolidate checks

```json
{
  "hooks": [
    {
      "type": "command",
      "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/comprehensive_check.sh",
      "timeout": 30
    }
  ]
}
```

### Issue: Long External Tool Calls

**Solution:** Add timeouts and fallbacks

```bash
# With timeout
timeout 30s expensive_operation || {
  echo "Operation timed out" >&2
  exit 124
}

# Background processing
expensive_operation &
PID=$!
sleep 30 && kill $PID 2>/dev/null
wait $PID
```

## Performance Monitoring

### Measure Execution Time

```bash
start=$(date +%s.%N)
# ... operation ...
end=$(date +%s.%N)
duration=$(echo "$end - $start" | bc)
echo "Execution time: ${duration}s"
```

### Log Performance Metrics

```bash
{
  "continue": true,
  "systemMessage": "Hook executed in ${duration}ms"
}
```

## Best Practices Summary

1. **Set realistic timeouts**
2. **Filter hooks with precise matchers**
3. **Cache expensive operations**
4. **Use parallel execution when possible**
5. **Optimize file operations**
6. **Monitor and log performance**
7. **Test with realistic data**
8. **Profile slow operations**
9. **Use background tasks for long operations**
10. **Implement exponential backoff for retries**
