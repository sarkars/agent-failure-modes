# Embedding Retrieval Pulls Mismatched Job-Family Leveling Precedent for Offer Band

## Issue: An Offer-Generation Agent's Embedding Search over Past Leveling Decisions Surfaces a Role with Lexically Similar Title and Description but a Different Career Track or Leveling Framework, and the Agent Anchors the New Offer's Band to That Mismatched Precedent

**Frequency**: Occasional

**Symptoms**
- The offer-generation agent's rationale cites a specific past leveling decision as precedent for the new hire's band, but the cited role belongs to a different career track (e.g., individual-contributor vs. management ladder, or a different functional leveling framework) than the role being offered
- Offers anchored to a mismatched leveling precedent show a band distribution inconsistent with offers for the same role and track set through the correct leveling framework, when compared on backtest
- The retrieved "comparable" role frequently shares only surface-level title vocabulary (e.g., both titled "Senior Engineer") with the new role, not the underlying leveling criteria (scope of ownership, reporting structure, technical track vs. management track) that actually determine the correct band
- Compensation analysts report that bands justified by "similar past leveling decision" frequently turn out, on manual review, to reference a role from a different leveling framework entirely
- Re-running the leveling decision with the retrieval step disabled, using only the structured leveling-framework rubric, produces a band that differs from the retrieval-anchored band and matches the framework's intended outcome

**Root Cause**
The offer-generation agent's precedent-retrieval step ranks past leveling decisions by embedding similarity over free-text role descriptions and titles, which captures lexical and topical overlap but not the structured leveling-framework criteria (track, scope, reporting line) that actually determine the correct band. A role in a different leveling framework can be highly similar in embedding space because it shares title vocabulary, while differing entirely on the dimensions the leveling rubric is built around, and the agent has no mechanism to weight retrieved precedents by leveling-framework match rather than text similarity alone.

**Example**
```
New offer is for a "Senior Engineer" role on the individual-contributor technical track, leveled under the engineering IC framework
Offer-generation agent's embedding retrieval over past leveling decisions surfaces a "Senior Engineer, Platform Operations" role as the top precedent, driven by shared title vocabulary, but that role was leveled under a separate operations management-track framework with different banding criteria
Agent anchors the new offer's band to the retrieved precedent's compensation range, citing it as a comparable leveling decision
Compensation analyst later finds the new hire's band is materially misaligned with same-track, same-framework peers, discovered only when an internal pay-equity review compares bands across the IC technical track
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Most-similar retrieved items are not necessarily the most relevant for the decision being made, a structural limitation of similarity-ranked retrieval used to justify downstream agent decisions | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Knowledge-oriented retrieval-augmented generation systems are documented to surface topically related but structurally mismatched precedents when the retrieval index is not filtered by the structured criteria relevant to the downstream task | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Allocational outcomes from LLM-driven hiring and compensation decisions are sensitive to small differences in how comparable cases are selected, with mismatched comparables producing materially different allocational results | [Small Changes, Large Consequences: Analyzing the Allocational Fairness of LLMs in Hiring Contexts](https://arxiv.org/pdf/2501.04316) |

**Contributing Factors**
- Precedent retrieval ranks by free-text title and description embedding similarity only, with no pre-filter by leveling-framework or career-track identity
- Offer-generation rationale surfaces the retrieved precedent prominently, anchoring the band even when the precedent's actual relevance is limited to shared title vocabulary
- No backtest separates band accuracy for retrieval-anchored decisions from decisions made strictly through the structured leveling rubric, so the retrieval step's net effect on banding accuracy is not visible

---

## Mitigation Strategies

1. **Constrain Retrieval to Matching Leveling Framework First**: Filter candidate precedent roles by leveling-framework and career-track identity before applying embedding similarity within that filtered set, rather than ranking the full leveling history by title-text similarity alone
2. **Separate Precedent Citation from Band Computation**: Use retrieved precedents for illustrative rationale only, and ensure the actual band is computed from the structured leveling rubric, with retrieval explicitly excluded from the band-computation path
3. **Backtest Retrieval-Anchored vs. Rubric-Driven Band Accuracy**: Periodically compare bands produced with retrieval-anchored precedent against bands produced strictly from the structured leveling rubric, and suppress the retrieval contribution if it diverges materially from the rubric outcome
4. **Surface Framework-Match Metadata in the Rationale**: When a precedent is cited, require the rationale to explicitly state whether the precedent's leveling framework and career track match the new role, so compensation analysts can see whether the match is substantive or merely lexical

### Metrics
- Rate of generated offers whose cited leveling precedent belongs to a different leveling framework or career track than the offered role
- Band divergence between retrieval-anchored decisions and decisions made strictly from the structured leveling rubric, sampled
- Pay-equity review findings attributable to a mismatched leveling precedent, by track and framework

### Alerts
- An offer is generated citing a leveling precedent from a different leveling framework or career track than the offered role → P1
- Backtest shows retrieval-anchored bands diverging materially from rubric-driven bands for two consecutive review cycles → P2
- A pay-equity review attributes a banding discrepancy to a mismatched leveling precedent → P1

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Small Changes, Large Consequences: Analyzing the Allocational Fairness of LLMs in Hiring Contexts](https://arxiv.org/pdf/2501.04316)
