# Embedding-Retrieval Wrong Endorsement Version Applied

## Issue: A Claims-Adjudication Agent's RAG Retrieval Step Pulls a Lexically Similar but Superseded or Wrong-State Policy Endorsement from the Document Store Instead of the Endorsement Actually Attached to the Policy in Force, Causing the Agent to Apply Incorrect Coverage Terms to the Claim

**Frequency**: Common

**Symptoms**
- Adjudication decision cites an endorsement clause (e.g., a named-driver exclusion or a water-damage sub-limit) that reads almost identically to the one actually attached to the policy, but differs in a coverage-determining detail such as the dollar sub-limit, the covered-peril list, or the effective state jurisdiction
- The cited endorsement's form number or effective date in the agent's adjudication rationale does not match the endorsement schedule on the actual policy declarations page when manually cross-checked
- Claims for policies with multiple historical endorsement versions (e.g., a policy amended at renewal three times) show a disproportionate share of the embedding-retrieval-driven coverage errors, because the document store holds several near-duplicate versions of the same clause
- Audit sampling finds the error concentrated in states or product lines where boilerplate endorsement language is reused across many policies with only a sub-limit or peril list changed, since those documents are the most lexically similar to one another in the vector store
- The same underlying retrieval behavior recurs across unrelated claims once a near-duplicate endorsement pair exists in the document store, rather than being a one-off random error

**Root Cause**
The claims agent retrieves applicable policy language via embedding similarity search over a document store containing the full historical library of endorsement forms rather than via a deterministic lookup keyed to the exact form number and effective date on the policy's actual declarations schedule. Because many endorsement forms are boilerplate with only a sub-limit, peril list, or jurisdiction clause changed between versions, their embeddings land close together in vector space; the retriever returns the highest-similarity match, which is frequently the wrong version, and the agent has no independent check that the retrieved clause's form number and effective date match the policy in force.

**Example**
```
Policy in force carries Water Damage Endorsement Form WD-204 (rev. 2026-01), with a $10,000 sub-limit for sump-pump backup, attached at the 2026 renewal
Claims agent's RAG retrieval over the endorsement-form library returns Form WD-204 (rev. 2023-06), 98% cosine-similar in embedding space, which carries a $25,000 sub-limit for the same peril -- the form predates a sub-limit reduction made at a subsequent renewal
Agent approves payment at $25,000 citing "Endorsement WD-204" without distinguishing revision dates, since the agent's prompt and retrieved-chunk metadata do not surface the revision date prominently
Overpayment of $15,000 is only caught three months later during a routine reinsurance-treaty audit that cross-references the actual declarations schedule
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Most-similar retrieved chunks are not necessarily the most relevant chunks, yet many RAG pipelines retrieve on similarity alone -- a documented structural failure mode of embedding-based retrieval | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Pulling a clause from a similar but distinct source document undermines output validity even when the retrieved text reads as locally correct, since correctness of the answer is insufficient if the supporting text came from the wrong source document | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Standard embedding models lack domain-specific structure and routinely overlook the few critical variables (dates, sub-limits, jurisdiction) that distinguish near-identical boilerplate documents | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |

**Contributing Factors**
- Document store contains multiple historical revisions of the same endorsement form without the agent's retrieval step filtering by form number and effective date before similarity ranking
- Retrieved-chunk metadata (revision date, form version) is not surfaced prominently enough in the agent's context for the model to weight it over the topical similarity of the clause text
- No deterministic cross-check step verifies that the form number and effective date in the agent's cited rationale match the policy's actual declarations schedule before the adjudication decision is finalized

---

## Mitigation Strategies

1. **Deterministic Pre-Filter Before Similarity Ranking**: Retrieve candidate endorsement chunks by exact form number and policy-effective-date match against the declarations schedule first, and only use embedding similarity to rank within that already-correct candidate set, never across the full historical library
2. **Surface Revision Metadata in the Retrieved Context**: Inject the form number and effective date as structured, high-salience fields in the prompt alongside the retrieved clause text, rather than relying on the model to infer recency from prose alone
3. **Declarations-Schedule Cross-Check Gate**: Require an automated, non-LLM verification step that the cited endorsement form number and date in the adjudication rationale exactly match the policy's current declarations schedule before payment authorization, blocking the decision on mismatch
4. **Near-Duplicate Audit of the Endorsement Library**: Periodically scan the document store for endorsement form clusters with near-identical embeddings but differing sub-limits or peril lists, and flag those clusters for mandatory deterministic-lookup routing rather than similarity search

### Metrics
- Rate of adjudication decisions where the cited endorsement form/revision date does not match the policy's actual declarations schedule, sampled via audit
- Dollar exposure from coverage-term mismatches traced to wrong-endorsement-version retrieval, by product line and state
- Count of near-duplicate endorsement form clusters identified in the document store with no deterministic-lookup override in place

### Alerts
- Adjudication payment authorized citing an endorsement form/revision date that fails the declarations-schedule cross-check → P1
- Audit sampling finds wrong-endorsement-version retrieval rate above baseline for a given product line/state → P2
- New endorsement form added to the document store creates a near-duplicate cluster with an existing form without a deterministic-lookup rule added → P3

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [LLMs and Agentic AI in Insurance Decision-Making: Opportunities and Challenges For Africa](https://arxiv.org/html/2508.15110)
