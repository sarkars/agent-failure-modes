# Label Noise and Errors

## Issue: Golden Dataset Contains Incorrect Expected Responses

**Frequency**: Common

**Symptoms**
- Agent gives correct answer, marked wrong
- Conflicting labels for similar inputs
- Human reviewers disagree with golden labels
- Model "accuracy" fluctuates based on labeler
- Correct fixes decrease eval scores

**Root Cause**
Golden datasets are created by humans who make mistakes, have biases, or disagree on correct answers. A labeler might mark a valid response as incorrect, provide an ambiguous expected response, or apply inconsistent standards. When the golden data itself is wrong, agents are penalized for being correct and rewarded for matching errors.

**Example**
```
Scenario: Sentiment analysis golden dataset

Golden dataset: 10,000 labeled examples
Created by: 5 annotators over 3 months

Quality audit findings:

Case #2341:
  Text: "The product is not bad at all"
  Golden label: Negative (incorrect)
  Correct label: Positive
  Agent output: Positive
  Eval result: FAIL

Case #5672:
  Text: "I guess it's okay"
  Golden label: Positive (inconsistent)
  Similar case #5891: "I suppose it's fine"
  Golden label: Negative (inconsistent)
  
Case #8901:
  Text: "Revolutionary but overpriced"
  Golden label: Positive
  Other labeler would say: Negative
  Inherently ambiguous

Audit results:
  - Clear errors: 3% (300 cases)
  - Inconsistent labels: 8% (800 cases)
  - Ambiguous/subjective: 12% (1,200 cases)
  - Total problematic: 23% (2,300 cases)

Impact:
  - Maximum achievable accuracy: 77%
  - Agent accuracy reported: 74%
  - Actual agent accuracy: ~85% (against corrected labels)
  - 11% artificial accuracy penalty
```

**Key Statistics**
From Label Quality Research (2026):
- 5-15% of labels have objective errors
- 10-20% additional labels are ambiguous/subjective
- Inter-annotator agreement: 70-85% typical
- Label errors cause 10-30% of perceived model failures
- Only 30% of organizations audit golden data quality

**Label Error Types**
| Type | Cause | Impact |
|------|-------|--------|
| Objective errors | Annotator mistake | False failures |
| Inconsistency | Different annotators disagree | Noisy training signal |
| Ambiguity | Genuinely unclear case | Unfair evaluation |
| Outdated | Was correct, now wrong | Staleness |
| Bias | Annotator perspective | Systematic errors |

**Contributing Factors**
- No inter-annotator agreement checks
- Single annotator per example
- Unclear labeling guidelines
- No expert review of labels
- Time pressure on annotators
- No ongoing label quality audits

**Mitigation Strategies**
1. **Multi-annotator labeling**: Multiple humans per example
2. **Inter-annotator agreement**: Measure and require threshold
3. **Expert review**: Subject matter experts validate labels
4. **Confidence scoring**: Track label certainty
5. **Error detection**: Use model to find likely label errors
6. **Regular audits**: Periodic label quality reviews

**Detection**
- Calculate inter-annotator agreement
- Flag cases where model consistently "fails"
- Sample failed cases for human review
- Track label corrections over time
- Monitor annotator consistency metrics

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Ground truth quality
- [Confident Learning](https://arxiv.org/abs/1911.00068) - Finding label errors
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Data quality
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Training data issues
- [Data-centric AI](https://datacentricai.org/) - Label quality focus
