# Query Decomposition Failure

## Issue: Complex Query Broken Into Wrong Subqueries

**Frequency**: Common

**Symptoms**
- Multi-part question partially answered
- Subquery misses original intent
- Decomposition introduces errors or ambiguity
- Parallel subqueries return contradictory results
- Final synthesis doesn't address original query

**Root Cause**
Complex queries are often decomposed into simpler subqueries for better retrieval. However, decomposition can fail: splitting at wrong boundaries, losing critical constraints, or creating subqueries that drift from original intent. RAGAS evaluates query decomposition quality through multi-hop reasoning metrics - each hop must maintain fidelity to the original question.

**Example**
```
Original query: "Compare our Q1 revenue in Europe to 
competitors who launched products in the same quarter"

Poor decomposition:
1. "What was our Q1 revenue?"
   - Misses: Europe constraint
2. "Who are our competitors?"
   - Misses: Same quarter launch constraint
3. "What products launched in Q1?"
   - Misses: Competitor context

Results retrieved:
- Global Q1 revenue (wrong scope)
- General competitor list (no launch filter)
- All Q1 launches (includes us, not just competitors)

Final answer: Compares wrong revenue to wrong competitors

Better decomposition:
1. "What was our Q1 revenue in Europe specifically?"
2. "Which competitors launched products in Q1?"
3. "What was the Q1 Europe revenue for [competitor names]?"

RAGAS multi-hop evaluation:
  Decomposition quality: 0.45 (poor)
  Constraint preservation: 2/4 constraints lost
  Final answer accuracy: 0.38
```

**Key Statistics**
From Query Decomposition Research (2026):
- Multi-part queries: 30-40% of complex questions
- Decomposition errors: 25-35% lose constraints
- Constraint preservation: 65-75% average
- Synthesis from bad decomposition: 40% accuracy drop
- LLM decomposition vs rule-based: More flexible but less reliable

**Decomposition Failure Types**
| Type | Description | Impact |
|------|-------------|--------|
| Constraint loss | Filters dropped in subquery | Wrong scope |
| Boundary errors | Split mid-concept | Semantic break |
| Dependency miss | Subqueries need ordering | Wrong results |
| Over-decomposition | Too many fragments | Context loss |
| Under-decomposition | Still too complex | Retrieval fails |

**Contributing Factors**
- LLM decomposition without validation
- No constraint tracking across subqueries
- Independent subquery execution
- No final verification against original
- Complex implicit constraints
- Domain-specific query structures

**Mitigation Strategies**
1. **Constraint extraction**: Explicit constraint tracking
2. **Decomposition validation**: Verify subqueries cover original
3. **Dependency ordering**: Respect subquery dependencies
4. **Iterative refinement**: Decompose → retrieve → refine
5. **Final verification**: Check answer addresses original query
6. **Minimal decomposition**: Prefer fewer, more complete subqueries

**Detection**
- Track constraint preservation rate
- Compare final answer to original query
- Monitor partial answer rates
- Analyze subquery-original semantic similarity
- Measure multi-hop reasoning accuracy


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

- [RAGAS Multi-hop](https://docs.ragas.io/en/latest/concepts/testset_generation.html) - Multi-hop evaluation
- [Query Decomposition](https://arxiv.org/abs/2205.10625) - Decomposition strategies
- [Self-Ask](https://arxiv.org/abs/2210.03350) - Compositional reasoning
- [IR-CoT](https://arxiv.org/abs/2212.10509) - Retrieval-augmented reasoning
