# Tool Use — Stable Patterns

Tool use enables Claude to interact with external systems through a standardized interface.

## Core Concepts

### Two Tool Types

#### Client Tools
**Execute on your systems**:
- You define the tool interface
- You implement the execution logic
- You handle the results

**Common pattern**:
```python
# Define tool
tools = [{
    "name": "get_weather",
    "description": "Get current weather",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string"}
        },
        "required": ["location"]
    }
}]

# User prompt
prompt = "What's the weather in Tokyo?"

# Claude decides to use tool
# Response: {"tool_use": {"name": "get_weather", "input": {"location": "Tokyo"}}}

# You execute and return result
result = {"tool_result": {"content": "15°C, sunny"}}
```

#### Server Tools
**Execute on Anthropic's servers**:
- Pre-defined by Anthropic
- No implementation needed
- Automatic execution

**Examples**:
- `web_search_20250305`: Search the web
- `web_fetch_20250305`: Fetch web content
- `computer_use_20250124`: Computer control

## Tool Definition Pattern

### Schema Structure
```python
tool = {
    "name": "tool_name",
    "description": "What this tool does",
    "input_schema": {
        "type": "object",
        "properties": {
            "param1": {"type": "string"},
            "param2": {"type": "number"}
        },
        "required": ["param1"]
    }
}
```

### Best Practices

#### 1. Clear Descriptions
```python
# Good
"description": "Get current weather for a city. Use city name like 'Tokyo' or 'New York'."

# Bad
"description": "Weather tool"
```

#### 2. Required Parameters Only
```python
# Good
"required": ["location"]

# Bad
"required": ["location", "unit", "forecast_days"]
```

#### 3. Specific Types
```python
# Good
"location": {"type": "string", "description": "City name, e.g., 'Tokyo'"}

# Bad
"location": {"type": "string"}
```

## MCP Integration

### Converting MCP Tools
MCP tools use `inputSchema`, Claude tools use `input_schema`:

```python
# MCP format
mcp_tool = {
    "name": "search",
    "inputSchema": {
        "type": "object",
        "properties": {"query": {"type": "string"}}
    }
}

# Convert to Claude format
claude_tool = {
    "name": "search",
    "input_schema": {
        "type": "object",
        "properties": {"query": {"type": "string"}}
    }
}
```

### Pattern
```python
async def get_claude_tools(mcp_session):
    mcp_tools = await mcp_session.list_tools()

    claude_tools = []
    for tool in mcp_tools.tools:
        claude_tools.append({
            "name": tool.name,
            "description": tool.description or "",
            "input_schema": tool.inputSchema  # Rename
        })

    return claude_tools
```

## Tool Use Workflows

### Workflow 1: Single Tool
```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    tools=[weather_tool],
    messages=[{"role": "user", "content": "Weather in Tokyo?"}]
)

# Claude uses tool
if response.stop_reason == "tool_use":
    # Extract tool call
    tool_use = response.content[1]  # Tool use block
    tool_name = tool_use.name
    tool_input = tool_use.input

    # Execute tool
    result = execute_tool(tool_name, tool_input)

    # Return result
    response = client.messages.create(
        messages=[
            {"role": "user", "content": "Weather in Tokyo?"},
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": tool_use.id, "content": result}
            ]}
        ]
    )
```

### Workflow 2: Multiple Tools
```python
# Tools available
tools = [search_tool, fetch_tool, analyze_tool]

response = client.messages.create(
    model="claude-sonnet-4-5",
    tools=tools,
    messages=[{"role": "user", "content": "Research AI trends"}]
)

# Claude may use multiple tools in parallel
# Return all results together
results = [...]
response = client.messages.create(
    messages=[
        ...,
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "id1", "content": "result1"},
            {"type": "tool_result", "tool_use_id": "id2", "content": "result2"}
        ]}
    ]
)
```

### Workflow 3: Sequential Tools
```python
# First tool provides input for second
response1 = client.messages.create(tools=[location_tool], messages=[...])

# Execute location tool
location = execute_tool(location_tool, input)

# Second tool uses location
response2 = client.messages.create(
    tools=[weather_tool],
    messages=[
        ...,
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "id", "content": location}
        ]}
    ]
)
```

## Parallel Tool Use

### Parallel Execution Pattern
Claude can call multiple tools simultaneously:

