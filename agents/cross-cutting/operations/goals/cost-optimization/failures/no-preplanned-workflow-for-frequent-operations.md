# No Preplanned Workflow for Frequent Operations

## Issue: Agent Re-Derives an Identical Multi-Step Plan From Scratch for Every Occurrence of a Routine, Frequently-Repeated Operation

**Frequency**: Common

**Symptoms**
- The same operation type (e.g., "process a return," "onboard a new employee," "reset a password") produces a fresh multi-step reasoning trace every time, with no reuse of the prior successful plan
- Planning-call token spend for a routine operation is comparable across occurrences even though the underlying steps never change
- No plan-shape cache or template store exists anywhere in the agent's architecture
- Support/ops teams can name the operation's steps from memory, but the agent re-derives them via full LLM reasoning each time

**Root Cause**
Frequent, structurally identical operations are treated by the agent's architecture the same way as novel, one-off tasks: every occurrence triggers full planning from a blank context. There is no mechanism that recognizes "this request is the Nth instance of an operation whose plan shape was already solved" and instead re-runs the same reasoning that originally produced the plan, at full token cost, every single time. Because the plan is genuinely correct and stable, this waste is invisible in quality metrics — only in cost.

**Example**
```
Operation: "Process a standard product return" (2,400 occurrences/month)

Every occurrence, the agent's planning call reasons through:
"Step 1: Verify the order exists and is within the return window.
 Step 2: Check the item's return eligibility.
 Step 3: Generate a return shipping label.
 Step 4: Issue a refund to the original payment method.
 Step 5: Send the customer a confirmation email."

This exact 5-step sequence is produced by a ~600-token planning call
2,400 times per month, identical in every occurrence apart from the
order ID and customer email address.

Monthly planning cost: 2,400 x 600 tokens = 1,440,000 tokens
Cost if the plan were cached and reused with only IDs substituted:
~2,400 x 40 tokens (template lookup + substitution) = 96,000 tokens

Waste: 1,344,000 tokens/month (93%) spent re-deriving a plan that
never changes.
```

**Contributing Factors**
- No mechanism to detect that an incoming request matches the shape of a previously-solved, frequently-recurring operation
- Planning and execution are tightly coupled in the same call, so there's no natural point to intercept and substitute a cached plan
- Absence of monitoring on plan-shape recurrence means the waste is never surfaced as an anomaly
- Fear that caching a plan will make the agent brittle to edge cases, when only the routine-path majority needs caching, not every request

---

## Test Scenario & Reproduction

### Scenario Setup
- An operation type with high, measurable recurrence (e.g., "process a standard return") and no plan-caching layer
- Planning call re-derives the same step sequence from scratch on every occurrence
- No keyword/intent matcher checks incoming requests against a store of previously-solved plan shapes

### Trigger Mechanism
1. Submit 50 occurrences of the same routine operation type (varying only the order ID/customer identifier) to the agent
2. Log the planning-call output and token cost for each occurrence
3. Compare the step sequences across occurrences for structural identity, and compute the token cost of re-deriving an identical plan repeatedly versus a cached-and-substituted alternative

**Example Reproduction Steps:**
```
1. Submit 50 "process a standard return" requests, varying only order_id and customer_email
2. Capture the planning-call output and token count for each of the 50 occurrences
3. Diff the 50 plan outputs against each other, accounting only for order_id/email substitution
4. Confirm structural identity (same steps, same order) across all 50
5. Compute total planning tokens spent across the 50 occurrences
6. Estimate the token cost of a cached-plan-plus-substitution approach (template lookup + ID injection) for the same 50 occurrences
7. Compute the percentage waste between the two approaches
```

### Expected Failure State
- All 50 plan outputs are structurally identical apart from the substituted order ID/email, confirming the operation is routine and cacheable
- Total planning-call token spend across the 50 occurrences is within a few percent of 50x a single occurrence's cost, i.e., no economy of repetition is being captured
- No cache-hit-rate metric exists for plan reuse because no plan cache exists to hit
- The waste percentage (recomputed-plan tokens versus cached-and-substituted tokens) exceeds 80%, consistent with the order-of-magnitude gap in the example

---

## Mitigation Strategies

