# Missing Citations

## Issue: Claims Made Without Attribution

**Frequency**: Common

**Symptoms**
- Factual claims lack source references
- Some statements cited, others not
- User can't verify important claims
- Inconsistent citation coverage

**Root Cause**
- Model doesn't consistently apply citation requirement
- Some claims feel "obvious" so not cited
- Citation instructions not emphasized
- Trade-off between readability and attribution

**Example**
```
Agent response: 
"The policy was updated in 2024 [1]. Employees can now work 
remotely up to 3 days per week. Manager approval is required 
for international travel [2]."

Missing citation: "3 days per week" claim has no reference

User question: Where does it say 3 days? Could be 2 or 4.

Result: User can't verify key detail
```

**Mitigation Strategies**
1. **Cite-every-claim rule**: Explicit instruction to cite all facts
2. **Citation density targets**: Minimum citations per response
3. **Structured output**: Require citation field for each claim
4. **Post-processing check**: Flag uncited factual claims
5. **Highlight uncited**: Visually mark claims without sources
6. **Self-review prompt**: "Verify all claims have citations"

**Detection**
- Count factual claims vs. citations
- Track citation density by response
- Flag responses with low citation coverage
- User feedback on unverifiable claims

## References
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Uncited claims
- [CMARix: RAG & AI Trust Statistics 2026](https://www.cmarix.com/blog/rag-ai-statistics/) - Citation coverage gaps
