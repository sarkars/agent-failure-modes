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

## References

- [RAGAS Context Recall](https://docs.ragas.io/en/latest/concepts/metrics/context_recall.html) - Information retention
- [Document Compression](https://arxiv.org/abs/2310.06839) - Compression techniques
- [LongLLMLingua](https://arxiv.org/abs/2310.06839) - Query-aware compression
- [RAG Optimization](https://www.pinecone.io/learn/series/rag/) - Context management
