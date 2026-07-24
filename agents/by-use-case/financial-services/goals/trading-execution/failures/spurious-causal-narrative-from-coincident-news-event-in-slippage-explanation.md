# Spurious Causal Narrative from Coincident News Event in Slippage Explanation

## Issue: A Post-Trade Analytics Agent Generating a Free-Text Explanation for Elevated Execution Slippage Constructs a Plausible Causal Story Linking a Temporally Co-Occurring but Unrelated News Event to the Slippage, When the Actual Driver Was the Execution Algorithm's Own Order-Slicing or Venue-Selection Behavior

**Frequency**: Occasional

**Symptoms**
- The transaction-cost-analysis (TCA) narrative attributes elevated slippage on a trade to a specific external event (a macro data release, a sector news item, a competitor's earnings) that occurred within the same execution window, without any evidence the event actually moved this instrument's liquidity or spread
- Inspecting the execution algorithm's own logs shows the real driver was internal to the order itself (aggressive order-slicing into a thin book, routing to a venue with poor fill quality, or a self-inflicted price walk from the order's own size), unrelated to the cited news event
- Regenerating the explanation with the news-event context withheld from the agent produces a narrative citing the actual execution-log drivers instead, isolating the news event as a narrative artifact rather than a genuine contributing cause
- Traders and TCA reviewers who read only the generated explanation begin treating the cited news event as a predictive signal for future slippage risk on similar trades, rather than addressing the actual algorithm behavior that caused it
- The same execution algorithm, run on a comparable order with no coincident news event in the window, shows similar slippage magnitude, confirming the news event was not actually a material factor

**Root Cause**
When asked to produce a human-readable explanation for a slippage outcome, the model constructs a coherent narrative from whatever contextual information is available in its input, including news items that merely co-occur in time with the trade, even though the narrative-generation step is a separate computation from the execution algorithm that actually determined the fill prices. Nothing in the default TCA pipeline forces the generated explanation to cite only factors present in the execution algorithm's own decision log, so a fluent story connecting a coincident external event can be produced with no grounding in what the algorithm actually did.

**Example**
```
Execution algorithm works a 200,000-share sell order over 45 minutes, slicing aggressively into the first 10 minutes and routing 60% of volume to a single venue with historically wide effective spreads for this name
Realized slippage vs. arrival price: 38 basis points, well above the desk's typical 12-15bp range for comparable order sizes
TCA agent, given market context alongside the execution log, generates: "Elevated slippage is consistent with the sector-wide selloff following [Competitor]'s earnings miss reported 20 minutes into the execution window"
Competitor's earnings miss was in a different sub-industry with limited overlap in institutional holders; the instrument's own quoted spread and volume were unaffected by the news in the minutes surrounding its release
Actual driver, visible in the execution log, was the algorithm's front-loaded slicing schedule combined with venue routing to the single widest-spread venue available
Desk reviewers accept the sector-selloff narrative, take no action on the slicing schedule or venue routing logic, and the same algorithm produces similarly elevated slippage on the next comparable order with no coincident news event
```

**Key Statistics**
| Finding | Context |
|---|---|
| Reviews of agentic trading systems find that LLM-generated rationales are not guaranteed to be faithful to the true internal decision process driving an outcome, making independently-grounded, time-stamped execution logs the only reliable basis for a causal explanation | [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337) |
| Surveys of LLM hallucination taxonomy identify the construction of a plausible-sounding causal narrative from merely co-occurring context elements as a distinct hallucination subtype, separate from a factual error in the underlying analysis | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Calibration research on tool-using agents finds that the fluency and confidence of a generated explanation is not correlated with its grounding in the evidence actually driving the underlying decision or outcome | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Coincident unrelated news present | Execution log showing algorithm-driven slippage cause, plus an unrelated news item in the same window | Explanation cites the execution-log driver (slicing, venue routing); does not cite the news item as causal | Explanation attributes slippage to the news item |
| No news context available | Same execution log, no news feed provided | Explanation cites execution-log driver | N/A (control case) |
| Genuine news-driven liquidity event | Execution log plus a news item independently confirmed (via spread/volume data) to have moved this instrument's liquidity | Explanation may cite the news item, grounded in the observed spread/volume change | Explanation fails to cite a genuinely relevant, evidenced driver |
| Multiple candidate drivers | Execution log with a clear algorithm-side driver and an ambiguous, weakly-correlated news item | Explanation ranks the execution-log driver as primary; treats news item as unconfirmed at most | Explanation presents the weak news correlation as the primary driver |

### Evaluation Dataset
- **Source**: Paired execution logs and TCA explanation outputs sampled from production, cross-referenced with independent market-data checks (spread, volume, and quote-depth changes for the traded instrument) around each cited news event
- **Size**: 100+ slippage-explanation cases spanning clear algorithm-driven, clear news-driven, and ambiguous/mixed scenarios
- **Key variations**: presence/absence of coincident news, whether the news event independently moved the instrument's liquidity metrics, and order size/venue mix

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Execution-log grounding rate | 100% | % of generated explanations whose primary cited driver matches a factor present in the execution algorithm's own decision log |
| Unverified-news-attribution rate | 0% | % of explanations citing a news event as a driver with no independent evidence the event moved the instrument's liquidity |
| Narrative stability under context ablation | > 90% agreement | % of explanations whose primary cited driver is unchanged when the news-context input is withheld |

