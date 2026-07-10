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

## Mitigation Strategies

### Prevention
1. **Domain-Controlled Vocabulary Expansion**: Restrict synonym/term expansion to a curated, domain-approved thesaurus rather than generic or LLM-generated synonyms, preventing wrong-sense expansions like "Mercury" (element) drifting to "Mercury" (planet) or "quicksilver fish tank."
2. **Expansion-Intent Validation Step**: After generating expansions (LLM rephrasing or HyDE), run a semantic-similarity or entailment check between the original query and each expansion, discarding any expansion that drifts below an intent-preservation threshold before it reaches retrieval.
3. **Weighted Query Fusion Favoring the Original**: When combining original and expanded query results, weight the original query's matches higher by default (e.g., 2x) so expansions can only add supplementary recall, not override precision on the primary intent — directly addressing the -0.33 net precision drop in the example.

### Detection & Response
1. **Precision Delta Monitoring (Expanded vs. Original)**: Continuously compute precision for original-only vs. expanded retrieval on the same query stream; alert when expansion's precision cost (0.85 -> 0.52 as in the example) exceeds its recall benefit.
2. **Expansion-Term Failure Logging**: Log which specific expansion terms appear in queries that subsequently produce low-precision or off-topic retrieval, building a denylist of failure-prone terms over time (e.g., "quicksilver", "planet Mercury").
3. **Retrieval Diversity Spike Detection**: Monitor topical diversity of the retrieved set after expansion; an abnormal spike (mixing unrelated domains like heavy-metal toxicity and astrology) signals the expansion introduced off-topic terms rather than useful synonyms.

### Architecture Patterns
1. **Selective/Conditional Expansion**: Only trigger expansion for queries independently classified as low-recall-risk (very short queries, queries with zero good initial matches), instead of expanding every query by default, since expansion's precision cost is unnecessary when the original query already retrieves well.
2. **Multi-Query With Per-Branch Scoring and Fusion Filtering**: Run the original query and each expansion as separate retrieval branches, score each branch independently, and fuse only branches whose top results pass a relevance floor — dropping a branch like "Mercury planet fish zodiac" entirely rather than merging it in.
3. **HyDE With Grounding Constraint**: When using hypothetical document embeddings, constrain the hypothetical generation with retrieved domain glossary terms or a domain-specific prompt to reduce the chance the LLM invents an off-domain interpretation, like the planetary Mercury tangent in the example.

### Metrics
1. **expansion_precision_delta**: Target: >= 0; Alert threshold: < -0.15
2. **expansion_recall_gain**: Target: 15-30%; Alert threshold: monitored jointly with precision delta, not in isolation
3. **off_domain_expansion_term_rate**: Target: < 10%; Alert threshold: > 20%
4. **intent_preservation_score**: Target: > 0.8; Alert threshold: < 0.65

### Alerts
1. **Precision Collapse From Expansion** (P1): Condition - expansion_precision_delta falls below -0.15 for a query category. Action: disable expansion for that category pending review, fall back to original-query-only retrieval.
2. **Wrong-Sense Term Detected** (P2): Condition - a denylisted or flagged ambiguous term appears in a generated expansion. Action: strip the term from the expansion, add it to the controlled-vocabulary blocklist.
3. **Diversity Spike Anomaly** (P3): Condition - retrieved-set topical diversity after expansion exceeds baseline by > 2x. Action: review the expansion generation prompt/technique for that query, consider reverting to narrower expansion.

## References

- [RAGAS Query Transformation](https://docs.ragas.io/en/latest/concepts/testset_generation.html) - Query modification
- [HyDE Paper](https://arxiv.org/abs/2212.10496) - Hypothetical document risks
- [Query Expansion Survey](https://arxiv.org/abs/2305.03653) - Expansion techniques
- [Multi-Query RAG](https://blog.langchain.dev/query-transformations/) - LangChain approaches