```python
response = client.messages.create(
    tools=[tool1, tool2, tool3],
    messages=[...]
)

# Response contains multiple tool_use blocks
for content_block in response.content:
    if content_block.type == "tool_use":
        tool_name = content_block.name
        tool_input = content_block.input
        # Execute each tool
        results.append(execute_tool(tool_name, tool_input))

# Return ALL results in single user message
response = client.messages.create(
    messages=[
        ...,
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "id1", "content": "result1"},
            {"type": "tool_result", "tool_use_id": "id2", "content": "result2"},
            {"type": "tool_result", "tool_use_id": "id3", "content": "result3"}
        ]}
    ]
)
```

### Parallel Requirements
1. **All tool_use blocks** in single assistant message
2. **All tool_result blocks** in single user message
3. **Matching IDs** for tool_use and tool_result

## Best Practices

### 1. Validate Inputs
```python
def execute_tool(name, input_data):
    # Validate required fields
    if name == "get_weather":
        if "location" not in input_data:
            raise ValueError("Missing required field: location")

        # Validate format
        location = input_data["location"]
        if not isinstance(location, str):
            raise TypeError("location must be string")

    # Execute
    return result
```

### 2. Handle Errors Gracefully
```python
def execute_tool(name, input_data):
    try:
        result = perform_operation(name, input_data)
        return {"status": "success", "data": result}
    except ValidationError as e:
        return {"status": "error", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": "Internal error"}
```

### 3. Provide Context
```python
# Good: Include context in results
{
    "location": "Tokyo",
    "temperature": 15,
    "unit": "celsius",
    "condition": "sunny",
    "timestamp": "2026-01-13T10:00:00Z"
}

# Bad: Just the data
15
```

### 4. Use Structured Outputs
```python
# Good: Structured data
{
    "users": [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"}
    ]
}

# Bad: Unstructured text
"Alice (alice@example.com), Bob (bob@example.com)"
```

### 5. Structured Outputs with JSON Schema
```python
# Guaranteed schema conformance
response = client.messages.create(
    model="claude-sonnet-4-5",
    tools=[...],
    messages=[...],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "evaluation_result",
            "schema": {
                "type": "object",
                "properties": {
                    "score": {"type": "number", "minimum": 0, "maximum": 100},
                    "passed": {"type": "boolean"},
                    "details": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["score", "passed"]
            }
        }
    }
)

# Response is guaranteed to match schema
result = response.content[0].text
# Type-safe, parseable JSON
```

### 6. Multi-Step Structured Evaluation
```python
# Step 1: Initial evaluation
session_id = None
results = {}

for step in evaluation_steps:
    for message in query(
        prompt=step["prompt"],
        options=ClaudeAgentOptions(
            output_format={
                "type": "json_schema",
                "schema": step["schema"]
            },
            resume=session_id
        )
    ):
        if message.type === 'result':
            if message.subtype === 'success':
                results.update(message.structured_output)
                session_id = message.session_id
```

## Anti-Patterns (Avoid)

❌ **No input validation**:
```python
# Bad
def execute_tool(name, input_data):
    return external_api_call(input_data)  # No validation

# Good
def execute_tool(name, input_data):
    validate_schema(input_data)
    return external_api_call(input_data)
```

❌ **Unstructured results**:
```python
# Bad
"Tokyo is 15 degrees"

# Good
{"location": "Tokyo", "temperature": 15, "unit": "celsius"}
```

❌ **Missing error handling**:
```python
# Bad
return external_api_call()  # Can throw

# Good
try:
    return external_api_call()
except Exception as e:
    return {"error": str(e)}
```

❌ **Tool name too generic**:
```python
# Bad
"name": "search"

# Good
"name": "search_database"
```

## Common Patterns

### Pattern 1: Data Retrieval
```python
search_tool = {
    "name": "search_database",
    "description": "Search application database",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "limit": {"type": "integer", "minimum": 1, "maximum": 100}
        },
        "required": ["query"]
    }
}
```

### Pattern 2: File Operations
```python
read_file_tool = {
    "name": "read_file",
    "description": "Read file contents",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {"type": "string"}
        },
        "required": ["path"]
    }
}
```

### Pattern 3: API Integration
```python
api_tool = {
    "name": "call_api",
    "description": "Call external REST API",
    "input_schema": {
        "type": "object",
        "properties": {
            "endpoint": {"type": "string"},
            "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE"]},
            "data": {"type": "object"}
        },
        "required": ["endpoint", "method"]
    }
}
```

## Error Handling

### Common Errors

#### Invalid Tool Call
```json
{
  "error": "Invalid parameters",
  "details": "Missing required field: location"
}
```

#### Tool Not Found
```json
{
  "error": "Tool not found",
  "tool_name": "unknown_tool"
}
```

