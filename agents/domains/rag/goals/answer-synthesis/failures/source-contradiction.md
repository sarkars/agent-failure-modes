# Source Contradiction

## Issue: Retrieved Documents Contain Conflicting Information

**Frequency**: Common

**Symptoms**
- Answer arbitrarily picks one source over another
- Conflicting facts not acknowledged
- User gets wrong information from outdated source
- No indication that sources disagree

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

## References

- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Conflicting sources
- [Atlan: LLM Hallucinations 2026](https://atlan.com/know/llm-hallucinations/) - Source reconciliation
