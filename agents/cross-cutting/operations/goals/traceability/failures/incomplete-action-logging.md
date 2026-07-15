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

## Mitigation Strategies

### Prevention
1. **Automatic instrumentation wrapping every tool/service call by default**: Wrap all tool invocations — including reads, internal validation checks, and retries — with logging middleware at the framework level, rather than logging being added ad hoc to "obvious" points like the PUT and POST calls in the example while the geocoding query, retries, and fraud check go unrecorded. Trade-off: comprehensive default logging increases storage volume and can add latency if implemented synchronously.
2. **Async, non-blocking logging to remove the performance objection**: Since "performance concerns limit logging" is named as a contributing factor, implement logging as a non-blocking async write so completeness doesn't have to be traded off against latency — removing the excuse for skipping retry or validation-check logging. Trade-off: async logging risks losing log entries on process crash between the action and the flush, requiring a durable buffer.
3. **Debug-full / production-sampled logging tiers**: Log every action type at full detail in non-production and staging environments, and use targeted (not blanket) sampling in production that still captures 100% of retries, validation failures, and internal tool calls even while sampling routine reads — since retries and validation checks are named as "High" importance despite being logged only 10-15% of the time today. Trade-off: differential sampling by action type adds configuration complexity versus a single global sampling rate.

### Detection & Response
1. **Time-gap detection in action sequences**: Automatically flag when the elapsed time between two consecutive logged actions is large relative to what a fully-instrumented sequence would show (the example's unexplained 4-second gap between GET and PUT), signaling missing intermediate actions even without knowing what they were.
2. **Expected-log-entry-sequence validation**: For known task types (e.g., "update address and send confirmation"), maintain an expected set of sub-actions (validation, geocoding, fraud check) and alert when a session's logged trace is missing entries from that expected set, rather than only noticing gaps informally during an investigation.
3. **Action-type logging-coverage audit**: Periodically measure what fraction of each action type (reads, retries, validation checks, reasoning steps) is actually captured in logs versus performed, directly quantifying the gap between the "30% of actual operations" baseline and a target coverage level.

### Architecture Patterns
1. **Uniform action-logging middleware across all tool types**: Build a single instrumentation layer that every tool call — read or write, internal or external, retry or first attempt — passes through, tagging each entry with action type for later filtering, rather than leaving reads and internal calls to be instrumented individually and inconsistently. Deployment consideration: requires retrofitting existing tools that weren't built with a common calling convention, which can be substantial work in a mature codebase.
2. **Structured action classification schema**: Tag every logged action with a type (external-write, external-read, internal-tool-call, retry, validation-check, reasoning-step) so investigations can filter and reconstruct the full sequence (as the example's hidden geocoding-retry-fraud-check chain would require) rather than parsing free-text logs. Deployment consideration: needs a shared taxonomy enforced across all agent components, including any third-party tools integrated into the pipeline.
3. **Automated gap-detection alerting on incomplete sequences**: Build a monitoring rule that compares actual logged sequences against the expected action-type distribution for a task type and fires when key categories (retries, validation, reasoning) are absent, rather than relying on a human investigator to notice the blind spot after the fact. Deployment consideration: requires maintaining per-task-type expected-sequence definitions, which need updating as agent workflows evolve.

### Metrics
1. **action_logging_coverage_rate**: % of actual agent operations that are logged, broken out by action type (reads, writes, retries, validation, reasoning); target > 90% overall, > 80% even for lowest-priority categories; alert if overall coverage < 50% (current baseline is ~30%, the failure state to avoid).
2. **retry_logging_rate**: % of retry attempts that are logged; target > 90%; alert if < 30% (matches the example's fully-unlogged geocoding retries).
3. **unexplained_time_gap_rate**: % of task executions with a time gap between logged actions exceeding an expected threshold with no corresponding log entry; target < 5%; alert if > 20%.
4. **expected_sequence_completeness_rate**: % of task executions where all expected sub-action types for that task category appear in the log; target > 90%; alert if < 60%.

### Alerts
1. **Logging Coverage Below Floor** (P2): Condition — action_logging_coverage_rate for any high-importance category (retries, validation, reasoning) drops below 30%. Action: prioritize instrumentation work for that category; treat recent investigations relying on that category's logs as potentially incomplete.
2. **Unexplained Time Gap Spike** (P2): Condition — unexplained_time_gap_rate exceeds 20% for a task type. Action: audit the task's tool-call chain for unlogged internal operations (validation, geocoding, retries) and add instrumentation to close the gap.
3. **Expected Sequence Incomplete** (P3): Condition — expected_sequence_completeness_rate falls below 60% for a task category. Action: review and update the expected-sequence definition and the underlying instrumentation for that task type.

## References

- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Comprehensive logging
- [LinkedIn: Silent Failures of Production AI](https://www.linkedin.com/pulse/silent-failures-production-ai-why-most-llm-monitoring-praveen-juyal-iqgyc) - Logging gaps
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Observability requirements
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Action tracking
