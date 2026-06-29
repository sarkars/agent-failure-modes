# Embedding Retrieval Selects Wrong Reference Instrument for Freshness Benchmark

## Issue: A Market-Data Freshness-Monitoring Agent Checking Whether an Illiquid Instrument's Price Is Plausibly Current Selects a "Comparable" Reference Instrument Using Embedding Similarity Over Free-Text Descriptions Rather Than Matching on Sector, Duration, and Credit-Quality Attributes, Producing a Freshness Benchmark That Moves Differently From the Instrument Being Checked

**Frequency**: Occasional

**Symptoms**
- An illiquid instrument's unchanged price is judged "plausibly current" against a reference instrument's price movement, even though the reference instrument differs materially in sector, duration, or credit quality from the instrument being checked
- The agent's reference-instrument selection is driven by a similarity match over free-text instrument descriptions, not by matching structured attributes such as sector classification, duration bucket, or credit-rating tier
- Auditing the selected reference instrument against the structured attributes of the instrument being checked shows a mismatch on at least one attribute that materially affects expected price co-movement
- The freshness check passes (reference instrument also appears unchanged or moved similarly) at a rate inconsistent with how often the reference instrument and the checked instrument actually share the structured attributes that would make their price movements comparable
- The mismatch concentrates on instruments with generic or sparse free-text descriptions, since those produce the least attribute-specific embedding signal and the highest chance of a superficially similar but structurally unrelated match

**Root Cause**
Selecting a comparable reference instrument by embedding similarity over free-text descriptions optimizes for the most textually similar description, not for confirming that two instruments share the structured attributes that actually drive correlated price movement. When an illiquid instrument's description is generic or sparse, the similarity signal driving the match does not distinguish a textually similar but structurally unrelated instrument from a true comparable, so the freshness benchmark ends up comparing the checked instrument's lack of price movement against an instrument that was never expected to move similarly in the first place.

**Example**
```
Freshness-monitoring agent checks an illiquid municipal bond's unchanged price over a multi-day window against a "comparable" reference instrument selected by embedding similarity over instrument descriptions
Selected reference instrument shares similar descriptive language ("revenue bond," "infrastructure") but differs materially in duration (3 years longer) and credit tier (one notch lower) from the checked bond
Reference instrument's price also happened to be flat over the same window, so the agent concludes the checked bond's unchanged price is plausibly current
Independent reconciliation, using a reference instrument matched on duration bucket and credit tier rather than description similarity, shows that a true comparable moved materially during the window
Checked bond's price is later found to have been stale; the freshness check's reference-instrument selection had compared it against an instrument that was never expected to co-move with it
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented and similarity-based matching systems are documented to surface a taxonomy of retrieval errors distinct from generation errors, including matching a topically or lexically similar but substantively unrelated record when similarity search is used in place of structured-attribute matching | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Knowledge-oriented retrieval-augmented generation surveys identify attribute-based disambiguation across structurally similar candidates as a distinct reliability challenge from single-source retrieval accuracy | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Research on agentic trading systems identifies comparable-instrument selection grounded in structured attributes, rather than free-text description similarity, as a distinct requirement for benchmarking illiquid-instrument pricing | [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337) |

**Contributing Factors**
- Reference-instrument selection for freshness benchmarking is performed via description-embedding similarity rather than matching on sector, duration bucket, and credit-rating tier
- No validation step confirms the selected reference instrument shares the structured attributes that drive comparable price movement before it is used as a freshness benchmark
- Instruments with generic or sparse free-text descriptions are not flagged for mandatory structured-attribute matching when an embedding-similarity reference selection is used

---

## Mitigation Strategies

1. **Structured-Attribute Matching as Primary Path**: Require reference-instrument selection for freshness benchmarking to match on sector, duration bucket, and credit-rating tier first, falling back to description similarity only when no structured-attribute match is available, and flagging that fallback explicitly
2. **Mandatory Attribute Confirmation Before Benchmark Use**: Before using a selected reference instrument in a freshness benchmark, require confirmation that it shares the structured attributes that drive comparable price movement with the instrument being checked
3. **Sparse-Description Flagging**: Maintain a list of instruments with generic or sparse free-text descriptions and require any freshness benchmark for those instruments to undergo mandatory structured-attribute verification of the reference instrument
4. **Surface Selection Method in Output**: Require any freshness-benchmark result to indicate whether the reference instrument was selected by structured-attribute match or by description similarity, so reviewers can prioritize verification of similarity-based selections

### Metrics
- Rate of freshness benchmarks whose reference instrument was selected by description similarity rather than structured-attribute match
- Rate of similarity-selected reference instruments that fail a structured-attribute verification check when audited
- Number of stale-price misses later found to trace back to a reference-instrument selection error

### Alerts
- A freshness benchmark used to clear a price for valuation has no structured-attribute confirmation of the reference-instrument match → P1
- A similarity-selected reference instrument fails structured-attribute verification on audit after being used in a finalized freshness check → P1
- Description-similarity fallback rate for reference-instrument selection exceeds the defined threshold for a rolling window → P2

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
