# Compression Information Loss

## Issue: Context Summarization Loses Critical Information

**Frequency**: Occasional

**Symptoms**
- Answer missing key details present in original documents
- Numerical values lost or approximated
- Caveats and conditions dropped
- Compression removes the specific fact needed
- Summarized context leads to incomplete answers

**Root Cause**
When context is too long, systems may compress or summarize it before sending to the LLM. This compression can lose critical information - specific numbers, dates, exceptions, or conditions. The summarizer doesn't know which details the query needs, so it may discard exactly what's required. RAGAS Context Recall can detect when relevant information is lost before synthesis.

**Example**
```
Query: "What is the late payment penalty for accounts over 90 days?"

Original document (500 words):
"Payment terms: Net 30 days. Late payments incur the
following penalties:
- 1-30 days: 1.5% monthly interest
- 31-60 days: 2% monthly interest  
- 61-90 days: 3% monthly interest + $50 fee
- Over 90 days: 5% monthly interest + $150 fee + 
  possible account suspension
Exceptions: Government accounts exempt from penalties.
Non-profit accounts capped at 1%..."

Compressed context (100 words):
"Payment terms are Net 30. Late payments incur interest
charges ranging from 1.5% to 5% depending on how overdue.
Additional fees may apply for significantly late accounts.
Some account types have different terms."

Answer from compressed context:
"Late payments over 90 days incur approximately 5% 
interest. Additional fees may apply."

Missing from compressed version:
- Exact $150 fee amount
- Account suspension risk
- Specific exemptions

Actual answer should be:
"Accounts over 90 days late incur 5% monthly interest
plus a $150 fee. Accounts may also be suspended."
```

**Key Statistics**
From Compression Research (2026):
- Summarization loses 30-50% of specific details
- Numerical accuracy after compression: 60-75%
- Critical fact retention: Varies by compressor
- Lossy compression: Default for most systems
- Query-aware compression: 85% retention vs 65%

**Information Loss Types**
| Type | Risk Level | Example |
|------|------------|---------|
| Numbers | High | $150 → "additional fees" |
| Dates | High | March 15 → "mid-March" |
| Exceptions | High | "except X" dropped |
| Conditions | Medium | "if Y, then Z" simplified |
| Caveats | Medium | "may vary" dropped |
| Specifics | Medium | Exact names, codes lost |

**Contributing Factors**
- Generic summarization not query-aware
- Aggressive compression ratios
- Summarizer optimizes for fluency over facts
- No verification of key fact retention
- One-size-fits-all compression
- No fallback to full documents

**Mitigation Strategies**
1. **Query-aware compression**: Preserve query-relevant details
2. **Key extraction**: Extract facts before summarizing prose
3. **Hierarchical context**: Summary + key facts + full docs
4. **Verification step**: Check if answer requires dropped details
5. **Conservative compression**: Favor relevance over brevity
6. **Fallback retrieval**: Fetch original if answer seems incomplete

**Detection**
- Compare answers from compressed vs. full context
- Track RAGAS Context Recall after compression
- Monitor numerical accuracy in answers
- Detect hedging language ("approximately", "around")
- Audit compression for fact retention


## Mitigation Strategies

### Prevention

1. **Implement query-answer consistency validation**: Decompose complex queries into atomic components and verify each component is addressed in the answer before returning. Use RAGAS Answer Relevancy metric (target: >0.75) with automatic re-generation for scores below threshold. Root cause mitigation: Prevents context-anchoring by explicitly binding answer generation to parsed query intent.

2. **Apply multi-source consensus verification**: Require answers synthesized from multiple sources to explicitly cite which sources support each claim and flag unresolved contradictions. Implementation: Use semantic similarity checks across source fragments to detect cherry-picked evidence patterns. Root cause: Ensures balanced representation of evidence when sources conflict.

3. **Enforce comprehensive coverage checks**: Implement structured extraction requiring explicit treatment of caveats, limitations, exceptions, and counterevidence for each claim type. Use template responses with mandatory caveat sections. Root cause: Prevents omission of qualifying information that would change user decision-making.

### Detection & Response

1. **Answer completeness monitoring**: Measure coverage of query intents in generated answers. Track query decomposition rate (% of query components explicitly addressed) and flag responses with coverage <85%. Instrument RAG pipeline to log query-answer similarity scores per component. Alert on sustained scores <0.70.

2. **Evidence balance scoring**: For each answer, compute evidence distribution across sources and flag one-sided responses (>70% from single source on multi-source queries). Implement automated extraction of caveat/limitation mentions and track inclusion rates by query type. Target: >80% of medical/financial answers include relevant caveats.

### Architecture Patterns

1. Query Intent Decomposition Graph: Parse complex queries into a DAG of atomic intents before retrieval. Each retrieved document is mapped to specific intent nodes. Answer generation must satisfy all leaf nodes. Validation layer computes coverage before response generation.

2. Evidence Consensus Engine: Maintain a fact graph where each claim is attributed to specific sources with confidence scores. Multi-source claims require consensus computation (intersection of sources supporting claim). Flagging layer surfaces contradictions to generation model.

3. Structured Response Templates: Use task-specific response schemas that enforce inclusion of: primary answer, supporting evidence, relevant caveats/exceptions, alternative interpretations, confidence bounds. Auto-flag template violations before user delivery.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Answer Relevancy Score | >0.75 | <0.70 | RAGAS metric on generated answers vs. original query |
| Query Coverage Rate | >90% | <85% | Percentage of query components explicitly addressed in answer |
| Evidence Balance Index | >0.6 | <0.4 | Distribution of citations across sources (Gini coefficient, 0=balanced, 1=single-source) |
| Caveat Inclusion Rate | >80% | <70% | Percentage of medical/financial answers including relevant limitations |
| User Clarification Rate | <5% | >10% | Percentage of answered queries requiring follow-up clarification |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Low Answer Relevancy | Answer Relevancy Score < 0.70 for >5% of queries in 1-hour window | HIGH | Page on-call; trigger re-generation with query reinforcement prompt |
| Single-Source Dominance | Evidence Balance Index < 0.4 on multi-source queries for >3 consecutive queries | MEDIUM | Log event; audit cherry-picking patterns in retrieval/synthesis |
| Rising Clarification Demand | User Clarification Rate exceeds 10% (vs. 5% baseline) over 24-hour window | HIGH | Investigate query decomposition or answer template effectiveness |


## References

- [RAGAS Context Recall](https://docs.ragas.io/en/latest/concepts/metrics/context_recall.html) - Information retention
- [Document Compression](https://arxiv.org/abs/2310.06839) - Compression techniques
- [LongLLMLingua](https://arxiv.org/abs/2310.06839) - Query-aware compression
- [RAG Optimization](https://www.pinecone.io/learn/series/rag/) - Context management
