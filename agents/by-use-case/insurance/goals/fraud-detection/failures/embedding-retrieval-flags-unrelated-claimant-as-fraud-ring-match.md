# Embedding Retrieval Flags Unrelated Claimant as Fraud-Ring Match

## Issue: A Fraud-Detection Agent's Link-Analysis Retrieval Step, Which Searches for Claimants Embedding-Similar to Known Fraud-Ring Members Based on Free-Text Claim-Narrative and Address Fields, Surfaces a Coincidental Lexical Match (a Common Surname, a High-Density Apartment Complex Address) and Treats It as a Fraud-Ring Association, Escalating a Legitimate Claimant for SIU Investigation Based on a Retrieval False Positive

**Frequency**: Occasional

**Symptoms**
- A claimant is escalated to Special Investigation Unit (SIU) review with a rationale citing similarity to a known fraud-ring member's name, address pattern, or claim-narrative phrasing, but manual investigation finds no actual connection beyond the coincidental textual similarity
- The retrieval trace shows the matched "similar" fraud-ring member shares only surface-level attributes (a common surname, a shared high-density residential address shared by many unrelated tenants, generic claim-narrative phrasing common across many unrelated claims) with the escalated claimant, not any of the structured link-analysis signals (shared bank account, shared phone number, shared repair-vendor billing pattern) that would indicate an actual ring association
- SIU investigators report a disproportionate share of embedding-retrieval-driven escalations resolve as false positives compared to escalations driven by structured link-analysis signals, when the two escalation paths are compared on investigation outcomes
- The miss concentrates on common surnames and high-density shared addresses (apartment complexes, mail-forwarding services), since these produce high textual similarity to a genuine fraud-ring member's records without any underlying behavioral connection
- Re-running the same escalation logic with the free-text retrieval step disabled, using only structured link-analysis signals, does not surface the same claimant for escalation

**Root Cause**
The fraud-detection agent's link-analysis retrieval step ranks candidate claimants by embedding similarity over free-text fields (name, address, claim-narrative phrasing), which captures lexical and topical overlap but not the structured relational signals that actually establish a fraud-ring connection. A claimant can be highly similar in embedding space to a known fraud-ring member purely because they share a common surname or a high-density shared address, while having no actual relational connection on the dimensions -- shared financial accounts, shared contact information, shared vendor billing patterns -- that genuine link analysis is built to detect, and the agent has no mechanism to require a structured relational signal before treating an embedding match as a fraud-ring association.

**Example**
```
Known fraud-ring member is recorded in the SIU case file as "J. Martinez, 4400 Oakwood Apartments Unit 12B," associated with a vendor-billing fraud scheme
New, unrelated claimant files a legitimate claim: "J. Martinez, 4400 Oakwood Apartments Unit 47C," a different unit in the same large apartment complex with no actual connection to the fraud-ring member
Fraud-detection agent's embedding-similarity retrieval over the SIU case file surfaces the known fraud-ring member as a close match based on shared name and address-complex text, and the agent's escalation rationale cites this as a fraud-ring association
Legitimate claimant is escalated to SIU review and experiences a significant payment delay during the investigation, which ultimately finds no connection beyond the coincidental shared surname and apartment complex
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Most-similar retrieved items are not necessarily the most relevant for the decision being made, a structural limitation of similarity-ranked retrieval used to justify downstream agent decisions | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Knowledge-oriented retrieval-augmented generation systems are documented to surface topically related but structurally unconnected records when the retrieval index is not filtered by the structured relational criteria relevant to the downstream task | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Agentic AI applications in insurance decision-making, including fraud and SIU referral workflows, are documented to require structured, verifiable relational signals rather than free-text similarity alone to support escalation decisions reliably | [LLMs and Agentic AI in Insurance Decision-Making: Opportunities and Challenges For Africa](https://arxiv.org/html/2508.15110) |

**Contributing Factors**
- Link-analysis retrieval ranks by free-text name, address, and narrative embedding similarity only, with no requirement for a corroborating structured relational signal (shared bank account, phone number, or vendor billing pattern)
- Escalation rationale surfaces the retrieved fraud-ring match prominently, driving the SIU referral even when the match's actual relevance is limited to a coincidental shared surname or shared high-density address
- No backtest separates SIU investigation outcomes for embedding-retrieval-driven escalations from structured-link-analysis-driven escalations, so the retrieval step's net false-positive contribution is not visible

---

## Mitigation Strategies

1. **Require Structured Relational Signal Before Escalation**: Treat an embedding-similarity match to a known fraud-ring member as insufficient on its own for SIU escalation; require at least one corroborating structured relational signal (shared bank account, phone number, vendor billing pattern) before escalating
2. **Address-Density Discount**: Apply a similarity discount for shared addresses known to be high-density, multi-unit residences or mail-forwarding services, since shared-address similarity in these cases carries materially less evidentiary weight than for single-occupancy addresses
3. **Backtest Retrieval-Driven vs. Structured-Signal-Driven Escalation Outcomes**: Periodically compare SIU investigation outcomes for escalations driven primarily by embedding-retrieval similarity against escalations driven by structured link-analysis signals, and suppress or reweight the retrieval contribution if it underperforms
4. **Surface Match-Basis Metadata in the Escalation Rationale**: When a fraud-ring match is cited, require the rationale to explicitly state which structured relational signals were checked and matched (if any), so SIU investigators can see whether the match is substantive or merely textual

### Metrics
- False-positive rate of SIU escalations attributable primarily to embedding-retrieval similarity versus escalations supported by a corroborating structured relational signal
- Rate of escalations involving a shared high-density address or common surname with no corroborating structured signal
- Average claimant payment delay attributable to an SIU escalation later found to be a retrieval false positive

### Alerts
- An SIU escalation is generated based on embedding-similarity match alone with no corroborating structured relational signal → P2
- Backtest shows embedding-retrieval-driven escalations underperforming structured-signal-driven escalations on investigation-outcome accuracy by a material margin for two consecutive review cycles → P2
- A claimant payment delay attributable to a retrieval-false-positive SIU escalation exceeds the defined threshold → P3

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [LLMs and Agentic AI in Insurance Decision-Making: Opportunities and Challenges For Africa](https://arxiv.org/html/2508.15110)
