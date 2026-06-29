# Self-Verification Illusion in Attrition Risk Score Recheck

## Issue: When Asked to Double-Check a Flagged High-Attrition-Risk Score Before a Retention-Intervention Budget Is Allocated, the Same Agent Re-Derives the Score From the Same Feature Set That Produced the Original Flag and Confirms It, Instead of Checking the Score Against Independent Evidence Such as Recent Manager Feedback or a Recent Compensation Change

**Frequency**: Occasional

**Symptoms**
- A "double-check this attrition risk score before we allocate a retention bonus" request returns a confident confirmation of high risk, even when an independent source -- such as a recent compensation adjustment or recent positive manager feedback -- would show the underlying risk has already changed
- The agent's recheck re-applies the same feature-weighting logic that produced the original score, rather than pulling an independent signal not already baked into that feature set
- Asking the agent to explain its recheck describes re-running the same risk-scoring computation and confirming it produced a consistent result, not a comparison against an independent, more recent signal
- Pulling an independent signal manually for the same employee, separate from the agent's narrative reasoning, sometimes shows the flagged risk is stale relative to a recent change
- The miss concentrates on employees who had a relevant change (comp adjustment, manager change, role change) shortly after the underlying feature snapshot was taken but before the recheck, since the same-feature recheck cannot see anything that happened after that snapshot

**Root Cause**
A same-model self-check re-derives its risk judgment from the same feature snapshot and weighting logic that produced the original score, so it cannot surface anything that changed after that snapshot was taken, even when an independent, more recent signal is available elsewhere in the system. Because the recheck produces a fluent, confident restatement of the same conclusion, it is indistinguishable in tone from a check that actually consulted an independent and more current source, giving the retention-budget decision-maker false confidence that the score was substantively re-verified.

**Example**
```
Retention-prediction agent flags an employee as high attrition risk based on a feature snapshot from three weeks ago: below-market comp, no recent promotion, declining engagement-survey score
HR manager requests the agent double-check the score before approving a retention bonus
Agent re-runs the same risk-scoring computation against the same three-week-old feature snapshot and confirms: "Risk score remains high, recommend retention bonus"
A compensation adjustment closing the below-market gap was processed two weeks ago and a recent one-on-one noted improved engagement -- neither signal is part of the feature snapshot the recheck used
Retention bonus is approved based on a risk score that no longer reflects the employee's actual situation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use and reasoning agents show a measurable gap between expressed confidence after a self-check and the actual correctness of the underlying conclusion, particularly when the self-check does not introduce an independent evidence source | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Surveys of multi-agent and agentic system failures identify same-source self-verification, where a recheck reuses the same inputs as the original judgment, as a recurring cause of false confidence in agentic decision pipelines | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Research on tool-use error detection finds that verification steps relying on the same computation path as the original action fail to catch errors that an independent data source would surface | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |

**Contributing Factors**
- The attrition-risk recheck is implemented as a re-run of the same feature-scoring computation rather than a pull of independent, more recent signals (recent comp changes, recent manager feedback, recent role changes)
- No distinction is enforced between "re-confirmed the same score" and "checked against independent, more current evidence" in how the recheck result is logged or reported to the budget decision-maker
- Feature snapshots used for risk scoring are not automatically invalidated or re-flagged when a relevant downstream event (comp change, manager change) occurs after the snapshot was taken

---

## Mitigation Strategies

1. **Independent Recency Check as Mandatory Verification Source**: Require any attrition-risk recheck to query for recent comp changes, manager changes, or recent feedback events that postdate the original feature snapshot, rather than relying on a re-run of the same scoring computation
2. **Snapshot Staleness Flag**: Automatically flag a risk score as stale and requiring recheck against independent signals whenever a relevant event (comp adjustment, manager change, role change) is logged after the feature snapshot date
3. **Disallow Same-Computation Self-Check as Sole Verification**: Prohibit a retention-budget approval from being satisfied solely by an agent re-running the same risk-scoring computation; require either an independent-signal check or human HR review
4. **Recheck Provenance Logging**: Log whether each recheck consulted an independent signal source or only re-ran the original computation, so budget decisions can be audited for which verification path was actually used

### Metrics
- Rate of "risk confirmed" rechecks where an independent-signal audit, run after the fact, finds a relevant change postdating the original feature snapshot
- Rate of attrition-risk rechecks that queried an independent signal source versus a same-computation re-run only
- Average age of the feature snapshot used in a recheck relative to the most recent relevant employee event

### Alerts
- An independent-signal audit finds a relevant change postdating the feature snapshot for a risk score marked "confirmed" by same-computation recheck alone → P2
- A retention-budget decision is approved based on a recheck that did not query any independent signal source → P2
- Same-computation-only rechecks as a share of total rechecks exceed the defined threshold for a rolling window → P3

---

## References

- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
