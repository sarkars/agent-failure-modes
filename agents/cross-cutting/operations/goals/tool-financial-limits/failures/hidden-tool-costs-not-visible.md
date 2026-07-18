# Hidden Tool Costs Not Visible

## Issue
An agent calls a tool whose advertised, per-call price is small or fixed, but the tool internally fans out to other billable services to fulfill the request — a "web search" call that triggers a paid image-recognition pass on every result thumbnail, or a "document lookup" that silently invokes an OCR sub-API for scanned PDFs. The agent's cost tracker only sees the price of the outer call, so its running budget total is systematically wrong, and the discrepancy is invisible until the vendor's actual invoice includes line items the agent never logged.

**Frequency**: Common

**Symptoms**
- Agent-tracked cumulative spend is consistently lower than the vendor invoice, by a roughly constant multiplier
- Vendor billing statements contain line items (sub-API calls, enrichment passes) that never appear in the agent's own cost log
- The same nominal tool call costs different real amounts depending on input content (e.g. a search with image-heavy results costs more than a text-only search) with no corresponding difference in what the agent recorded
- Budget alerts based on the agent's internal tracker never fire even though real spend is over cap
- Vendor support tickets/contract clauses reference "composite" or "bundled" operations that aren't documented in the primary API reference the integration was built against

## Root Cause
Cost estimation in agent tool wrappers is almost always based on the documented price of the endpoint being called directly, because that's the only cost information exposed in the API contract the integration was built against. When a vendor implements a tool as an orchestration layer over other paid services — often for reasons unrelated to the agent's use case, such as reusing an internal enrichment pipeline — those downstream costs are absorbed into the vendor's own margin calculation and only surfaced in aggregate billing, not in the per-call response the agent's cost tracker reads.

## Example
```
An agent uses "WebSearchPro" at an advertised $0.01/query. Its cost
tracker increments $0.01 per call and halts calls once cumulative spend
hits a $5.00/day cap, expecting roughly 500 calls/day.

Unknown to the agent, WebSearchPro runs a paid third-party image-safety
classifier ($0.03) on every result page that contains an image, and a
paid entity-resolution lookup ($0.02) whenever a result mentions a named
organization — both invisible in the search API's response payload and
undocumented in the primary API reference.

After 200 calls (well under the modeled 500-call cap), the agent's tracker
shows $2.00 spent, but the real vendor-side cost is already $9.40 because
most of the day's queries returned image-heavy, entity-rich results. The
$5.00 cap is breached in vendor billing while the agent's own dashboard
still shows 60% of budget remaining.
```

## Statistics
| Finding | Context |
|---------|---------|
| Composite/orchestrated API products carry 1.5-4x the effective cost of their advertised base price when downstream fan-out is included | Typical range reported across vendor billing reconciliation exercises |
| Agent-tracked cost estimates diverge from actual vendor invoices by more than 20% in a meaningful share of integrations that wrap multi-stage or "smart" API products | Commonly observed in production cost audits |
| Detection of hidden fan-out costs typically happens only at invoice reconciliation, a lag of days to weeks after the spend occurred | Typical range |

## Mitigations
1. **Invoice-based cost calibration**: Periodically reconcile the agent's internal per-call cost model against actual vendor invoices, and adjust the modeled per-call cost upward (or apply a safety multiplier) whenever a persistent gap is detected.
2. **Contract and billing-doc review beyond the API reference**: Have engineering read the vendor's billing schedule and terms of service, not just the API reference docs, since fan-out charges are often disclosed only in billing documentation.
3. **Conservative cost multiplier for orchestration-style tools**: For any tool whose response could plausibly trigger sub-calls (image processing, enrichment, entity resolution), apply a padding factor (e.g. 2-3x the advertised price) to the internal cost tracker until real costs are measured.
4. **Vendor cost-attribution API where available**: Prefer vendors that expose actual per-call cost in the response payload (many do, as a line item like `billed_amount`) and use that value directly instead of a static price table.
5. **Sampling audit**: Regularly sample a subset of calls and cross-reference their reported cost against the vendor's billing API or statement to catch model drift early rather than at monthly invoice time.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| modeled_vs_actual_cost_ratio | Ratio of agent-tracked cumulative cost to actual vendor-reported/invoiced cost for the same period | Alert if ratio < 0.85 |
| unattributed_billing_line_items | Count of vendor invoice line items with no corresponding entry in the agent's cost log | Alert if > 0 recurring monthly |
| per_call_cost_variance | Standard deviation of actual per-call cost for a nominally fixed-price tool | Alert if variance exceeds 2x the advertised base price |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Invoice/tracker divergence | modeled_vs_actual_cost_ratio falls below 0.85 for two consecutive billing periods | High | Freeze further budget increases, initiate vendor billing review, recalibrate cost model |
| Undocumented line item detected | A new billing line item appears with no mapped internal cost category | Medium | Route to integration owner to update the cost model and confirm with vendor |

## Related Patterns
- [Per-Tool Cost-Per-Operation Surprise](./per-tool-cost-per-operation-surprise.md) - both involve the agent's cost model failing to predict true call cost, one from payload variation and one from hidden fan-out
- [Per-Tool Tiered Pricing Unknown](./per-tool-tiered-pricing-unknown.md) - another case of the agent lacking visibility into the vendor's true pricing mechanics
- [Per-Tool Monthly Budget Overrun](./per-tool-monthly-budget-overrun.md) - hidden costs are a common root cause of the reporting-lag overrun described there
