# Tool Availability Assumptions

## Issue: Agent Assumes Tool Is Available When It's Not

**Frequency**: Common

**Symptoms**
- Agent plans workflow using unavailable tools
- Rate-limited tools called without backoff
- Temporarily offline services cause complete failures
- No fallback when primary tool unavailable
- Agent retries indefinitely on unavailable tool

**Root Cause**
Agents assume tools listed in their configuration are always available, ignoring runtime realities: API rate limits, service outages, authentication expiry, network issues, or maintenance windows. Without availability checking and fallback logic, agents either fail entirely or waste resources retrying unavailable tools.

**Example**
```
Scenario: Data analysis agent with external API tools

Tool configuration:
  - weather_api: Get weather data
  - maps_api: Get location data
  - database: Query internal DB

Agent task: "Analyze weather patterns for our store locations"

Runtime state (unknown to agent):
  - weather_api: Rate limited (429), resets in 1 hour
  - maps_api: Available
  - database: Available

Agent execution:
  Step 1: Get store locations → database ✓
  Step 2: Get coordinates → maps_api ✓
  Step 3: Get weather → weather_api ✗ (429 error)
  
Agent response to 429:
  - Retry immediately → 429
  - Retry again → 429
  - Retry 10 more times → 429
  - After 2 minutes of retries: "Task failed"

Better approach:
  - Check tool availability before planning
  - Implement exponential backoff
  - Have fallback weather source
  - Cache recent weather data
  - Report partial results if acceptable
```

**Key Statistics**
From Availability Research (2026):
- 23% of tool calls fail due to availability issues
- Average API availability: 99.5% (43 hours downtime/year)
- Rate limit hits: 5-15% of high-volume integrations
- 67% of agents have no fallback for primary tools
- Recovery time without backoff: 10-50x longer

**Availability Failure Types**
| Type | Cause | Recovery |
|------|-------|----------|
| Rate limit | Too many requests | Backoff, queue |
| Auth expired | Token timeout | Re-authenticate |
| Service outage | Provider down | Fallback, wait |
| Network | Connectivity loss | Retry, timeout |
| Maintenance | Scheduled downtime | Wait, notify |

**Contributing Factors**
- No pre-flight availability checks
- Missing rate limit awareness
- No exponential backoff implementation
- Single tool dependency (no fallbacks)
- No circuit breaker pattern
- Optimistic availability assumptions

**Mitigation Strategies**
1. **Health checks**: Verify tool availability before use
2. **Exponential backoff**: Implement proper retry logic
3. **Circuit breakers**: Stop retrying after threshold
4. **Fallback tools**: Alternative tools for critical functions
5. **Rate limit tracking**: Track and respect limits proactively
6. **Graceful degradation**: Partial results when tools unavailable

**Detection**
- Monitor tool call success rates
- Track retry patterns and counts
- Alert on rate limit approaches
- Measure time lost to unavailable tools
- Audit fallback activation frequency

## References

- [AWS: Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Timeout and retry patterns
- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - Tool reliability
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html) - Fault tolerance
- [Braintrust: Agent Observability](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Tool monitoring
- [Silent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - Tool failure handling
