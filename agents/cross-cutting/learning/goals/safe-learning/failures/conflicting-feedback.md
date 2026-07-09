# Conflicting Feedback

## Issue: Different reviewers prefer different behaviors.

**Frequency**: Occasional

**Symptoms**
- High reviewer disagreement.
- [Add more specific symptoms]

**Root Cause**
Different reviewers prefer different behaviors.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Reviewer Rubric Standardization**: Define a shared, example-anchored rubric (behavior categories, scoring scale, edge-case worked examples) that every reviewer must apply, rather than leaving "good"/"bad" to individual judgment. Rubric versions are tracked so drift over time is visible and reviewers are re-certified against updated rubrics before labeling resumes.
2. **Multi-Rater Adjudication Workflow**: Route every item through 2+ independent reviewers; when labels disagree beyond a defined tolerance, escalate to a senior adjudicator whose ruling becomes the training label and is fed back into the rubric as a new worked example. This stops any single reviewer's preference from unilaterally shaping agent behavior.
3. **Inter-Rater Reliability Gating**: Before a reviewer's labels are trusted for training, require them to pass a calibration set scored against gold-standard labels with a minimum agreement score (e.g., Cohen's kappa). Reviewers below threshold are retrained rather than allowed to contribute conflicting signal.

### Detection & Response
1. **Inter-Rater Agreement Monitoring**: Continuously compute Fleiss'/Cohen's kappa across reviewer pairs and categories; sustained low agreement on a specific behavior signals the rubric itself is ambiguous, not just reviewer error, and triggers a rubric review.
2. **Conflicting-Label Quarantine**: Items where reviewers disagree beyond tolerance are automatically excluded from the training/update pipeline until adjudicated, preventing contradictory signal from silently averaging out into a confused policy.
3. **Reviewer Drift Analysis**: Track each reviewer's agreement rate with the adjudicated consensus over time; flag reviewers whose divergence is increasing, which often indicates undocumented personal preferences taking hold.

### Architecture Patterns
1. **Adjudication Service**: A dedicated workflow/queue that receives disagreement cases, assigns a senior/tie-breaker reviewer, and writes the final ruling back to the label store with a link to the original conflicting labels for auditability.
2. **Label Provenance Store**: Persist every individual reviewer's raw label alongside the adjudicated consensus (not just an averaged score), so downstream analysis can distinguish "clear signal" from "resolved conflict" when weighting training examples.
3. **Disagreement-Weighted Training Pipeline**: Down-weight or exclude high-disagreement examples from automatic behavior updates by default, only including them once adjudicated, so noisy consensus never silently dominates the update.

### Metrics
1. **inter_rater_agreement_kappa**: Target: > 0.7; Alert threshold: < 0.5 on any tracked behavior category
2. **conflicting_label_rate_percent**: Target: < 5% of reviewed items; Alert threshold: > 15%
3. **adjudication_queue_depth**: Target: < 24h backlog; Alert threshold: > 72h backlog
4. **reviewer_consensus_divergence_percent**: Target: < 10% per reviewer; Alert threshold: > 25% sustained over 2 weeks

### Alerts
1. **Rubric-Level Disagreement Spike** (P1 - Critical): Condition - kappa drops below 0.5 for a specific behavior category across 3+ reviewer pairs. Action: Freeze training updates using that category's labels, convene rubric review, block conflicting data from pipeline.
2. **Adjudication Backlog Breach** (P2 - Warning): Condition - adjudication queue depth exceeds 72 hours. Action: Reassign adjudicators, escalate to review lead, pause ingestion of new conflicting items if backlog keeps growing.
3. **Reviewer Drift Detected** (P3 - Info): Condition - a reviewer's divergence from adjudicated consensus exceeds 25% over 2 weeks. Action: Schedule recalibration session, temporarily reduce weight of that reviewer's labels.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
