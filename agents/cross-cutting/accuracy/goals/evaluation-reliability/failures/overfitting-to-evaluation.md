# Overfitting to Evaluation

## Issue: Agent Optimized for Eval Set, Fails on Real Queries

**Frequency**: Common

**Symptoms**
- Perfect or near-perfect eval scores
- Dramatic performance drop in production
- Agent handles eval patterns but not variations
- Fixes that improve eval hurt production
- Eval set performance improves while production degrades

**Root Cause**
When the same evaluation set is used repeatedly for development, teams (consciously or not) optimize specifically for those cases. The agent learns to handle the exact patterns, phrasings, and scenarios in the eval set but fails to generalize. This is especially problematic when eval sets are small or not representative.

**Example**
```
Scenario: Code generation agent evaluation

Evaluation set: 100 coding problems
Development cycle: 6 months, 50 iterations

Eval performance over time:
  Month 1: 72%
  Month 2: 81%
  Month 3: 89%
  Month 4: 94%
  Month 5: 97%
  Month 6: 99%  ← "Ready for production"

Production deployment:
  Week 1 accuracy: 61%
  
Analysis of failures:
  - Eval set: "Write a function to sort a list"
  - Production: "Can you help me organize this data?"
  
  - Eval set: Clean, well-specified problems
  - Production: Ambiguous, contextual requests
  
  - Eval set: 100 problems, repeated 50 times
  - Agent essentially memorized solutions
  
Overfitting indicators:
  - Performance gap: 99% → 61% (38 points)
  - 40% of production queries unlike any eval case
  - Agent struggles with rephrased eval questions
  - Eval set hasn't changed in 6 months
```

**Key Statistics**
From Overfitting Research (2026):
- Average eval-to-production gap: 15-40%
- 85% of teams reuse same eval set for >6 months
- Overfitting detectable after ~20 eval iterations
- Small eval sets (<500 cases) highly prone to overfitting
- 70% of "improvements" on small evals don't generalize

**Overfitting Indicators**
| Indicator | Warning Sign | Threshold |
|-----------|--------------|-----------|
| Eval improvement | Continuous gains | >5% monthly for 3+ months |
| Eval-prod gap | Growing divergence | >15% difference |
| Variation sensitivity | Rephrased queries fail | >20% drop |
| Plateau then spike | Sudden improvement | >10% jump |
| Fix specificity | Changes target specific cases | Multiple targeted fixes |

**Contributing Factors**
- Same eval set used throughout development
- Small, unrepresentative eval set
- Eval set visible to developers
- No held-out test set
- Optimization pressure on eval metrics
- No production feedback loop

---

## Test Scenario & Reproduction

### Scenario Setup
- A fixed, 100-problem code-generation evaluation set reused across ~50 development iterations over 6 months, with full developer visibility into every case
- No held-out final test set separate from the iterated-on dev eval set, and no eval-set rotation/refresh policy
- A parallel production traffic stream containing materially different query phrasing (ambiguous, contextual requests vs. clean, well-specified problems)

### Trigger Mechanism
1. Track the eval score across each monthly development checkpoint over the 6-month cycle
2. At the point the eval score reaches near-ceiling (99%), deploy to production and measure real-world accuracy over a comparable window
3. Systematically rephrase a sample of existing eval cases (not verbatim) and re-test the deployed agent against the rephrased variants
4. Compare eval-set performance, rephrased-variant performance, and production performance

**Example Reproduction Steps:**
```
1. Record monthly eval score on the fixed 100-problem set: Month 1: 72%, Month 2: 81%, Month 3: 89%, Month 4: 94%, Month 5: 97%, Month 6: 99%
2. Deploy the Month-6 model version to production
3. Measure Week 1 production accuracy on live user requests (expect a sharp drop, e.g., 61%)
4. Pull a sample of production failures and compare their phrasing to the eval set (e.g., eval: "Write a function to sort a list" vs. production: "Can you help me organize this data?")
5. Rephrase 20 existing eval-set problems without changing their underlying requirements, and re-run the agent against the rephrased set
6. Compare rephrased-variant accuracy against original eval-set accuracy
```

### Expected Failure State
- Production accuracy (e.g., 61%) is dramatically lower than the final eval-set score (99%), a gap of roughly 38 points
- Rephrased variants of the same underlying problems show a significant accuracy drop compared to the original eval-set phrasing, indicating memorization of exact wording rather than genuine problem-solving capability
- A large share of production queries (e.g., ~40%) don't resemble any eval-set case in structure or ambiguity level
- A correctly-behaving development process would have tracked the eval-production gap and rephrased-variant accuracy throughout the 6 months, flagging the sustained monthly eval gains (>5%/month for 3+ months) as an overfitting signal well before the 99%-to-61% gap was discovered in production

