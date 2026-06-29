# Unvalidated Paginated Price-Feed Response Treated as Full Instrument Universe

## Issue: A Market-Data Freshness-Monitoring Agent Calling a Vendor API to Pull Current Prices Across a Portfolio's Full Instrument Universe Receives a Page- or Length-Capped Response Covering Only Part of the Requested Universe, and Proceeds to Generate a Portfolio-Wide Freshness Report Treating the Returned Subset as if It Were the Complete Set of Instruments, Without Checking the Response for a Continuation Token or Returned-Count-Versus-Requested-Count Mismatch

**Frequency**: Common

**Symptoms**
- Freshness report states "all portfolio instruments checked, no stale prices detected" while a material portion of the portfolio's instruments were never actually returned by the underlying API call
- The vendor API response includes a returned-count field or continuation token indicating fewer records came back than the number requested, but the agent's report generation does not check for or surface this discrepancy
- Instruments omitted from the truncated response are silently absent from the freshness report rather than being flagged as "not checked," so downstream consumers cannot distinguish "checked and fresh" from "never actually checked"
- Re-running the identical API call with explicit pagination handling (following every continuation token and reconciling returned count against requested count) surfaces the missing instruments, some of which turn out to have genuinely stale or stalled prices
- The failure recurs specifically on large or recently-expanded portfolios, since those are the cases most likely to exceed a single page or length-capped response from the vendor API

**Example**
```
Freshness-monitoring agent is asked to confirm price currency across a portfolio of 1,200 instruments ahead of end-of-day valuation
Agent calls the vendor's batch price API requesting all 1,200 instruments; the API returns prices for only the first 1,000 due to a per-call response-size cap, along with a "returned: 1000, requested: 1200" field and a continuation token
Agent's freshness report, generated directly from the 1,000 returned prices, states "all portfolio instruments checked; no stale prices detected" -- the 200 omitted instruments are simply absent, not flagged as unchecked
One of the 200 omitted instruments has in fact had a stalled feed for three days; because it was never actually retrieved in this check, the stale price it already holds in the valuation system is carried forward into end-of-day NAV without any freshness review
Discrepancy is discovered only when a portfolio manager manually notices the instrument's price has not moved in three trading sessions, well after the freshness report had already certified the portfolio as fully checked
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM agents frequently assert task completion (here, "all instruments checked") based on the apparent shape of a returned result rather than verifying the result reflects the complete requested scope, a pattern documented as false success driven by surface-level closing signals rather than ground-truth verification | [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/html/2606.09863) |
| Tool-use error detection research finds agents frequently fail to treat an incomplete, capped, or paginated tool result as a distinct error condition requiring follow-up, instead generating output as if a complete result had been returned | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Agent-environment interaction failure research documents that agents frequently act on a tool's returned result without verifying it matches the scope of the original request, treating any successful API call as evidence of task completion regardless of completeness | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |

**Contributing Factors**
- No explicit instruction or guardrail requires the agent to check a price-feed API response's returned-count against the requested-count, or to follow a continuation token to exhaustion, before generating a portfolio-wide freshness conclusion
- Large or recently-expanded portfolios are exactly the cases most likely to need a full freshness check and also the cases most likely to exceed a single page of vendor API results, compounding the risk
- The freshness report's output format has no field distinguishing "checked and fresh" from "not actually returned by the API call," so an omitted instrument is indistinguishable from a confirmed-fresh one
- Pagination-handling logic for vendor price APIs is treated as a generic engineering concern rather than a valuation-accuracy-critical control, so it is not consistently enforced across every feed integration

---

## Mitigation Strategies

1. **Mandatory Returned-Count Reconciliation**: Require the agent to compare the number of instruments actually returned by any batch price-feed call against the number requested, and treat any mismatch as a hard stop requiring further pagination before a freshness conclusion is generated
2. **Explicit Not-Checked Status**: Require the freshness report to list every requested instrument with an explicit status of "fresh," "stale," or "not checked," rather than silently omitting instruments the API call failed to return
3. **Pagination-to-Exhaustion Requirement**: Require the agent to follow every continuation token to exhaustion before generating any portfolio-wide freshness or valuation-readiness conclusion
4. **Pre-Valuation Completeness Gate**: Block end-of-day valuation from proceeding on any portfolio for which the most recent freshness check did not confirm 100% of the instrument universe was actually returned and checked

### Metrics
- Rate of freshness reports where the number of instruments checked does not match the number actually held in the portfolio
- Number of "all instruments checked" reports later found to have omitted instruments due to unaddressed API pagination or response-size caps
- Percentage of batch price-feed calls that included an explicit returned-count-versus-requested-count reconciliation

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Returned-count mismatch | Batch price-feed API response's returned count is less than the requested count with no evidence of follow-up pagination | P1 | Block freshness report finalization; re-query to completion |
| Freshness report omits portfolio instruments | Number of instruments in the freshness report is less than the portfolio's full instrument count | P1 | Treat report as incomplete; halt downstream valuation reliance until reconciled |
| Recurring truncation on same vendor feed | Multiple unaddressed pagination/truncation events traced to the same vendor API integration | P2 | Audit and fix pagination handling for that integration |

---

## References

- [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/html/2606.09863)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
