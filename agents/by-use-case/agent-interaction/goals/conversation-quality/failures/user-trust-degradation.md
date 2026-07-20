# User Trust Degradation

## Issue
Individually minor failures — a small contradiction, a slightly wrong assumption, an overclaimed capability, a tone mismatch — don't each cause a user to distrust the agent on their own, but repeated exposure across many sessions builds a background skepticism where the user starts double-checking the agent's outputs, hedging their reliance on it, and treating confident-sounding claims with suspicion, even in cases where the agent is actually correct. Trust, once degraded, doesn't recover at the same rate it eroded, and its loss changes user behavior (more verification overhead, less delegation) even absent any further errors.

**Frequency**: Common

**Symptoms**
- Users increasingly ask the agent to double-check or cite sources for claims it previously would have been accepted on the first response
- Users independently verify agent outputs at a rate that rises over the relationship rather than falling as usage increases
- Language in user messages shifts toward hedging or skepticism ("are you sure," "double check that") even for low-risk requests
- A single new error after a series of correct responses produces an outsized negative reaction relative to the error's actual severity
- Users delegate progressively less consequential work to the agent over time, reserving it for low-stakes tasks only

## Root Cause
Trust calibration in human-agent interaction behaves asymmetrically: a confidently stated wrong answer is more damaging to trust than an honestly hedged uncertain one, because it demonstrates the agent's confidence signal is unreliable, not just that it made a mistake. Each individual conversation-quality failure (contradiction, wrong assumption, overclaim) independently damages a small amount of trust, and because these are usually not tracked cumulatively per user or per relationship, no system-level signal exists to show that a string of small, individually-tolerable failures has crossed a threshold where the user has fundamentally recalibrated how much to rely on the agent — the degradation is invisible until it shows up as reduced delegation or churn.

## Example
```
Over six weeks, a user experiences with the same agent:
- Week 1: agent contradicts an earlier stated fact about a project
  deadline (later corrected).
- Week 3: agent confidently states a wrong capability ("I've saved
  that for next time") that turns out to be false.
- Week 5: agent makes a silent wrong assumption about report scope,
  requiring a redo.

None of these individually generated a complaint. But by week 6, the
user's request pattern has changed: they now ask the agent to "confirm
this is definitely right" on requests that used to be accepted without
question, and they've stopped delegating anything with real
consequences, restricting the agent to low-stakes drafting only.

When asked directly, the user says "I just don't fully trust it
anymore, I always have to check its work" — unable to point to one
specific incident, because the erosion was cumulative across several
minor ones.
```

## Statistics
| Finding | Context |
|---------|---------|
| Confidently-stated incorrect claims produce measurably larger trust-recovery costs than honestly-flagged uncertain claims of similar factual severity | Typical range observed in human-AI trust research and production feedback analysis |
| Verification/double-checking behavior by users tends to increase, not decrease, over a relationship with an agent that has produced even a small number of confident errors | Estimated from longitudinal usage pattern analysis |
| Explicit, calibrated confidence signaling (distinguishing verified facts from inferred ones) measurably slows trust erosion compared to uniformly confident phrasing | Reported range across teams that added confidence calibration |

## Mitigations
1. **Calibrated confidence signaling**: Have the agent explicitly distinguish verified, source-backed claims from inferred or uncertain ones in its phrasing, so confidence language remains a reliable signal rather than uniformly high regardless of actual certainty.
2. **Cumulative trust-impact tracking**: Track per-user counts of trust-damaging incidents (contradictions, overclaims, wrong assumptions) over time as a distinct metric from per-session quality, since the damage is cumulative rather than isolated.
3. **Proactive error acknowledgment**: When a past error is identified, acknowledge it explicitly and explain what changed, rather than silently correcting and hoping it goes unnoticed, since unacknowledged corrections read as further inconsistency.
4. **Verification-behavior monitoring**: Track the rate at which users double-check, ask for sources, or express skepticism over time as an early, un-self-reported signal of trust erosion, since users rarely volunteer "I don't trust you" directly.
5. **Consequence-tiered reliability investment**: Invest disproportionate accuracy and confidence-calibration effort in request categories users treat as higher-stakes, since trust damage in those categories generalizes faster to overall skepticism.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| verification_request_rate_trend | Trend in how often users ask the agent to double-check or confirm its own outputs | Alert if rising over a rolling multi-week window |
| cumulative_trust_incident_count | Per-user running count of contradictions, overclaims, and wrong-assumption incidents | Alert if exceeding a defined threshold per user |
| high_stakes_delegation_rate | Share of requests routed to the agent that are consequential/high-stakes versus low-stakes drafting only | Alert if declining trend detected |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Rising verification behavior detected | verification_request_rate_trend increases sustained over multiple weeks for a user cohort | Medium | Audit recent conversation-quality incidents for that cohort, review confidence calibration |
| Trust incident threshold exceeded for a user | cumulative_trust_incident_count crosses defined threshold | Medium | Flag for proactive outreach or quality review before churn occurs |

## Related Patterns
- [Conversation Contradiction](./conversation-contradiction.md) - one of the fastest-acting individual contributors to cumulative trust erosion
- [User Expectation Mismatch](./user-expectation-mismatch.md) - overclaimed capabilities are a specific trust-damaging pattern that compounds into general skepticism
- [User Retention Decline](./user-retention-decline.md) - degraded trust is one of the primary underlying mechanisms driving the gradual usage decline described in that pattern
