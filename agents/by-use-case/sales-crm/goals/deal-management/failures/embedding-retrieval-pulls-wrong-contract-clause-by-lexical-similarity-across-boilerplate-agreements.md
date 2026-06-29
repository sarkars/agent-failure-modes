# Embedding Retrieval Pulls Wrong Contract Clause by Lexical Similarity Across Boilerplate Agreements

## Issue: A Deal-Management Agent Assembling a Custom Order Form or Amendment Retrieves a Liability-Cap or Termination-for-Convenience Clause via Embedding Search over the Company's Contract Repository, and Because Most Enterprise Agreements Share Highly Standardized, Boilerplate Language, the Retrieval Step Surfaces a Clause From a Different Customer's Contract With a Different (and More Favorable to That Other Customer) Negotiated Term, Which the Agent Inserts Into the Current Deal's Document as if It Were the Company's Standard Clause

**Frequency**: Occasional

**Symptoms**
- The clause inserted into the new deal's order form matches, nearly word for word, language from a different, named customer's previously negotiated contract rather than the company's actual standard template clause
- The retrieved clause contains a negotiated deviation (a higher liability cap, a shorter termination notice period, a non-standard renewal term) that was specific to the other customer's deal and was never approved as the general standard
- Deal-desk or legal review catches the mismatch only on manual read-through, after the agent has already produced a draft that was sent for the customer's signature
- Querying the embedding index directly for the inserted clause's text shows it is near-identical in wording to the standard template clause, differing primarily in a few negotiated numeric or date terms -- exactly the kind of difference embedding similarity is least sensitive to in highly boilerplate legal text
- The same retrieval mechanism, when tested across multiple customer contracts with similar boilerplate structure, shows a measurably high rate of pulling content from the wrong source contract rather than the intended template

**Example**
```
Deal-management agent is assembling an order-form amendment for Customer A and needs the
company's standard liability-cap clause
Agent's retrieval step runs an embedding search over the contract repository for
"liability cap clause" and returns the highest-similarity match
Because liability-cap clauses are highly standardized boilerplate across most enterprise
agreements, the highest-similarity result is not the canonical template but Customer B's
previously negotiated version, which carries a liability cap twice the company's standard
ceiling -- a concession Customer B specifically negotiated and legal approved only for
that one deal
Agent inserts Customer B's clause language into Customer A's amendment, presenting it as
standard
Deal desk approves the amendment without flagging the discrepancy, since the clause reads
as plausible boilerplate
Legal catches the deviation during a routine post-signature audit, after Customer A has
already signed an amendment with a non-standard, unapproved liability term
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Research on retrieval reliability in legal RAG systems finds retrievers frequently select content from an entirely incorrect source document, with document-level retrieval mismatch exceeding 95% in some legal-contract test sets because agreements are highly standardized and largely uniform apart from a few key negotiated variables | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Survey research on LLM-agent hallucination documents retrieval-augmented generation systems surfacing plausible but incorrect source content when semantic similarity is high but provenance is wrong, with agents then presenting that content as authoritative | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Execution-provenance research argues generated contract language needs a traceable link to its specific source document and that document's approval status, since semantic similarity alone cannot distinguish an approved standard clause from a one-off negotiated exception | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- Liability caps, termination clauses, and renewal terms are written in highly standardized boilerplate language across most enterprise contracts, so embedding similarity is dominated by shared structural and legal phrasing rather than the specific negotiated terms that actually differ between contracts
- The contract repository is not partitioned or filtered by "canonical template" versus "customer-specific negotiated instance" before retrieval, so a one-off exception is exactly as retrievable as the approved standard
- No metadata check confirms the retrieved clause's source document is the designated template rather than an arbitrary prior customer contract
- The agent's output does not surface which source document a retrieved clause came from, so legal/deal-desk reviewers cannot quickly spot that the clause originated from an unrelated customer's contract

---

## Mitigation Strategies

1. **Canonical-Template Isolation**: Maintain the approved standard clause library as a separate, explicitly labeled retrieval source from the general contract repository, so retrieval for "standard clause" queries cannot return a customer-specific negotiated instance
2. **Source-Document Citation in Output**: Require every inserted clause to be tagged with its source document ID and approval status (standard template vs. customer-specific exception) visibly in the draft, so reviewers can catch a mismatch before signature
3. **Document-Level Match Verification**: Before inserting retrieved clause language, verify the retrieved chunk's parent document matches the intended canonical template document ID, not just that the chunk's text is semantically similar
4. **Pre-Signature Clause Diff**: Run an automated diff between every inserted clause and the actual approved standard-template text, flagging any deviation for legal review before the document is sent for signature

### Metrics
- Rate of inserted clauses whose source document is not the designated canonical template
- Number of post-signature audits finding a clause deviation that originated from a different customer's contract
- Document-level retrieval mismatch rate measured against a labeled template-vs-exception test set

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Non-template clause source | Inserted clause's source document ID does not match the canonical template library | P1 | Block document from being sent; route to legal for clause replacement |
| Unapproved clause deviation pre-signature | Automated diff finds inserted clause text deviates from approved standard language | P1 | Hold for legal review before signature |
| Recurring cross-customer retrieval | Multiple deals in a rolling window show clause retrieval sourced from a different customer's contract | P3 | Audit retrieval index partitioning between template and exception documents |

---

## References

- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
