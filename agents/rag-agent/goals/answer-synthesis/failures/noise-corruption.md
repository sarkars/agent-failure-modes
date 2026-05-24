# Noise Corruption

## Issue: Irrelevant Context Corrupts the Response

**Frequency**: Common

**Symptoms**
- Answer includes information from unrelated documents
- Relevant facts mixed with irrelevant details
- Model distracted by tangential content
- Quality degrades as more context added
- Correct answer available but ignored for noisy content

**Root Cause**
When retrieved context includes irrelevant documents (noise), the model may incorporate that noise into its response. RAGAS Noise Sensitivity metric specifically measures this: how much does adding irrelevant context degrade answer quality? Models struggle to ignore plausible-sounding but irrelevant information, especially when noise is semantically similar to the query topic.

**Example**
```
Query: "What is our refund policy for digital products?"

Retrieved context (5 documents):
1. Digital product refund policy ← RELEVANT
2. Physical product return shipping ← NOISE (similar topic)
3. Customer service hours ← NOISE
4. Digital product features ← NOISE (mentions digital)
5. Payment processing guide ← NOISE

Clean answer (only doc 1):
"Digital products are non-refundable once the download 
link has been accessed. Exceptions are made for technical
issues preventing access."

Noisy answer (all 5 docs):
"Digital products are generally non-refundable, though
you can return physical products within 30 days with 
prepaid shipping. Our customer service team is available
9-5 EST to help with payment processing issues and 
technical problems with digital downloads."

RAGAS Noise Sensitivity evaluation:
  Context: [relevant_doc]
  Answer quality: 0.95
  
  Context: [relevant_doc, 4 noise docs]
  Answer quality: 0.62
  
  Noise Sensitivity Score: 0.35 (high = bad)
  Quality degradation: -33%
```

**Key Statistics**
From Noise Research (RAGAS studies, 2026):
- Adding noise degrades answers: 20-40% quality drop
- Models use noise content: 30-50% of noisy contexts
- More noise = worse quality (linear degradation)
- Semantically similar noise: Most harmful
- Instruction tuning reduces but doesn't eliminate

**Noise Impact Factors**
| Factor | Impact | Notes |
|--------|--------|-------|
| Noise volume | High | More noise = worse |
| Semantic similarity | High | Related noise worst |
| Noise position | Medium | Early noise more harmful |
| Noise confidence | High | Authoritative noise worse |
| Query specificity | Medium | Vague queries more susceptible |

**Contributing Factors**
- Over-retrieval (too many documents)
- Low precision retrieval
- No relevance filtering before synthesis
- Context window stuffing
- No noise detection mechanism
- Model attention spread too thin

**Mitigation Strategies**
1. **Precision over recall**: Fewer, more relevant documents
2. **Relevance scoring**: Score and filter before synthesis
3. **Chunk-level filtering**: Remove low-relevance chunks
4. **Noise-aware prompting**: Instruct model to ignore irrelevant
5. **Iterative synthesis**: Generate, verify, regenerate
6. **Abstention**: "Insufficient relevant context" when noisy

**Detection**
- Track RAGAS Noise Sensitivity score
- A/B test with filtered vs. unfiltered context
- Monitor answer length (noise often increases it)
- Detect off-topic content in answers
- Measure answer relevance to query

## References

- [RAGAS Noise Sensitivity](https://docs.ragas.io/en/latest/concepts/metrics/noise_sensitivity.html) - Noise measurement
- [Lost in the Middle](https://arxiv.org/abs/2307.03172) - Context position effects
- [RAG Challenges](https://arxiv.org/abs/2401.05856) - Noise impact research
- [Context Filtering](https://www.pinecone.io/learn/series/rag/filtering/) - Noise reduction
