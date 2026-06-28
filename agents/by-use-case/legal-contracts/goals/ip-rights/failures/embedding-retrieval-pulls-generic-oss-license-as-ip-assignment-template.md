# Embedding Retrieval Pulls Generic OSS License as IP Assignment Template

## Issue: A Contract-Drafting Agent's RAG Step, Asked to Retrieve the Company's Standard Work-for-Hire IP-Assignment Template for a New Contractor Agreement, Retrieves a Lexically and Semantically Similar but Substantively Different Document -- An Open-Source Contributor License Agreement or Inbound-IP Template -- Because Both Documents Share Dense "Intellectual Property," "Assignment," and "License Grant" Vocabulary

**Frequency**: Occasional

**Symptoms**
- Drafted contractor agreement contains IP language granting the company a license to use the contractor's work rather than a full assignment of ownership, because the retrieved template was built for an inbound open-source contribution scenario, not a work-for-hire engagement
- The retrieved clause's defined terms ("Contribution," "Licensor") do not match the rest of the contractor agreement's defined terms ("Work Product," "Contractor"), a mismatch only visible on close manual read
- Re-running the same retrieval query with the literal phrase "work-for-hire assignment" instead of "intellectual property terms" returns the correct template, showing the failure is a query-phrasing-to-embedding-space mismatch rather than the correct template being absent from the library
- Legal ops discovers the gap only when a contractor later claims they retained ownership of deliverables, pointing to the license-grant language the agent actually inserted
- The mismatch concentrates on templates with high lexical overlap in the IP domain (OSS licenses, inbound license agreements, assignment agreements), where surface vocabulary similarity is highest and the actual legal effect is most different

**Root Cause**
The drafting agent's RAG step selects a template by embedding-similarity over document text rather than by a structured template-category tag (e.g., `template_type: contractor-ip-assignment` vs. `template_type: oss-contributor-license`). OSS contributor license agreements and work-for-hire IP-assignment agreements are drafted by the same legal teams using overlapping clause vocabulary, so they sit close together in embedding space even though one transfers no ownership and the other transfers full ownership -- the retrieval step has no signal that distinguishes "similar wording" from "same legal effect."

**Example**
```
Drafting request: "Generate the IP terms section for a new software-development contractor agreement"
RAG query embeds the request and searches the template library by semantic similarity
Highest-similarity match: the company's open-source-contributor-license-agreement template (high lexical overlap: "intellectual property," "license," "grant," "ownership")
Correct match (lower similarity score due to different phrasing conventions): the company's work-for-hire IP-assignment template
Agent inserts the OSS contributor-license language; contractor agreement now grants the company a license to use the contractor's code rather than assigning ownership
Six months later, contractor asserts ownership of the delivered codebase, citing the license-grant clause the agent itself inserted
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval reliability in large legal document corpora is a documented open problem, with semantically similar but legally distinct documents frequently confused by similarity-based retrieval | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Version and variant control for legal documents is identified as a distinct technical challenge from general document retrieval, precisely because near-duplicate documents can carry materially different legal effect | [Version Control for Legal Documents](https://arxiv.org/abs/2108.06421) |
| Surveys of LLMs in legal applications flag template and clause-retrieval accuracy as a key unresolved evaluation gap for production legal-drafting systems | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |

**Contributing Factors**
- Template library has no structured `template_type` or `legal_effect` tag that retrieval can filter on before or alongside semantic similarity
- OSS contributor-license and work-for-hire-assignment templates were authored by the same legal team and share boilerplate IP vocabulary, maximizing embedding-space proximity between documents with opposite legal effect
- No post-retrieval check compares the retrieved template's defined terms against the rest of the contract being drafted to flag a terminology mismatch

---

## Mitigation Strategies

1. **Structured Template-Type Filter Before Semantic Search**: Require the RAG step to filter candidate templates by a structured `template_type` field matching the drafting task's contract category before ranking by semantic similarity, rather than relying on similarity ranking alone
2. **Defined-Terms Consistency Check**: After retrieval, automatically compare the retrieved clause's defined terms against the rest of the contract being drafted and flag a mismatch (e.g., "Contribution" vs. "Work Product") for human review before insertion
3. **Legal-Effect Tagging at Template Authoring Time**: Require every template added to the library to be tagged with its legal effect (assignment vs. license vs. waiver) as structured metadata, independent of its prose content, so retrieval can be effect-aware
4. **Sampled Retrieval Audits on High-Overlap Template Families**: Periodically sample retrieval results for template families known to have high lexical overlap but different legal effect (IP assignment vs. license; NDA vs. confidentiality side letter) and verify the correct template was retrieved

### Metrics
- Rate of drafted contracts where the inserted template's `template_type` tag does not match the requested contract category
- Number of defined-terms mismatches flagged between retrieved clause and surrounding contract per drafting session
- Retrieval precision@1 measured specifically within high-lexical-overlap template families, not just overall

### Alerts
- A drafted contract is finalized with a retrieved template whose `template_type` tag does not match the requested category → P1
- Defined-terms consistency check finds a mismatch between retrieved clause and contract body and the document proceeds to signature without resolution → P1
- Retrieval precision@1 within a high-overlap template family drops below baseline for two consecutive drafting batches → P2

---

## References

- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [Version Control for Legal Documents](https://arxiv.org/abs/2108.06421)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
