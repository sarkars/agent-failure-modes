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

## Mitigation Strategies

### Prevention
1. **Reject malformed IDs instead of silently stripping prefixes**: The most destructive pattern here — `get_order_status(order_id="ORD-42")` having its "ORD-" prefix silently stripped to query order #42, a completely different order — must become a hard validation failure ("order_id must match pattern ORD-\d+, got a bare integer after normalization") rather than a best-effort parse. Trade-off: strict format enforcement means genuinely benign format variations (e.g., a client that always omits the prefix) start failing loudly, which can feel like a regression if not communicated.
2. **Strict Pydantic/schema validation with no implicit coercion enabled**: Configure validation models to reject rather than auto-convert (Pydantic's `strict=True` mode, or equivalent), since the root cause is specifically that "lenient tools accept the input and return structurally valid but semantically wrong results" — the fix is removing leniency, not improving it. Trade-off: some legitimately safe conversions (numeric string "123" to int 123 with no semantic ambiguity) also start failing, requiring an explicit allowlist of safe coercions if any leniency is kept.
3. **Semantic response validation — verify the response actually answers the request**: Since the tool returned "a structured response with status, tracking, etc." that looked entirely valid despite being for the wrong order, add a check that `response.order_id == request.order_id` (post-normalization) before the tool result is trusted, catching the exact "wrong but valid ID" pattern identified as the most destructive of the three coercion types. Trade-off: requires every tool to echo back the resolved identifier in its response, which not all APIs naturally provide.

### Detection & Response
1. **Contradiction queries across input/output logs**: Since every tool call is logged with input/output pairs, run scheduled queries specifically for `response.<id_field> != request.<id_field>` across the fleet — this is a direct, mechanical way to surface the exact silent-coercion pattern in the example without waiting for a user to notice a wrong order status.
2. **Retry-without-error-signal tracking**: The detection notes call out that agents sometimes retry the same call when "something's wrong" even without an explicit error — track cases where the same tool+similar-input is called multiple times in close succession with no error response in between, since this pattern often indicates the agent sensed something was off with a seemingly-successful but semantically wrong result.
3. **Format-mismatch-without-failure sampling**: Periodically sample tool calls where the input format didn't exactly match the documented schema (e.g., string where int expected) but the call still returned "success," and manually verify whether the result was actually correct — this catches coercion happening below the error-log threshold.

### Architecture Patterns
1. **Strict schema validation gate with zero silent coercion**: Insert a validation layer (Pydantic strict mode, JSON Schema with `additionalProperties: false` and no type coercion) between the agent's tool call and the underlying implementation, so "ORD-42" is rejected at the gate rather than reaching business logic that strips it to 42; deployment consideration — this is a breaking change for any existing lenient caller, so needs a rollout with monitoring for a spike in newly-rejected (previously silently-miscoerced) calls.
2. **Contradiction-check middleware on every response**: Wrap tool responses in a middleware that automatically checks identifier fields in the response against the request before returning to the agent, independent of the specific tool's internal implementation; deployment consideration — only catches cases where the tool echoes an identifiable field back, so doesn't cover every possible coercion (e.g., an aggregate query with no single echoable ID).
3. **Enum/pattern constraints on identifier-shaped parameters**: Where order IDs, customer IDs, etc. follow a known format, enforce it as a regex-constrained string type rather than a loosely-typed integer-or-string field, closing off the entire class of "coerce/strip to make a valid-looking integer" bugs at the type-system level; deployment consideration — format constraints must be kept in sync if the underlying ID scheme ever changes.

### Metrics
1. **silent_coercion_rate**: Target < 2% of tool calls (down from the cited 37% parameter-mismatch baseline for lenient/legacy tools); Alert if > 15% for any single tool over a week.
2. **response_request_id_mismatch_rate**: Target: 0% — any occurrence of response.id != request.id (post-normalization) is a confirmed instance of this failure mode; Alert on any detected occurrence over a 1-hour window exceeding 1 case.
3. **rejected_malformed_input_rate**: Target: tracked as a positive signal post-migration to strict validation — a rise here (from 0 under the old lenient system) indicates the strict gate is now catching inputs that previously silently miscoerced; no alert threshold, but should be reviewed weekly during rollout.
4. **retry_without_error_rate**: Target < 3% of tool calls followed by a same-tool retry with no intervening error; Alert if > 10% (possible silent-coercion pattern going undetected by the agent's own suspicion).

### Alerts
1. **Confirmed Wrong-Resource Access** (P1): Condition - response_request_id_mismatch_rate detects a response for a different resource than requested (e.g., wrong order_id). Action: page immediately — this is potentially a data-exposure issue (user seeing another customer's order), disable the affected tool's lenient parsing path until patched.
2. **Silent Coercion Rate Elevated** (P2): Condition - silent_coercion_rate exceeds 15% for a specific tool over a week. Action: migrate that tool to strict validation, audit recent input logs for the specific coercion patterns occurring.
3. **Elevated Retry-Without-Error Pattern** (P3): Condition - retry_without_error_rate exceeds 10% for a tool. Action: investigate whether the agent is compensating for suspected-but-undetected wrong results; add contradiction-check middleware if not already present.

## References

- [Roborhythms: Fix AI Agent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - 37% silent failure rate
- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Input validation (#4)
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Tool verification failures
