# Embedding Retrieval Pulls Mismatched Historical Deal Cohort as Stage-Conversion Benchmark

## Issue: A Pipeline-Forecasting Agent Justifying Its Stage-Conversion-Rate Assumption for a Set of Open Opportunities Retrieves "Comparable Historical Deals" via Embedding Search over Closed-Deal History, and the Search Surfaces a Cohort of Past Deals That Share Lexical Similarity in Industry Tags or Deal-Name Keywords but Differ Substantially in Buying-Committee Structure or Deal Size, Producing a Stage-Conversion Benchmark That Systematically Overstates or Understates the Forecast for the Current Cohort

**Frequency**: Occasional

**Symptoms**
- Forecast narrative cites a specific historical close rate ("deals like this typically close at 68% from this stage") attributed to a retrieved comparable cohort
- Manually inspecting the retrieved comparable deals shows they share industry tags or surface-level keywords with the current opportunities but differ in deal size by an order of magnitude, buying-committee size, or sales-cycle length
- A more appropriate comparable cohort -- matched on deal size and buying-committee structure rather than industry keyword -- exists in the same closed-deal history but was not the highest embedding-similarity match and was not retrieved
- The forecast's actual realized conversion rate, once the quarter closes, diverges substantially from the cited benchmark in the direction predicted by the more appropriate (but unretrieved) comparable cohort
- The same mismatch recurs specifically for industries with high keyword overlap across very differently structured deals (e.g., "healthcare" spanning both small clinic deals and large hospital-system enterprise deals)

**Example**
```
Pipeline-forecasting agent is asked to justify its conversion-rate assumption for a
cohort of mid-funnel enterprise healthcare-system opportunities this quarter
Agent's retrieval step runs an embedding search over closed-deal history for
"healthcare opportunities at this stage" and surfaces the highest-similarity matches
The retrieved cohort is dominated by small single-clinic deals from two years ago that
share the "healthcare" industry tag and similar deal-name keywords, but have a single
buyer, a much shorter sales cycle, and one-tenth the deal size of the current
enterprise-system opportunities being forecast
Agent cites this cohort's 68% historical close rate from this stage as the benchmark for
the current enterprise deals
A more appropriate comparable cohort -- enterprise multi-stakeholder healthcare-system
deals of similar size and buying-committee complexity -- exists in the same closed-deal
history with a 34% close rate from the same stage, but was not the highest-similarity
embedding match and was never surfaced
Forecast overstates the quarter's expected closed revenue; actual results land much
closer to the unretrieved, more structurally appropriate cohort's historical rate
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Hallucination survey research documents retrieval-augmented agents citing superficially similar but substantively mismatched source content as supporting evidence, particularly when surface-level keyword or tag overlap dominates the similarity signal over structural differences | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Research on agent-environment failures finds retrieval steps in agentic pipelines frequently surface the highest lexical-similarity match rather than the most task-relevant match, especially when relevance depends on structural attributes (deal size, buying-committee complexity) not well captured by the embedding space used | [Aegis: Agent-Environment Failures in LLM-Driven Agentic Systems](https://arxiv.org/html/2508.19504) |
| Execution-provenance research argues a cited comparable benchmark should be traceable to the specific attributes that made it actually comparable, not merely to a high similarity score, so reviewers can judge whether the comparison is structurally sound | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- The embedding index used for comparable-deal retrieval is built primarily over industry tags and deal-name text, which is dominated by keyword overlap rather than structural attributes like deal size or buying-committee complexity that actually drive conversion-rate differences
- No filtering or re-ranking step constrains retrieval to a comparable deal-size or buying-committee-complexity band before similarity ranking is applied
- The forecast narrative presents the retrieved cohort's close rate as if it were the most relevant available benchmark, with no indication that a structurally closer but lower-lexical-similarity cohort exists in the same data
- Forecasters reviewing the agent's narrative have no easy way to see the retrieved cohort's actual deal-size or buying-committee profile alongside the cited close rate, making the mismatch hard to catch without manually pulling the underlying deals

---

## Mitigation Strategies

1. **Structural Pre-Filtering Before Similarity Ranking**: Filter the closed-deal candidate pool by deal-size band and buying-committee-complexity before applying embedding-similarity ranking, rather than ranking the entire closed-deal history on lexical similarity alone
2. **Comparable-Cohort Attribute Disclosure**: Require the forecast narrative to display the retrieved cohort's deal-size range and buying-committee profile alongside the cited close rate, so reviewers can judge structural comparability at a glance
3. **Multi-Cohort Comparison**: Retrieve and present the top several candidate comparable cohorts ranked by structural fit, not just the single highest lexical-similarity match, and let the forecaster or a secondary check select the most appropriate one
4. **Backtest Validation**: Periodically backtest cited historical benchmarks against actual realized conversion rates for the current cohort's deal-size/complexity band, flagging benchmarks that have historically diverged

### Metrics
- Rate of forecast narratives whose cited comparable cohort differs from the current cohort by more than a defined deal-size or buying-committee-complexity threshold
- Variance between cited benchmark close rates and actual realized close rates by cohort structural band
- Number of forecast corrections traced back to a structurally mismatched retrieved comparable

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Structural mismatch in cited cohort | Retrieved comparable cohort's deal-size or buying-committee band differs from current cohort beyond threshold | P2 | Flag forecast for review; re-run retrieval with structural pre-filter |
| Benchmark divergence from backtest | Cited historical close rate diverges from backtested actuals for the matching structural band | P2 | Adjust forecast assumption; review retrieval ranking logic |
| Single-match citation without disclosure | Forecast narrative cites a comparable cohort without displaying its deal-size/complexity profile | P3 | Require narrative regeneration with attribute disclosure |

---

## Related Patterns

- [Semantic Similarity Retrieval Misses Structural Attributes (by-capability)](../../../../../by-capability/knowledge-retrieval/goals/retrieval-relevance/failures/semantic-similarity-retrieval-misses-structural-attributes.md) - the general mechanism behind this pipeline-forecasting-specific instance

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Aegis: Agent-Environment Failures in LLM-Driven Agentic Systems](https://arxiv.org/html/2508.19504)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
