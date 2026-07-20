# Output Ordering Nondeterminism

## Issue
An agent returns a list or array whose element order varies from call to call for logically equivalent input, even though the consuming system depends on a stable order — for pagination cursors, for diffing successive results, for deterministic display, or for stable IDs derived from position. Because the list's *contents* are correct each time, the failure is easy to miss in isolated testing and only surfaces when two calls are compared against each other or when a consumer's assumption of stability is violated.

**Frequency**: Occasional

**Symptoms**
- The same query returning the same set of items in a different order across repeated calls
- Diff-based change-detection logic reporting spurious "changes" between two snapshots that actually contain identical data, just reordered
- Pagination breaking (duplicate or skipped items across pages) because the underlying order shifted between page requests
- Position-derived identifiers (e.g. "item #3") referring to a different logical item on a subsequent call
- UI flicker or unexpected reordering on refresh for a list a user expects to remain stable absent an explicit sort action

## Root Cause
Ordering stability is not a free byproduct of correctness — it has to be explicitly guaranteed, and several common causes strip it out silently. Generative-model-produced lists (e.g. an agent enumerating extracted entities or ranked results) have no inherent commitment to consistent ordering across calls unless the prompt or downstream logic imposes an explicit, deterministic sort key. Database queries without an `ORDER BY` clause are not guaranteed to return rows in the same order across executions, even for identical data, because the underlying storage engine is free to return rows in whatever order is most efficient for that particular query plan. Parallel/concurrent fan-out patterns (calling multiple tools or sub-agents and aggregating results) introduce ordering that depends on which call happens to complete first, which varies with network timing rather than any property of the data itself.

## Example
```
A research agent fans out to five source APIs concurrently to gather
candidate answers, then aggregates and returns them as a ranked list to
a UI that displays "Result 1" through "Result 5" and lets the user click
"mark result 3 as helpful."

The aggregation step appends each source's results to a list as that
source's call completes:

    results = []
    for future in as_completed(source_futures):
        results.extend(future.result())
    return results

On the first page load, Source C happens to respond fastest due to
transient network conditions, so its results appear first; the user
reviews the list and clicks "mark result 3 as helpful" on what is, at
that moment, a specific finding from Source A.

The click handler sends only the index (3) back to the server, which
re-runs the same aggregation to resolve what "result 3" refers to. This
time Source A responds fastest instead, and "result 3" now refers to a
completely different finding from Source D. The wrong result gets marked
helpful, silently corrupting the ranking-feedback data used to tune
future result ordering.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of "phantom diff" or "spurious change" alerts in change-detection pipelines resolve, on investigation, to reordering rather than an actual content change | Typical range observed in change-detection and diff-tooling incident logs |
| Concurrent fan-out aggregation without an explicit stable sort is a common source of ordering nondeterminism in multi-source agent pipelines | Common pattern observed in agent architecture reviews |
| Adding an explicit deterministic sort key at the aggregation boundary eliminates the large majority of ordering-nondeterminism incidents | Estimated from the directness of the fix relative to the failure mechanism |

## Mitigations
1. **Always sort by an explicit, deterministic key before returning a list**: Never rely on insertion order, completion order, or database-engine default order; apply an explicit `ORDER BY` (with a tiebreaker on a unique field) or an explicit sort step on any aggregated list before it's returned to a consumer.
2. **Use stable, content-derived identifiers instead of positional references**: Where a consumer needs to reference a specific list item across calls (e.g. "mark item 3"), have it reference a stable ID carried with the item rather than its positional index, so reordering between calls doesn't corrupt the reference.
3. **Deterministic aggregation for concurrent fan-out**: When aggregating results from concurrent/parallel calls, sort or key the combined list by source identity or another stable property rather than by completion order, so timing variance doesn't leak into the returned order.
4. **Idempotency/stability tests for list-returning endpoints**: Include repeated-call tests in CI that assert identical order for identical input, not just identical content, catching ordering regressions before deployment.
5. **Explicit "order not guaranteed" contracts where true statelessness is intended**: If a consumer genuinely doesn't need stable ordering, document that explicitly in the API contract so downstream code doesn't develop implicit assumptions of stability that later break.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| repeated_call_order_stability_rate | Share of repeated identical calls returning items in the same order | Alert if < 99% for endpoints expected to be stable |
| pagination_duplicate_or_skip_rate | Rate of duplicate or missing items detected across sequential paginated requests | Alert if > 0.5% |
| position_reference_mismatch_count | Count of position-based references (e.g. "item N") resolving to a different logical item across calls | Alert on any occurrence |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Ordering instability detected on stable-contract endpoint | Repeated identical calls to an endpoint documented as order-stable return items in different order | High | Audit for missing ORDER BY or unsorted aggregation, patch, verify fix with regression test |
| Pagination integrity failure | Sequential paginated requests show duplicate or skipped items | High | Halt pagination-dependent workflows, investigate underlying sort stability |

## Related Patterns
- [Output Inconsistency](./output-inconsistency.md) - ordering nondeterminism is a specific, narrower instance of the broader output-inconsistency problem
- [Output Format Not Validated](./output-format-not-validated.md) - both stem from insufficient guarantees on the shape/structure of generated output being verified before use
- [Output Precision Loss](./output-precision-loss.md) - both are subtle data-fidelity failures where the returned content looks correct in isolation and only proves wrong under comparison
