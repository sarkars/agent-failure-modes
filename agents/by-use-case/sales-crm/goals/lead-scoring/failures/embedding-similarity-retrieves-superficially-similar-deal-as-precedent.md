# Embedding-Similarity Retrieves Superficially Similar Deal as Precedent

## Issue: A Lead-Scoring Agent That Justifies Its Score by Retrieving "Similar Past Deals" via Embedding Search over the Closed-Deal History Pulls a Lexically Similar but Substantively Different Deal (Same Industry Keywords, Different Buying Stage or Company Size) and Cites It as Supporting Evidence for an Inflated Score

**Frequency**: Common

**Symptoms**
- Lead-scoring rationale cites a specific past "comparable" closed-won deal whose account size, deal cycle length, or buyer persona differs substantially from the new lead, despite reading as topically similar (same industry vertical, similar product line keywords)
- High scores driven primarily by retrieved-precedent similarity show a lower actual conversion rate than scores driven by structured firmographic/behavioral features, when the two scoring paths are compared on held-out outcomes
- The retrieved "similar deal" in the rationale frequently shares only surface-level vocabulary (industry name, product SKU mentioned) with the new lead, not the underlying deal-stage signals (budget confirmed, multiple stakeholders engaged) that actually drove the precedent deal's closure
- Sales reps report that leads scored highly "because of a similar deal we closed before" frequently turn out, on manual review, to resemble that deal only in industry and not in any qualifying signal
- Re-scoring the same lead with the retrieval step disabled (structured features only) produces a meaningfully different and, on backtesting, more accurate score

**Root Cause**
The scoring agent's retrieval step ranks historical deals by embedding similarity over free-text fields (account description, opportunity notes, industry tags), which captures topical and lexical overlap but not the structured qualifying signals that actually determined whether the precedent deal closed. Two deals can be highly similar in embedding space because they share industry vocabulary while differing entirely on the dimensions -- budget authority confirmed, active evaluation timeline, multi-threaded stakeholder engagement -- that determine deal quality, and the agent has no mechanism to weight retrieved precedents by how similar they are on those qualifying dimensions rather than on text similarity alone.

**Example**
```
New lead: a 50-person regional logistics company that downloaded a whitepaper, no sales engagement yet
Lead-scoring agent's embedding retrieval over closed-won history surfaces a 2,000-person national logistics enterprise deal as the top "similar deal" match, driven by shared industry vocabulary ("logistics," "fleet management," "route optimization") in the free-text opportunity notes
Agent cites this precedent in its rationale: "Similar profile to [enterprise account], which closed at $180K -- scoring this lead high-priority"
Lead is routed to an AE as high-priority; AE spends disproportionate time on a lead that, on actual qualification, has no budget authority and a sub-$5K total addressable spend, unlike the cited 2,000-person precedent
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Leading LLM agents on realistic CRM tasks achieve only around 58% single-turn success and roughly 35% in multi-turn settings, reflecting systematic gaps between surface-level task performance and the structured, policy-aware reasoning enterprise CRM tasks require | [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878) |
| Most-similar retrieved items are not necessarily the most relevant for the decision being made, a structural limitation of similarity-ranked retrieval used to justify downstream agent decisions | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| CRM environments require agents to integrate multiple structured data fields and adhere to domain-specific qualification policies, not merely retrieve topically related records, to perform realistic enterprise tasks correctly | [CRMArena: Understanding the Capacity of LLM Agents to Perform Professional CRM Tasks in Realistic Environments](https://arxiv.org/html/2411.02305v2) |

**Contributing Factors**
- Precedent retrieval ranks by free-text embedding similarity only, with no weighting by structured qualifying-signal similarity (budget, stage, company size band)
- Scoring rationale surfaces the retrieved precedent prominently, which anchors the score upward even when the precedent's actual relevance is limited to shared vocabulary
- No backtest separates the predictive value of precedent-retrieval-driven scores from structured-feature-driven scores, so the retrieval step's net effect on score accuracy is not visible

---

## Mitigation Strategies

1. **Constrain Retrieval to Comparable Structured Cohort First**: Filter candidate precedent deals by structured comparability (company size band, deal stage reached, industry sub-segment) before applying embedding similarity within that filtered set, rather than ranking the full closed-deal history by text similarity alone
2. **Separate Precedent Citation from Score Contribution**: Use retrieved precedents for illustrative rationale only, and ensure the actual numeric score is driven by structured, backtested features, with retrieval explicitly excluded from the score-computation path
3. **Backtest Retrieval-Driven vs. Feature-Driven Score Accuracy**: Periodically measure conversion-rate accuracy of scores attributable primarily to retrieved-precedent similarity against scores attributable to structured features, and suppress or reweight the retrieval contribution if it underperforms
4. **Surface Comparability Metadata in the Rationale**: When a precedent is cited, require the rationale to explicitly state the structured comparability dimensions checked (or not checked), so reps can see whether the match is substantive or merely topical

### Metrics
- Conversion-rate accuracy of leads scored highly primarily due to retrieved-precedent similarity vs. leads scored highly on structured features alone
- Rate of AE-reported "mismatched precedent" feedback on high-priority-routed leads
- Structured-comparability overlap (company size band, stage, vertical sub-segment) between new leads and their cited retrieved precedent, sampled

### Alerts
- Backtest shows retrieval-driven score component underperforming structured-feature component by a material margin for two consecutive cycles → P1
- AE-reported mismatched-precedent feedback rate exceeds baseline for a given lead source or segment → P2
- New scoring model version deployed without a structured-comparability pre-filter on the retrieval step → P3

---

## References

- [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878)
- [CRMArena: Understanding the Capacity of LLM Agents to Perform Professional CRM Tasks in Realistic Environments](https://arxiv.org/html/2411.02305v2)
- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
