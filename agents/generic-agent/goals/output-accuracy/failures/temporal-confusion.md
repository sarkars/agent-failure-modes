# Temporal Confusion

## Issue: Agent Confuses Timeframes or Uses Outdated Information

**Frequency**: Common

**Symptoms**
- Agent uses training data as current fact
- Past events described as ongoing
- Future events described as completed
- Version numbers, dates, or status outdated

**Root Cause**
LLMs have knowledge cutoffs and don't inherently track time. They may present training data as current truth even when information has changed.

**Example**
```
User: "Who is the CEO of Example Corp?"

Agent: "John Smith is the CEO of Example Corp. He's been leading 
the company since 2019."

Reality: John Smith resigned in 2024. Jane Doe is current CEO.

Result: User acts on outdated information
```

**Mitigation Strategies**
1. **Timestamp awareness**: Include dates in retrieved information
2. **Recency signals**: Indicate when information was last verified
3. **Real-time retrieval**: Fetch current data for time-sensitive queries
4. **Knowledge cutoff disclosure**: State when training data ends
5. **Freshness requirements**: Flag queries needing current data
6. **Version tracking**: Explicitly track versions for software/products

**Detection**
- Compare outputs to current authoritative sources
- Track corrections related to outdated information
- Monitor queries about recent events
- Audit time-sensitive information regularly

---

## References

- [Atlan: LLM Hallucinations 2026](https://atlan.com/know/llm-hallucinations/) - Overview of temporal hallucination patterns in LLMs
- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Analysis of time-related hallucination causes in RAG systems
