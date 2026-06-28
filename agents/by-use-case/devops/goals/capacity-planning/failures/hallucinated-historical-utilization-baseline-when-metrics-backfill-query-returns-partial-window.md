# Hallucinated Historical-Utilization Baseline When Metrics-Backfill Query Returns Partial Window

## Issue: A Capacity-Planning Agent Building a Forecast From a Metrics Backfill Query That Returns Only Part of the Requested Historical Window -- Because a Subset of Data Points Were Dropped, Retention-Expired, or the Query Was Silently Throttled -- Treats the Partial Result as the Complete Historical Baseline and Produces a Forecast That Understates True Peak Utilization

**Frequency**: Occasional

**Symptoms**
- The forecast's stated historical peak utilization is lower than the actual peak utilization recorded for the same period in a separate, manually pulled metrics export
- The metrics-backfill query's response contains gaps -- missing data points for specific days or hours within the requested window -- but the forecasting step treats the returned points as the full record rather than checking for completeness
- Re-running the same backfill query with retry logic or a longer timeout returns additional data points that include a higher peak than what the original forecast was based on
- The gap concentrates on historical windows covering retention boundaries or known monitoring-system migration periods, where backfill completeness is most likely to be compromised
- The forecast is presented with full confidence and no indication that the underlying historical data was incomplete

**Root Cause**
A metrics-backfill query that silently drops, throttles, or fails to retrieve a subset of requested data points returns a response that is structurally valid -- a well-formed time series -- with no signal distinguishing "this is the complete requested window" from "this is whatever subset succeeded." The forecasting step has no instruction to verify completeness against the requested window's expected point count, so it proceeds as if the partial series were the full historical record, understating any peak that fell within the missing gap.

**Example**
```
Capacity-planning agent requests 90 days of hourly utilization metrics to forecast next quarter's required headroom
Backfill query silently drops 12 days' worth of data points due to a monitoring-system migration that occurred during the requested window, returning a structurally valid but incomplete 78-day series
Agent computes the historical peak from the returned 78 days and forecasts required capacity headroom based on that peak
The 12 missing days included the highest utilization peak of the entire quarter, driven by a promotional traffic event
Forecast understates required headroom; the next comparable traffic event triggers capacity exhaustion the plan did not account for
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to complete plausible-sounding conclusions from incomplete tool output, rather than treating a partial or gapped result as a signal requiring further verification | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Frameworks for detecting and correcting tool-use errors in agentic systems identify failure to recognize incomplete or gapped tool responses as a distinct, recurring tool-use error category | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Tool-use agents show measurable miscalibration between expressed confidence and actual correctness when relying on a tool response that is incomplete rather than fully representative | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |

**Contributing Factors**
- The metrics-backfill query's response includes no explicit point-count or completeness signal that the forecasting step is required to check against the requested window
- The forecasting step treats "data returned without an error" as equivalent to "complete requested window returned," with no distinction between the two
- No automated check compares the returned series' point count against the expected count for the requested window before the forecast is generated

---

## Mitigation Strategies

1. **Mandatory Completeness Check Before Forecasting**: Require the forecasting step to verify the backfill query's returned point count against the expected count for the requested window, blocking forecast generation on any gap and triggering a retry or explicit flag
2. **Explicit Gap-Reporting in Backfill Tool Schema**: Require the metrics-backfill tool to return an explicit list of missing or dropped intervals alongside the data it did retrieve, rather than silently omitting them
3. **Known-Gap-Period Flagging for Migration and Retention Boundaries**: Maintain an explicit list of known monitoring-system migration windows and retention boundaries, and require any forecast whose historical window overlaps one to undergo mandatory secondary data-source verification
4. **Cross-Source Peak Verification for Capacity Forecasts**: Before finalizing a capacity forecast, cross-check the computed historical peak against at least one independent metrics source or export, flagging any forecast where the two disagree beyond a defined tolerance

### Metrics
- Rate of capacity forecasts generated from a backfill query result with fewer data points than the requested window's expected count
- Rate of forecasts later found to understate true historical peak utilization when audited against a cross-source export
- Number of capacity-exhaustion incidents attributable to a forecast based on an incomplete historical baseline

### Alerts
- A capacity forecast is generated from a backfill query result with an unresolved point-count gap → P1
- A cross-source peak verification finds the forecast's historical peak materially understates an independently sourced peak → P1
- Backfill query gap rate exceeds the defined threshold for a rolling window → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
