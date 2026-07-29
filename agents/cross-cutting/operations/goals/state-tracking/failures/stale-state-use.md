# Stale State Use

## Issue: Agent uses old tool results after new data arrives.

**Frequency**: Common

**Symptoms**
- Later output uses earlier version/timestamp.
- Agent takes an action (booking, purchase, confirmation) that fails at execution time because the underlying resource changed after the agent's last fetch.
- No re-fetch occurs before a time-sensitive action even though many turns or minutes elapsed since the original fetch.
- Cached tool results carry no freshness timestamp or max-age policy that would have flagged them as stale before use.
- External changes (another user/agent modifying the resource) go completely unnoticed because no cache-invalidation event exists for that resource type.

**Root Cause**
Agent uses old tool results after new data arrives.

**Example**
```
Agent checks a hotel room's rate at the start of a chat session:
check_rate("ROOM-812") -> {rate: 149.00, retrieved_at: "09:00:00"}

The user spends 20 minutes comparing amenities and asking unrelated
questions. At 09:14:00, the hotel's revenue system raises the rate
to $189.00 due to a demand spike.

At 09:20:00 the user says "book it at that rate." The agent, still
holding its 09:00:00 snapshot in context, calls book_room("ROOM-812",
rate=149.00) without re-checking current pricing. The booking tool
either rejects the mismatched rate or, worse, silently books at the
stale price, creating a billing discrepancy discovered only at
checkout.
```

**Contributing Factors**
- Fetched tool results are held in context for the remainder of a multi-turn session with no cache-invalidation-on-write mechanism.
- No freshness timestamp or per-resource max-age policy exists to force a re-fetch before using older data.
- No mandatory re-fetch policy is enforced for time-sensitive operations (pricing, inventory, availability, balances).
- Long gaps between the initial fetch and the dependent action increase the odds that an external actor changed the underlying resource in the meantime.
- Tool APIs don't return a version/ETag alongside data, so there's nothing for the agent's decision logic to check before committing an action.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Stale availability before booking | Agent fetches availability early, resource changes externally, then user confirms booking after a long gap | Agent re-fetches availability immediately before the booking call rather than reusing the old snapshot | Agent calls the booking tool using the original fetch with no re-fetch, despite exceeding the max-age policy |
| Cache invalidation on external write | A resource is modified by an external writer while cached in the agent's context | Cache entry is evicted/marked stale and the next read triggers a fresh fetch | Agent's next decision still uses the pre-change cached value |
| Version-mismatch rejection | Agent attempts a write using a version/ETag older than the resource's current version | Write is rejected and the agent is forced to re-fetch and reconcile | Write succeeds despite an outdated version, silently applying a decision based on stale data |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| eval_refetch_compliance_rate_percent | 100% of eval time-sensitive actions preceded by a fresh fetch | Run eval scenarios with injected time gaps before dependent actions, check for a re-fetch call immediately prior |
| eval_stale_action_rate_percent | 0% of eval actions execute using data older than the defined max-age policy | Compare each eval action's input timestamp/version against the policy threshold |
| eval_invalidation_propagation_latency_ms | < 1000ms from simulated write event to cache eviction in test harness | Inject a resource-change event mid-eval-scenario and measure time until the cached copy is invalidated |

## Test Scenario & Reproduction

### Scenario Setup
- Deploy a booking agent that fetches flight seat availability early in a session and holds the result in context for the rest of a multi-turn conversation, with no cache-invalidation-on-write or freshness-timestamp check before use
- No mandatory re-fetch policy exists for time-sensitive operations like seat booking
- Seat availability for the flight changes (another customer books the last seat) partway through the agent's session

### Trigger Mechanism
1. Early in the session, the agent checks seat availability: 3 seats remain
2. Several turns later, after the user asks unrelated questions, all 3 remaining seats are booked by other customers (external event, not observed by the agent)
3. The user confirms they want to book a seat
4. The agent, still relying on its earlier "3 seats remain" fetch rather than re-checking, proceeds to attempt the booking without a fresh availability check

### Example Reproduction Steps
```
1. Turn 2: agent calls check_availability("AB123") -> {seats: 3,
   retrieved_at: "10:00:00"}
2. Turns 3-8: unrelated conversation (seat selection preferences,
   pricing questions) spanning 15 minutes
3. External event at 10:12:00: all 3 seats sold via a different
   channel
4. Turn 9: user: "Great, book me a seat"
5. Agent calls: book_seat("AB123") using its turn-2 belief that seats
   are available, with no re-fetch of current availability
6. Booking tool returns: "ERROR: no seats available" -- but only
   after attempting the write, having never checked freshness first
7. Check version_mismatch_at_output_rate for this session -> the
   agent's action was based on a 12-minute-old fetch, well beyond the
   defined max-age policy for seat availability
```

