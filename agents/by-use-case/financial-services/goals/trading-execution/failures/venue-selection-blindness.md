# Venue Selection Blindness

## Issue: Agent Routes Orders to the Venue With the Best Quoted Price Without Accounting for Realistic Fill Probability, Rebate Structure, or Information Leakage Risk at That Venue

**Frequency**: Common

**Symptoms**
- Order routing agent selects the venue showing the best displayed price, but that price is frequently unavailable by the time the order arrives (low realized fill rate at the quoted price)
- Maker/taker rebate and fee differences across venues are not incorporated into the effective execution cost comparison, only the headline price
- Routing repeatedly sends large orders to venues with higher information leakage risk (e.g., visible order book depth signaling), resulting in adverse price movement before the full order is filled
- Post-trade execution quality analysis shows persistent negative slippage concentrated in specific venues that the routing logic continues to favor based on pre-trade quoted price alone

**Root Cause**
Venue selection logic that ranks venues purely by displayed/quoted price treats the quote as if it were a guaranteed, static execution price, when in reality realized execution quality depends on fill probability, latency to the venue, fee/rebate structure, and the venue's typical information leakage characteristics for orders of the relevant size. An agent optimizing for quoted price alone is optimizing a proxy that diverges from actual realized execution cost, particularly for larger orders where leakage and fill-probability effects dominate the headline price difference.

**Example**
```
Scenario: Large equity order routed to Venue A, which shows the best displayed price for a small top-of-book quantity
Realized outcome: Only 15% of the order fills at the quoted price before the quote moves against the order; remainder fills at progressively worse prices
Venue B: Slightly worse quoted price but historically much higher fill rate and lower information leakage for orders of this size
Routing logic: Selected Venue A based on quoted price alone
Impact: Realized execution cost (including slippage) ends up worse than if Venue B had been selected
```

**Key Statistics**
- Standard-benchmark evaluation research on LLM-based financial agents identifies execution-quality blind spots (focusing on headline metrics rather than realized outcomes) as an overlooked risk category in agentic trading systems
- Realized fill rate and information leakage are consistently identified in market microstructure research as material drivers of execution cost that diverge from quoted price, especially for larger orders
- Reliability evaluations of LLM-based trading agents note a gap between agents' stated execution rationale and their actual realized performance, underscoring the need for outcome-grounded (not quote-grounded) routing evaluation

---

## Mitigation Strategies

1. **Realized-Outcome-Based Venue Scoring**: Score venues on historical realized fill rate and effective execution cost (including fees/rebates and slippage) for orders of comparable size, not displayed quoted price alone
2. **Order-Size-Aware Leakage Modeling**: Incorporate venue-specific information leakage characteristics, especially for large orders, into the routing decision rather than treating all venues as equivalent beyond price
3. **Post-Trade Execution Quality Feedback Loop**: Continuously feed realized execution quality data back into the venue scoring model so routing adapts to actual, not assumed, venue performance
4. **Smart Order Splitting**: For large orders, split execution across multiple venues weighted by realized fill probability rather than concentrating on the single best-quoted venue

### Metrics
- Realized slippage vs. quoted price at time of routing decision, broken down by venue
- Fill rate at quoted price, by venue and order size bucket
- Effective execution cost (price + fees - rebates + slippage) by venue, compared against the routing decision's expected cost

### Alerts
- Realized fill rate at a venue falls below a defined threshold for orders above a size cutoff → P2
- Effective execution cost for a venue persistently exceeds the routing model's expectation by a defined margin → P1

---

## References

- [Position: Standard Benchmarks Fail – LLM Agents Present Overlooked Risks](https://www.arxiv.org/pdf/2502.15865v1)
- [TradeTrap: Are LLM-based Trading Agents Truly Reliable and Faithful?](https://arxiv.org/html/2512.02261v1)
