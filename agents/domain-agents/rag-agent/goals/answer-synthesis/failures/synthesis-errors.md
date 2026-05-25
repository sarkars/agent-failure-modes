# Synthesis Errors

## Issue: Model Incorrectly Combines Information from Multiple Sources

**Frequency**: Common

**Symptoms**
- Facts from different entities merged incorrectly
- Temporal mixing (past/present confused)
- Attributes assigned to wrong subjects
- Calculations or aggregations wrong

**Root Cause**
When synthesizing from multiple sources, model may incorrectly associate facts with wrong entities or contexts.

**Example**
```
Retrieved context:

Doc 1: "Product A: Price $99, ships in 2-3 days"
Doc 2: "Product B: Price $149, includes free installation"

Query: "Tell me about Product A"

Agent: "Product A costs $99 and includes free installation, 
shipping in 2-3 days."

Error: Free installation is from Product B, not A

Result: User expects installation that won't be provided
```

**Mitigation Strategies**
1. **Entity tracking**: Maintain clear entity-attribute associations
2. **Structured extraction**: Extract to schema before synthesizing
3. **Single-source answers**: Prefer one authoritative source per fact
4. **Attribution requirements**: Cite source for each claim
5. **Validation checks**: Verify synthesized facts against sources
6. **Chain-of-thought**: Show reasoning for synthesis

**Detection**
- Cross-check synthesized facts against individual sources
- Track entity-attribute assignment accuracy
- Monitor multi-source synthesis errors
- User reports of mixed-up information

## References

- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Synthesis failures
- [FloTorch: 2026 RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Multi-source synthesis
