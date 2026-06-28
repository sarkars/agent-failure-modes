# Embedding-Retrieval Pulls Wrong Clause Version from Template Library

## Issue: A Contract-Drafting Agent's RAG Step, Used to Pull the Firm's or Company's Approved Boilerplate Clause for a Given Section (Limitation of Liability, Indemnification, Governing Law) from the Template Library, Retrieves a Lexically Similar but Superseded or Jurisdiction-Wrong Version of the Clause, and the Drafted Contract Is Issued with the Wrong Terms

**Frequency**: Common

**Symptoms**
- Drafted contract section reads as well-formed boilerplate but contains a clause version that differs from the currently approved template in a legally material way (a liability cap amount, a notice-period length, a governing-law jurisdiction) when compared directly against the canonical template
- The retrieved clause shares extensive structurally identical language with the correct current version, since most clause libraries hold several historical revisions of the same clause differing only in the negotiated or jurisdiction-specific variable terms
- The error concentrates on clause types with many historical negotiated variants in the library (e.g., limitation-of-liability clauses customized per deal size or jurisdiction), since those variants are the most lexically similar to one another in the vector store
- Legal review catches the wrong-version clause only during final read-through, or it goes out to the counterparty and is caught during their redline, rather than being prevented at drafting time
- Re-running the same drafting request with retrieval restricted to a deterministic lookup against the canonical, currently-approved clause ID (rather than free-text similarity search over the full historical library) correctly returns the right version, isolating retrieval as the point of failure

**Root Cause**
The drafting agent retrieves boilerplate clause language via embedding similarity search over a document store containing the full historical library of clause variants, rather than via a deterministic lookup keyed to the clause's canonical, currently-approved version ID for the relevant jurisdiction and deal type. Legal boilerplate is highly standardized and contains formally defined, repeated phrasing across many historical variants differing only in a few critical negotiated terms, which is a well-documented condition under which similarity-based retrieval confuses structurally near-identical but substantively different source documents.

**Example**
```
Drafting agent is asked to insert the standard limitation-of-liability clause for a new mid-market services agreement
Clause-template library contains several historical variants of this clause from past negotiated deals, all differing primarily in the liability cap multiplier (1x fees, 2x fees, uncapped-for-gross-negligence carve-out) and jurisdiction-specific enforceability language
Agent's RAG retrieval returns a variant negotiated for a specific large enterprise deal with a 1x-fees cap and a now-outdated jurisdiction carve-out, rather than the firm's current standard 2x-fees template, because the two versions are over 90% lexically identical and the retrieval ranks by overall text similarity
Drafted contract goes to the counterparty with the wrong liability cap; the error is only caught when the counterparty's redline flags the cap as inconsistent with the term sheet previously agreed
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Pulling a clause from a similar but distinct contract undermines the legal validity of the generated output and erodes user trust, even when the retrieved text reads as locally well-formed boilerplate | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Legal language is highly standardized with boilerplate clauses and formally defined phrasing repeated across many documents differing only in a few critical variables, a structural condition that confuses retrieval models relying on surface-level or vector similarity | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Version control for legal documents is identified as a distinct technical challenge precisely because near-identical historical document variants are difficult to disambiguate without deterministic versioning metadata | [Version Control for Legal Documents](https://arxiv.org/abs/2108.06421) |

**Contributing Factors**
- Clause-template library contains multiple historical negotiated variants of the same clause type without the retrieval step filtering by canonical version ID and jurisdiction before similarity ranking
- Retrieved-clause metadata (version ID, approval date, jurisdiction applicability) is not surfaced prominently enough in the agent's context for the model to weight it over the topical/structural similarity of the clause text
- No deterministic cross-check step verifies that the retrieved clause's version ID matches the currently-approved canonical template for the relevant jurisdiction and deal type before the draft is finalized

---

## Mitigation Strategies

1. **Deterministic Canonical-Version Lookup Before Similarity Ranking**: Retrieve the applicable clause by its canonical, currently-approved version ID for the relevant jurisdiction and deal type first, and only use embedding similarity for genuinely open-ended drafting tasks where no canonical version exists, never for standard boilerplate retrieval
2. **Surface Version Metadata in the Retrieved Context**: Inject the clause's version ID, approval date, and jurisdiction applicability as structured, high-salience fields in the prompt alongside the retrieved clause text, rather than relying on the model to infer currency from prose alone
3. **Canonical-Template Cross-Check Gate**: Require an automated, non-LLM verification step that the version ID of every boilerplate clause inserted into a draft matches the canonical, currently-approved template for that jurisdiction and deal type before the draft is sent for review or to a counterparty
4. **Near-Duplicate Clause Audit of the Template Library**: Periodically scan the clause library for near-identical clause variants differing in legally material terms (cap amounts, notice periods, jurisdiction), and flag those clusters for mandatory deterministic-lookup routing rather than similarity search

### Metrics
- Rate of drafted contracts where an inserted boilerplate clause's version ID does not match the canonical, currently-approved template, sampled via review
- Count of near-duplicate clause clusters identified in the template library with no deterministic-lookup override in place
- Time between draft issuance and detection of a wrong-clause-version error, by detection method (internal review vs. counterparty redline)

### Alerts
- Draft finalized with a boilerplate clause whose version ID fails the canonical-template cross-check → P1
- Review sampling finds wrong-clause-version rate above baseline for a given clause type or jurisdiction → P2
- New clause variant added to the template library creates a near-duplicate cluster with an existing canonical clause without a deterministic-lookup rule added → P3

---

## References

- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [Version Control for Legal Documents](https://arxiv.org/abs/2108.06421)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
