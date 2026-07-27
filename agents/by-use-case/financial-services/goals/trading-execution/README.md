# What Are the Most Common Trading Execution Failures in AI Agents?

**Trading execution failures occur when agents size, time, or route orders without modeling the actual cost and feasibility of execution, or when they misdiagnose what actually filled versus what was intended, leading to unintended positions, regulatory exposure (wash trades), and slippage that erodes or reverses the intended alpha.** Execution failures are often asymmetric in detection: an order fills at a worse price than estimated and the loss is diffuse (1-2 basis points times thousands of shares), while a major execution error (wrong instrument filled, wash-trade pattern, venue routing to a thin book) surfaces only in post-trade reconciliation hours later. Execution agents frequently optimize for a single dimension (best quoted price, lowest fees) without considering the full cost surface (fill probability, information leakage, slippage under realistic book depth, tax impact of forced liquidation).

## Key Takeaways

- 8 distinct failure patterns affect trading execution, spanning cost modeling (slippage underestimation, market-impact blindness, venue-selection blindness), execution validation (fill confirmation mismatch, wash-trade detection gap), and TCA/analytics (spurious causal narratives in slippage explanations).
- Slippage underestimation is very common: linear/static cost models underestimate realized cost by 2-4x for orders >1% of ADV in institutional execution data, because they assume order-book depth remains constant throughout the fill.
- Market-impact blindness is common on multi-account platforms: platform-wide aggregate order flow can exceed 15% of ADV, but routing agents treat each account's order independently, leading to self-inflicted impact that compounds unfavorably.
- Fill-confirmation mismatch (agent trusts a "filled" status without verifying the actual instrument/quantity/side matches the submitted request) is rare but extremely high-severity: downstream position systems inherit the wrong instrument or quantity, and the discrepancy is discovered only during end-of-day reconciliation.

## Scope

- **Cost Modeling and Market-Impact Blind Spots** — [slippage-underestimation](failures/slippage-underestimation.md), [market-impact-blindness](failures/market-impact-blindness.md), [venue-selection-blindness](failures/venue-selection-blindness.md). Cost models assume constant liquidity, ignore platform-wide footprints, select venues by quoted price alone without considering realized fill probability.
- **Execution Validation Gaps** — [fill-confirmation-status-trusted-without-diffing](failures/fill-confirmation-status-trusted-without-diffing-against-submitted-order-intent.md), [wash-trade-detection-gap](failures/wash-trade-detection-gap.md). Order confirmations trusted at status level without field-by-field verification; offsetting orders across related accounts not cross-checked.
- **Execution Benchmarking and Analysis Mismatches** — [embedding-retrieval-selects-wrong-historical-benchmark](failures/embedding-retrieval-selects-wrong-historical-benchmark-order-for-tca-comparison.md), [spurious-causal-narrative-from-coincident-news](failures/spurious-causal-narrative-from-coincident-news-event-in-slippage-explanation.md). Historical-comparable selection via text similarity produces mismatched benchmarks; TCA narratives attribute slippage to news events unrelated to the instrument's actual price movement.
- **Multi-Agent Risk Handoff Gaps** — [multi-agent-handoff-drops-risk-limit-breach-flag](failures/multi-agent-handoff-drops-risk-limit-breach-flag-between-pre-trade-risk-agent-and-execution-agent.md). Pre-trade risk agent flags marginal-breach scenarios in free text; execution agent receives only pass/fail status and routes the order without escalation.

## When Trading Execution Matters

- Execution agents route or size orders autonomously or with minimal human review, where execution error directly translates to unintended positions or regulatory exposure
- Multiple strategies or accounts send orders concurrently to the same markets, creating platform-level aggregate footprints invisible to individual execution agents
- Post-trade analytics narratives influence future execution decisions or risk management behavior: spurious causal claims propagate as if validated, affecting strategy design

## Cross-Pattern Insight

All 8 trading-execution patterns share a common root mechanism: execution agents are optimized for a single observable dimension (quoted price, status response, narrative plausibility) while remaining blind to the full cost surface or actual execution outcome. Slippage models use historical ADV but ignore current order-book depth and time-of-day liquidity seasonality. Market-impact models assume single-order isolation without visibility into platform-wide aggregate flow. Venue selection ranks by quote quality without measuring realized fill probability or information leakage. Fill validation checks status without diffing actual fields. TCA narratives are generated fluently without grounding in the execution log's actual decision factors. The reliable fix is architectural: (1) replace static cost models with real-time, order-book-aware impact estimation, (2) implement platform-level flow aggregation and netting before routing, (3) require field-by-field reconciliation of confirmations against orders before any completion narration, (4) ground TCA narratives in execution logs, not free-form market-event correlation, (5) block execution on any pre-trade risk scenario flag with mandatory escalation rather than treating scenarios as advisory.

