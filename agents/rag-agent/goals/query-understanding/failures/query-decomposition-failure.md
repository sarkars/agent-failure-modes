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

## References

- [RAGAS Multi-hop](https://docs.ragas.io/en/latest/concepts/testset_generation.html) - Multi-hop evaluation
- [Query Decomposition](https://arxiv.org/abs/2205.10625) - Decomposition strategies
- [Self-Ask](https://arxiv.org/abs/2210.03350) - Compositional reasoning
- [IR-CoT](https://arxiv.org/abs/2212.10509) - Retrieval-augmented reasoning
