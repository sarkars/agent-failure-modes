# Multi-Agent Handoff Drops Stale-Feed Flag Between Ingestion Agent and Valuation Agent

## Issue: A Market-Data Ingestion Agent Notes in Free Text That a Price Feed Showed No Update Across an Unusually Long Window and May Be Stale, but the Structured Price Record Handed Off to the Downstream Valuation Agent Has No Field for Staleness Suspicion, So the Valuation Agent Treats the Last Received Price as Current

**Frequency**: Common

**Symptoms**
- A position's valuation uses a price the ingestion agent's own notes flagged as suspiciously unchanged across an unusually long window, with no staleness field carried into the structured price record consumed by the valuation agent
- The structured handoff between ingestion and valuation agents contains only the last price and its nominal timestamp, with no field for a staleness suspicion the ingestion agent's free-text monitoring notes raised about that same price
- Valuation agents operating purely from the structured price record show a materially higher reliance rate on suspected-stale prices than valuation agents given the ingestion agent's full monitoring transcript alongside the record
- The staleness is discovered only when a separate reference feed or end-of-day reconciliation shows the price should have moved, by which point the valuation has already been published or used in a risk calculation
- Lower-liquidity instruments and after-hours windows account for a disproportionate share of the misses, since an unchanged price there is more plausibly a genuinely stale feed than a genuinely flat market, yet those are exactly the cases least likely to get a downstream cross-check

**Root Cause**
The valuation agent's pricing logic consumes only the structured price record produced by the ingestion stage, and that record was built to carry the latest price and timestamp, not whether the ingestion agent's own monitoring flagged the feed as suspiciously unchanged. Because a staleness suspicion is expressed through the ingestion agent's free-text monitoring notes rather than a structured staleness field, it has no corresponding place in the handoff schema and is therefore invisible to the valuation agent, even though the same model, given the ingestion transcript, would readily flag the price as suspect.

**Example**
```
Market-data ingestion agent monitors a thinly traded corporate bond's price feed and notes in free text: "Price unchanged for 14 consecutive updates over 6 hours during active trading hours -- unusual for this instrument, possible feed staleness"
Ingestion agent passes the structured price record to the valuation pipeline showing the last price and its nominal timestamp, with no staleness field
Valuation agent consumes the structured record, treats the price as current, and publishes the day's mark using it
Independent reference feed, checked during a later reconciliation, shows the bond actually traded twice during the unchanged window at materially different prices
Published mark is found to be stale, triggering a restatement and a review of risk exposure calculated off the incorrect valuation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of multi-agent LLM system failures identify narrow handoff interfaces between staged agents, where a downstream agent's structured input omits a signal an upstream agent's free-text monitoring surfaced, as a distinct and recurring failure category | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Platform-orchestrated agentic workflow failure studies find that narrowing the interface between orchestrated stages to a fixed value-plus-timestamp schema is a primary mechanism by which a staleness or data-quality signal present upstream fails to reach a downstream consuming stage | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |
| Research on agentic trading systems identifies the absence of a shared, continuously synced structured state between data-ingestion and valuation stages as a distinct reliability gap from either stage's individual pricing accuracy | [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337) |

**Contributing Factors**
- Structured price-record schema tracks only last price and nominal timestamp, with no field for a staleness suspicion raised during ingestion monitoring
- Ingestion agent's staleness monitoring output is recorded only in free-text notes, with no structured escalation path into the valuation agent's input
- No mandatory hold or flag is triggered in the valuation pipeline when the ingestion agent's free-text notes contain staleness-suspicion language, since the valuation agent's logic does not parse those notes

---

## Mitigation Strategies

### Prevention

1. **Staleness-suspicion field in the price-record handoff schema**: Extend the structured price record passed from ingestion to valuation to include `staleness_suspected: bool`, `unchanged_update_count: int`, and `unchanged_window_seconds: int`. Require the ingestion agent to populate these fields whenever its own monitoring logic detects an unusually long unchanged run for that instrument's typical update cadence, rather than leaving the observation in free-text notes only. Root cause: gives the staleness signal a structured home so it cannot be dropped simply because it originated as a narrative observation.

2. **Instrument-cadence-aware staleness threshold, not a single global timeout**: Compute an expected update-frequency baseline per instrument (or liquidity tier) from historical feed behavior, and flag staleness relative to that baseline rather than a single fixed timeout that works for liquid names but under-triggers for thin ones. Root cause: a flat "no update in N minutes" threshold misses exactly the lower-liquidity instruments where staleness is both more likely and most consequential.

3. **Valuation-agent read of the staleness field before publishing a mark**: Require the valuation agent to check `staleness_suspected` before treating a price as current; if set, either fall back to a secondary reference feed or hold the mark and route it to a human trader/quant for confirmation rather than publishing silently. Root cause: closes the gap where a downstream agent has no incentive to look past the fields its own logic already consumes.

### Detection & Response

1. **Ingestion-note-to-schema reconciliation audit**: Periodically scan the ingestion agent's free-text monitoring notes for staleness language ("unchanged for", "no update since", "possible feed staleness") and cross-check that the corresponding structured price record has `staleness_suspected` set. Flag and log any mismatch as a handoff gap, independent of whether the price later proves to have actually been stale.

2. **Post-publication staleness reconciliation**: On a rolling basis, compare published marks against an independent reference feed or end-of-day settlement price for the same instrument; where the published mark diverges materially and the instrument had an unusually long unchanged run at publication time, trace back to whether the ingestion agent's monitoring had already raised (but failed to propagate) the suspicion.

### Architecture Patterns

1. **Structured Staleness-Aware Price Record**: Price record schema carries `last_price`, `last_update_ts`, `staleness_suspected`, `unchanged_update_count`, and `source_feed_id` as first-class fields populated at ingestion time, not derived downstream from a raw timestamp diff.

2. **Cadence-Baseline Service**: A per-instrument (or per-liquidity-tier) expected-update-frequency baseline, refreshed periodically from historical feed behavior, that the ingestion agent's staleness check is computed against instead of a single global timeout.

3. **Valuation Fallback Gate**: Valuation pipeline step that checks `staleness_suspected` before using a price; on a flagged price, either substitutes a secondary reference feed or blocks the mark pending human confirmation, with the block/substitution logged for audit.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Staleness-Field Population Rate | 100% | <98% | # of ingestion records where free-text notes contain staleness language and `staleness_suspected` is set / total records with staleness language in notes |
| Valuation Fallback Trigger Rate | tracked, no fixed target | sustained spike vs. trailing baseline | # of marks where valuation agent triggered a fallback or hold due to `staleness_suspected` / total marks published |
| Post-Publication Staleness Miss Rate | 0% | >0.2% | # of published marks later found stale via reconciliation with no prior `staleness_suspected` flag / total published marks |
| Cadence-Baseline Freshness | <24h stale | >72h stale | Time since a given instrument's expected-update-frequency baseline was last recomputed |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Staleness Note Not Reflected in Schema | Ingestion notes contain staleness language but `staleness_suspected` is unset in the handed-off price record | P1 | Block record from valuation consumption; escalate to data-ops for manual staleness determination |
| Mark Published on Suspected-Stale Price | Valuation agent publishes a mark despite `staleness_suspected` being set | P1 | Recall/flag the mark; require secondary-feed confirmation before republishing |
| Post-Publication Reconciliation Miss | Reconciliation finds a published mark was stale with no prior staleness flag anywhere in the pipeline | P2 | Investigate cadence-baseline accuracy for the affected instrument/tier; recompute baseline if systematically off |


## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