## Frequently Asked Questions

### Can a better slippage model fix underestimation without changing how orders are sized and timed?

Partially. Better models (order-book-aware, time-of-day aware, size-sensitive) reduce underestimation from 2-4x down toward 1.5-2x. But the fundamental issue is that slippage is nonlinear: a 2% order experiences disproportionately higher impact than two 1% orders spread over time. No model fixes this without changing behavior: implement dynamic order slicing (size child orders based on live book depth), stagger orders across time windows, and consider dark pools or internal crossing for large trades.

### What is the minimum pre-trade check needed to catch market-impact blindness on a multi-account platform?

Compute platform-wide aggregate order flow per instrument before approving any individual order. Alert if the aggregate flow for a single instrument exceeds defined thresholds (5% of ADV, or 1 million shares in 15 minutes). For flow exceeding threshold, implement: (1) order netting (cancel offsetting orders), (2) staggered execution scheduling (spread orders over hours), (3) venue diversification (do not concentrate on single venue). Track realized aggregate impact vs. model's single-order estimate and feed back into sizing logic.

### How do you distinguish a genuine fill confirmation from a partial-success or symbol-collision error without manual review?

Implement mandatory field-level diff: before narrating an order as "executed successfully," verify that every material field in the confirmation payload (symbol, quantity, side, price) matches the originally submitted request. Use a canonical security master (not string equality) for symbol matching to catch venue-side reused tickers. If any field diverges, route to manual review and do not update position records until the divergence is resolved.

### Can better TCA narrative generation fix spurious-causal-narrative hallucinations if trained on more execution-log examples?

Not without structural change. The issue is not data coverage but the fundamental mismatch between TCA narrative generation (a free-form language model task) and execution-log grounding (a deterministic lookup task). Require TCA narratives to: (1) cite only factors present in the execution algorithm's own logged decision factors, (2) label any market-context claim with independent evidence (did the instrument's spread/volume actually move during the event?), (3) present the execution log's structured factors as the primary explanation, not as supporting detail.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Slippage Underestimation](failures/slippage-underestimation.md) | Cost models linear/static; realized slippage 2-4x estimate for orders >1% ADV |
| [Market-Impact Blindness](failures/market-impact-blindness.md) | Multi-account platform aggregate flow 15% of ADV; execution agents unaware; self-inflicted impact compounds |
| [Venue-Selection Blindness](failures/venue-selection-blindness.md) | Routing selects best-quoted venue; ignores realized fill probability and information leakage |
| [Fill-Confirmation Status Trusted Without Diffing](failures/fill-confirmation-status-trusted-without-diffing-against-submitted-order-intent.md) | Confirmation status "filled" trusted; actual instrument/quantity/side differs; position system corrupted |
| [Embedding Retrieval Selects Wrong Historical Benchmark](failures/embedding-retrieval-selects-wrong-historical-benchmark-order-for-tca-comparison.md) | TCA historical comparable via text similarity; differs in size/liquidity regime; benchmark cost wrong |
| [Spurious Causal Narrative in Slippage Explanation](failures/spurious-causal-narrative-from-coincident-news-event-in-slippage-explanation.md) | TCA narrative attributes slippage to news event; news unrelated to actual instrument movement; narrative artifact |
| [Multi-Agent Handoff Drops Risk-Limit-Breach Flag](failures/multi-agent-handoff-drops-risk-limit-breach-flag-between-pre-trade-risk-agent-and-execution-agent.md) | Pre-trade risk flags marginal-breach scenario; execution agent receives only pass/fail, routes order |
| [Wash-Trade Detection Gap](failures/wash-trade-detection-gap.md) | Multi-strategy execution; offsetting buy/sell orders cross without pre-trade detection; regulatory exposure |

**Total: 8 patterns**

## Related Goals

- [Portfolio Recommendation Accuracy](../portfolio-recommendation-accuracy/) — execution quality and slippage erode alpha generated by portfolio recommendations
- [Market Data Freshness](../market-data-freshness/) — stale prices directly affect execution cost estimation and venue routing decisions
