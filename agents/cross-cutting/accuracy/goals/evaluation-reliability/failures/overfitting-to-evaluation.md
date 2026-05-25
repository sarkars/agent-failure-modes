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

**Mitigation Strategies**
1. **Held-out test set**: Never touch until final evaluation
2. **Rotating eval sets**: Refresh evaluation data regularly
3. **Production sampling**: Evaluate on real production queries
4. **Generalization testing**: Test on rephrased/variant queries
5. **Blind evaluation**: Developers don't see eval details
6. **Overfitting detection**: Monitor eval-production correlation

**Detection**
- Track eval vs. production performance gap
- Test on query variations
- Monitor improvement rate for anomalies
- Sample production failures against eval
- Calculate generalization metrics

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Benchmark gaming
- [RAGAS Fails 83% of Time](https://medium.com/data-science-collective/air-canada-lost-a-lawsuit-because-their-rag-hallucinated-yours-will-too-b92b6b9a4d39) - Eval-production gap
- [FloTorch: RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Benchmark limitations
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Evaluation design
- [Databricks: OfficeQA Benchmark](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - Real-world vs benchmark gap
