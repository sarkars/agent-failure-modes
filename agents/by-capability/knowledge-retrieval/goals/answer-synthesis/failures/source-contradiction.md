# AI Agent Silently Picks One Answer When Retrieved Sources Disagree: Causes and Fixes

## Issue: AI agent's retrieved documents contain conflicting information, and the agent picks one arbitrarily instead of surfacing the disagreement.

**Frequency**: Common

**Symptoms**
- Answer arbitrarily picks one source over another
- Conflicting facts not acknowledged
- User gets wrong information from outdated source
- No indication that sources disagree
- Commonly reported in RAG pipelines (LangChain, LlamaIndex) that don't rank or timestamp retrieved documents before synthesis

**Root Cause**
Multiple documents may contain different information due to updates, errors, different contexts, or legitimate disagreement. Model must reconcile but often ignores conflicts.

**Example**
```
Retrieved documents:

Doc 1 (2023): "Maximum file upload size is 10MB"
Doc 2 (2024): "Maximum file upload size is 25MB"
Doc 3 (FAQ): "Large files up to 100MB supported for premium users"

Query: "What's the max file size I can upload?"

Agent: "The maximum file upload size is 10MB."

Reality: Picked oldest doc, ignored updates and context

Result: User can't upload files they should be able to
```

**Mitigation Strategies**
1. **Recency preference**: Prefer newer documents when conflicting
2. **Conflict detection**: Identify when sources disagree
3. **Transparent disagreement**: Report conflicts to user
4. **Source authority ranking**: Weight authoritative sources higher
5. **Context disambiguation**: Use user context to pick right answer
6. **Ensemble answers**: Show range of information found

**Detection**
- Track contradiction frequency in retrievals
- Monitor answer changes based on which source prioritized
- User feedback on conflicting information
- Automated conflict detection in retrieved sets

**How to fix it**: detect contradictions across retrieved sources, then prefer the most authoritative or recent one or surface the disagreement to the user — see Mitigation Strategies below.

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

- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Conflicting sources
- [Atlan: LLM Hallucinations 2026](https://atlan.com/know/llm-hallucinations/) - Source reconciliation
