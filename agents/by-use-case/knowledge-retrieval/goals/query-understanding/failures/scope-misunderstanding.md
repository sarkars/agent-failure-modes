# Scope Misunderstanding

## Issue: Agent Answers at Wrong Scope or Specificity

**Frequency**: Common

**Symptoms**
- Answer too broad when specific info needed
- Answer too narrow when overview requested
- Wrong product/version/context assumed
- Timeframe mismatch (current vs. historical)

**Root Cause**
Query doesn't specify scope, and model assumes wrong scope. Or scope is specified but not respected.

**Example**
```
Query: "What changed in the last update?"

Context: User is on mobile app
Retrieved: Web platform changelog (last update)

Agent: "The last update includes improved dashboard loading times, 
new keyboard shortcuts, and better multi-monitor support."

Reality: These are web features, not mobile app changes

Result: User looks for features that don't exist in their app
```

**Mitigation Strategies**
1. **Scope detection**: Identify product, version, timeframe from query
2. **User context**: Use known user attributes for scoping
3. **Scope confirmation**: "Are you asking about X or Y?"
4. **Metadata filtering**: Filter retrieval by scope
5. **Scope tagging**: Tag documents with applicable scope
6. **Explicit scope in answer**: "For the mobile app, ..."

**Detection**
- Track scope-related follow-up corrections
- Monitor scope filter usage and accuracy
- Compare query scope to answer scope
- User feedback on relevance

## References

- [CMARix: RAG & AI Trust Statistics 2026](https://www.cmarix.com/blog/rag-ai-statistics/) - Scope detection challenges
- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Context boundaries
