# Embedding Retrieval Selects Wrong Historical Benchmark Order for TCA Comparison

## Issue: A Transaction-Cost-Analysis Agent Benchmarking a Trade's Execution Quality Against Historical Comparable Orders Selects the "Most Similar" Past Order Using Embedding Similarity Over Free-Text Order Notes, Rather Than Matching on Instrument, Order Size, and Time-of-Day Liquidity Regime, Producing a Benchmark That Was Never Executed Under Comparable Conditions

**Frequency**: Occasional

**Symptoms**
- A trade's execution quality is benchmarked as "in line with historical comparables" against a past order whose free-text notes describe a similar strategy or rationale, even though that past order differs materially in size, time-of-day liquidity regime, or instrument-specific spread characteristics from the trade being benchmarked
- The agent's historical-comparable selection is driven by similarity matching over order notes or strategy descriptions, not by matching structured attributes such as instrument, order size bucket, or time-of-day liquidity window
- Auditing the selected historical order against the structured attributes of the trade being benchmarked shows a mismatch on at least one attribute that materially affects expected execution cost
- The benchmark passes (current trade's cost falls within the historical comparable's range) at a rate inconsistent with how often the selected historical order and the current trade actually share the structured attributes that would make their execution costs comparable
- The mismatch concentrates on trades with generic or templated order notes, since those produce the least attribute-specific embedding signal and the highest chance of a superficially similar but structurally unrelated historical match

**Root Cause**
Selecting a historical comparable order by embedding similarity over free-text order notes optimizes for the most textually similar note, not for confirming that two orders share the structured attributes that actually drive comparable execution cost. When an order's notes use generic or templated language, the similarity signal driving the match does not distinguish a textually similar but structurally unrelated historical order from a true comparable, so the TCA benchmark ends up comparing the current trade's cost against an order that was never executed under comparable liquidity conditions.

**Example**
```
TCA agent benchmarks a 50,000-share order executed during a low-liquidity midday window against a historical comparable selected by embedding similarity over order notes
Selected historical order shares similar strategy language ("VWAP execution, minimize market impact") but was for 5,000 shares executed during the high-liquidity market-open window, a materially different size and liquidity regime
Historical order's realized slippage was low given its smaller size and favorable liquidity timing, so the agent benchmarks the current 50,000-share midday order as "in line" with that low-slippage comparable
Independent benchmark using a historical order matched on size bucket and time-of-day liquidity regime shows materially higher expected slippage for orders of that size executed in that window
Current trade's actual slippage exceeds the embedding-matched benchmark by a wide margin, but is reported as "in line with historical comparables" because the wrong comparable was selected
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented and similarity-based matching systems are documented to surface a taxonomy of retrieval errors distinct from generation errors, including matching a topically or lexically similar but substantively unrelated record when similarity search is used in place of structured-attribute matching | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Knowledge-oriented retrieval-augmented generation surveys identify attribute-based disambiguation across structurally similar candidates as a distinct reliability challenge from single-source retrieval accuracy | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Research on agentic trading systems identifies comparable-order selection grounded in structured attributes, rather than free-text note similarity, as a distinct requirement for reliable transaction-cost benchmarking | [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337) |

**Contributing Factors**
- Historical-comparable selection for TCA benchmarking is performed via order-note similarity rather than matching on instrument, order-size bucket, and time-of-day liquidity regime
- No validation step confirms the selected historical order shares the structured attributes that drive comparable execution cost before it is used as a benchmark
- Orders with generic or templated free-text notes are not flagged for mandatory structured-attribute matching when an embedding-similarity comparable selection is used

---

## Mitigation Strategies

1. **Structured-Attribute Matching as Primary Path**: Require historical-comparable selection for TCA benchmarking to match on instrument, order-size bucket, and time-of-day liquidity regime first, falling back to order-note similarity only when no structured-attribute match is available, and flagging that fallback explicitly
2. **Mandatory Attribute Confirmation Before Benchmark Use**: Before using a selected historical order in a TCA benchmark, require confirmation that it shares the structured attributes that drive comparable execution cost with the trade being benchmarked
3. **Templated-Notes Flagging**: Maintain a flag for orders with generic or templated free-text notes and require any TCA benchmark involving those orders to undergo mandatory structured-attribute verification of the historical comparable
4. **Surface Selection Method in Output**: Require any TCA benchmark result to indicate whether the historical comparable was selected by structured-attribute match or by order-note similarity, so reviewers can prioritize verification of similarity-based selections

### Metrics
- Rate of TCA benchmarks whose historical comparable was selected by order-note similarity rather than structured-attribute match
- Rate of similarity-selected historical comparables that fail a structured-attribute verification check when audited
- Number of execution-quality misses later found to trace back to a historical-comparable selection error

### Alerts
- A TCA benchmark used to clear a trade as "in line with historical comparables" has no structured-attribute confirmation of the comparable match → P1
- A similarity-selected historical comparable fails structured-attribute verification on audit after being used in a finalized TCA report → P1
- Order-note-similarity fallback rate for historical-comparable selection exceeds the defined threshold for a rolling window → P2

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
