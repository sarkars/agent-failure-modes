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

---

## Test Scenario & Reproduction

### Scenario Setup
- A golden evaluation set (500 Q&A pairs) and a fine-tuning dataset (10,000 Q&A pairs), both sourced from the same production logs with no deduplication step between them
- No provenance/lineage tracking distinguishing which examples are eval-only versus training-eligible
- No exact-match or near-duplicate contamination audit run before trusting eval scores

### Trigger Mechanism
1. Run exact-match deduplication between the golden set and the fine-tuning corpus
2. Run near-duplicate/semantic-similarity screening between the two sets
3. Split eval results into "confirmed leaked," "near-duplicate," and "clean" case buckets
4. Compare accuracy, exact-match rate, and response latency across the buckets

**Example Reproduction Steps:**
```
1. Run exact-match deduplication of the 500-case golden set against the 10,000-case fine-tuning set; identify the overlapping subset (expect ~127 pairs, 25%)
2. Run semantic-similarity screening for near-duplicates; identify additional overlap (expect ~89 pairs, 18%)
3. Re-run the eval, separately scoring the 127 leaked cases, the 89 near-leaked cases, and the remaining 284 clean cases
4. Record accuracy, exact-match rate, and average response time for each bucket
5. Compare aggregate reported eval accuracy (89%) against the clean-only subset accuracy
6. Compute the inflation gap between reported and clean-subset accuracy
```

### Expected Failure State
- Leaked cases show anomalously high accuracy (~98%), near-instant response time (~0.3s), and high exact-match rate (~94%) consistent with memorization rather than reasoning
- Clean, non-leaked cases show materially lower accuracy (~72%) and longer response time (~1.2s)
- The aggregate reported eval accuracy (89%) significantly overstates true capability (~72%), an inflation of roughly 17 percentage points
- A correctly-behaving eval process would have blocked overlapping examples from ever appearing in both sets, or at minimum flagged the anomalous accuracy/latency cluster before the 89% score was reported as trustworthy

---

## Mitigation Strategies

### Prevention
1. **Enforced eval/training data separation with provenance tracking**: Track data lineage for every training and eval example from source, and gate the training pipeline so no example with an ID present in the eval set can be ingested, since leakage here occurred because "same logs used for fine-tuning" with "no deduplication between datasets." Trade-off: requires investment in a data lineage system and discipline in tagging every dataset at ingestion.
2. **Post-training held-out eval creation**: Create the eval set only after the training/fine-tuning cutoff, drawn from data provably outside the training window, rather than reusing historical production logs also used for training. Trade-off: delays eval availability and may not reflect the exact distribution used during training-time development iterations.
3. **Deduplication and near-duplicate screening before eval use**: Run exact and semantic-similarity deduplication between the eval set and training corpus before trusting any eval run, catching both the 25% direct overlap and 18% near-duplicate paraphrase overlap found in the example's audit. Trade-off: near-duplicate detection via semantic similarity has false positives/negatives and requires threshold tuning.

### Detection & Response
1. **Exact-match-rate anomaly monitoring**: Track exact-match rate as a signal distinct from overall accuracy; a rate as high as the example's 94% exact match on leaked cases versus 31% on clean cases is a strong contamination signal warranting audit.
2. **Response-latency differential analysis**: Compare response time across eval cases, since memorized/leaked cases in the example returned in 0.3s versus 1.2s for genuinely-reasoned cases, giving an operational tell independent of the accuracy score itself.
3. **Periodic n-gram/embedding overlap audits**: Run scheduled contamination audits (n-gram overlap, semantic similarity) between the current eval set and the full training corpus, since only 20% of teams do this per the Key Statistics and leakage is otherwise invisible until an accuracy gap appears in production.

### Architecture Patterns
1. **Isolated eval-data custody with separate ownership**: Assign eval-set creation and custody to a team/process organizationally separate from the training-data pipeline team, structurally preventing the "no separation between eval and training teams" contributing factor.
2. **Canary-example injection pipeline**: Inject unique, traceable canary examples into the eval set (never into training) so that if they later surface in the training corpus or a model's memorized outputs, contamination is definitively detected via a controlled marker rather than statistical inference.
3. **Versioned golden-set registry with cryptographic hashing**: Hash-fingerprint every eval example and check training-data ingestion against the fingerprint registry at pipeline time, giving an automated, structural block on direct-inclusion leakage rather than relying on after-the-fact audits.

### Metrics
1. **eval_training_overlap_rate**: Target: 0% exact-match overlap between eval and training sets; Alert on any overlap detected
2. **eval_training_near_duplicate_rate**: Target: <2% semantic-similarity near-duplicates; Alert above 5%
3. **exact_match_rate_anomaly**: Target: exact-match rate variance consistent with genuine reasoning; Alert when a subset of cases shows exact-match rate >90% while overall accuracy is materially lower
4. **contamination_audit_freshness_days**: Target: audit run within last 30 days; Alert when audit age exceeds 60 days

### Alerts
1. **Eval-Training Overlap Detected** (P1): Condition - deduplication finds any eval example (exact or near-duplicate) present in the training corpus. Action: quarantine affected eval cases, recompute eval score excluding them, investigate the ingestion path that caused overlap.
2. **Suspicious Exact-Match/Latency Cluster** (P2): Condition - a subset of eval cases shows anomalously high exact-match rate and low latency relative to the rest of the set. Action: manually review the flagged subset for memorization, cross-check against training data provenance.
3. **Canary Example Surfaced Outside Eval Context** (P1): Condition - a planted canary example is found in training data, model output, or logs outside its intended eval-only use. Action: treat as confirmed contamination, invalidate current eval scores, trace and fix the leak path before the next eval run.

## References

- [Contamination in Language Models](https://arxiv.org/abs/2310.10628) - Benchmark contamination study
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Evaluation integrity
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Evaluation best practices
- [Data Leakage in ML](https://machinelearningmastery.com/data-leakage-machine-learning/) - Leakage patterns
- [RAGAS Study](https://medium.com/data-science-collective/air-canada-lost-a-lawsuit-because-their-rag-hallucinated-yours-will-too-b92b6b9a4d39) - Benchmark reliability
