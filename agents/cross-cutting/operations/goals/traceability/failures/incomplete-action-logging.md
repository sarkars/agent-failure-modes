# Incomplete Action Logging

## Issue: Only Some Agent Actions Are Logged, Creating Blind Spots

**Frequency**: Very Common

**Symptoms**
- Gaps in action sequences during investigation
- Some tool calls logged, others missing
- Read operations not tracked
- Internal reasoning steps invisible
- Partial picture of agent behavior

**Root Cause**
Logging is typically added to obvious action points like API calls and database writes, but agents perform many other actions: reading files, querying context, making internal decisions, retrying operations. These "invisible" actions aren't logged, creating gaps in the action timeline that make debugging and auditing incomplete.

**Example**
```
Agent task: "Update customer address and send confirmation"

What was logged:
  10:30:01 - API call: GET /customer/123
  10:30:05 - API call: PUT /customer/123 {address: "..."}
  10:30:06 - API call: POST /email/send

Investigation question: "Why did update take 4 seconds?"

What actually happened (not logged):
  10:30:01 - GET customer data
  10:30:01 - Read address validation rules (NOT LOGGED)
  10:30:02 - Query geocoding service (NOT LOGGED)
  10:30:02 - Geocoding failed, retry (NOT LOGGED)
  10:30:03 - Geocoding retry 2 (NOT LOGGED)
  10:30:04 - Check fraud rules (NOT LOGGED)
  10:30:04 - Fraud check passed (NOT LOGGED)
  10:30:05 - PUT customer update
  10:30:05 - Generate email content (NOT LOGGED)
  10:30:06 - POST send email

Blind spots:
  - Geocoding service issues (potential SLA violation)
  - Fraud check logic (compliance requirement)
  - Email content generation (customer communication audit)
```

**Key Statistics**
From Observability Research (2026):
- Average agent logs 30% of actual operations
- Read operations logged 10% as often as writes
- Retry logic almost never logged
- Internal tool calls frequently missed
- "What happened between X and Y?" - common question

**Logging Gaps**
| Action Type | Typical Logging | Importance |
|-------------|-----------------|------------|
| External API writes | 90% | High |
| External API reads | 40% | Medium |
| Internal tool calls | 20% | High |
| Retry attempts | 10% | High |
| Validation checks | 15% | High |
| Context retrieval | 25% | Medium |
| Reasoning steps | 5% | High |

**Contributing Factors**
- Focus on "important" actions only
- Performance concerns limit logging
- Read operations seem unimportant
- Internal operations not instrumented
- Logging added reactively, not by design

**Mitigation Strategies**
1. **Comprehensive instrumentation**: Log all action types by default
2. **Action classification**: Tag actions by type for filtering
3. **Async logging**: Non-blocking logging for performance
4. **Sampling strategies**: Log everything in debug, sample in production
5. **Automatic instrumentation**: Wrap all tools with logging
6. **Gap detection**: Alert when expected log sequences incomplete

**Detection**
- Time gaps in action sequences
- "Unknown action" periods in traces
- Missing expected log entries
- Incomplete tool call chains
- Audit trail gap analysis

## References

- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Comprehensive logging
- [LinkedIn: Silent Failures of Production AI](https://www.linkedin.com/pulse/silent-failures-production-ai-why-most-llm-monitoring-praveen-juyal-iqgyc) - Logging gaps
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Observability requirements
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Action tracking
