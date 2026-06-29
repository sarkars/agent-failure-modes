# Embedding Retrieval Applies Wrong Jurisdiction's Clause Template by Name Similarity

## Issue: A Drafting Agent Asked to Insert a Jurisdiction-Specific Clause (a Non-Compete, a Consumer-Arbitration Provision, a Statutory Notice) for a Contract Governed by One State or Country's Law Retrieves the Clause From a Multi-Jurisdiction Template Library Using Semantic Similarity Over the Clause's General Subject Matter, Rather Than Matching Strictly on Governing Jurisdiction, and Pulls a Differently-Jurisdictioned Template That Is Lexically Almost Identical but Legally Ineffective or Unenforceable Under the Contract's Actual Governing Law

**Frequency**: Common

**Symptoms**
- Drafted contract contains a jurisdiction-specific clause (e.g., a non-compete, an arbitration carve-out, a statutory consumer notice) whose substantive requirements match a different jurisdiction than the one actually governing the contract
- The retrieved clause reads as well-formed and topically correct -- it is, after all, a real template for the same general clause type -- but its enforceability conditions, required statutory language, or permitted scope reflect the wrong jurisdiction's rule
- The error is concentrated on clause types where many jurisdictions regulate the same general topic with similar-sounding statutory requirements but materially different substantive rules (non-compete enforceability standards, consumer-arbitration opt-out language, data-breach notice triggers), since those clauses are the most lexically similar to one another across jurisdictions in the template library
- Legal review or opposing counsel's redline catches the wrong-jurisdiction clause only after the document is drafted or issued, rather than during retrieval
- Re-running the same drafting request with retrieval restricted to a deterministic lookup keyed to the contract's actual governing-law jurisdiction (rather than free-text similarity search over clause subject matter) correctly returns the applicable template, isolating retrieval as the point of failure

**Root Cause**
The drafting agent's retrieval step ranks candidate jurisdiction-specific clause templates by embedding similarity over the clause's subject matter and general legal language, rather than by a deterministic match keyed to the contract's actual governing-law jurisdiction. Statutory and clause-type names recur across jurisdictions precisely because many jurisdictions regulate the same underlying activity (non-competes, arbitration, breach notice), producing templates that are highly similar in vocabulary and structure but differ in the specific substantive rule that controls enforceability -- the exact condition under which similarity-based retrieval reliably confuses jurisdiction-distinct but topically near-identical source documents.

**Example**
```
Drafting agent is asked to insert a non-compete clause into an employment agreement governed by the law of State A
Clause-template library holds non-compete templates for many states, including State A and several others with similarly structured (but substantively different) enforceability standards -- some impose salary thresholds, some ban non-competes outright for certain worker classes, some allow broader geographic scope than State A permits
Agent's retrieval, ranking by similarity to "non-compete clause for employment agreement," surfaces a template from a different state whose clause language is over 90% lexically identical to State A's template but omits a mandatory consideration-and-notice requirement that State A's statute requires for enforceability
Drafted agreement is executed with the wrong-jurisdiction non-compete language; the clause is later found unenforceable in litigation because it lacks the consideration disclosure State A's statute requires, a defect traceable directly to the wrong template having been retrieved
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrievers in legal RAG systems frequently select content from the wrong source document because legal text addressing the same subject matter across different jurisdictions shares dense, structurally similar vocabulary that confuses similarity-based ranking | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Document-Level Retrieval Mismatch rates exceeding 95% were observed on structurally standardized legal document sets, attributed to linguistic homogeneity across near-identical but substantively distinct source documents | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Surveys of LLM evaluation in legal applications note that legal tasks span multiple jurisdictions with materially different substantive rules, and that benchmark and deployment methodologies must account for jurisdiction as a first-class variable rather than treating legal text as a single undifferentiated domain | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |

**Contributing Factors**
- Template library is organized and searched primarily by clause type and subject matter rather than indexed first by governing jurisdiction
- No deterministic pre-filter restricts candidate templates to the contract's actual governing-law jurisdiction before similarity ranking over clause text is applied
- Jurisdiction metadata is present on each template but not surfaced as a high-salience, checkable field in the agent's retrieval context, so the model has no strong signal to prefer it over topical similarity
- Clause types regulated similarly-but-differently across many jurisdictions (non-competes, arbitration, statutory notices) are common enough that this retrieval confusion is structural rather than a rare edge case

---

## Mitigation Strategies

1. **Jurisdiction-First Deterministic Filter**: Restrict candidate clause templates to the contract's actual governing-law jurisdiction via a deterministic lookup before any similarity-based ranking over clause subject matter is applied
2. **Surface Governing-Law Metadata as a Required Field**: Require the retrieved template's jurisdiction and statutory citation to be displayed alongside the contract's actual governing-law jurisdiction so a mismatch is visually checkable before the draft proceeds
3. **Cross-Jurisdiction Near-Duplicate Audit**: Periodically scan the template library for clause templates with closely overlapping subject matter across different jurisdictions and flag those clusters for mandatory deterministic jurisdiction-based routing rather than similarity search
4. **Enforceability Cross-Check Gate**: Require an automated, non-LLM verification step confirming the retrieved clause's statutory citation and substantive requirements (thresholds, required notices) match the contract's actual governing-law jurisdiction before the draft is finalized

### Metrics
- Rate of drafted contracts where a jurisdiction-specific clause's template jurisdiction does not match the contract's actual governing-law jurisdiction, sampled via review
- Count of cross-jurisdiction near-duplicate clause clusters identified in the template library without a deterministic-routing rule in place
- Time between draft issuance and detection of a wrong-jurisdiction clause error, by detection method

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Governing-law citation mismatch | Retrieved clause's statutory citation does not match the contract's recorded governing-law jurisdiction | P1 | Block finalization; route to legal review for correct-jurisdiction template |
| Cross-jurisdiction near-duplicate detected | New template added to library creates a near-duplicate cluster with an existing template from a different jurisdiction | P3 | Add deterministic jurisdiction-routing rule for the cluster |
| Recurring mismatch on same clause type | Multiple wrong-jurisdiction errors traced to the same clause type (e.g., non-compete, arbitration) | P2 | Audit retrieval configuration for that clause type |

---

## References

- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
