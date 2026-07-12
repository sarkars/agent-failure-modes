# Golden Data Staleness

## Issue: Golden Dataset Contains Outdated Information or Expectations

**Frequency**: Common

**Symptoms**
- Agent gives correct current answer, marked wrong
- Expected responses reference deprecated features
- Golden data reflects old business rules
- Evaluation scores drop after real-world improvements
- New capabilities not covered in golden set

**Root Cause**
Golden datasets are created at a point in time and reflect the knowledge, products, and expectations of that moment. As the world changes—products update, prices change, policies evolve, knowledge advances—the golden dataset becomes stale. Agents giving correct current answers are penalized for not matching outdated expected responses.

**Example**
```
Scenario: Customer support agent evaluation

Golden dataset created: January 2025
Evaluation run: June 2026

Golden test case #47:
  Query: "What is the price of the Pro plan?"
  Expected: "$29/month"
  
Current reality:
  Pro plan price: $39/month (changed March 2026)
  
Agent response: "$39/month"
Evaluation result: FAIL (doesn't match expected)

Impact:
  - Agent marked as "inaccurate"
  - Development time spent "fixing" correct behavior
  - Evaluation score: 94% (should be 98%)
  - 47 of 1000 test cases have stale expectations

Root cause analysis:
  - No golden data refresh process
  - Expected responses hardcoded
  - No connection to source of truth
  - Last audit: 18 months ago
```

**Key Statistics**
From Data Quality Research (2026):
- Average golden dataset age: 8-14 months
- 15-25% of test cases stale after 6 months
- 40% of "failures" are actually stale expectations
- Only 23% of organizations have golden data refresh process
- Price/feature data stale within 30-90 days

**Staleness Dimensions**
| Dimension | Example | Decay Rate |
|-----------|---------|------------|
| Pricing | Product costs | 30-90 days |
| Features | Product capabilities | 60-180 days |
| Policies | Business rules | 90-365 days |
| Knowledge | Facts, statistics | 180-365 days |
| Personnel | Contact info, roles | 30-60 days |

**Contributing Factors**
- No refresh schedule for golden data
- Manual golden data maintenance
- No connection to authoritative sources
- Expected responses hardcoded as strings
- No staleness detection mechanism
- Infrequent evaluation audits

## Mitigation Strategies

### Prevention
1. **Dynamic expectations pulled from source-of-truth systems**: Replace hardcoded expected-response strings with live lookups against the authoritative source system (pricing DB, policy store) at eval-run time, since the root cause here was explicitly "expected responses hardcoded as strings" with "no connection to source of truth." Trade-off: requires building and maintaining integration between the eval harness and each source-of-truth system.
2. **Scheduled golden-data refresh cadence tied to known decay rates**: Set refresh schedules per data category matched to its documented decay rate (pricing every 30-90 days, policies every 90-365 days per the Staleness Dimensions table), rather than an ad hoc audit cycle. Trade-off: high-decay-rate categories demand frequent refresh work, competing for bandwidth with new eval development.
3. **Assertion-based tests for volatile fields**: For fields known to change frequently (price, personnel, features), test structural properties (e.g., "price is a positive dollar amount matching the current catalog") rather than an exact expected string, so a legitimate change doesn't require golden-data maintenance to avoid a false failure. Trade-off: assertion-based tests are more complex to author and can be too permissive, missing genuine errors within the accepted range.

### Detection & Response
1. **Failure-rate trend spike investigation**: Monitor eval failure rate over time and treat a sudden spike as a staleness signal to investigate first, not necessarily a genuine regression, since the example found 40% of "failures" were actually stale expectations.
2. **Golden-record age tracking against source-system change timestamps**: Track a "last validated" timestamp per golden entry and compare it against the corresponding source system's last-changed timestamp, automatically flagging entries where the source changed more recently than the golden record was validated.
3. **Sampled manual review before "fixing" the agent**: Before treating an eval failure as a real agent bug, route it through a manual staleness check, since the example describes developer time wasted "fixing" behavior that was actually correct (the $39 answer was right; the golden data was wrong).

### Architecture Patterns
1. **Source-of-truth-linked golden data pipeline**: Architect golden data storage so volatile fields (price, features, policy text) are stored as references/queries into the authoritative system rather than as frozen literal strings, structurally eliminating this failure class for those fields.
2. **Staleness-scored golden-data registry**: Maintain a registry that scores every golden entry's staleness risk based on category decay rate and time since last validation, surfacing a prioritized refresh queue rather than requiring manual full-set audits.
3. **Automated stale-entry flagging via periodic diffing**: Run a scheduled job that diffs golden expected values against current source-system values and auto-flags mismatches for review, rather than relying on the "last audit: 18 months ago" cadence described in the example.

### Metrics
1. **golden_entry_average_age_days**: Target: <90 days since last validation; Alert when average age exceeds 180 days
2. **stale_expectation_failure_rate**: Target: <5% of failures attributable to stale golden data; Alert when stale-attributed failures exceed 25% of total failures
3. **source_of_truth_drift_count**: Target: 0 golden entries with source-system value changed since last validation; Alert on any detected drift, prioritized by category decay rate
4. **hardcoded_volatile_field_count**: Target: 0 volatile-category (pricing/policy) fields stored as hardcoded strings; Alert on any new hardcoded volatile entry introduced

### Alerts
1. **Failure Rate Spike** (P2): Condition - eval failure rate increases sharply without a corresponding agent/model change. Action: investigate for golden-data staleness before treating as regression; sample failed cases for manual staleness review.
2. **Source-of-Truth Drift Detected** (P2): Condition - automated diff finds a source system value changed since the linked golden entry was last validated. Action: refresh the golden entry, re-run affected eval cases, confirm agent behavior against the new expected value.
3. **Golden Data Age Threshold Exceeded** (P3): Condition - a category's average golden-entry age exceeds its defined decay-rate threshold (e.g., pricing entries older than 90 days). Action: schedule a refresh sprint for that category before the next eval run is trusted for release decisions.

## References

- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Evaluation best practices
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Data quality issues
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Evaluation challenges
- [FloTorch: RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Benchmark limitations
