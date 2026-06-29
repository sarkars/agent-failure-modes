# Hallucinated Complete Sales History When POS Feed Returns Partial Data

## Issue: A Demand-Forecasting Agent Queries a Point-of-Sale Data Feed for a SKU's Trailing Sales History and, When the Feed Returns a Partial Window (Missing Several Recent Weeks) Without an Explicit Error, the Agent Generates a Forecast as If It Had Received the Full History, Silently Treating the Truncated Window as Complete

**Frequency**: Occasional

**Symptoms**
- A generated forecast's trend component shows an abrupt, unexplained shift that traces back to the forecast having been computed over fewer weeks of history than the standard lookback window calls for
- Re-querying the same POS feed for the same SKU and date range, after the fact, returns additional weeks of data that were missing from the response the forecasting run actually used
- The agent's forecast output contains no flag, caveat, or confidence reduction indicating that the input history was shorter than the configured lookback window
- The gap is most visible for SKUs whose POS feed connection experienced a partial outage or delayed batch load in the days before a forecast run, since those are the only cases where the truncated and full windows diverge
- Inventory planners who consume the forecast without checking the row count of the underlying query treat the truncated-history forecast as equivalent in reliability to a full-history one

**Root Cause**
The POS feed returns a partial result set without an explicit error code when an upstream batch load is delayed or incomplete, and the forecasting agent has no instruction to verify the row count or date coverage of a tool response against the lookback window it was configured to use before treating that response as the complete input. Because the model's forecast-generation step produces a fluent, complete-looking output regardless of whether the underlying data was complete, the truncation is silently absorbed into the forecast rather than surfaced as a data-quality blocker.

**Example**
```
Demand-forecasting agent queries the POS feed for a SKU's trailing 26 weeks of sales history to run the standard forecast
Feed's batch load for the most recent 4 weeks was delayed and the feed returns only 22 weeks of rows, with no error code distinguishing this from a complete response
Agent proceeds to generate a forecast using the 22-week window as if it were the full 26-week lookback, producing a trend estimate skewed by the missing weeks
Re-querying the same feed two days later, after the delayed batch load completes, returns the full 26 weeks and produces a materially different trend estimate
Inventory plan built on the truncated-window forecast over- or under-orders the SKU until the next scheduled forecast run corrects it
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use error taxonomies for dialogue and agentic systems identify silent partial or truncated tool responses as a distinct failure category from explicit tool errors, since downstream reasoning treats both omission types identically unless the response is explicitly validated against the expected shape | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Surveys of LLM agent hallucination document that agents frequently complete a plausible, complete-looking output from an incomplete tool result rather than flagging the incompleteness, treating the absence of an explicit error as confirmation of completeness | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Research on LLM agents for supply chain management notes that forecast quality is highly sensitive to the completeness of the historical input window, with truncated windows producing systematically biased trend and seasonality estimates | [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597) |

**Contributing Factors**
- No validation step compares the row count or date range of a POS feed response against the lookback window the forecast configuration expects before the forecast run proceeds
- The POS feed's partial-batch-load condition returns HTTP 200 with a shorter-than-expected data set rather than a distinguishable error or warning code
- Forecast output format does not surface the actual date range of the input data used, so planners have no visible signal that the window was shorter than standard

---

## Mitigation Strategies

1. **Row-Count and Date-Range Validation Before Forecast Generation**: Require the agent to compare the returned date range and row count of any POS feed response against the configured lookback window, blocking the forecast run and surfacing a data-quality alert if the response is shorter than expected
2. **Explicit Partial-Response Signaling from the Feed**: Where feasible, modify the POS feed to return a distinguishable partial/incomplete flag when a batch load is delayed, rather than HTTP 200 with truncated rows indistinguishable from a complete response
3. **Visible Input-Window Disclosure on Forecast Output**: Require every forecast output to display the actual date range of the historical data used, making truncation visible to planners without requiring them to separately query the feed
4. **Automatic Forecast Re-Run on Delayed Batch Completion**: When a delayed POS batch load completes after a forecast run used a truncated window, automatically trigger a re-run and flag the prior forecast as superseded

### Metrics
- Rate of forecast runs where the input data's date range was shorter than the configured lookback window
- Mean and maximum trend-estimate delta between forecasts run on truncated versus subsequently completed full POS windows for the same SKU
- Rate of forecast outputs lacking an input-window disclosure

### Alerts
- A forecast run proceeds with an input date range shorter than the configured lookback window and no data-quality flag is raised → P1
- A delayed POS batch load completes after a forecast run used the truncated window, with no automatic re-run triggered → P2
- Truncated-input forecast rate across all SKUs exceeds the defined threshold for a rolling window → P3

---

## References

- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597)
