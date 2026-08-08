# Single-Path Planning

## Issue: Agent has no fallback when the first route fails.

**Frequency**: Occasional

**Symptoms**
- Failure after one empty search/API error.
- Agent reports "unable to fulfill shipment" after a single carrier API returns an error, without checking any alternate carrier or route.
- Plan lists exactly one supplier/route for a sourcing task with no documented fallback if that supplier is out of stock.
- Agent retries the identical failed call several times (same carrier, same endpoint) rather than switching to a structurally different approach.
- Task terminates as "blocked" immediately following one empty inventory-lookup result, with no secondary warehouse or vendor queried.

**Root Cause**
Planning produces a single linear strategy rather than being required to output ranked alternatives for anything above a basic complexity threshold, partly because time-boxed sessions discourage spending budget on candidate paths that might not end up being needed, and partly because alternate providers or routes that do exist in system configuration are never surfaced to the planner as viable options at generation time. With no library mapping common failure signatures — timeouts, empty results, rate limits — to predefined fallback strategies, the executor has nothing to reach for when a call fails, so it treats the tool failure as equivalent to task failure instead of a signal to try the next-ranked approach.

**Example**
```
A logistics coordination agent is asked to "arrange expedited shipment of replacement parts to the Denver facility." It queries its primary carrier's rate API, which returns a timeout error due to an unrelated outage. The agent's plan had only ever considered this one carrier, so it reports back "unable to arrange shipment, carrier API unavailable" and stops — even though two other approved carriers are configured in the system and could have fulfilled the request within the same SLA. The Denver facility misses its production deadline because no fallback route was ever part of the plan.
```

**Contributing Factors**
- Planning stage generates a single strategy rather than being required to produce ranked alternatives for tasks above a risk/complexity threshold.
- No fallback-trigger library exists mapping common failure signatures (timeout, empty result, rate limit) to predefined alternate routes.
- The executor treats a tool failure as task failure rather than a signal to select the next-ranked strategy.
- Time-boxed sessions discourage generating multiple candidate strategies upfront since only one is expected to be needed.
- Alternate providers/routes exist in the system configuration but aren't surfaced to the planner as viable options at plan-generation time.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Carrier fallback on API failure | Primary carrier rate API returns a timeout/5xx error | Agent selects the next-ranked configured carrier and completes the shipment plan | Task reported as failed/blocked immediately after the single carrier error, no fallback attempted |
| Empty inventory result | Primary warehouse inventory lookup returns zero stock for requested part | Agent queries at least one alternate warehouse/vendor before reporting unavailability | Task terminates as unfulfillable after one empty lookup with no secondary source queried |
| Distinguishing transient vs. structural failure | Primary carrier returns a transient rate-limit error vs. a permanent route-unavailable error | Transient error triggers backoff+retry; structural error triggers a fallback strategy switch | Agent applies the same bare retry to both error types, or gives up on a transient error |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| fallback_generation_rate_percent | > 90% of eligible plans include a ranked alternate strategy | Check plan artifacts for tasks above the risk/complexity threshold for a second-ranked strategy field |
| task_success_rate_after_primary_failure_percent | > 70% | Of tasks where the primary route/tool failed, measure how many still completed successfully via a fallback |

---

## Mitigation Strategies

### Prevention
1. **Mandatory Alternate-Path Generation**: For tasks above a complexity/risk threshold, require the planner to produce at least 2-3 candidate strategies with an explicit fallback ordering before execution begins, so a single API failure or empty result doesn't leave the agent with nothing to try next.
2. **Fallback Trigger Library**: Predefine common failure signatures (empty search result, API error code, timeout) mapped to specific fallback strategies per tool/domain, so the agent doesn't need to invent a fallback ad hoc under failure pressure — it consults a known-good alternate route.
3. **Retry-with-Alternate-Strategy Policy**: Enforce at the executor level that a failed action triggers selection of the next-ranked strategy from the plan (not a bare retry of the same failed call, and not immediate task termination).

### Detection & Response
1. **Single-Attempt Failure Terminator Detector**: Flag sessions/tasks that terminate or report failure immediately after exactly one failed tool call with no alternate strategy attempted, which is the direct signature of single-path planning.
2. **Fallback Utilization Rate Tracking**: Measure how often generated plans actually contain and use a fallback path versus how often tasks fail on the first route; low fallback utilization combined with high first-route failure indicates missing fallback generation.
3. **Dead-End Pattern Mining**: Mine logs for recurring single-path failure points (same tool, same error signature) across many sessions and feed these back into the fallback trigger library so future plans handle them proactively.

### Architecture Patterns
1. **Multi-Path Planner**: Produces a ranked strategy list with explicit fallback edges (a small graph rather than a linear plan), so the executor has a defined next step whenever the current strategy fails.
2. **Fallback Policy Engine**: Maps failure signatures to alternate actions in a rules table, consulted automatically by the executor on failure so fallback selection doesn't require a full agent re-planning cycle.
3. **Retry/Backoff Orchestrator with Strategy Switching**: Distinguishes transient failures (worth retrying the same call) from structural failures (requiring a different strategy), routing each to the appropriate recovery path.

### Metrics
1. **single_path_failure_rate_percent**: Target: < 5%; Alert threshold: > 15%
2. **fallback_invocation_rate_percent**: Target: matches expected failure rate of primary route; Alert threshold: near 0% despite nonzero primary failures
3. **task_success_rate_after_fallback_percent**: Target: > 70%; Alert threshold: < 40%
4. **mean_fallback_attempts_per_task**: Target: 1-2; Alert threshold: 0 (no fallback ever attempted)

### Alerts
1. **Terminal Failure After Single Attempt** (P2 - Warning): Condition - task reported as failed after exactly one tool-call failure with no fallback attempted. Action: Route to fallback policy review; consider manual retry.
2. **Fallback Library Miss** (P3 - Info): Condition - a failure signature has no mapped fallback strategy in the library. Action: Add the signature and an appropriate fallback to the library.
3. **Fallback Success Rate Decline** (P2 - Warning): Condition - task_success_rate_after_fallback drops below 40% over a rolling week. Action: Audit fallback strategies for staleness or broken alternate routes.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| single_path_failure_rate_percent | > 15% |
| fallback_invocation_rate_percent | near 0% despite nonzero primary failures |
| task_success_rate_after_fallback_percent | < 40% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| **Terminal Failure After Single Carrier/Route Attempt** | Task reported as failed after exactly one tool-call failure with no fallback route attempted | Medium |
| **Fallback Library Miss for New Failure Signature** | A failure signature (error code/pattern) has no mapped fallback strategy in the library | Low |
| **Fallback Success Rate Decline** | task_success_rate_after_fallback drops below 40% over a rolling week | Medium |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
