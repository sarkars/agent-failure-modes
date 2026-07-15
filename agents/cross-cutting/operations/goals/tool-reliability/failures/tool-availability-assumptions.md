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

## Mitigation Strategies

### Prevention
1. **Exponential backoff with a hard retry cap replacing naive immediate retries**: The example shows the agent retrying a 429 immediately, then again, then 10 more times before giving up after 2 minutes — replace this with capped exponential backoff (e.g., 1s, 2s, 4s, 8s, max 5 attempts) that respects the API's `retry_after: 60` hint instead of hammering a known-limited endpoint. Trade-off: backoff delays legitimate retries too, so a task that could recover in 3 seconds under naive retry might now wait longer under a conservative backoff schedule.
2. **Pre-flight availability check before planning a multi-tool workflow**: Before committing to a plan that depends on `weather_api`, check its current rate-limit/health status (a lightweight status endpoint or cached recent-failure flag) so the agent can route around it or degrade gracefully from the start, rather than discovering unavailability mid-execution as in the example. Trade-off: adds a availability-check call to every planning cycle, which is wasted overhead when tools are healthy (the common case, per the 99.5% average availability stat).
3. **Cache recent successful results as a fallback for rate-limited/unavailable data sources**: For non-critical-freshness data like weather, serve a recent cached result when the live API is rate-limited rather than failing the whole task — directly addressing the "cache recent weather data" fallback named in the example's better-approach list. Trade-off: stale cached data can be wrong for time-sensitive queries, so cache TTL must be tuned per data type's volatility.

### Detection & Response
1. **Retry-count-before-failure distribution**: Track how many retries occur before a tool call ultimately succeeds or gives up; the example's pattern (12+ retries over 2 minutes with no backoff) should be visible as an outlier retry count compared to tools using proper backoff, which typically resolve or fail within 3-5 attempts.
2. **Rate-limit-approach tracking, not just rate-limit-hit tracking**: Since 5-15% of high-volume integrations hit rate limits per the cited stats, monitor request rate against known limits proactively (e.g., alert at 80% of quota) rather than only reacting after the first 429, giving time to throttle before the agent experiences the failure at all.
3. **Fallback activation audit**: Given that 67% of agents reportedly have no fallback for primary tools, explicitly track how often a fallback path exists and fires for each critical tool — a tool with 0% fallback activation despite recurring unavailability signals a missing fallback that should be built.

### Architecture Patterns
1. **Circuit breaker per external tool**: Implement the classic circuit breaker (closed → open → half-open) so that after N consecutive rate-limit/failure responses from `weather_api`, the breaker trips and short-circuits further calls to an immediate fallback for a cooldown period, rather than each call independently retrying 12+ times as in the example; deployment consideration — needs per-tool tuning of the failure threshold and cooldown, since a weather API's recovery pattern differs from a payments API's.
2. **Fallback provider chain for critical data types**: For data available from multiple sources (e.g., a secondary weather provider), configure an ordered fallback chain the agent's tool layer tries automatically when the primary is unavailable, rather than the agent's workflow simply failing at step 3 as in the example; deployment consideration — secondary providers may have different data schemas/coverage, requiring a normalization layer.
3. **Token-bucket rate-limit tracking client-side**: Track the API's rate limit budget client-side (requests remaining, reset time) so the tool layer can proactively throttle or queue requests before hitting a 429, rather than discovering the limit reactively; deployment consideration — requires the external API to expose limit/remaining headers, which not all providers do consistently.

### Metrics
1. **tool_availability_rate** (per tool): Target > 99.5% (matching the cited industry average); Alert if a tool's rolling 1-hour availability drops below 95%.
2. **naive_retry_incident_rate**: Target: 0 calls exceeding 5 retry attempts without backoff escalation; Alert on any tool exhibiting the example's 12+-retry pattern.
3. **fallback_activation_rate**: Target: > 90% of critical tools have a working fallback that activates when the primary is unavailable; Alert if a critical tool shows 0% fallback activation despite > 3 primary-unavailability events in a week.
4. **rate_limit_approach_rate**: Target: proactive throttling engages before 80% quota consumption; Alert if quota-exhaustion (429) events occur without a preceding throttle-engagement log entry.

### Alerts
1. **Task Failure After Excessive Retries** (P1): Condition - a tool call sequence exhibits naive_retry_incident_rate pattern (5+ retries with no backoff) ending in task failure. Action: page on-call, patch the retry logic to enforce capped exponential backoff immediately, review whether a circuit breaker should have engaged.
2. **Critical Tool Availability Drop** (P1): Condition - tool_availability_rate for a tool marked critical drops below 95% over 1 hour. Action: activate fallback provider if configured, notify users of degraded functionality, investigate root cause with the tool/API owner.
3. **Missing Fallback Confirmed** (P3): Condition - fallback_activation_rate is 0% for a critical tool despite repeated unavailability events. Action: prioritize building a fallback or cache-based degradation path for that tool in the next sprint.

## References

- [AWS: Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Timeout and retry patterns
- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - Tool reliability
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html) - Fault tolerance
- [Braintrust: Agent Observability](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Tool monitoring
- [Silent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - Tool failure handling
