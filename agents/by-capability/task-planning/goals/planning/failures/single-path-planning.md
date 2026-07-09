# Single-Path Planning

## Issue: Agent has no fallback when the first route fails.

**Frequency**: Occasional

**Symptoms**
- Failure after one empty search/API error.
- [Add more specific symptoms]

**Root Cause**
Agent has no fallback when the first route fails.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
