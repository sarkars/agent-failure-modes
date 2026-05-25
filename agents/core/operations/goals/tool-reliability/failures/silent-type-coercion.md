# Silent Type Coercion

## Issue: Tools Accept Wrong Types and Silently Produce Wrong Results

**Frequency**: Very Common (37% of tool calls affected)

**Symptoms**
- Tool executes without error but returns wrong data
- Agent continues with corrupted results
- No validation errors despite wrong parameter types
- Wrong resource accessed due to type conversion
- Compounding errors across multiple turns

**Root Cause**
Tools silently coerce or ignore malformed arguments instead of failing loudly. When an AI passes a string where an integer is expected, or passes a valid ID for the wrong resource, lenient tools accept the input and return structurally valid but semantically wrong results. The agent has no signal that anything went wrong.

**Example**
```
Tool call from AI:
get_order_status(order_id="ORD-42")

What happened internally:
- Tool expected: order_id as integer (42)
- Tool received: string "ORD-42"  
- Tool silently stripped "ORD-" prefix
- Tool queried order #42 (wrong customer's order!)
- Tool returned valid-looking response for wrong order

Agent's view:
✓ Tool call succeeded
✓ Got structured response with status, tracking, etc.
✓ Response looks valid
✗ Data is for completely wrong order

Result: Agent tells user their order shipped
        when it hasn't, because it checked wrong order
```

**Key Statistics**
From Roborhythms Tool Call Analysis (2026):
- 37% of tool calls have parameter mismatches that never raise errors
- Developers logged 72 hours of Claude agent tool calls to find this
- Problem affects OpenAI, Anthropic, and local model setups equally
- Third pattern (wrong but valid ID) is most destructive

**Coercion Patterns**
| Input Type | Expected Type | Coercion | Problem |
|------------|--------------|----------|---------|
| "123" | int | Silent parse | Works but risky |
| "ORD-123" | int | Strip prefix | Wrong ID extracted |
| None | str | Empty string | Silent empty query |
| 123 | str | Auto-convert | May work, may not |
| "true" | bool | Truthy check | Inconsistent logic |

**Contributing Factors**
- Python's duck typing encourages lenient functions
- Tools designed for human callers who "know what they mean"
- No schema validation on tool inputs
- Tools tested with correct inputs only
- Error handling catches exceptions but not semantic errors

**Mitigation Strategies**
1. **Strict Pydantic models**: Validate types before execution
2. **Fail loudly on mismatch**: Return structured error, don't coerce
3. **Contradiction checks**: Verify response matches request
4. **Semantic validation**: Check response.order_id == request.order_id
5. **Logging wrapper**: Log input/output for every tool call
6. **Enum constraints**: Limit valid values where possible

**Detection**
- Log all tool calls with input/output pairs
- Run contradiction queries: "response ID != request ID"
- Compare expected vs. actual types in logs
- Track cases where agent retries same call (knows something's wrong)

## References

- [Roborhythms: Fix AI Agent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - 37% silent failure rate
- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Input validation (#4)
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Tool verification failures
