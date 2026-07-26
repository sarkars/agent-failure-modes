# Non-Generalized Plan Template

## Issue: Agent's "Reused" Plans Are Not Actually Parameterized, So Near-Identical Requests Still Trigger Full Re-Planning Instead of a Template Substitution

**Frequency**: Common

**Symptoms**
- A plan cache or "reuse prior plan" mechanism exists, but hit rates are low even for requests that are obviously the same operation with a different ID
- Cached plans bake specific literal values (order IDs, customer names, dates) directly into the plan's reasoning text rather than treating them as substitutable slots
- Engineers observe "we already solved this exact workflow yesterday" yet the agent re-plans from scratch today because the ID differs
- Plan cache entries proliferate almost one-to-one with request volume instead of collapsing to a small number of distinct templates

**Root Cause**
A caching or reuse mechanism may technically exist, but it operates on exact-match or near-exact-match of the full plan text, including the specific entity IDs and values that were part of the original request. Because the plan was never actually generalized into a template with explicit variable slots (operation shape plus parameters), the cache can only ever hit when the entire request is identical, which almost never happens in practice — only the operation type recurs, not the exact IDs. This is a distinct failure from having no cache at all: the caching infrastructure exists, but the plans it stores are not in a genuinely reusable, parameterized form.

**Example**
```
Day 1: Agent processes "cancel subscription for customer C-88213"
Plan generated and cached (verbatim):
  "Step 1: Look up customer C-88213's subscription.
   Step 2: Confirm subscription C-88213-SUB is active.
   Step 3: Cancel subscription C-88213-SUB effective end of billing cycle.
   Step 4: Send cancellation confirmation to customer C-88213's email."

Day 2: Agent processes "cancel subscription for customer C-90447"
Cache lookup: no match (different customer ID baked into cached text)
Result: full re-planning call issued, ~550 tokens, producing an
identical plan shape with C-90447 substituted for C-88213.

Across 1,000 "cancel subscription" requests/month, cache hit rate is
effectively 0% because no two requests share the same literal ID,
even though all 1,000 share the exact same 4-step operation shape.
```