---

## Mitigation Strategies

### Prevention
1. **Held-out final test set never used during iteration**: Maintain a separate held-out set used only once for a final go/no-go decision, never touched during the development iterations, directly addressing "no held-out test set" in Contributing Factors. Trade-off: requires disciplined process to resist peeking, and iteration feedback comes only from the (still-overfittable) dev eval set.
2. **Rotating/refreshing eval sets on a fixed cadence**: Refresh a meaningful portion of the evaluation set on a scheduled cadence rather than reusing the same 100 problems for 6+ months, since 85% of teams reuse the same eval set for over 6 months per Key Statistics and overfitting is detectable after roughly 20 iterations. Trade-off: rotating eval sets makes historical score trends harder to compare directly, since the underlying cases change.
3. **Blind evaluation with restricted developer visibility**: Restrict developers' direct visibility into exact eval case details during iterative development, exposing only aggregate scores, so fixes target genuine generalization rather than the exact phrasing pattern (e.g., "Write a function to sort a list"). Trade-off: reduces diagnostic detail available for root-causing a specific failure, slowing debugging.

### Detection & Response
1. **Eval-vs-production performance gap tracking**: Continuously track the delta between eval-set score and real production performance; the example's 99%→61% gap is a textbook overfitting signature that should trigger investigation well before reaching that magnitude.
2. **Generalization testing via rephrased/variant queries**: Periodically test the current model against systematically rephrased versions of existing eval cases (not the literal originals) to measure whether performance holds; a drop above 20% per the Overfitting Indicators table signals memorization rather than genuine capability.
3. **Improvement-rate anomaly monitoring**: Monitor the eval score's month-over-month improvement rate and flag sustained gains above threshold (>5% monthly for 3+ months per the Overfitting Indicators table) as a signal to investigate whether the eval set itself, not agent capability, is what's improving.

### Architecture Patterns
1. **Shadow evaluation against live production traffic**: Run continuous shadow evaluation on real, unseen production queries in parallel with the static eval set, so a true generalization signal exists independent of whatever the static eval set has become optimized for.
2. **Separated dev-set/held-out-set architecture with access controls**: Architecturally separate the iterable dev eval set from the held-out final test set at the infrastructure level (different storage, different access permissions), so separation isn't merely a policy convention that can be casually violated under deadline pressure.
3. **Versioned eval-set registry with rotation scheduling**: Maintain eval sets as versioned artifacts with an enforced rotation/expiry policy built into the eval pipeline itself, so an eval set automatically ages out of "trusted for release gating" status rather than being silently reused indefinitely.

### Metrics
1. **eval_production_performance_gap**: Target: <10 percentage points; Alert when gap exceeds 20 points
2. **eval_score_monthly_improvement_rate**: Target: track trend; Alert on sustained >5% monthly improvement for 3+ consecutive months without corresponding production improvement
3. **rephrased_variant_accuracy_drop**: Target: <10% accuracy drop on paraphrased eval variants vs. originals; Alert when drop exceeds 20%
4. **eval_set_age_since_rotation_days**: Target: <180 days since last meaningful refresh; Alert when age exceeds 270 days

### Alerts
1. **Eval-Production Gap Exceeds Threshold** (P1): Condition - the tracked gap between eval score and production performance crosses the alert threshold (e.g., >20 points). Action: freeze eval-driven release decisions, investigate for overfitting, initiate eval-set refresh/rotation.
2. **Suspicious Sustained Eval Improvement** (P2): Condition - eval score shows sustained monthly gains above threshold for 3+ months. Action: run generalization testing against rephrased variants and shadow production evaluation before trusting the trend.
3. **Eval Set Rotation Overdue** (P3): Condition - the active eval set has exceeded its defined rotation age without refresh. Action: schedule eval-set refresh, treat current eval scores as lower-confidence until refreshed.

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Benchmark gaming
- [RAGAS Fails 83% of Time](https://medium.com/data-science-collective/air-canada-lost-a-lawsuit-because-their-rag-hallucinated-yours-will-too-b92b6b9a4d39) - Eval-production gap
- [FloTorch: RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Benchmark limitations
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Evaluation design
- [Databricks: OfficeQA Benchmark](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - Real-world vs benchmark gap
