# Embedding Retrieval Pulls Mismatched Rating-Territory Policy Precedent for Renewal

## Issue: A Policy-Renewal Agent's Retrieval Step Surfaces a "Similar Policy" Precedent via Embedding Similarity to Determine an Appropriate Rate Adjustment for an Unusual Risk Profile, but the Matched Policy Is in a Different Rating Territory With Different Loss Experience, Leading to a Mispriced Renewal

**Frequency**: Occasional

**Symptoms**
- A renewal for a policy with an unusual risk profile (a property with a non-standard construction type, in a less common rating territory) is priced using a rate adjustment copied from a "similar policy" precedent that is in a different rating territory with materially different loss experience
- The retrieved precedent and the policy being renewed share surface-level similarity (same construction type, similar coverage limits, similar age), which is exactly the pattern that produces a high embedding-similarity score despite the underlying territory-specific loss experience being substantively different
- Asking the renewal agent to cite its source for the rate adjustment shows it retrieved the "similar policy" precedent by similarity score across policy attributes, without filtering by rating territory before ranking
- The miss concentrates on policies in less common rating territories, since the dominant territory in the policy corpus produces the highest similarity scores for almost any query regardless of actual territory match
- Manually filtering candidate precedent policies by rating territory before running the similarity search surfaces a substantively better-matched precedent every time

**Root Cause**
The renewal agent's retrieval step ranks candidate precedent policies by embedding similarity across the full policy-attribute feature set, but construction type, coverage limits, and age are similar across many policies regardless of rating territory, so the embedding match is dominated by these shared attributes rather than the territory-specific loss-experience data that actually determines the appropriate rate adjustment. Without a hard filter on rating territory applied before the similarity ranking, the search returns the most common territory's policy in the corpus rather than the one that is actually analogous for this renewal's territory.

**Example**
```
Policy up for renewal covers a property with a non-standard timber-frame construction in a rating territory with elevated wildfire loss experience
Renewal agent retrieves a "similar policy" precedent via embedding similarity on construction type, coverage limit, and property age
Search returns a precedent policy with the same construction type and similar coverage limit, but located in a rating territory with low wildfire exposure, since that territory dominates the precedent corpus
Renewal agent applies the precedent's modest rate adjustment to this renewal, without ever surfacing a territory-appropriate adjustment reflecting elevated wildfire loss experience
Policy renews underpriced relative to its actual territory risk, an error caught only during a later loss-ratio review of the rating territory
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of retrieval-augmented generation systems identify embedding-similarity retrieval favoring records with high surface-attribute overlap over records that are substantively analogous as a distinct and recurring error category | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Taxonomies of RAG system errors find that retrieval components frequently surface a superficially similar but substantively mismatched record when the dominant cluster in the corpus differs from the query's actual relevant subgroup | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Research on memory and retrieval mechanisms in autonomous LLM agents identifies the absence of metadata-based pre-filtering before similarity ranking as a contributing factor in retrieval errors for attribute-overlapping record sets | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |

**Contributing Factors**
- Policy-attribute embeddings are dominated by shared features (construction type, coverage limit, age) that are similar across territories, rather than the territory-specific loss-experience data that determines the correct rate adjustment
- The retrieval step does not apply a hard filter on rating territory before ranking candidate precedent policies by similarity
- Less common rating territories are underrepresented in the precedent corpus relative to the dominant territory, so similarity search defaults toward the dominant territory's pricing regardless of actual fit

---

## Mitigation Strategies

1. **Mandatory Rating-Territory Pre-Filter Before Similarity Ranking**: Require the retrieval step to filter candidate precedent policies by rating territory before any embedding-similarity ranking is applied, rather than relying on similarity alone to select the comparison policy
2. **Loss-Experience-Weighted Embedding**: Weight the policy-attribute embedding toward territory-specific loss-experience features rather than surface attributes that are similar across territories
3. **Confidence Threshold on Cross-Territory Matches**: Flag any retrieval result where the matched precedent's rating-territory metadata does not match the policy being renewed, even if the similarity score is high
4. **Underrepresented-Territory Coverage Audit**: Periodically audit renewal-pricing accuracy specifically for less common rating territories, since they are the population most likely to be overridden by the dominant territory's precedent in the corpus

### Metrics
- Rate of renewal-pricing precedent retrievals where the matched policy's rating-territory metadata does not match the policy being renewed
- Loss-ratio deviation for renewals priced using a cross-territory precedent versus a territory-matched precedent
- Rate of renewals later flagged for repricing after a loss-ratio review identifies a territory mismatch in the original precedent

### Alerts
- A renewal-pricing precedent is retrieved and applied where the matched policy's rating-territory metadata does not match the policy being renewed → P2
- Rate of cross-territory precedent matches exceeds the defined threshold for a rolling window → P3
- A loss-ratio review identifies a renewal mispriced due to a territory-mismatched precedent → P2

---

## References

- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
