# Semantic Similarity Retrieval Misses Structural Attributes

## Issue: When retrieving a comparable or reference item using embedding similarity over text descriptions, agent selects textually similar but structurally incompatible item; downstream operations assume structural compatibility that doesn't exist

**Frequency**: Common

**Symptoms**
- Retrieval selects item matching text similarity but differing on structured attributes (category, type, jurisdiction, tier)
- Downstream operation assumes structural properties match (price co-movement, legal applicability, drug interactions)
- Similarity-selected items perform differently than expected
- Mismatch concentrates on items with generic or sparse text descriptions (low signal for attribute matching)

**Root Cause**
Embedding similarity optimizes for textual resemblance, not structural alignment. When text descriptions are generic or sparse, the embedding signal doesn't distinguish textually similar but structurally unrelated items. True comparability requires structured-attribute matching (category, type, jurisdiction), not text similarity.

**Examples**

### Financial Services (Pricing Benchmark)
```
Market-data agent checks if an illiquid municipal bond's unchanged price is plausibly current
Selects reference instrument using text-embedding similarity over descriptions
Reference shares similar language ("revenue bond", "infrastructure") but differs in:
  - Duration: 3 years longer
  - Credit tier: one notch lower
Both happen to show flat prices over window; agent concludes checked bond's price is current
Reality: True comparable (matched on duration + credit tier) moved materially
Outcome: Stale price passes validation; downstream valuation uses outdated data
```

### Healthcare (Drug Lookup)
```
Treatment agent retrieves drug interactions using embedding similarity over drug names
Query: "Ibuprofen drug interactions"
Retrieved: "Ibuprofen-analog compound (experimental drug in phase 2 trials)"
Textual match: STRONG (both are ibuprofen-related)
Structural compatibility: NONE (experimental drug has no safety data)
Agent reports: "No known interactions found"
Reality: Experimental drug safety completely unknown
Outcome: Dangerous drug combination recommended without safety data
```

### Legal (Case Law Retrieval)
```
Contract agent retrieves precedent case law using embedding similarity over case summaries
Query: "Contract dispute remedies precedent"
Retrieved: "Contract dispute case - Texas jurisdiction"
Textual match: STRONG (same legal topic)
Structural compatibility: NONE (different state law applies)
Agent reports: "Precedent supports remedy approach"
Reality: Texas precedent doesn't apply to New York contract
Outcome: Contract negotiation based on inapplicable case law
```

### Supply Chain (Parts Lookup)
```
Procurement agent retrieves supplier catalog using embedding similarity over part descriptions
Query: "Steel bearing 25mm diameter"
Retrieved: "Bearing-like component, similar industrial application"
Textual match: STRONG (both are bearing-related)
Structural compatibility: NONE (completely different part specifications)
Agent reports: "Compatible replacement found"
Reality: Different part won't fit in assembly; supplier wrong
Outcome: Wrong component ordered; production halted
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval error taxonomy: semantic similarity vs structural attribute matching | [Classifying Errors in RAG Systems](https://arxiv.org/html/2510.13975v1) |
| Attribute-based disambiguation in knowledge retrieval | [Survey on Knowledge-Oriented RAG](https://arxiv.org/pdf/2503.10677) |
| Structured-attribute matching requirement for domain-specific retrieval | [Domain-Specific Retrieval Challenges](https://arxiv.org/abs/2605.19337) |

---

## Mitigation Strategies

1. **Structured-Attribute Matching First**: Match on structured attributes (category, type, jurisdiction, tier) before falling back to text similarity
2. **Attribute Verification Before Use**: Before using retrieved item downstream, verify it shares structural attributes that drive compatibility
3. **Sparse-Description Flagging**: Mark items with generic descriptions; require mandatory attribute verification for those
4. **Surface Selection Method**: Output which retrieval method was used (attribute match vs similarity); reviewers prioritize similarity-based results for verification

### Metrics
- % of retrievals using similarity instead of attribute match
- % of similarity-selected items that fail attribute verification on audit
- Downstream compatibility rate: similarity-selected vs attribute-matched items

### Alerts
- Similarity-selected item used downstream with no attribute verification → P1
- Retrieved item fails attribute check after downstream use → P1

---

## Related Patterns

Domain-specific instances of this same mechanism, each with mitigations tailored to that domain's structural attributes rather than the generic ones above:

- [Devops: Capacity Profile Matched by Name Similarity](../../../../../by-use-case/devops/goals/capacity-planning/failures/embedding-retrieval-applies-wrong-services-capacity-profile-by-name-similarity.md) - matches on statefulness/write-topology instead of service name
- [Devops: Cost Playbook Matched by Tag Similarity](../../../../../by-use-case/devops/goals/cost-optimization/failures/embedding-retrieval-applies-wrong-workloads-cost-playbook-by-tag-similarity.md) - matches on workload resource profile instead of tags
- [Devops: Deployment Checklist Mismatch](../../../../../by-use-case/devops/goals/deployment-safety/failures/embedding-retrieval-applies-wrong-services-deployment-checklist.md) - matches on deployment topology instead of service description
- [Healthcare: Drug Interaction Class Mismatch](../../../../../by-use-case/healthcare/goals/adverse-drug-interaction/failures/embedding-retrieval-matches-structurally-similar-different-class-drug-for-interaction-check.md) - matches on drug class instead of active-ingredient interaction profile
- [Sales-CRM: Deal Cohort Benchmark Mismatch](../../../../../by-use-case/sales-crm/goals/pipeline-forecasting/failures/embedding-retrieval-pulls-mismatched-historical-deal-cohort-as-stage-conversion-benchmark.md) - matches on deal description instead of segment/stage attributes
- [Supply Chain: Logistics Lane Benchmark Mismatch](../../../../../by-use-case/supply-chain/goals/logistics-routing/failures/embedding-retrieval-selects-wrong-historical-lane-as-transit-time-benchmark.md) - matches on route description instead of mode/distance attributes

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Domain-Specific Retrieval in Agentic Systems](https://arxiv.org/abs/2605.19337)
