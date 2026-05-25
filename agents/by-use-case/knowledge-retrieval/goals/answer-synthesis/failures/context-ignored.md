# Context Ignored

## Issue: Model Ignores Retrieved Context

**Frequency**: Common

**Symptoms**
- Answer doesn't use information from retrieved documents
- Generic response when specific info was available
- Model responds from parametric knowledge instead
- Context provided but not reflected in answer

**Root Cause**
- Prompt doesn't emphasize context usage
- Context buried in long prompt
- Model attention focuses elsewhere
- Context format not conducive to extraction

**Example**
```
Retrieved context:
"Our return policy allows returns within 30 days. Items must be 
unopened and in original packaging. Refunds are processed within 
5-7 business days."

Query: "What's your return policy?"

Agent response: "Most retailers offer a 30-60 day return window. 
You should check the specific store's policy for details."

Reality: Specific policy was in context but ignored

Result: Generic unhelpful answer instead of specific policy
```

**Mitigation Strategies**
1. **Context-first prompting**: Place context prominently, instruct to use it
2. **Extractive grounding**: Require quotes from context
3. **Context highlighting**: Format context to draw attention
4. **Instruction emphasis**: Explicitly say "Answer ONLY from the context"
5. **Answer validation**: Verify answer references context content
6. **Attention visualization**: Debug which context parts model attends to

**Detection**
- Track context utilization rate
- Compare answer to context overlap
- Monitor generic vs. specific response rates
- Flag answers without context references

## References

- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Context utilization failures
- [Self-Healing RAG Layer](https://towardsdatascience.com/rag-hallucinates-i-built-a-self-healing-layer-that-fixes-it-in-real-time/) - Fixing context issues
