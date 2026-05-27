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

## References

- [RAGAS Answer Relevancy](https://docs.ragas.io/en/latest/concepts/metrics/answer_relevance.html) - Relevancy metric
- [Query-Focused Summarization](https://arxiv.org/abs/2305.14526) - Query attention
- [RAG Evaluation](https://arxiv.org/abs/2309.01431) - Answer quality metrics
- [LangChain RAG](https://python.langchain.com/docs/tutorials/rag/) - RAG patterns
