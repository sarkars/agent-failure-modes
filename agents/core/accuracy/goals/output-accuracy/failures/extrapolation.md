# Extrapolation Beyond Data

## Issue: Agent Makes Unsupported Inferences

**Frequency**: Very Common

**Symptoms**
- Conclusions drawn beyond what data supports
- Correlation stated as causation
- Trends projected without basis
- Generalizations from limited examples

**Root Cause**
LLMs are pattern-completion machines that naturally extend patterns. They may extrapolate beyond available evidence without signaling this.

**Example**
```
Data: "Revenue was $1M in Q1, $1.2M in Q2, $1.4M in Q3"

Agent: "Based on this trend, Q4 revenue will be approximately $1.6M, 
and annual revenue will reach $8M by 2026."

Reality: No data supports future projections. Q4 actual: $1.1M (seasonal dip)

Result: User makes decisions based on unsupported projections
```

**Mitigation Strategies**
1. **Explicit grounding**: Only state what data directly supports
2. **Inference labeling**: Mark extrapolations as such
3. **Uncertainty bounds**: Provide confidence intervals for projections
4. **Source requirements**: Require sources for quantitative claims
5. **Hedged language**: Use "may", "might", "could" for inferences
6. **Inference limits**: Restrict how far agent can extrapolate

**Detection**
- Compare claims to source data coverage
- Flag unsourced quantitative statements
- Track inference accuracy over time
- Audit projection vs. actual outcomes

---

## References

- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Analysis of extrapolation-related hallucinations in RAG pipelines
- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Coverage of unsupported inference patterns
