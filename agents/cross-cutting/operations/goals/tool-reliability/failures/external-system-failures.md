# External System Failures

## Issue: External APIs and Tools Fail, Causing Agent Errors

**Frequency**: Common

**Symptoms**
- API calls return errors agent cannot handle
- Schema changes break previously working integrations
- Rate limits trigger unexpected agent behaviors
- Agent misattributes external failures to its own logic

**Root Cause**
External tools and APIs that agents depend on can fail, change schemas, hit rate limits, or experience runtime issues. Unlike tool invocation errors (where the agent calls tools incorrectly), external system failures occur when correct agent calls encounter broken or changed external systems. These failures propagate through the agent's pipeline, often being misdiagnosed as agent logic errors.

**Example**
```
Task: "Look up the customer's recent orders"

Agent tool call (correct):
get_orders(customer_id="cust_12345", limit=10)

External API response:
{
  "error": "rate_limit_exceeded",
  "retry_after": 60
}

Agent behavior:
"I was unable to find any orders for this customer. 
The customer may be new or have no order history."

Problem:
- Agent received rate limit error, not "no orders"
- Interpreted API failure as data absence
- Gave confident but incorrect answer to user

Result: User believes customer has no orders,
        actual issue is temporary rate limiting
```

**Key Statistics**
From Failure Modes in LLM Systems (arxiv:2511.19933):
- External tool failures identified as distinct from tool invocation errors
- Schema changes, rate limits, and runtime issues propagate downstream
- Failures often misattributed to model logic rather than tool instability
- Concurrent operations amplify cascading failures

**External Failure Types**
- **Schema drift**: API fields renamed, removed, or restructured
- **Rate limiting**: Requests throttled causing timeouts or errors
- **Authentication expiry**: Tokens or keys become invalid
- **Service outages**: External services temporarily unavailable
- **Type mismatches**: API returns different data types than expected

**Agent Misinterpretation Patterns**
| Error | Agent's Interpretation | Actual Cause |
|-------|----------------------|--------------|
| 400 Bad Request | "I made a typo" | Schema changed |
| 401 Unauthorized | "User needs to login" | Token expired |
| 403 Forbidden | "I'll try another tool" | Permissions changed |
| 404 Not Found | "Record doesn't exist" | Endpoint moved |
| 429 Too Many Requests | "System is down" | Rate limited |
| 500 Internal Server Error | "Request succeeded" | Backend crashed |
| 200 OK (empty) | "No data exists" | Wrong query executed |

**Contributing Factors**
- Agents can't distinguish "failed to get data" from "no data exists"
- Error messages designed for developers, not LLMs
- No explicit training on API failure handling
- External changes happen without agent awareness
- Silent failures return valid but wrong responses

## Mitigation Strategies

### Prevention
1. **Explicit error-code-to-meaning mapping in the tool layer, not the agent's head**: Don't rely on the LLM to correctly infer that a 429 means "rate limited, not out of data" — intercept the HTTP status/error body in the tool wrapper and return a structured `{status: "rate_limited", retryable: true}` field so the agent never has to guess, closing the exact misinterpretation shown in the example (rate limit read as "no orders"). Trade-off: requires maintaining a mapping per external API, which drifts as providers change error formats.
2. **Distinguish "no data" from "failed to get data" at the schema level**: Make the tool's success response and error response structurally different (e.g., success always includes `"orders": []` explicitly, while any failure is `{"error": ...}` with no `orders` key at all), so the agent can't conflate an empty result with a failed call the way it did in the example. Trade-off: adds a schema contract that every tool must honor consistently, including for legitimately empty results.
3. **Schema validation on every external response before it reaches the agent**: Validate incoming API payloads against an expected schema (fields, types) before passing them to the agent, catching schema drift (fields renamed/removed) as a distinct, reported failure rather than silently confusing the agent downstream. Trade-off: overly strict validation can reject a response that's still usable, causing false failures on minor, harmless API changes.

### Detection & Response
1. **HTTP status code distribution per tool**: Track the mix of 2xx/4xx/5xx per external tool; a spike in 429s or 401s that the agent logs are treating as generic failures (per the misinterpretation table) reveals systematic misattribution even when the agent's final answer looks confident.
2. **Claim-vs-response mismatch audits**: Sample agent final answers against the raw tool response that produced them (e.g., agent says "no orders" — check whether the underlying call actually returned an empty list or an error object); this directly catches the pattern in the example where a rate-limit error became a false "no orders" claim.
3. **Success-rate step changes**: Alert on sudden drops in a specific external tool's success rate — since agents misattribute failures to their own logic, a silent external outage otherwise looks like "the agent got worse" rather than "the API broke."

### Architecture Patterns
1. **Circuit breaker per external dependency**: Trip a breaker after N consecutive failures from a given external API (e.g., 5 failures in 60s) so the agent gets an immediate "service unavailable" rather than repeatedly hitting a broken/rate-limited endpoint and generating confused interpretations each time; deployment consideration — needs a half-open probe interval tuned to the API's typical outage/recovery duration.
2. **Retry-with-backoff wrapper distinguishing transient vs. permanent errors**: Auto-retry 429/503 with exponential backoff inside the tool layer (never surfacing the raw error to the agent until retries are exhausted), while 400/404 fail immediately since retrying won't help; deployment consideration — must respect `retry_after` headers when providers supply them to avoid worsening rate limiting.
3. **Contract testing against the external API**: Run scheduled contract tests that call the real external API with known inputs and assert the response schema still matches what the agent's tools expect, catching schema drift before agents encounter it in production; deployment consideration — requires test credentials/sandbox access to the external system, which isn't always available.

### Metrics
1. **external_error_misattribution_rate**: Target < 5% of sampled agent answers where the stated reason (e.g., "no data") contradicts the actual tool response (e.g., a 429); Alert if > 15% over a weekly audit sample.
2. **external_5xx_rate** (per API): Target < 0.5%; Alert if > 2% over 15 minutes.
3. **external_429_rate** (per API): Target < 1%; Alert if > 5% over 15 minutes (signals rate-limit pressure the agent may be misreading).
4. **schema_validation_failure_rate**: Target < 0.1%; Alert if > 1% over a 1-hour window (signals schema drift).

### Alerts
1. **External API Outage Suspected** (P1): Condition - external_5xx_rate or timeout rate for a given API exceeds 10% over 5 minutes. Action: trip the circuit breaker, notify users of degraded functionality for that integration, page the team owning the integration if it's internal.
2. **Rate Limit Pressure** (P2): Condition - external_429_rate exceeds 5% over 15 minutes. Action: verify backoff logic is engaged, check for a recent traffic increase or quota change, consider request batching or caching.
3. **Schema Drift Detected** (P2): Condition - schema_validation_failure_rate exceeds 1% for a given external API. Action: diff the current response schema against the last known-good version, update the tool's expected schema and notify agent-facing documentation of the change.

## References

- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) - External tool failure & runtime breakdowns
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Unhandled external API schema changes
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Tool coordination failures
