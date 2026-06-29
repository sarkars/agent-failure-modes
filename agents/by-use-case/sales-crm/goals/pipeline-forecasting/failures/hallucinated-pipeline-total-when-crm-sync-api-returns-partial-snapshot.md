# Hallucinated Pipeline Total When CRM Sync API Returns Partial Snapshot

## Issue: A Pipeline-Forecasting Agent Reports a Complete Quarterly Pipeline Total When the CRM-Sync API Call Underlying That Total Timed Out Partway Through Pulling Open Opportunities, Returning Only a Subset of Records That the Agent Treats as the Full Pipeline Instead of Flagging the Sync as Incomplete

**Frequency**: Common

**Symptoms**
- A forecasting agent reports "Q3 pipeline: $4.2M across 38 open opportunities" in a forecast summary, but the CRM-sync API call underlying that figure returned only 38 of the account's actual ~55 open opportunities before timing out on a paginated request
- The forecasting agent's summary presents the partial pull as the complete pipeline, with no indication that the sync was cut off mid-pagination
- Asking the agent to show its source for the total surfaces a raw API response with a pagination cursor indicating more records were available, which the agent's summary did not follow or flag
- The miss concentrates on forecasting runs during periods of CRM API load (end-of-quarter, when many systems are querying simultaneously), since that is when partial-pagination timeouts are most likely
- Re-running the same pull later, once the API is no longer under load, returns the full opportunity set and a materially different, usually higher, pipeline total

**Root Cause**
The forecasting agent's summarization step composes a single pipeline-total figure from whatever opportunity records the CRM-sync API returned, without checking whether the API's pagination cursor indicated additional records remained unretrieved. Because a partial paginated pull and a complete pull both return a populated, well-formed list of opportunity records, the agent's natural-language summarization treats the partial list as the full pipeline rather than treating an unresolved pagination cursor as a hard stop requiring a retry before the total is reported.

**Example**
```
Sales-ops requests Q3 pipeline forecast from the forecasting agent during the last week of the quarter, a period of heavy CRM API load
Forecasting agent calls the CRM-sync API to pull all open opportunities; the API returns the first page of 38 records along with a pagination cursor for additional pages, then the connection times out before the next page is requested
Forecasting agent generates the forecast summary using only the 38 records it received: "Q3 pipeline: $4.2M across 38 open opportunities"
17 additional open opportunities worth roughly $1.8M, including several large late-stage deals, were never retrieved
Leadership makes resourcing and discounting decisions for the quarter based on a pipeline total that is missing more than 30% of actual open opportunities
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use agents frequently fail to distinguish a tool call that returned a partial or paginated result from one that returned a complete result, producing confident downstream summaries from incomplete data | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Surveys of LLM agent hallucination identify completion of plausible aggregate values from incomplete tool or retrieval output as a distinct and recurring failure category | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Agentic CRM and sales-workflow research notes that pipeline aggregation tasks are sensitive to incomplete data pulls from CRM sync APIs, particularly during high-load periods such as quarter-end | [CRMWeaver: Building Powerful Business Agent via Agentic RL and Shared Memories](https://arxiv.org/pdf/2510.25333) |

**Contributing Factors**
- The CRM-sync API's paginated response format does not force the calling agent to check for a remaining pagination cursor before treating the returned records as the complete set
- No mandatory rule requires the forecasting agent to confirm full pagination completion before generating a final pipeline-total summary
- Quarter-end forecasting runs, when the API is under the highest load and most likely to time out mid-pagination, are not flagged for a stricter completion check despite being the highest-stakes forecasting period

---

## Mitigation Strategies

1. **Pagination Completion Gate**: Require the agent to confirm the CRM-sync API's pagination cursor is exhausted (no further pages) before generating any pipeline-total summary; treat an unresolved cursor as blocking, not as defaulting to "complete"
2. **Structural Distinction Between Partial and Complete Pulls**: Modify the CRM-sync integration so a partial or timed-out paginated pull is surfaced to the agent as a distinct status that cannot be summarized as a complete pipeline total
3. **Mandatory Retry on Pagination Timeout**: Automatically retry any timed-out pagination request, with a capped retry count, before allowing the forecasting workflow to proceed to a final total
4. **Quarter-End Load Flagging**: Route forecasting runs during known high-load periods (quarter-end) through a stricter completion check given their higher likelihood of triggering a partial pull

### Metrics
- Rate of "pipeline total" summaries later found, on audit, to have been generated from a CRM-sync pull with an unresolved pagination cursor at the time of generation
- Average time-to-completion for full pipeline pulls, broken out by whether pagination completed on the first attempt or required retry
- Rate of CRM-sync API responses with an unresolved pagination cursor, by time period

### Alerts
- A pipeline-total summary is generated while the underlying CRM-sync pull still shows an unresolved pagination cursor → P1
- A forecast is delivered to leadership with a known-incomplete pipeline pull on record → P1
- Partial-pagination rate from the CRM-sync API exceeds the defined threshold for a rolling window → P3

---

## References

- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [CRMWeaver: Building Powerful Business Agent via Agentic RL and Shared Memories](https://arxiv.org/pdf/2510.25333)
