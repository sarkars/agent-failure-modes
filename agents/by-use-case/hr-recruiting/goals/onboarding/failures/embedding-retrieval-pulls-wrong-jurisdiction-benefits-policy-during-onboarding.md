# Embedding Retrieval Pulls Wrong-Jurisdiction Benefits Policy During Onboarding

## Issue: An Onboarding Agent's Retrieval Step Surfaces a Benefits-Eligibility Policy Document for a Similarly Named but Different Work Jurisdiction or Employment Classification, and the New Hire Is Told Incorrect Eligibility Terms Because the Embedding Match Favored Lexical Similarity Over an Exact Jurisdiction/Classification Match

**Frequency**: Common

**Symptoms**
- A new hire in a contractor or international-employee classification is told benefits-eligibility terms that actually apply to the standard full-time domestic-employee policy document, because that document was retrieved instead of the classification-specific one
- The retrieved document and the correct document share most of their section headers and much of their boilerplate language, differing only in a few jurisdiction- or classification-specific clauses, which is exactly the pattern that produces a high embedding-similarity score despite being the wrong document
- Asking the onboarding agent to cite its source shows it retrieved the general policy document by similarity score, without first filtering candidate documents by the new hire's recorded jurisdiction or employment classification
- The miss concentrates on new hires whose jurisdiction or classification is less common in the document corpus, since the standard domestic full-time policy document dominates the embedding space and is the nearest match for almost any benefits query
- Running the same query with an explicit jurisdiction or classification filter applied before the similarity search returns the correct document every time

**Root Cause**
The onboarding agent's retrieval step ranks candidate policy documents by embedding similarity to the new hire's benefits question, but benefits-policy documents for different jurisdictions or employment classifications are written from a shared template and differ in only a small fraction of their text, so the document's overall semantic embedding is dominated by the shared boilerplate rather than the jurisdiction- or classification-specific clauses that actually determine which document applies. Without a hard filter on jurisdiction or classification metadata applied before the similarity ranking, the search returns the most common document in the corpus rather than the one that is actually correct for this new hire.

**Example**
```
New hire is classified as an international remote employee under a local employer-of-record arrangement
Onboarding agent retrieves "benefits eligibility policy" via embedding similarity search to answer the new hire's question about waiting periods
Search returns the standard domestic full-time policy document, since it shares nearly all section headers and boilerplate with the employer-of-record policy and dominates the embedding space
Onboarding agent tells the new hire benefits begin after the standard 30-day waiting period
Employer-of-record arrangement actually specifies immediate benefits eligibility with no waiting period, a difference the agent never surfaced because it never retrieved the correct document
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of retrieval-augmented generation systems identify embedding-similarity retrieval favoring documents with high lexical or structural overlap over documents that are substantively correct as a distinct and recurring error category | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Taxonomies of RAG system errors find that retrieval components frequently surface a superficially similar but substantively wrong document when candidate documents share a common template and differ only in a small distinguishing fraction of their content | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Research on memory and retrieval mechanisms in autonomous LLM agents identifies the absence of metadata-based pre-filtering before similarity ranking as a contributing factor in retrieval errors for template-derived document sets | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |

**Contributing Factors**
- Benefits-policy documents for different jurisdictions and employment classifications are derived from a shared template, producing high embedding similarity across documents that have materially different eligibility terms
- The retrieval step does not apply a hard filter on the new hire's recorded jurisdiction or employment classification before ranking candidate documents by similarity
- Less common classifications (contractor, employer-of-record, international remote) are underrepresented in the document corpus relative to the standard domestic full-time policy, so similarity search defaults toward the dominant document

---

## Mitigation Strategies

1. **Mandatory Metadata Pre-Filter Before Similarity Ranking**: Require the retrieval step to filter candidate policy documents by the new hire's recorded jurisdiction and employment classification before any embedding-similarity ranking is applied, rather than relying on similarity alone to select the correct document
2. **Distinguishing-Clause Embedding Weighting**: For template-derived document sets, weight the embedding representation toward the jurisdiction- or classification-specific clauses that actually differ between documents, rather than the full document text dominated by shared boilerplate
3. **Confidence Threshold on Cross-Classification Matches**: Flag any retrieval result where the matched document's recorded jurisdiction or classification metadata does not match the new hire's recorded classification, even if the similarity score is high
4. **Underrepresented-Classification Coverage Audit**: Periodically audit retrieval accuracy specifically for less common classifications, since they are the population most likely to be overridden by the dominant document in the corpus

### Metrics
- Rate of benefits-policy retrievals where the matched document's jurisdiction/classification metadata does not match the new hire's recorded classification
- Retrieval accuracy broken out by employment classification, to surface underrepresented-classification degradation
- Rate of new-hire benefits questions requiring correction after the initial onboarding-agent answer

### Alerts
- A benefits-policy document is retrieved and presented to a new hire whose recorded jurisdiction or classification does not match the document's metadata → P1
- Retrieval accuracy for any employment classification falls below the defined threshold for a rolling window → P2
- A new hire reports incorrect benefits-eligibility information traced to an onboarding-agent answer → P2

---

## References

- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
