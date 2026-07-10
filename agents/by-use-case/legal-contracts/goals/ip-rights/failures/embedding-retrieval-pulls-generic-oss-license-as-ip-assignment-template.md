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

### Prevention

1. **Structured template-type filtering before semantic-similarity ranking**: Implement template-retrieval pipeline: (a) Every template tagged with structured fields: {template_type (enum: contractor-ip-assignment, oss-contributor-license, inbound-license, ip-waiver, etc.), legal_effect (enum: full-assignment, limited-license, waiver, cross-license), contract_category, jurisdiction}, (b) RAG query includes explicit intent signal (e.g., "Need IP terms for: contractor work-for-hire assignment"), (c) Retrieval first filters by template_type and legal_effect matching the intent, (d) Only within filtered set apply semantic similarity ranking, (e) Retrieve top 3 candidates; require drafter to select one + confirm legal effect before insertion. Root cause: Prevents high-lexical-overlap documents from being ranked by similarity alone.

2. **Legal-effect matching at retrieval-intent stage**: Before RAG query, parse drafting request for legal-effect signals: "work-for-hire" → search for legal_effect='full-assignment', "licenseonly" → search for legal_effect='limited-license'. Map drafting intent to required legal effect, then constrain retrieval: retrieve only templates with matching legal_effect tag. If no templates match, return None and escalate to human drafter: "No templates found with legal effect: full-assignment. Please manually select." Root cause: Ensures retrieval is effect-aware, not just vocabulary-aware.

3. **Defined-terms and key-concept consistency checking post-retrieval**: After template retrieved, automatically: (a) extract defined terms from retrieved template (e.g., "Contribution", "Licensor", "Work Product", "Contractor"), (b) extract defined terms from drafting context (existing clauses, party names, roles), (c) compare sets: flag if >20% of key terms are disjoint or map to different parties (e.g., template says "Licensor" but contract says "Contractor"), (d) if mismatch detected, flag for human review before insertion, show side-by-side comparison. Root cause: Detects unsuitable templates before they're inserted into contract.

### Detection & Response

1. **Retrieval audit logging with effect-matching verification**: For each template retrieval, log: {query_intent, requested_legal_effect, retrieved_template_id, template_type_tag, template_legal_effect_tag, semantic_similarity_score, effect_match_status (MATCH/MISMATCH), defined_terms_check_result (PASS/FLAG), drafter_action_taken}. Run daily audit: sample 5% of retrievals from past 24h, verify: (a) template_legal_effect matches query intent, (b) semantic_similarity_score for correct-effect templates is within 10% of retrieved-template score. Alert if: mismatch rate >2%, or correct-effect templates ranked >2 positions lower than retrieved templates.

2. **Template-family collision detection and monitoring**: Identify high-lexical-overlap template families (contractor-ip-assignment vs. oss-contributor-license, nda vs. confidentiality-side-letter). For these families, monitor retrieval precision: weekly, run 10 queries designed to retrieve each template type, measure precision@1 for effect-correct template. Alert if precision drops >5% vs. baseline. Trigger root-cause analysis if collision family shows degradation.

### Architecture Patterns

1. **Effect-First Template Retrieval Engine**: Parse drafting intent → Infer legal_effect requirement → Filter template_index by legal_effect → Retrieve top-3 candidates by semantic_similarity → Rank by defined-terms consistency with drafting context → Return ranked candidates with effect-match and term-consistency scores. Drafter confirms selection + effect before insertion. Logs all decisions for audit.

2. **Template Tagging & Metadata Registry**: Maintains curated template library with structured fields: template_id, template_name, template_type, legal_effect, contract_category, defined_terms[], high_collision_family (boolean), last_updated, usage_count. Enables filtering and effect-aware retrieval. Collision-family flag triggers enhanced monitoring and defined-terms checking.

3. **Defined-Terms Consistency Validator**: On template insertion, extracts defined_terms from template and compares against contract-drafting context. Builds term-mapping rules: "if template uses 'Licensor' and contract says 'Contractor', flag mismatch". Flags high-risk mismatches (definitions that imply different ownership intent) before insertion.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Template Retrieval Legal-Effect Accuracy | >99% | <98% | # of retrievals with legal_effect matching query intent / total retrievals |
| High-Collision-Family Precision@1 | >98% | <95% | # of retrievals returning effect-correct template in position 1 for high-overlap families / total queries for those families |
| Defined-Terms Mismatch Detection Rate | >95% | <90% | # of defined-terms mismatches caught by automated checker before insertion / total mismatches in audited drafts |
| Template Category Match Rate | 100% | <99% | # of finalized contracts using templates matching requested contract_category / total drafted contracts |
| Post-Signature Legal-Effect Disputes | 0% | >0.5% | # of post-execution disputes attributing to template legal-effect mismatch / total executed contracts |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Effect-Mismatched Template Retrieved | Template with legal_effect not matching query intent ranked #1 | CRITICAL | Block insertion; escalate to drafter with explanation; require manual selection from effect-filtered candidates |
| Defined-Terms Inconsistency Flagged | Defined-terms consistency check finds >20% mismatch between template and contract context | HIGH | Prevent insertion into contract; show side-by-side term comparison; require drafter confirmation that mismatch is intentional |
| Collision-Family Precision Degradation | Retrieval precision@1 for high-lexical-overlap family drops >5% for 3 consecutive days | HIGH | Investigate retrieval engine performance; audit recent queries; may require re-tuning effect-filtering weights |
| Legal-Effect Mismatch Discovered Post-Signature | Post-execution, contract discovered to have legal_effect not matching original drafting intent | CRITICAL | Legal escalation; assess enforceability and remediation; audit all contracts drafted in same session; may require amendment |

---

## References

- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [Version Control for Legal Documents](https://arxiv.org/abs/2108.06421)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
