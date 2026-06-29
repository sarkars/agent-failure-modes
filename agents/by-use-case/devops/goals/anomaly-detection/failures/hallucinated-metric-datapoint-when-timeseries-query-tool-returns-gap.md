# Hallucinated Metric Datapoint When Timeseries Query Tool Returns Gap

## Issue: When an Anomaly-Detection Agent's Call to the Metrics-Timeseries Query Tool Returns a Gap -- a Window With Missing Datapoints Due to a Collector Outage or Downsampling -- the Agent's Anomaly Explanation Cites a Specific Numeric Value and Timestamp for the Missing Window as if It Had Been Retrieved, Fabricated to Complete a Continuous-Looking Narrative Rather Than Flagging the Gap as Missing Data

**Frequency**: Occasional

**Symptoms**
- Anomaly explanation states a specific metric value at a specific timestamp (e.g., "CPU utilization spiked to 94% at 03:14 UTC") for a time window that the metrics-query tool's trace shows returned no data for that window
- Re-querying the same window through a different collector or after backfill shows either no real datapoint at the cited timestamp or a genuinely different value, confirming the originally cited figure was fabricated
- The fabricated datapoint is presented with the same formatting and confidence as genuinely retrieved values elsewhere in the same explanation, making it indistinguishable without checking the underlying tool trace
- An engineer investigating the cited spike finds the monitoring backend has no record of any datapoint at that timestamp for that metric, only a recorded gap
- The pattern recurs specifically following collector outages, downsampling boundaries, or retention-window edges where partial or missing data is a known, recurring condition rather than a rare edge case

**Root Cause**
When the timeseries-query tool returns a gap instead of a complete series, the model can produce a numerically and stylistically plausible datapoint to keep its anomaly narrative continuous and complete, rather than explicitly representing the gap as missing data requiring a different mode of analysis (interpolation flagged as such, or an explicit "insufficient data" conclusion). Nothing in the default workflow forces the agent to treat a data gap as a hard constraint on what it can claim to have observed.

**Example**
```
Anomaly-detection agent investigates a latency spike alert and queries the request-latency timeseries for the preceding 30 minutes
Metrics-query tool returns data for the first 22 minutes but a 4-minute gap during which the metrics collector was itself restarting
Agent's anomaly narrative states: "Latency climbed steadily from 120ms to 850ms between 03:10 and 03:14 UTC, peaking at 03:14 before recovering" -- the 03:10-03:14 window is exactly the gap the tool reported no data for
No datapoint exists in the metrics backend for that window; the climbing-then-peaking narrative was fabricated to bridge the gap between the known pre-gap and post-gap values
Engineer investigating the "03:14 peak" finds no corresponding datapoint and loses time trying to correlate a peak that never existed against deploy and infra logs
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to fabricate plausible-sounding content to fill gaps left by failed or incomplete tool calls, a well-characterized hallucination subtype distinct from a reasoning error over real data | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds agents frequently do not surface a partial or gapped tool result as a hard stop, instead proceeding to generate output as if the call had returned complete data | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Execution-provenance research for LLM agents argues that traceable evidence linking generated claims to actual tool outputs is necessary specifically because models do not reliably self-report when a claim lacks real grounding | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- Anomaly-narrative generation implicitly rewards a smooth, continuous-sounding explanation, with no explicit instruction that representing a data gap as missing is an acceptable and expected output
- No automated step verifies that every cited datapoint and timestamp in the narrative resolves to an actual retrieved value in the underlying tool trace
- Collector restarts, downsampling boundaries, and retention-window edges are known, recurring sources of gaps but are not flagged to the agent as heightened-fabrication-risk windows
- Tool-call results showing partial data are not surfaced prominently in the agent's output, so a reviewer has no visible signal that part of the cited window was never actually queried successfully

---

## Mitigation Strategies

1. **Mandatory Evidence Resolution Check**: Before an anomaly narrative is finalized, automatically verify that every cited datapoint and timestamp resolves to an actual value retrieved from the metrics backend, flagging any unresolved citation for removal
2. **Explicit Gap Representation**: Require the agent to represent a data gap explicitly in its narrative (e.g., "no data available 03:10-03:14 UTC due to collector restart") rather than bridging it with an inferred or fabricated value
3. **Execution Provenance Logging**: Log which specific tool call produced each cited datapoint in the narrative, so any citation with no corresponding successful tool-call result is automatically flagged as a likely fabrication
4. **Gap-Aware Retry Policy**: Require a gapped timeseries query to be retried against a secondary collector or backfill source before the agent proceeds to narrative generation, reducing the frequency of investigations that proceed on a known-incomplete series

### Metrics
- Rate of cited datapoints or timestamps in finalized anomaly narratives that fail automated resolution against the metrics backend
- Number of anomaly investigations proceeding to narrative generation despite a logged data-gap in the queried window
- Mean time-to-detection for fabricated datapoints, measured from narrative publication to an engineer flagging it as unverifiable

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Fabricated datapoint published | An anomaly narrative cites a datapoint that fails evidence resolution against the metrics backend | P1 | Retract narrative; re-investigate with explicit gap representation |
| Narrative generated over known gap | Anomaly analysis proceeds to narrative generation despite a logged data-gap with no retry or backfill attempt | P2 | Require backfill or explicit gap disclosure before re-publishing |
| Fabrication rate above baseline | Rate of unresolved cited datapoints across anomaly investigations exceeds baseline for two consecutive reporting periods | P2 | Audit narrative-generation prompt and evidence-resolution enforcement |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
