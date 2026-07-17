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

---

## Test Scenario & Reproduction

### Scenario Setup
- A 10,000-example sentiment-analysis golden dataset labeled by 5 annotators over 3 months, with no inter-annotator agreement checks or adjudication step
- Specific known-problematic cases present in the set: an objectively mislabeled example (#2341), a pair of near-identical phrasings labeled inconsistently (#5672 vs #5891), and a genuinely ambiguous case (#8901)
- No periodic label-quality audit process in place

### Trigger Mechanism
1. Run the agent against the full golden set and record the reported accuracy
2. Pull a sample of "failed" cases and manually re-review the golden label's correctness against the source text
3. Identify near-identical phrasings labeled differently across the dataset
4. Recompute agent accuracy against a corrected subset of labels

**Example Reproduction Steps:**
```
1. Run agent on case #2341: text "The product is not bad at all" → agent outputs "Positive," golden label is "Negative" → recorded as FAIL
2. Manually re-review case #2341's golden label against the text; confirm "Positive" is the objectively correct sentiment
3. Compare case #5672 ("I guess it's okay" → golden: Positive) against case #5891 ("I suppose it's fine" → golden: Negative) for labeling consistency on near-identical phrasing
4. Review case #8901 ("Revolutionary but overpriced" → golden: Positive) for inherent ambiguity/reasonable disagreement
5. Sample and audit a larger batch (e.g., 1,000 cases) for objective errors, inconsistencies, and ambiguous cases; compute the problematic-case rate
6. Recompute agent accuracy excluding/correcting the problematic cases and compare to the originally reported accuracy
```

### Expected Failure State
- The agent's objectively correct output on case #2341 ("Positive") is scored as a failure because the golden label itself is wrong ("Negative")
- Near-identical phrasings (#5672 vs #5891) receive contradictory golden labels with no adjudication trail explaining the discrepancy
- Reported agent accuracy (e.g., 74%) is materially lower than the agent's true accuracy against corrected labels (e.g., ~85%), an artificial penalty of roughly 11 points
- A correctly-behaving evaluation process would route case #2341 and the #5672/#5891 pair through multi-annotator adjudication before accepting them into the golden set, rather than letting single-annotator errors silently penalize a correct agent

---

## Mitigation Strategies

### Prevention
1. **Multi-annotator labeling with adjudication**: Require every golden example to be labeled by multiple independent annotators, with disagreements routed to an adjudication step, rather than a single annotator's judgment standing as ground truth, since the example's cases #5672 and #5891 showed the same underlying phrasing pattern labeled inconsistently. Trade-off: multiplies labeling cost and time proportional to the number of annotators per example.
2. **Clear, example-anchored labeling guidelines**: Write labeling guidelines with explicit worked examples for known-ambiguous patterns (e.g., "not bad" sentiment framing, mixed statements like "Revolutionary but overpriced"), rather than leaving standards implicit, since inconsistency and ambiguity accounted for 20% of problematic labels in the example's audit. Trade-off: guidelines require ongoing maintenance and can't fully eliminate genuinely subjective cases.
3. **Expert review pass for high-stakes or ambiguous categories**: Route labels in domains requiring subject-matter judgment through an expert reviewer before they enter the golden set, addressing "no expert review of labels" in Contributing Factors. Trade-off: expert reviewer time is scarce and expensive, limiting how much of the dataset can receive this level of review.

### Detection & Response
1. **Inter-annotator agreement measurement and threshold enforcement**: Calculate inter-annotator agreement (e.g., Cohen's kappa) on overlapping-labeled samples and require it to clear a minimum threshold before a batch is accepted into the golden set, since the example's typical agreement range (70-85%) leaves meaningful room for undetected inconsistency.
2. **Model-disagreement-driven label review**: When the model "consistently fails" a specific case across multiple otherwise-strong checkpoints, flag that case for human re-review rather than assuming the model is wrong, since this is a known signal of label error and the example found true agent accuracy (~85%) was actually higher than reported (74%).
3. **Periodic label-quality audits with corrected-label tracking**: Run scheduled audits sampling golden labels for correctness, tracking the volume and rate of corrections over time as a first-class quality metric, rather than a one-time dataset creation with no ongoing quality process.

### Architecture Patterns
1. **Inter-rater reliability pipeline as a first-class labeling stage**: Architect the golden-data creation pipeline so every example passes through multi-annotator labeling, automatic agreement scoring, and adjudication-on-disagreement as sequential pipeline stages, not an optional add-on, structurally preventing single-annotator errors from entering the golden set unchecked.
2. **Confidence-scored label registry**: Store a confidence/agreement score alongside every golden label, derived from inter-annotator agreement and adjudication history, enabling downstream eval reporting to weight or exclude low-confidence labels rather than treating all golden labels as equally authoritative.
3. **Continuous label-correction feedback loop**: Architect a pipeline where model-disagreement flags and periodic audits feed directly into a label-correction queue that updates the golden set in place, versioning each correction, rather than treating the golden set as static after initial creation.

### Metrics
1. **inter_annotator_agreement_score**: Target: >85% agreement (e.g., Cohen's kappa >=0.8) on multi-labeled samples; Alert when agreement falls below 70%
2. **label_correction_rate**: Target: <5% of golden labels require correction per audit cycle; Alert when correction rate exceeds 15%
3. **model_consistent_failure_flag_backlog**: Target: all flagged consistent-failure cases reviewed within one sprint; Alert when the backlog of unreviewed flagged cases exceeds threshold
4. **single_annotator_label_percent**: Target: 0% of golden labels from only a single annotator with no adjudication; Alert on any batch accepted below full multi-annotator coverage

### Alerts
1. **Inter-Annotator Agreement Below Threshold** (P2): Condition - a labeling batch's measured agreement score falls below the required minimum. Action: halt acceptance of that batch into the golden set, route to adjudication/expert review, revise guidelines if the disagreement pattern is systematic.
2. **Model Consistently Fails Specific Case(s)** (P3): Condition - the model fails the same golden case(s) across multiple independent evaluation runs despite otherwise strong performance. Action: flag case for human re-review as a likely label error before penalizing the model further.
3. **Label Correction Rate Spike** (P2): Condition - a scheduled audit finds correction rate significantly above historical baseline. Action: investigate the labeling batch/annotator/process that produced the affected examples, consider re-auditing adjacent batches from the same source.

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Ground truth quality
- [Confident Learning](https://arxiv.org/abs/1911.00068) - Finding label errors
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Data quality
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Training data issues
- [Data-centric AI](https://datacentricai.org/) - Label quality focus
