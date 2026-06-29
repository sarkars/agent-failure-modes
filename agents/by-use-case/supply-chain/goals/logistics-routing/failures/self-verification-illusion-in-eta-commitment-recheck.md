# Self-Verification Illusion in ETA-Commitment Recheck

## Issue: A Logistics-Routing Agent's "Double-Check" of an Estimated-Time-of-Arrival Commitment Before Sending It to a Customer Re-Derives the Estimate From the Same Reasoning Trace and Cached Inputs That Produced the Original Estimate, Rather Than Querying an Independent, Live Source, So an Error in the Original Estimate Survives the Recheck Unchanged

**Frequency**: Occasional

**Symptoms**
- An ETA commitment that is flagged as "verified" or "double-checked" before being sent to a customer is later found, when checked against a live carrier-tracking source, to be wrong in exactly the same way as the original, unverified estimate
- Inspecting the recheck step's actual inputs shows it reused the same cached carrier data and the same routing reasoning as the original estimate, rather than issuing a fresh query to a live tracking source
- The recheck consistently passes (reports no discrepancy) even on ETAs later proven wrong, because the recheck and the original estimate share the same blind spot rather than functioning as two independent checks
- Routing supervisors who see a "verified" label on an ETA commitment treat it as having passed an independent confirmation step and do not separately spot-check it against live tracking
- The pattern is most visible for shipments where the underlying carrier or traffic data was stale or wrong at the time of the original estimate, since the recheck on the same stale data cannot catch what the original estimate already missed

**Root Cause**
A self-check or recheck step that prompts the same model to reconsider its own prior output, using the same context and the same underlying data, is not equivalent to an independent verification against a different source; if the original estimate's inputs were stale or wrong, re-reasoning over those same inputs reliably reproduces the same conclusion. Genuine verification requires querying a source that is independent of the original estimate's inputs and reasoning, which a same-context recheck does not provide regardless of how it is framed in the workflow.

**Example**
```
Logistics-routing agent generates an ETA commitment for a shipment using a cached carrier-status snapshot that is, unknown to the agent, twelve hours stale
Before sending the commitment to the customer, a "verification" step asks the agent to recheck the ETA, but the recheck step is given the same cached carrier-status snapshot and the same routing trace, not a fresh live-tracking query
Recheck step reports the ETA as confirmed, since reasoning over the same stale snapshot reproduces the same estimate
ETA commitment, now labeled as verified, is sent to the customer
Live tracking, checked independently after the fact, shows the shipment is delayed well beyond the committed ETA, a discrepancy the same-context recheck had no way to surface
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Calibration research in tool-using and decision-support agents notes that self-generated confidence or verification signals are frequently uncorrelated with actual correctness, particularly when the verification step has access to the same information that produced the original output | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Failure-mode analysis of platform-orchestrated agentic workflows identifies same-context self-verification as a distinct failure category from genuine cross-source verification, since both share the same upstream data and reasoning errors | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |
| Research on LLM agents for supply chain management notes that ETA reliability depends on the freshness and independence of the data source queried at commitment time, not on the number of internal reasoning passes applied to a single data snapshot | [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597) |

**Contributing Factors**
- The recheck step's prompt design does not require querying a source independent of the original estimate's inputs, allowing it to default to re-reasoning over the same cached data
- A "verified" label is applied to the ETA commitment based solely on the recheck step completing, with no requirement that the recheck used a different data source than the original estimate
- Routing supervisors treat the verified label as equivalent to independent confirmation, reducing the rate of separate spot-checks against live tracking

---

## Mitigation Strategies

1. **Independent-Source Requirement for ETA Verification**: Require any ETA-commitment recheck to query a live tracking source independent of the original estimate's cached inputs, rejecting a recheck that reuses the same data snapshot
2. **Verification Provenance Logging**: Require every "verified" label on an ETA commitment to log which specific data source the verification queried, making it auditable whether the recheck was genuinely independent or same-context
3. **Staleness Threshold on Recheck Inputs**: Block a recheck from passing if the data source it queries is older than a defined freshness threshold, forcing a fresh live query rather than allowing reuse of stale cached data
4. **Periodic Independent Spot-Audits**: Regardless of recheck status, route a sample of "verified" ETA commitments to an independent live-tracking spot-check to measure whether the recheck step is functioning as genuine verification

### Metrics
- Rate of "verified" ETA commitments whose recheck step queried the same data source as the original estimate rather than an independent live source
- Discrepancy rate between "verified" ETA commitments and subsequent live-tracking ground truth
- Mean data-source age at the time a recheck step reports an ETA as confirmed

### Alerts
- An ETA commitment is labeled "verified" with a recheck step that queried the same cached data source as the original estimate → P2
- A "verified" ETA commitment is found to diverge from live-tracking ground truth by more than the defined threshold → P1
- Same-source recheck rate across all ETA commitments exceeds the defined threshold for a rolling window → P3

---

## References

- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597)
