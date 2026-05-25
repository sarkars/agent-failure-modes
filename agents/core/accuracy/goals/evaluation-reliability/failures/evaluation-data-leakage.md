# Evaluation Data Leakage

## Issue: Golden Data Contaminated Training or Model Has Seen Eval Cases

**Frequency**: Occasional

**Symptoms**
- Suspiciously high eval scores
- Perfect performance on specific cases
- Production performance much lower than eval
- Model memorizes rather than generalizes
- Eval scores don't improve with fixes

**Root Cause**
Evaluation data leaks into training through various paths: eval examples included in training data, foundation model trained on benchmark datasets, fine-tuning on eval set, or prompt engineering using eval examples. The model has effectively "seen the test" and its eval performance doesn't reflect true capability.

**Example**
```
Scenario: Customer service agent evaluation

Evaluation setup:
  - Golden dataset: 500 Q&A pairs
  - Fine-tuning dataset: 10,000 Q&A pairs
  
Discovery during audit:
  - 127 eval pairs found in fine-tuning data (25% leakage)
  - Additional 89 pairs nearly identical (18% near-leakage)
  - Total contamination: 43%

Performance analysis:

Leaked cases (127):
  - Accuracy: 98%
  - Response time: 0.3s (memorized)
  - Exact match to expected: 94%

Non-leaked cases (284):
  - Accuracy: 72%
  - Response time: 1.2s (reasoning)
  - Exact match to expected: 31%

Reported eval accuracy: 89%
Actual capability: ~72%
Inflation: 17 percentage points

How leakage occurred:
  1. Eval set created from production logs
  2. Same logs used for fine-tuning
  3. No deduplication between datasets
  4. No leakage detection process
```

**Key Statistics**
From Contamination Research (2026):
- 10-30% of benchmarks contaminated in foundation models
- 25% of organizations have eval-training overlap
- Leakage inflates scores by 10-25 percentage points
- Only 20% of teams check for contamination
- Popular benchmarks most likely contaminated

**Leakage Vectors**
| Vector | Mechanism | Detection |
|--------|-----------|-----------|
| Direct inclusion | Eval in training data | Deduplication |
| Foundation model | Pre-trained on benchmarks | N-gram analysis |
| Near-duplicates | Paraphrased versions | Semantic similarity |
| Prompt engineering | Developers use eval examples | Process audit |
| Data augmentation | Eval used to generate training | Provenance tracking |

**Contributing Factors**
- No separation between eval and training teams
- Shared data sources
- No deduplication process
- Using popular benchmarks (likely contaminated)
- No contamination testing
- Pressure to show high scores

**Mitigation Strategies**
1. **Data separation**: Strict isolation of eval from training
2. **Deduplication**: Check for overlaps before evaluation
3. **Contamination testing**: Probe model for memorization
4. **Held-out creation**: Create fresh eval data after training
5. **Provenance tracking**: Track data lineage
6. **Canary examples**: Include unique markers to detect leakage

**Detection**
- Check exact match rates (too high = suspicious)
- Compare response times (memorized = fast)
- Test on paraphrased versions of eval
- Run deduplication against training data
- Analyze n-gram overlap with training corpus

## References

- [Contamination in Language Models](https://arxiv.org/abs/2310.10628) - Benchmark contamination study
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Evaluation integrity
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Evaluation best practices
- [Data Leakage in ML](https://machinelearningmastery.com/data-leakage-machine-learning/) - Leakage patterns
- [RAGAS Study](https://medium.com/data-science-collective/air-canada-lost-a-lawsuit-because-their-rag-hallucinated-yours-will-too-b92b6b9a4d39) - Benchmark reliability
