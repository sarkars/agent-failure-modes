# Embedding-Retrieval Wrong Endorsement Version Applied

## Issue: A Claims-Adjudication Agent's RAG Retrieval Step Pulls a Lexically Similar but Superseded or Wrong-State Policy Endorsement from the Document Store Instead of the Endorsement Actually Attached to the Policy in Force, Causing the Agent to Apply Incorrect Coverage Terms to the Claim

**Frequency**: Common

**Symptoms**
- The dollar impact is directly measurable and often one-directional: because renewal amendments to a sub-limit more often tighten than loosen coverage, a stale endorsement pulled from before the tightening tends to authorize an overpayment rather than an underpayment, making this failure mode a recurring source of claims leakage rather than claimant complaints
- The retrieval error is invisible in the adjudication rationale's prose -- "Endorsement WD-204" reads the same whether it's the 2023 or the 2026 revision -- because the agent's citation format was never built to carry a revision date as a first-class field, only a form name
- Policies that have been amended at multiple renewals are overrepresented in the error population for a mechanical reason: each renewal that touches the same clause adds one more near-duplicate revision to the vector store for that exact endorsement, so the odds of the wrong one winning the similarity ranking rise with every renewal cycle rather than staying constant
- The overpayment is caught by a process entirely outside the claims-adjudication pipeline -- a reinsurance-treaty audit reconciling paid claims against declarations schedules -- which means the retrieval error can persist across many claims before anything inside the adjudication system itself surfaces it
- Once a near-duplicate revision pair exists for a given form, every future claim touching that form is exposed to the same mis-retrieval risk, not just the claim that first surfaced it, since nothing about the underlying vector store changes between claims

**Root Cause**
The retrieval step was built against a document store that accumulates every historical revision of every endorsement form, because form libraries in insurance are kept for audit and legal-defense purposes and nothing prunes or supersedes old revisions out of the searchable index. Sub-limit and peril-list edits at renewal are deliberately drafted as minimal, surgical changes to an existing form rather than wholesale rewrites -- that's standard actuarial and legal practice for keeping a form defensible across revisions -- which is precisely what makes consecutive revisions of the same form nearly indistinguishable to a similarity ranking that has no access to the declarations schedule's effective-date field.

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
