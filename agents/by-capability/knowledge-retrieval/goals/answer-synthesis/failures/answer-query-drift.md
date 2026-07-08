# Answer-Query Drift

## Issue: Answer Doesn't Address the Actual Question

**Frequency**: Common

**Symptoms**
- Answer is coherent but doesn't answer the question
- Response addresses related but different topic
- Model latches onto context rather than query
- Factually correct information that's not relevant
- User must re-ask to get actual answer

**Root Cause**
The model may be distracted by retrieved context and generate an answer about what's in the context rather than what was asked. RAGAS Answer Relevancy metric measures this: is the answer relevant to the query, regardless of whether it's factually correct? This is distinct from hallucination - the answer may be grounded and accurate, just not addressing the actual question.

**Example**
```
Query: "Can I use my corporate card for personal expenses?"

Retrieved context includes:
- Corporate card policy (relevant)
- Expense reimbursement procedures (related)
- Card activation instructions (tangential)

Drifted answer:
"To activate your corporate card, you'll need to call
the number on the back and verify your identity. Once
activated, you can register for online access through
the HR portal. The expense reimbursement process requires
submitting receipts within 30 days..."

Expected answer:
"No, corporate cards cannot be used for personal expenses
per company policy. Personal use may result in card
revocation and disciplinary action."

RAGAS Answer Relevancy calculation:
  Generated answer components analyzed
  Relevance to original query: 0.25
  
  The answer is about corporate cards (topic match)
  but doesn't address the actual question (can I use
  for personal expenses?)
```

**Key Statistics**
From Answer Relevancy Research (RAGAS, 2026):
- Answer Relevancy scores: Median 0.72 in production
- Context-distracted responses: 25-35% of queries
- Query-answer mismatch undetected: 40% by users
- Related-but-wrong answers: Harder to catch than wrong answers
- Multi-part queries: Higher drift risk

**Drift Patterns**
| Pattern | Description | Example |
|---------|-------------|---------|
| Topic drift | Right topic, wrong aspect | Asked cost, answered features |
| Context anchoring | Answers context not query | Query ignored, context summarized |
| Partial answer | Addresses part of query | Multi-part question, one answer |
| Scope shift | Different scope than asked | Asked specific, got general |
| Action drift | Wrong action suggested | Asked "how", got "what" |

**Contributing Factors**
- Overwhelming context drowns query
- Vague or complex queries
- Context semantically similar to query
- Model attention favors long context
- No query-answer verification step
- Training bias toward context utilization

**Mitigation Strategies**
1. **Query reinforcement**: Repeat query in prompt structure
2. **Answer-query verification**: Check answer addresses query
3. **Query decomposition**: Break complex queries into parts
4. **Context summarization**: Reduce context dominance
5. **Relevancy scoring**: Score answer relevance before returning
6. **Iterative refinement**: Generate, check relevance, regenerate

**Detection**
- Track RAGAS Answer Relevancy score
- Measure query-answer semantic similarity
- Monitor user re-asks and clarifications
- Analyze answer coverage of query intents
- A/B test query reinforcement techniques


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

- [RAGAS Answer Relevancy](https://docs.ragas.io/en/latest/concepts/metrics/answer_relevance.html) - Relevancy metric
- [Query-Focused Summarization](https://arxiv.org/abs/2305.14526) - Query attention
- [RAG Evaluation](https://arxiv.org/abs/2309.01431) - Answer quality metrics
- [LangChain RAG](https://python.langchain.com/docs/tutorials/rag/) - RAG patterns
