# Embedding-Retrieval Matches Wrong SLA-Tier Policy Document

## Issue: An SLA-Management Agent's RAG Step, Used to Retrieve the Applicable Response-Time and Resolution-Time Commitments for an Incoming Ticket Based on the Customer Account's Description, Pulls a Lexically Similar but Wrong-Tier SLA Policy Document, Causing the Agent to Apply Incorrect Commitment Clocks to the Ticket

**Frequency**: Common

**Symptoms**
- The failure is silent by default: a wrong-tier SLA document that's more lenient than the account's real commitment means the breach clock simply never trips, so nothing alerts until the customer themselves escalates
- Premium accounts are disproportionately affected relative to their share of ticket volume, because a ticket's own text rarely has any reason to restate the word "Premium" -- the customer is describing their outage, not their contract -- so the one token that would have disambiguated the tier is usually absent from exactly the tickets that need it most
- Since SLA tiers are near-identical documents by design (the whole point of tiering is that Standard, Premium, and Enterprise share the same service description and differ mainly in a couple of numeric thresholds), the ticket's free text ends up matching whichever tier document happens to be most generically worded, not the one the account actually pays for
- Customer success discovers the pattern in aggregate before any individual case is investigated -- a cluster of premium accounts whose historical tickets all cleared against standard-tier windows -- which is a symptom of the retrieval step failing systematically rather than on isolated tickets
- Re-running the same tickets against a tier resolved from the account ID in the billing system rather than from ticket text eliminates the mismatch entirely, confirming the ticket-content retrieval step, not the SLA documents themselves, is where the account's actual commitment gets lost

**Root Cause**
Ticket intake was built to resolve "what SLA applies" from whatever context the ticket itself carries, because the intake agent's only guaranteed input is the ticket's free text -- account ID is available but wiring intake to look it up against the billing/contract system was treated as a later integration step, not the initial retrieval path. That gap matters specifically for SLA tiering because tier documents are a textbook case of intentional near-duplication: the business requirement that tiers read as "the same service, at different response speeds" is exactly what makes them nearly indistinguishable to a similarity search that has no privileged access to the one field -- contracted tier -- that actually determines the answer.

**Example**
```
Premium-tier customer submits a ticket describing a checkout-flow outage; the ticket's free-text content discusses generic product-area terms without restating "Premium" anywhere in the text
SLA agent's RAG retrieval over the SLA-document corpus returns the Standard-tier SLA document as the top similarity match, since its boilerplate overlaps heavily with the ticket's generic product-area language, while the Premium document's distinguishing clauses (faster response window, dedicated escalation path) are a smaller fraction of that document's overall text
Ticket is tracked against the Standard 8-hour response window instead of the Premium 1-hour window the account is actually contracted for
Premium customer escalates after receiving no response for several hours, well past their actual contracted commitment, triggering a contract-compliance review that traces the root cause to the wrong SLA document having been applied at ticket intake
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Most-similar retrieved documents are not necessarily the most relevant for the decision being made, a structural limitation of similarity-ranked retrieval that does not account for category-determining details represented by only a small fraction of a document's text | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Standard embedding models lack domain-specific structure and routinely overlook the few critical variables that distinguish near-identical boilerplate documents from one another | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Information freshness and consistency in chatbot-driven support systems is documented as a structural risk when retrieval is not anchored to a deterministic, authoritative account record | [Information Freshness & Chatbots](https://arxiv.org/abs/2109.12771) |

**Contributing Factors**
- SLA-document retrieval relies on free-text embedding similarity against the ticket's context rather than a deterministic lookup against the account's contracted tier as recorded in the billing/contract system
- SLA tier documents across the product line share extensive common boilerplate, with tier-determining clauses making up only a small fraction of the document's overall text and embedding signature
- No automated cross-check compares the applied SLA document's tier against the account's actual contract record before the response/resolution clock is started

---

## Mitigation Strategies

1. **Deterministic Tier Lookup Before Similarity Ranking**: Require ticket intake to resolve the account's contracted SLA tier via a deterministic lookup against the billing/contract system using the account ID, and use that tier -- not free-text similarity -- to select the applicable SLA document
2. **Tier-Determining Clause Weighting**: When similarity search is used at all (e.g., for sub-clauses within a confirmed tier), weight the tier-determining clauses more heavily than the shared boilerplate in the ranking
3. **Account-Record Cross-Check Gate**: Require an automated, non-LLM verification step that the applied SLA document's tier matches the account's contract record before the response/resolution clock starts, blocking the clock-start on mismatch
4. **Near-Duplicate Tier-Document Audit**: Periodically scan the SLA-document corpus for tier pairs with near-identical embeddings but differing time thresholds, and flag those pairs for mandatory deterministic-lookup routing rather than similarity search

### Metrics
- Rate of tickets tracked against an SLA tier that does not match the account's contract record, sampled via audit
- Count of SLA escalation alerts that fired late or not at all due to a wrong, more lenient tier threshold being applied
- Time between ticket intake and detection of a wrong-tier mismatch, by detection method (audit-driven vs. customer-escalation-driven)

### Alerts
- SLA clock started on a ticket where the applied tier document fails the account-record cross-check → P1
- Audit sampling finds wrong-tier-application rate above baseline for a given account segment → P2
- New SLA tier document added to the corpus creates a near-duplicate cluster with an existing tier document without a deterministic-lookup rule added → P3

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Information Freshness & Chatbots](https://arxiv.org/abs/2109.12771)