### Prevention
1. **Plan-shape extraction and reuse for recurring intents**: After a plan is generated and successfully executed for an operation type, extract its structural template (steps, tool sequence, decision points) and store it keyed by intent/operation type; on subsequent occurrences, match the incoming request's intent against the store and substitute the request-specific values (order ID, customer email) into the cached template rather than re-planning. Trade-off: requires an intent-matching step that must be accurate enough not to misapply a cached plan to a superficially similar but actually different operation.
2. **Frequency-triggered caching threshold**: Rather than attempting to cache every plan from the first occurrence, promote a plan template to the cache only after it has recurred identically N times (e.g., 3+), avoiding premature caching of what might turn out to be a one-off. Trade-off: the first N occurrences of a genuinely frequent operation still pay full planning cost before the cache kicks in.
3. **Template invalidation on operation change**: Because the underlying operation's correct step sequence can legitimately change (e.g., a new compliance check gets added to returns processing), version the cached template and invalidate it when the operation's defining tool set or policy changes, rather than relying on a stale cached plan indefinitely. Trade-off: requires an explicit signal that the operation's rules changed, which may not always be available upstream.

### Detection & Response
1. **Plan-shape recurrence monitoring**: Periodically cluster planning-call outputs by structural similarity (same tool sequence, same step count and order, differing only in substituted values); a cluster with high occurrence count and no corresponding cache entry is a direct signal of this failure.
2. **Planning-cost-per-operation-type tracking**: Track total planning-call token spend per operation type per month; operation types with both high occurrence count and flat per-occurrence planning cost (no reduction from repetition) indicate a missing caching opportunity.
3. **Cache-hit-rate-for-plans metric**: Once a plan cache exists, monitor its hit rate specifically for high-frequency operation types; a low hit rate despite high recurrence suggests the intent-matching step is too narrow or miscalibrated.

### Architecture Patterns
1. **Test-time plan-cache layer**: Introduce a caching layer between intent recognition and the planning call that extracts, stores, and adapts plan templates from completed executions, matching new requests against cached plans via keyword/intent similarity and substituting task-specific values — mirroring the test-time memory approach used in recent agentic-plan-caching research. Deployment consideration: needs a lightweight adaptation step for cases where the cached template needs minor per-instance adjustment beyond simple value substitution.
2. **Operation-type registry with versioned templates**: Maintain an explicit registry of known routine operation types, each with a versioned plan template, rather than relying on implicit pattern-matching alone; new operation types start uncached and get promoted into the registry once recurrence crosses the caching threshold. Deployment consideration: requires an owner/process for reviewing and versioning templates as underlying operations evolve.
3. **Fallback to full planning on low-confidence match**: When the intent-matching step's confidence in a cached-template match is below a threshold, fall back to full planning rather than forcing a possibly-wrong cached plan, preserving correctness for edge cases while still capturing the bulk of savings on clear-cut recurrences. Deployment consideration: the confidence threshold must be tuned to avoid both false-positive cache application and excessive fallback that erodes the savings.

### Metrics
1. **plan_cache_hit_rate_by_operation_type**: Target > 70% for operation types with monthly occurrence > 100; Alert if < 30% for a high-frequency operation type.
2. **planning_tokens_per_occurrence_trend**: Target declining toward the template-substitution floor as occurrence count grows; Alert if flat/non-declining after 10+ occurrences of the same operation type.
3. **misapplied_cached_plan_rate**: Target < 1% of cache-hit executions require a corrective re-plan due to a wrong template match; Alert if > 5%.
4. **template_staleness_incidents**: Target 0 executions using an invalidated/outdated template; Alert if > 0.

### Alerts
1. **High-Frequency-Operation-Without-Cache** (P2): Condition - an operation type crosses 100 monthly occurrences with plan_cache_hit_rate at or near 0%. Action: prioritize plan-template extraction and caching for that operation type.
2. **Misapplied-Template-Spike** (P2): Condition - misapplied_cached_plan_rate exceeds 5% for a given operation type. Action: tighten the intent-matching confidence threshold and review recent near-duplicate operation types that may be getting conflated.

## References

- [Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents](https://arxiv.org/abs/2506.14852) - test-time extraction, storage, adaptation, and reuse of plan templates across semantically similar tasks
- [SkillReducer: Optimizing LLM Agent Skills for Token Efficiency](https://arxiv.org/pdf/2603.29919) - reusable procedural skill packages as a mechanism for avoiding repeated re-derivation of known workflows
- [What Should a Skill Remember? Quality-Cost Trade-offs in Cost-Aware Skill Rewriting for Language Model Agents](https://arxiv.org/html/2606.09421) - trade-offs in what gets cached/reused versus re-derived per task