**Contributing Factors**
- Plan caching was implemented by storing the literal plan output text rather than extracting an ID-parameterized template at authoring/caching time
- No entity-extraction step separates "what varies per request" (IDs, names, dates) from "what is structurally constant" (the operation's steps) before caching
- Cache-key design uses a hash of the full request or full plan text, which by construction changes whenever any ID changes
- Success metrics track "cache exists" rather than "cache hit rate," so the near-zero effective hit rate goes unnoticed

---

## Test Scenario & Reproduction

### Scenario Setup
- A plan-caching mechanism is present and stores generated plans, but stores them as literal text including the specific IDs from the originating request
- No parameterization/templating step extracts variable slots before storage
- Multiple requests for the same operation type but different entity IDs are available to test against

### Trigger Mechanism
1. Submit a request for a routine operation (e.g., "cancel subscription for customer C-88213") and let the agent plan and cache the result
2. Submit a second request for the identical operation type but a different customer ID (e.g., "cancel subscription for customer C-90447")
3. Check whether the cache is consulted and hit, or whether a full re-planning call is issued

**Example Reproduction Steps:**
```
1. Submit "cancel subscription for customer C-88213"; capture the generated plan and confirm it is cached
2. Submit "cancel subscription for customer C-90447" (same operation type, different ID)
3. Log whether a cache hit occurs or a fresh planning call is issued
4. Repeat with 20 more "cancel subscription" requests, each with a unique customer ID
5. Compute cache_hit_rate across the 20 requests
6. Inspect the cached plan text directly to confirm whether it contains the literal ID from request 1 baked in, versus a parameterized slot
```

### Expected Failure State
- cache_hit_rate across the 20 same-operation-type, different-ID requests is at or near 0%, despite a cache mechanism being present and populated
- Inspecting the cached plan confirms the specific ID from the first request is embedded as literal text rather than a substitutable variable
- Each of the 20 requests triggers a full re-planning call producing a structurally identical plan to the one already cached, differing only in the ID
- No template-extraction step exists anywhere in the caching pipeline to separate structure from instance-specific values

---

## Mitigation Strategies

### Prevention
1. **Slot extraction before caching**: When a plan is generated, run an extraction pass that identifies which tokens in the plan correspond to request-specific entities (IDs, names, dates, amounts) versus fixed structural language, and store the plan as a template with explicit `{customer_id}`-style slots rather than literal values. Trade-off: slot extraction adds a processing step to the caching path and must correctly distinguish "this value varies" from "this value is coincidentally the same as a structural keyword."
2. **Template-keyed caching by operation shape, not request text**: Key the cache on the detected operation type/intent (e.g., "cancel_subscription") rather than a hash of the full request or plan text, so that any request matching that intent looks up the same template regardless of which specific IDs it carries. Trade-off: requires a reliable intent classifier upstream of the cache lookup, and misclassification risks matching the wrong template to a superficially similar but different operation.
3. **Substitution validation before execution**: After substituting request-specific values into a cached template, validate that all slots were filled (no leftover placeholder text) and that substituted values pass basic type/format checks (e.g., an ID looks like an ID) before executing, preventing a malformed substitution from silently proceeding. Trade-off: validation adds a small amount of processing overhead per cache-hit execution, though far less than the avoided re-planning call.

### Detection & Response
1. **True cache-hit-rate monitoring, not cache-existence monitoring**: Track the actual hit rate of the plan cache against total requests of a matching operation type, rather than only confirming the cache mechanism is deployed; a near-zero hit rate despite high request volume for a known-routine operation is the direct signature of this failure.
2. **Cache-entry-count-versus-distinct-operation-type audit**: Periodically compare the number of stored cache entries against the number of genuinely distinct operation shapes; a cache growing roughly one-to-one with request volume (rather than converging to a small number of templates) indicates literal-value caching rather than parameterized templating.
3. **Literal-value-in-template scan**: Automatically scan cached plan templates for patterns resembling specific IDs, emails, or dates that should have been extracted as slots; a high rate of literal values embedded in "templates" confirms the extraction step is missing or malfunctioning.

### Architecture Patterns
1. **Two-stage plan generation: structure then instantiation**: Separate plan generation into (a) determining the operation's step structure and (b) instantiating it with request-specific values, caching only stage (a)'s output as the reusable template and running stage (b) as a cheap substitution step on every request. Deployment consideration: requires refactoring the planning call to produce structure and instance data as distinguishable outputs rather than one blended plan.
2. **Entity-tagging pipeline before cache write**: Run named-entity recognition (or a lightweight extraction model) over the generated plan before writing to cache, replacing detected entities with typed slot markers, so caching infrastructure downstream never has to guess what varies. Deployment consideration: entity-tagging accuracy directly determines template quality — under-tagging leaves literal values baked in, over-tagging can accidentally genericize truly fixed content.
3. **Template registry decoupled from request cache**: Maintain a small, explicitly-curated registry of operation templates (reviewed and versioned) separate from any raw request/response cache, so the reusable-template store isn't polluted by literal per-request caching attempts. Deployment consideration: requires a promotion path for moving a newly detected recurring operation from "no template" to "registered template."

### Metrics
1. **plan_cache_true_hit_rate**: Target > 60% for requests matching a known-routine operation type; Alert if < 10% despite the operation type having a cache entry.
2. **cache_entries_to_distinct_operation_ratio**: Target close to 1:1 at the template level (one template per operation type); Alert if ratio exceeds 5:1 (indicating near-literal caching per request).
3. **literal_value_in_template_rate**: Target 0% of cached templates contain unextracted specific IDs/emails/dates; Alert if > 5%.
4. **substitution_validation_failure_rate**: Target < 1% of cache-hit executions fail slot-fill validation; Alert if > 5%.

### Alerts
1. **Near-Zero-Hit-Rate-Despite-Cache** (P2): Condition - plan_cache_true_hit_rate falls below 10% for an operation type known to recur frequently. Action: inspect cached entries for embedded literal values and add a slot-extraction step if missing.
2. **Cache-Entry-Explosion** (P3): Condition - cache_entries_to_distinct_operation_ratio exceeds 5:1. Action: review the cache-key design; likely keyed on request/plan text hash rather than operation intent.

## References

- [Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents](https://arxiv.org/abs/2506.14852) - extraction and adaptation of structured, parameterized plan templates versus literal plan-text caching
- [What Should a Skill Remember? Quality-Cost Trade-offs in Cost-Aware Skill Rewriting for Language Model Agents](https://arxiv.org/html/2606.09421) - what should be generalized into a reusable skill versus left instance-specific
- [Related Pattern: No Preplanned Workflow for Frequent Operations](./no-preplanned-workflow-for-frequent-operations.md) - the case where no reuse mechanism exists at all, as opposed to this pattern's case where reuse exists but isn't genuinely parameterized