#### Execution Error
```json
{
  "error": "Execution failed",
  "message": "Connection timeout",
  "code": "TIMEOUT"
}
```

### Error Response Pattern
```python
def execute_tool(name, input_data):
    try:
        # Validate
        if name not in available_tools:
            return {"error": f"Unknown tool: {name}"}

        # Execute
        result = perform_operation(name, input_data)
        return {"status": "success", "data": result}

    except ValidationError as e:
        return {"error": "Invalid input", "details": str(e)}
    except TimeoutError:
        return {"error": "Timeout", "code": "TIMEOUT"}
    except Exception as e:
        return {"error": "Internal error", "message": str(e)}
```

## Testing Patterns

### Pattern 1: Mock Tools
```python
from unittest.mock import Mock

# Mock tool execution
with mock.patch('your_module.execute_tool') as mock_execute:
    mock_execute.return_value = {"temperature": 15}

    # Test
    result = execute_tool("get_weather", {"location": "Tokyo"})
    assert result["temperature"] == 15
```

### Pattern 2: Test Tool Definitions
```python
def test_tool_schema():
    tool = get_weather_tool()

    # Test required fields
    assert "name" in tool
    assert "description" in tool
    assert "input_schema" in tool

    # Test schema structure
    schema = tool["input_schema"]
    assert schema["type"] == "object"
    assert "location" in schema["properties"]
    assert schema["required"] == ["location"]
```

### Pattern 3: Integration Testing
```python
async def test_tool_integration():
    # Define tools
    tools = [get_weather_tool()]

    # Create request
    response = await client.messages.create(
        model="claude-sonnet-4-5",
        tools=tools,
        messages=[{"role": "user", "content": "Weather in Tokyo?"}]
    )

    # Verify tool was used
    assert response.stop_reason == "tool_use"

    # Execute and return result
    tool_use = response.content[1]
    result = execute_tool(tool_use.name, tool_use.input)

    # Send result back
    final_response = await client.messages.create(
        messages=[...],
        # ... include tool result
    )

    # Verify final response
    assert "Tokyo" in final_response.content
```

## Performance Optimization

### 1. Batch Operations
```python
# Good: Bulk operations
def search_many(queries):
    return [search_single(q) for q in queries]

# Bad: One by one
for query in queries:
    search_single(query)
```

### 2. Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_weather(location):
    return fetch_weather_api(location)
```

### 3. Async Execution
```python
import asyncio

async def execute_tools_parallel(tool_calls):
    tasks = [execute_tool(name, input) for name, input in tool_calls]
    return await asyncio.gather(*tasks)
```

## Security Considerations

### 1. Input Sanitization
```python
def execute_tool(name, input_data):
    # Sanitize inputs
    if "path" in input_data:
        input_data["path"] = os.path.abspath(input_data["path"])
        if not input_data["path"].startswith(ALLOWED_DIR):
            raise PermissionError("Path not allowed")

    # Execute
    return operation(name, input_data)
```

### 2. Rate Limiting
```python
import time

last_call = 0

def rate_limited_tool(name, input_data):
    global last_call
    now = time.time()
    if now - last_call < 1:  # 1 second limit
        time.sleep(1)
    last_call = now
    return operation(name, input_data)
```

### 3. Audit Logging
```python
def execute_tool(name, input_data):
    log_entry = {
        "timestamp": time.time(),
        "tool": name,
        "input": input_data,
        "user": get_current_user()
    }
    audit_log.append(log_entry)

    return operation(name, input_data)
```

## Volatile Details (Look Up)

These change frequently:
- Server tool names (web_search_20250305, etc.)
- Structured output schemas
- Tool use token pricing
- MCP protocol versions

**Always verify**: Use latest documentation for current tool names and schemas.

## Resources

### Official Tools
- Web Search: `web_search_20250305`
- Web Fetch: `web_fetch_20250305`
- Computer Use: `computer_use_20250124`
- Text Editor: `text_editor_20250124`

### Examples
- Calculator tool: https://platform.claude.com/cookbook/tool-use-calculator-tool
- Customer service agent: https://platform.claude.com/cookbook/tool-use-customer-service-agent
- JSON extractor: https://platform.claude.com/cookbook/tool-use-extracting-structured-json

---

## Official Documentation Links

- **Tool Use Overview**: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md
- **Structured Outputs**: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- **Messages API**: https://platform.claude.com/docs/en/api/messages
- **Model Context Protocol**: https://modelcontextprotocol.io
- **Claude API Reference**: https://platform.claude.com/docs/api/reference

### Verification
Last verified: 2026-01-13
