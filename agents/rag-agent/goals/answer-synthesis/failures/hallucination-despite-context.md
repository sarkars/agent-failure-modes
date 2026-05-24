# Hallucination Despite Context

## Issue: Model Generates Information Not in Retrieved Documents

**Frequency**: Common

**Symptoms**
- Answer includes facts not present in context
- Plausible-sounding additions beyond retrieved content
- Numbers, dates, or names fabricated
- Details added that "make sense" but weren't provided

**Root Cause**
Even with relevant context, models may fill gaps with generated content, especially when context is incomplete or query asks for specifics not in documents.

**Example**
```
Retrieved context:
"The software update includes performance improvements and 
bug fixes. Users should backup data before updating."

Query: "What's in the new software update?"

Agent response: "The new update (version 3.2.1) includes:
- 40% faster startup time
- Memory leak fixes
- New dark mode feature
- Improved battery efficiency"

Reality: Version number, percentages, and dark mode all fabricated

Result: User expects features that don't exist
```

**Key Statistic**
Legal RAG tools hallucinate at rates of 17-33% even with retrieval augmentation.

**Mitigation Strategies**
1. **Strict grounding instructions**: "Only state what's explicitly in the documents"
2. **Admit gaps**: Train model to say "The documents don't specify..."
3. **Extractive answers**: Quote directly rather than paraphrase
4. **Hallucination detection**: Post-process to verify claims against context
5. **Confidence gating**: Only include high-confidence, grounded claims
6. **Fine-tuning for faithfulness**: Train specifically on grounded generation

**Detection**
- NLI-based faithfulness checking
- Compare answer claims to context
- Track fabrication patterns
- User reports of incorrect information

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - 17-33% hallucination despite RAG
- [RAGAS Fails 83% of Time](https://medium.com/data-science-collective/air-canada-lost-a-lawsuit-because-their-rag-hallucinated-yours-will-too-b92b6b9a4d39) - RAG hallucination rates
- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Hallucination causes