### Expected Failure State
The agent attempts to book a seat based on a 12-minute-old availability snapshot that no longer reflects reality, resulting in a failed booking and a confused customer who was told a seat was available. A correctly defended system enforces a mandatory re-fetch for time-sensitive operations like seat booking, re-checking current availability immediately before the booking call rather than trusting the turn-2 snapshot held in context.

## Mitigation Strategies

### Prevention
1. **Cache Invalidation on Write Events**: Any cached tool result or fetched state is tied to an invalidation trigger — when the underlying resource changes (via any writer, agent or external), a change event evicts or marks stale the cached copy, so the agent's next read is forced to re-fetch rather than reuse a snapshot taken before the change.
2. **Freshness Timestamp Checks Before Use**: Every piece of fetched state carries a retrieved_at timestamp and, where available, a resource-side last_modified/version marker. Before using state in a decision, the agent compares its freshness against a per-resource max-age policy and re-fetches if stale, rather than assuming the first fetch in the session remains valid throughout.
3. **Mandatory Re-Fetch for Time-Sensitive Operations**: For operations where staleness has real consequences (inventory checks, pricing, availability, account balance), the pipeline structurally disallows using any cached/remembered value older than a defined window — the tool call is re-issued immediately before the dependent action, no exceptions.

### Detection & Response
1. **Version/Timestamp Mismatch Scanning**: Compare the timestamp or version marker embedded in the agent's final output against the current live value of the same resource; a mismatch beyond the acceptable window indicates stale state was used and is logged for review.
2. **Multi-Fetch Session Auditing**: For sessions that fetch the same resource more than once, check whether later decisions correctly used the most recent fetch rather than an earlier one still lingering in context — flag cases where an earlier value's use persisted after a newer fetch was available.
3. **Downstream Error Correlation**: When an action fails because the real-world state had changed (e.g., "item no longer available"), check whether the agent had a stale local copy that should have been invalidated, and feed that resource type into tighter freshness policy.

### Architecture Patterns
1. **Event-Driven Cache Invalidation Bus**: Resource writers publish change events to a bus; a caching layer subscribes and evicts/marks-stale any cached entries for the changed resource, decoupling invalidation from the agent having to manually decide to re-fetch.
2. **Freshness-Aware State Accessor**: All state reads go through an accessor that checks retrieved_at against a per-resource TTL policy and transparently re-fetches expired entries, so freshness enforcement is centralized rather than repeated ad hoc at each call site.
3. **Version-Stamped Tool Responses**: Tool APIs return a version/ETag alongside data; the agent's decision logic can require a version-match against the latest known version before committing an action that depends on that data, refusing to proceed on a version mismatch.

### Metrics
1. **stale_state_use_incident_count**: Target: 0 per week; Alert threshold: > 3 per week
2. **cache_invalidation_lag_ms**: Target: < 1000ms from write event to cache eviction; Alert threshold: > 10000ms
3. **time_sensitive_op_refetch_compliance_percent**: Target: 100%; Alert threshold: < 100%
4. **version_mismatch_at_output_rate_percent**: Target: < 0.5% of resource-dependent responses; Alert threshold: > 2%

### Alerts
1. **Stale State Drove Incorrect Action** (P1 - Critical): Condition - an agent action was taken based on state confirmed stale (version mismatch beyond window) for a time-sensitive resource. Action: Reverse/correct the action if possible, notify affected user, audit the freshness policy for that resource type.
2. **Cache Invalidation Lag Spike** (P2 - Warning): Condition - cache_invalidation_lag_ms exceeds 10s consistently over 1h. Action: Investigate event bus backlog or subscriber lag, check for dropped invalidation events.
3. **Time-Sensitive Refetch Bypass** (P1 - Critical): Condition - a time-sensitive operation proceeded using a cached value instead of the mandated re-fetch. Action: Immediate patch of the bypass, audit recent actions of that type for stale-state impact.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| stale_state_use_incident_count | > 3 per week |
| cache_invalidation_lag_ms | > 10000ms |
| time_sensitive_op_refetch_compliance_percent | < 100% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Stale State Drove Incorrect Action | An agent action was taken based on state confirmed stale (version mismatch beyond window) for a time-sensitive resource | Critical |
| Cache Invalidation Lag Spike | cache_invalidation_lag_ms exceeds 10s consistently over 1h | Warning |
| Time-Sensitive Refetch Bypass | A time-sensitive operation proceeded using a cached value instead of the mandated re-fetch | Critical |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
