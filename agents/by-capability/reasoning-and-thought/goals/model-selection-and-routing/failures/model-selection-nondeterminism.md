# Model Selection Nondeterminism

## Issue
The same logical task, submitted multiple times under ostensibly the same routing rules, gets sent to different underlying models across runs — because the router's selection logic incorporates a non-reproducible factor (current load, a rolling A/B assignment, a randomized tie-break, cache state) without the calling agent or user being aware selection could vary at all. Results differ run to run not because the task is ambiguous, but because a different model actually answered it each time.

**Frequency**: Occasional

**Symptoms**
- Identical requests submitted minutes apart return meaningfully different quality, tone, or even factual content, traced back to different backend models having served them
- Debugging a reported bad output is difficult because the routing decision that produced it isn't recorded, so the specific model version involved can't be identified after the fact
- A/B test or canary rollout logic unintentionally affects production traffic outside its intended experiment scope, because routing assignment isn't scoped tightly enough to the experiment
- Support and QA teams can't reproduce a reported issue because re-running the same request routes to a different model than the one that produced the original bad output
- Aggregate quality metrics show more variance than expected for a supposedly fixed pipeline, and the variance correlates with routing logs once those are examined

## Root Cause
Many production routers incorporate real-time factors — current instance load, rolling experiment cohort assignment, random tie-breaking among equally-scored candidates, or cache/session affinity — as legitimate parts of their selection logic, but rarely surface which factor determined a given routing decision back to the calling code or logs in a way that's easy to correlate with output quality later. This is often a deliberate design choice (load-based routing needs to vary by definition) that becomes a failure only when it isn't paired with adequate logging and reproducibility tooling — without a durable record of "which model served this exact request," any variance in output is indistinguishable from the model behaving inconsistently versus different models having genuinely been used. A/B test frameworks compound this when cohort boundaries aren't scoped precisely (e.g. by session vs. by individual request), letting a single logical conversation get split across model versions mid-flight without anyone intending that.

## Example
```
A QA engineer files a bug: "Ticket summarization agent produced a summary
that fabricated a refund amount." They attach the exact input and re-run
it through the same API endpoint to reproduce it - and get a correct,
fabrication-free summary instead.

Investigation of routing logs (added after the fact, since none existed
originally) reveals the platform runs a rolling 15% canary of a newer
model version, with cohort assignment based on a hash of (user_id,
current_minute) rather than a stable per-request or per-session key. The
original buggy output came from the canary version; the QA re-run, minutes
later, hashed into the stable-version cohort instead.

Without a routing decision log tied to the original request ID, the team
cannot confirm which model actually produced the reported bug, and the
canary rollout continues serving 15% of production traffic with the
suspected regression for several more days before enough reports
accumulate to correlate the pattern manually.
```

## Statistics
| Finding | Context |
|---------|---------|
| A significant share of "unreproducible" quality bug reports in multi-model routing systems are ultimately traced to routing nondeterminism rather than the model itself behaving inconsistently | Estimated from postmortems of quality bug investigations in routed agent systems |
| Adding per-request routing-decision logging (which specific model/version served this request) typically reduces bug-reproduction time from days to hours in affected teams | Typical range reported by teams that added this logging |
| Coarse cohort-assignment keys (e.g. time-based rather than session-based) are a factor in a majority of canary-rollout-related nondeterminism incidents | Estimated from review of A/B routing configuration incidents |

## Mitigations
1. **Durable per-request routing logs**: Record which specific model/version/instance served every request, keyed to the request ID, so any downstream bug report can be traced back to the exact model that produced it.
2. **Stable cohort-assignment keys**: Scope A/B and canary rollout assignment to a stable key (user or session ID, not time-window hashes) so a single logical conversation or workflow doesn't get split across model versions mid-flight.
3. **Reproducibility mode for debugging**: Provide a debug/support-facing routing override that pins a specific request replay to the exact model/version that served the original, rather than re-routing through live (and possibly different) selection logic.
4. **Variance monitoring**: Track output-quality variance for logically identical or near-identical repeated requests as a first-class metric, since elevated variance is a leading indicator of unintended routing nondeterminism.
5. **Explicit experiment scoping documentation**: Maintain a single source of truth for which routing decisions are intentionally variable (load balancing, A/B tests) versus expected to be deterministic, so unexpected variance is quickly recognized as a bug rather than assumed to be by design.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| routing_log_coverage | Share of production requests with a durable, queryable record of which model served them | Alert if < 100% for any traffic tier |
| repeated_request_output_variance | Quality/content variance across repeated submissions of logically identical requests | Alert if variance exceeds expected baseline |
| unscoped_cohort_split_rate | Rate at which a single session/conversation is served by more than one model version due to cohort reassignment | Alert if > 0 for session-continuity-sensitive flows |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Missing routing log on bug report | A quality bug report references a request with no corresponding routing-decision log | Medium | Prioritize closing the logging gap, treat report as unconfirmed until reproducible |
| Mid-session cohort split detected | A session is found to have been served by multiple model versions across turns | High | Fix cohort-assignment key scoping, audit affected sessions for continuity issues |

## Related Patterns
- [Model Switching Mid-Session](./model-switching-mid-session.md) - the specific, session-continuity-breaking consequence of unscoped cohort assignment described here
- [Model Load Balancing Failure](./model-load-balancing-failure.md) - load-based routing is one legitimate source of the nondeterminism this pattern describes, when not paired with adequate logging
- [Model Capability Mismatch](./model-capability-mismatch.md) - nondeterministic selection increases the chance that some fraction of requests land on a capability-incompatible model inconsistently
