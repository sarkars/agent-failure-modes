# Multi-Agent Handoff Drops Stale-Feed Flag Between Ingestion Agent and Valuation Agent

## Issue: A Market-Data Ingestion Agent Notes in Free Text That a Price Feed Showed No Update Across an Unusually Long Window and May Be Stale, but the Structured Price Record Handed Off to the Downstream Valuation Agent Has No Field for Staleness Suspicion, So the Valuation Agent Treats the Last Received Price as Current

**Frequency**: Common

**Symptoms**
- A position's valuation uses a price the ingestion agent's own notes flagged as suspiciously unchanged across an unusually long window, with no staleness field carried into the structured price record consumed by the valuation agent
- The structured handoff between ingestion and valuation agents contains only the last price and its nominal timestamp, with no field for a staleness suspicion the ingestion agent's free-text monitoring notes raised about that same price
- Valuation agents operating purely from the structured price record show a materially higher reliance rate on suspected-stale prices than valuation agents given the ingestion agent's full monitoring transcript alongside the record
- The staleness is discovered only when a separate reference feed or end-of-day reconciliation shows the price should have moved, by which point the valuation has already been published or used in a risk calculation
- The mismatch concentrates on lower-liquidity instruments and after-hours windows, where an unchanged price is more likely to be genuinely stale rather than a genuinely flat market, and where the ingestion agent's staleness suspicion is least likely to be cross-checked downstream

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

1. **Add a Staleness-Suspicion Field to the Handoff Schema**: Require the ingestion agent to record a staleness-suspicion flag, with the basis for it (consecutive unchanged updates, elapsed time since last genuine tick), in a dedicated structured field passed to the valuation agent, rather than leaving it only in free-text monitoring notes
2. **Valuation Agent Cross-Checks Ingestion Transcript for Staleness Language**: Require the valuation agent to scan the ingestion agent's free-text monitoring notes for staleness-suspicion language before using a price with full confidence, not just the structured price-and-timestamp field
3. **Mandatory Independent-Feed Check on Flagged Staleness**: Automatically route any price carrying a staleness-suspicion flag to an independent reference-feed check before it is used in a published valuation, rather than allowing the original feed's last price to pass through unchallenged
4. **Track Staleness-Field-Absent Valuation Rate**: Continuously measure how often a price the ingestion agent's monitoring flagged as suspect is nonetheless used in a valuation with no staleness field carried through the handoff

### Metrics
- Rate of valuations that consumed a price whose ingestion transcript contained staleness-suspicion language not reflected in a structured staleness field
- Time between a flagged staleness suspicion and an independent-feed confirmation or refutation of it
- Valuation reliance rate on flagged-stale prices, segmented by presence vs. absence of a structured staleness field in the handoff

### Alerts
- A published valuation uses a price whose ingestion transcript contains unresolved staleness-suspicion language with no structured staleness flag → P1
- An independent-feed check confirms a price flagged as suspect was in fact stale and already used in a published valuation → P1
- Staleness-field-absent valuation rate across a rolling window exceeds the defined threshold → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
