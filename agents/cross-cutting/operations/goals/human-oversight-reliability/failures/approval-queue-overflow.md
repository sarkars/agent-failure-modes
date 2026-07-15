# Approval Queue Overflow

## Issue: Too Many Pending Approvals Cause Delays or Dropped Requests

**Frequency**: Occasional

**Symptoms**
- Approval requests lost in queue
- Long wait times for approval
- Approvers overwhelmed with requests
- Important requests buried in noise
- Approval backlogs during peak periods

**Root Cause**
Agents generate approval requests faster than humans can process them. Queues overflow, causing requests to be dropped, delayed, or lost. Approvers experience fatigue and either rubber-stamp or ignore requests. Priority requests get buried among routine ones. The system lacks mechanisms to manage queue depth, prioritize requests, or throttle approval generation.

**Example**
```
Scenario: Content moderation agent generating approval requests

Normal state:
  Requests/hour: ~20
  Approvers: 3
  Processing capacity: 30/hour
  Queue depth: 0-5

Viral content event:
  10:00 - Controversial post goes viral
  10:15 - 500 related posts flagged
  10:30 - Queue depth: 450 requests
  11:00 - Queue depth: 800 requests
  
Approver behavior:
  - First 30 minutes: Careful review
  - Next 30 minutes: Faster review, lower quality
  - After 1 hour: Batch approve without reading
  - After 2 hours: Give up, requests timing out
  
Results:
  - 340 requests auto-expired
  - 200 batch-approved without review
  - 15 problematic posts published
  - 3 posts required emergency takedown
  
System failures:
  - No queue depth limit
  - No request prioritization
  - No approver scaling
  - No throttling of request generation
```

**Key Statistics**
From Queue Management Research (2026):
- 60% of approvers rubber-stamp after 20+ requests
- Average queue depth before degradation: 50 requests
- 25% of requests lost during overflow events
- Priority escalation used in only 18% of systems
- Queue overflow events occur monthly for 45% of orgs

**Overflow Effects**
| Effect | Description | Impact |
|--------|-------------|--------|
| Request loss | Requests dropped silently | Actions never reviewed |
| Approval fatigue | Approvers stop reviewing | Poor approval quality |
| Priority inversion | Important buried by routine | Critical delays |
| Batch approval | Bulk approve without review | Defeats oversight |
| Timeout cascade | Mass expiration | System failure |

**Contributing Factors**
- No queue depth limits
- No request prioritization
- Static approver capacity
- No throttling mechanism
- No overflow alerting

## Mitigation Strategies

### Prevention
1. **Backpressure on the request-generating agent**: Cap queue depth and have the agent slow or pause request generation once the cap is approached, rather than letting requests pile up unboundedly during a spike like the viral-content event in the example (0 → 800 requests in an hour). Trade-off: throttling the agent means some legitimate actions get delayed or blocked during genuine surges, not just runaway generation.
2. **Priority queues keyed to actual risk, not arrival order**: Route requests through a priority queue so high-risk items (the 15 problematic posts) surface ahead of routine ones instead of being buried among 800 undifferentiated requests. Trade-off: requires a reliable risk-scoring step at request-creation time, which adds its own failure surface if scoring is wrong.
3. **Request batching for similar low-risk items**: Group near-duplicate or clearly-similar requests (e.g., near-identical flagged posts from the same viral event) into a single reviewable batch rather than 500 separate approval prompts, reducing the raw volume hitting the queue. Trade-off: batching can cause an approver to rubber-stamp an entire batch based on a few samples, missing an outlier within it.

### Detection & Response
1. **Queue-depth threshold monitoring**: Continuously track queue depth against the research-identified degradation point (~50 requests, per the example's key statistics) and trigger response before approvers hit the rubber-stamp threshold (60% rubber-stamp after 20+ requests).
2. **Approval-latency-percentile tracking during volume spikes**: Monitor p50/p95/p99 approval latency in real time; the example's progression (careful review → faster review → batch approve → give up) is directly visible as latency percentiles compress and then requests start expiring.
3. **Post-overflow quality audit**: After any overflow event, sample the batch-approved and auto-expired requests (the 200 batch-approved, 340 auto-expired in the example) and check outcomes against what careful review would have found, to calibrate whether the response mechanisms worked.

### Architecture Patterns
1. **Dynamic approver capacity scaling**: Automatically pull in additional qualified approvers (on-call rotation, cross-trained staff) when queue depth crosses a threshold, rather than leaving a fixed 3-approver pool to absorb a 40x volume spike. Deployment consideration: requires a pool of pre-trained backup approvers ready to be activated, which has its own staffing cost.
2. **Throttle-and-triage gateway in front of the approval queue**: Insert a triage layer that applies automated pre-filtering (confidence-based auto-clear for clearly-fine items, auto-escalate for clearly-risky items) so only the genuinely ambiguous middle tier reaches human approvers during a spike. Deployment consideration: the triage layer itself needs to be reliable enough not to auto-clear something that should have been caught — it's a new failure point layered on the old one.
3. **Overflow circuit breaker with graceful degradation**: When queue depth exceeds a hard ceiling, stop accepting new low-priority requests entirely (rather than accepting them and letting them silently expire) and surface an explicit "queue full, request deferred" state to the requester. Deployment consideration: requires defining what's safe to defer versus what must always be processed, which needs domain-specific risk classification.

### Metrics
1. **queue_depth_p95**: 95th-percentile queue depth over rolling hour; target < 50 (per research-identified degradation point); alert if > 200.
2. **approval_latency_p95**: 95th-percentile time from request creation to decision; target < 30 minutes; alert if > 2 hours.
3. **request_drop_expiry_rate**: % of requests auto-expired or dropped without review; target < 2%; alert if > 15% (the example's 340/800 ≈ 42% would trip this hard).
4. **rubber_stamp_rate**: % of approvals granted in under a defined minimum review time during high-volume periods; target < 10%; alert if > 40%.

### Alerts
1. **Queue Depth Critical** (P1): Condition — queue_depth_p95 exceeds 200 requests. Action: activate backpressure on the request-generating agent, page on-call for dynamic capacity scaling, and enable priority-queue mode if not already active.
2. **Request Drop/Expiry Spike** (P1): Condition — request_drop_expiry_rate exceeds 15% during an active event. Action: treat as an oversight failure in progress; escalate to incident response and manually triage the highest-risk expired items immediately.
3. **Rubber-Stamp Pattern Detected** (P2): Condition — rubber_stamp_rate exceeds 40% during sustained high queue depth. Action: pause non-critical request generation, bring in additional approvers, and flag recent rapid approvals for post-hoc review.

## References

- [Queue Theory](https://en.wikipedia.org/wiki/Queueing_theory) - Queue management principles
- [MFA Fatigue Attacks](https://community.microsoft.com/t5/microsoft-entra-blog/defend-your-users-from-mfa-fatigue-attacks/ba-p/2365677) - Approval fatigue patterns
- [Braintrust: Agent Observability](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Queue monitoring
- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Human-in-the-loop scaling
