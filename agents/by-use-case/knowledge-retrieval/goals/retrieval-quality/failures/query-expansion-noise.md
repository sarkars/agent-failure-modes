# Query Expansion Noise

## Issue: Query Expansion Adds Irrelevant Terms

**Frequency**: Common

**Symptoms**
- Expanded query retrieves off-topic documents
- Synonyms shift meaning in domain context
- Multi-query fusion adds contradictory terms
- LLM-generated variations miss intent
- Recall increases but precision drops sharply

**Root Cause**
Query expansion techniques (synonyms, LLM rephrasing, HyDE) aim to improve recall by broadening the search. However, expansions can introduce terms that shift meaning, especially in domain-specific contexts where words have precise definitions. "Bank" expanded to include "financial institution" and "river bank" retrieves irrelevant content. RAGAS query transformation metrics highlight when expansions help vs. hurt.

**Example**
```
Original query: "Mercury toxicity levels in fish"

LLM query expansion generates:
1. "Mercury poisoning fish contamination"
2. "Heavy metal toxicity seafood"
3. "Mercury planet fish zodiac" ← Wrong "Mercury"
4. "Fish death mercury pollution"
5. "Quicksilver fish tank" ← Wrong context

HyDE (Hypothetical Document Embedding) generates:
"Mercury is a heavy metal that accumulates in fish tissue,
particularly in large predatory species like tuna and 
swordfish. The planet Mercury has no fish..."
← Includes irrelevant planetary reference

Retrieved documents after expansion:
- 40% about mercury in fish (relevant)
- 25% about general heavy metals (partially relevant)
- 20% about planet Mercury (irrelevant)
- 15% about fish tanks, aquariums (irrelevant)

RAGAS evaluation:
  Original query precision: 0.85
  Expanded query precision: 0.52
  Recall improvement: +15%
  Net quality impact: Negative
```

**Key Statistics**
From Query Expansion Research (2026):
- Query expansion improves recall: 20-40%
- Expansion hurts precision: 15-30% of queries
- Domain-specific queries: 40% negatively impacted
- LLM expansions: More creative but less reliable
- Synonym expansion: 25% introduce wrong sense

**Expansion Failure Modes**
| Technique | Risk | Example |
|-----------|------|---------|
| Synonym expansion | Word sense errors | Bank → river bank |
| LLM rephrasing | Semantic drift | Adds interpretations |
| HyDE | Hallucinated content | Fake facts in pseudo-doc |
| Multi-query fusion | Contradictory terms | Competing intents |
| Back-translation | Nuance loss | Technical term simplified |

**Contributing Factors**
- Generic expansion without domain knowledge
- No expansion quality validation
- Single expansion used blindly
- No fallback to original query
- LLM expansion hallucinations
- Ignoring query specificity signals

**Mitigation Strategies**
1. **Controlled vocabulary**: Expand only with domain-approved synonyms
2. **Expansion validation**: Verify expansions maintain intent
3. **Weighted fusion**: Weight original query higher than expansions
4. **Selective expansion**: Only expand low-recall queries
5. **Diversity filtering**: Remove contradictory expansions
6. **A/B testing**: Measure expansion impact rigorously

**Detection**
- Compare precision with/without expansion
- Track semantic similarity: original vs. expanded
- Monitor retrieval diversity (too diverse = drift)
- Log expansion terms that correlate with failures
- Measure intent preservation in expansions

## References

- [RAGAS Query Transformation](https://docs.ragas.io/en/latest/concepts/testset_generation.html) - Query modification
- [HyDE Paper](https://arxiv.org/abs/2212.10496) - Hypothetical document risks
- [Query Expansion Survey](https://arxiv.org/abs/2305.03653) - Expansion techniques
- [Multi-Query RAG](https://blog.langchain.dev/query-transformations/) - LangChain approaches
