# Outdated Memory

## Issue: Agent uses information that changed.

**Frequency**: Occasional

**Symptoms**
- Stored fact conflicts with recent user statement.
- [Add more specific symptoms]

**Root Cause**
Agent uses information that changed.

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
1. **Freshness Scoring with Category-Specific TTLs**: Assign each memory category a decay policy reflecting how often it realistically changes (address: months, current project: days, name: years). Retrieval applies a freshness score that down-weights or excludes facts past their expected TTL unless recently reconfirmed, so the agent doesn't treat a six-month-old "currently working on X" as still true.
2. **Update-on-Contradiction Workflow**: When the user states something that contradicts a stored fact, the agent doesn't just use the new statement for the current turn — it triggers a memory-update action that supersedes the old record with a new versioned entry, closing the loop so the next session also gets the updated fact.
3. **Active Reconfirmation for High-Volatility Facts**: For facts known to change often and that materially affect agent behavior (e.g., current employer, active project, subscription tier), periodically prompt a lightweight reconfirmation ("still working on the Atlas project?") rather than trusting an old value indefinitely.

### Detection & Response
1. **Contradiction-on-Read Check**: When assembling context, compare stored facts against any explicit statements made earlier in the current conversation; if the live conversation contradicts a stored fact, flag it and prefer the live statement while queuing a background memory-update.
2. **Freshness Audit Sweep**: A scheduled job scans the memory store for records past their category TTL that haven't been reconfirmed or superseded, and either soft-expires them (excluded from retrieval) or queues them for reconfirmation on next relevant interaction.
3. **Stale-Use Incident Logging**: Whenever a response is later found to have used an outdated fact (via user correction or downstream error), log the memory_id, its age at time of use, and the category, feeding back into TTL calibration.

### Architecture Patterns
1. **Versioned Fact Store with Freshness Metadata**: Store each fact with created_at, last_confirmed_at, and category; retrieval computes a freshness score at query time rather than treating all facts as equally durable, and the score is exposed to the generation step for optional hedging language.
2. **Update Propagation Pipeline**: A background pipeline listens for detected contradictions/updates during conversations and writes new versioned records, superseding rather than duplicating, ensuring both the freshness sweep and future retrieval see one current value per field.
3. **Reconfirmation Scheduler**: A service tracks last_confirmed_at per high-volatility fact and schedules low-friction reconfirmation prompts, keeping durable memory synchronized with reality without requiring the user to proactively correct the agent every time.

### Metrics
1. **stale_fact_usage_rate_percent**: Target: < 1% of responses using volatile-category facts; Alert threshold: > 3%
2. **contradiction_to_update_latency_minutes**: Target: < 5 min from detected contradiction to memory update; Alert threshold: > 60 min
3. **facts_past_ttl_unreconfirmed_percent**: Target: < 5% of volatile-category records; Alert threshold: > 15%
4. **user_correction_rate_for_outdated_facts**: Target: < 1% of personalized responses; Alert threshold: > 2.5%

### Alerts
1. **High-Volatility Fact Used Past TTL** (P2 - Warning): Condition - a response used a high-volatility category fact whose last_confirmed_at exceeds its TTL by more than 2x. Action: Trigger reconfirmation prompt, flag response for review, lower confidence weighting for that fact category.
2. **Contradiction Detected But Not Propagated** (P2 - Warning): Condition - contradiction_to_update_latency_minutes exceeds SLA for a detected live contradiction. Action: Investigate update pipeline lag, manually push the corrected fact, check for pipeline backlog.
3. **Repeated User Corrections on Same Field** (P3 - Info): Condition - same user corrects the same memory field 2+ times in a month. Action: Review TTL calibration for that field's category, consider shortening decay window or adding active reconfirmation.

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

- [MS-Agentic-Failure-Taxonomy](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)
- Note: Agentic AI failure modes; safety/security; memory poisoning; tool use; multi-agent risks.
