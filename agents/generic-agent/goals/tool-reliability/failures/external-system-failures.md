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

**Mitigation Strategies**
1. **Error classification**: Teach agents to categorize API errors
2. **Retry logic**: Implement backoff for transient failures
3. **Schema validation**: Verify API responses match expected format
4. **Failure transparency**: Report external errors to users explicitly
5. **Fallback strategies**: Define alternative actions for common failures

**Detection**
- HTTP error codes in tool call logs
- Mismatch between agent claims and actual API responses
- Sudden changes in tool success rates
- User reports of "no data" when data should exist

## References

- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) - External tool failure & runtime breakdowns
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Unhandled external API schema changes
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Tool coordination failures