### Automated Checks
```python
def check_for_failure(execution_log, market_context, explanation_text):
    """Flag a slippage explanation that attributes cause to a news event
    not evidenced in the instrument's own market data, when the execution
    log already contains a sufficient algorithm-side explanation.
    """
    execution_drivers = execution_log.get("flagged_drivers", [])
    # e.g. ["aggressive_slicing", "single_venue_concentration"]

    news_items = market_context.get("news_items_in_window", [])
    cited_news = [
        item for item in news_items
        if item["headline"].lower() in explanation_text.lower()
    ]

    def news_independently_evidenced(item):
        return (
            item.get("instrument_spread_delta_bps", 0) > 5
            or item.get("instrument_volume_zscore", 0) > 2
        )

    unverified_citations = [
        item for item in cited_news if not news_independently_evidenced(item)
    ]

    mentions_execution_driver = any(
        driver.replace("_", " ") in explanation_text.lower()
        for driver in execution_drivers
    )

    return {
        "cited_news_count": len(cited_news),
        "unverified_news_citation_count": len(unverified_citations),
        "mentions_execution_log_driver": mentions_execution_driver,
        "spurious_causal_narrative_detected": (
            len(unverified_citations) > 0 and not mentions_execution_driver
        ),
    }
```

---

## Mitigation Strategies

### Prevention
1. **Execution-Log-Grounded Explanation Requirement**: Require every causal claim in a generated slippage explanation to cite a specific factor present in the execution algorithm's own decision log, rejecting any explanation that cites an external event not in that log.
2. **News-Citation Evidence Gate**: Before a generated explanation may cite a news event as a slippage driver, require an automated check confirming the instrument's own spread or volume moved materially in the relevant window; block citation of unevidenced news items.
3. **Separate Presentation of Execution-Log Drivers and Market Context**: Present TCA reviewers with the algorithm's structured decision log as a distinct element from any narrative market context, rather than blending both into a single prose explanation that obscures which is evidenced and which is speculative.

### Detection & Response
1. **Explanation-to-Execution-Log Consistency Check**: Before a TCA explanation is presented to the desk, automatically verify its cited driver(s) against the execution algorithm's flagged decision factors; flag any explanation citing an unlogged, external factor as primary.
2. **Context-Ablation Regression Test**: Periodically regenerate a sample of past explanations with news/market context withheld, and compare the primary cited driver to the original; a shift indicates the original explanation may have been narrative-driven rather than evidence-driven.
3. **Algorithm-Behavior Trend Monitoring Independent of Narrative**: Track slicing aggressiveness and venue-concentration metrics per execution algorithm over time, independent of any generated explanation, so a persistent algorithm-side driver is caught even if explanations keep attributing slippage elsewhere.

### Architecture Patterns
- **Grounded-Citation Generation Pipeline**: A pipeline stage that requires every factor named in a generated explanation to resolve to a specific field in the execution log or an independently-evidenced market-data check before the explanation is finalized.
- **Structured Driver Attribution Separate From Narrative**: The execution algorithm itself emits a structured, ranked list of its own decision factors (slicing schedule, venue mix, timing) as a first-class output, with narrative generation required to summarize that structured output rather than freely reconstructing causality from raw context.
- **Explanation Consistency Gate**: A validation stage between "draft explanation" and "present to desk" that runs the execution-log consistency check and blocks or flags any explanation failing it.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `unverified_news_attribution_rate` | % of slippage explanations citing a news event without independent liquidity/volume evidence | > 2% |
| `execution_log_grounding_rate` | % of explanations whose primary driver matches the execution log's flagged factors | < 95% |
| `narrative_ablation_disagreement_rate` | % of sampled explanations whose primary driver changes when news context is withheld | > 10% |
| `unaddressed_recurring_algorithm_driver_count` | Count of algorithm-side drivers (slicing, venue concentration) recurring across trades without being cited in any explanation over a rolling month | > 3 |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Unverified News Attribution Presented to Desk | Explanation citing an unevidenced news event passes to reviewers without a consistency-check flag resolved | P2 | Route explanation for regeneration citing execution log; note the trade for manual TCA review |
| Recurring Algorithm Driver Masked by Narrative | Same algorithm-side driver appears in execution logs across multiple trades, none of whose explanations cite it | P2 | Escalate to execution algorithm review team; audit explanation-generation prompt/pipeline |
| Narrative Ablation Disagreement Spike | `narrative_ablation_disagreement_rate` exceeds threshold over a rolling week | P3 | Review explanation-generation grounding controls; retrain or reprompt narrative step |

---

## References
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
