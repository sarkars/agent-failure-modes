# Citation Doesn't Support Claim

## Issue: Cited Source Doesn't Actually Support the Claim Made

**Frequency**: Common

**Symptoms**
- Citation exists and source exists, but claim isn't in source
- Source says something different than claim
- Claim is inference not stated in source
- Citation is tangentially related but doesn't support specific claim

**Root Cause**
Model may make a claim, then attach a citation to a related source that doesn't actually support the specific statement made.

**Example**
```
Agent response: "The company guarantees 99.9% uptime [1]"

Source [1] actual text: "We strive to maintain high availability 
for all services."

Gap: "Strive to maintain high availability" ≠ "guarantees 99.9%"

Result: User believes guarantee exists when it doesn't
```

**Mitigation Strategies**
1. **Extractive verification**: Require quoted text to match citation
2. **NLI checking**: Use entailment model to verify support
3. **Claim-source matching**: Explicitly verify claim is in source
4. **Conservative claims**: Only state what source explicitly says
5. **Inference labeling**: Mark when claim is inference vs. stated
6. **Quote requirements**: Include direct quote alongside citation

**Detection**
- NLI-based claim-source entailment checking
- Compare claim text to cited content
- Track support verification failure rate
- User reports of misleading citations


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
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Claims without support
- [Self-Healing RAG Layer](https://towardsdatascience.com/rag-hallucinates-i-built-a-self-healing-layer-that-fixes-it-in-real-time/) - Citation verification
