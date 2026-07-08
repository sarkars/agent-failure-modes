# Misgrounded Citation

## Issue: Citation Exists But Doesn't Support the Claim

**Frequency**: Common (contributes to 17-33% hallucination rate in legal RAG)

**Symptoms**
- Citations link to real documents
- Cited source doesn't actually support the claim made
- Source may be irrelevant to the topic
- Source may contradict the claim
- Users verify citation exists but miss that it's misapplied

**Root Cause**
RAG system retrieves and cites real documents, but the generation model incorrectly asserts the source supports a claim it doesn't. Unlike fabricated citations (which are easy to catch), misgrounded citations pass basic verification because the source exists - the failure is in the semantic relationship between claim and source.

**Example**
```
Query: "What standard applies to abortion regulations after Dobbs?"

RAG Response:
"After Dobbs, abortion regulations are subject to the undue burden
standard established in Casey. See Planned Parenthood v. Casey, 
505 U.S. 833 (1992)."

Problem:
- Casey citation is REAL and correctly formatted
- BUT Casey's undue burden standard was OVERRULED by Dobbs
- Correct answer: rational basis review now applies
- System cited real case but claim is completely wrong

Verification trap:
- User clicks citation link → Casey exists ✓
- User assumes citation validates the claim
- User doesn't realize Casey is no longer controlling law
```

**Key Statistics**
From Stanford Legal RAG Hallucinations Study (2025):
- Legal RAG tools hallucinate 17-33% of time
- Westlaw AI-Assisted Research: hallucination rate ~2x other tools
- Misgrounding is distinct from "incorrect" - claim may seem plausible
- Particularly insidious because citations pass basic verification

**Misgrounding Patterns**
- **Semantic mismatch**: Source discusses topic but doesn't support specific claim
- **Overruled precedent**: Cites law that's been superseded
- **Wrong jurisdiction**: Cites law from inapplicable jurisdiction
- **Dicta vs. holding**: Cites dicta as if it were binding
- **Distinguishable facts**: Case has different material facts

**Contributing Factors**
- Retrieval based on text similarity, not legal relevance
- Model doesn't understand legal hierarchy (holdings vs. dicta)
- No temporal awareness of legal changes
- Jurisdictional context not properly weighted
- Generation model "looks for support" rather than validates claims

**Mitigation Strategies**
1. **Citation verification**: Check source actually supports claim
2. **Temporal validation**: Verify cited law is still good law
3. **Jurisdictional filtering**: Ensure sources match query jurisdiction
4. **Claim-source alignment scoring**: Measure semantic match
5. **Citation explanation**: Require explanation of how source supports claim

**Detection**
- Expert review of claim-source relationships
- Automated citation verification systems (Shepard's, KeyCite)
- User feedback on "citation didn't support claim"
- A/B testing with domain expert evaluation


## Mitigation Strategies

### Prevention

1. **Implement query-answer consistency validation**: Decompose complex queries into atomic components and verify each component is addressed in the answer before returning. Use RAGAS Answer Relevancy metric (target: >0.75) with automatic re-generation for scores below threshold. Root cause mitigation: Prevents context-anchoring by explicitly binding answer generation to parsed query intent.

2. **Apply multi-source consensus verification**: Require answers synthesized from multiple sources to explicitly cite which sources support each claim and flag unresolved contradictions. Implementation: Use semantic similarity checks across source fragments to detect cherry-picked evidence patterns. Root cause: Ensures balanced representation of evidence when sources conflict.

3. **Enforce comprehensive coverage checks**: Implement structured extraction requiring explicit treatment of caveats, limitations, exceptions, and counterevidence for each claim type. Use template responses with mandatory caveat sections. Root cause: Prevents omission of qualifying information that would change user decision-making.

### Detection & Response

1. **Answer completeness monitoring**: Measure coverage of query intents in generated answers. Track query decomposition rate (% of query components explicitly addressed) and flag responses with coverage <85%. Instrument RAG pipeline to log query-answer similarity scores per component. Alert on sustained scores <0.70.

2. **Evidence balance scoring**: For each answer, compute evidence distribution across sources and flag one-sided responses (>70% from single source on multi-source queries). Implement automated extraction of caveat/limitation mentions and track inclusion rates by query type. Target: >80% of medical/financial answers include relevant caveats.

### Architecture Patterns

1. Query Intent Decomposition Graph: Parse complex queries into a DAG of atomic intents before retrieval. Each retrieved document is mapped to specific intent nodes. Answer generation must satisfy all leaf nodes. Validation layer computes coverage before response generation.

2. Evidence Consensus Engine: Maintain a fact graph where each claim is attributed to specific sources with confidence scores. Multi-source claims require consensus computation (intersection of sources supporting claim). Flagging layer surfaces contradictions to generation model.

3. Structured Response Templates: Use task-specific response schemas that enforce inclusion of: primary answer, supporting evidence, relevant caveats/exceptions, alternative interpretations, confidence bounds. Auto-flag template violations before user delivery.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Answer Relevancy Score | >0.75 | <0.70 | RAGAS metric on generated answers vs. original query |
| Query Coverage Rate | >90% | <85% | Percentage of query components explicitly addressed in answer |
| Evidence Balance Index | >0.6 | <0.4 | Distribution of citations across sources (Gini coefficient, 0=balanced, 1=single-source) |
| Caveat Inclusion Rate | >80% | <70% | Percentage of medical/financial answers including relevant limitations |
| User Clarification Rate | <5% | >10% | Percentage of answered queries requiring follow-up clarification |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Low Answer Relevancy | Answer Relevancy Score < 0.70 for >5% of queries in 1-hour window | HIGH | Page on-call; trigger re-generation with query reinforcement prompt |
| Single-Source Dominance | Evidence Balance Index < 0.4 on multi-source queries for >3 consecutive queries | MEDIUM | Log event; audit cherry-picking patterns in retrieval/synthesis |
| Rising Clarification Demand | User Clarification Rate exceeds 10% (vs. 5% baseline) over 24-hour window | HIGH | Investigate query decomposition or answer template effectiveness |


## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - 17-33% hallucination rate in legal RAG tools
- [Journal of Empirical Legal Studies](https://doi.org/10.1111/jels.12413) - First empirical study of legal AI hallucinations
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Verification failures
