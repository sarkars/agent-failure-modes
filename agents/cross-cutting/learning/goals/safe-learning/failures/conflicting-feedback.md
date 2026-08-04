# Conflicting Feedback

## Issue: Different reviewers prefer different behaviors.

**Frequency**: Occasional

**Symptoms**
- High reviewer disagreement.
- The agent's behavior oscillates version to version as training batches happen to be dominated by different reviewers' preferences.
- Two agent instances fine-tuned on overlapping data but different reviewer splits diverge in tone/behavior on the same input class.

**Root Cause**
Different reviewers prefer different behaviors.

**Example**
```
A support-ticket triage agent proposes "close as resolved" for a class of ambiguous refund requests.
Reviewer A (trained on a strict cost-containment rubric) consistently marks these proposals "good."
Reviewer B (trained on a customer-satisfaction rubric) consistently marks the same proposals "bad."
The training pipeline averages the two thumbs-up/thumbs-down signals into a single reward per example.
The resulting policy update nudges the agent toward closing tickets slightly more often on some days
and slightly less on others, tracking which reviewer's labels happened to dominate that batch, with no
stable improvement in either direction.
```

**Contributing Factors**
- No shared, example-anchored rubric, so reviewers fall back to personal judgment on ambiguous behaviors.
- Reviewers come from different functions (e.g., support ops vs. trust & safety) with different incentive structures baked into their evaluation criteria.
- Labels are averaged/aggregated into a single reward signal before training rather than tracked per-reviewer, hiding the disagreement.
- No adjudication step exists, so conflicting labels flow directly into the update pipeline instead of being resolved first.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Dual-rater ambiguous case | Same borderline refund-ticket transcript sent to 2 calibrated reviewers | Both raters land within tolerance of the gold adjudicated label | Raters disagree beyond tolerance on >1 in 5 ambiguous cases |
| Reward aggregation check | Synthetic example set with known split-reviewer labels (half "good", half "bad") | Pipeline flags the example as conflicting/quarantined rather than emitting an averaged reward | Item receives a blended reward and enters training without adjudication |
| Cross-rubric consistency | Same 20-item calibration set scored by reviewers from each function/team | Scores should correlate above the kappa target across teams | One team's scores systematically diverge from the others on a specific category |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Eval-set inter-rater kappa | > 0.7 | Compute Cohen's/Fleiss' kappa across reviewer pairs on a held-out calibration set before each training run |
| Conflicting-example quarantine rate | 100% of items above disagreement tolerance | Audit training batches for any item with split labels that was not routed to adjudication |
| Adjudicated-label coverage | 100% of quarantined items resolved before use | Check label store for quarantined items missing a final adjudicated ruling |

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
| inter_rater_agreement_kappa | < 0.5 on any tracked behavior category |
| conflicting_label_rate_percent | > 15% of reviewed items |
| adjudication_queue_depth | > 72h backlog |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Rubric-Level Disagreement Spike | kappa drops below 0.5 for a behavior category across 3+ reviewer pairs | Critical |
| Adjudication Backlog Breach | adjudication queue depth exceeds 72 hours | Medium |
| Reviewer Drift Detected | a reviewer's divergence from adjudicated consensus exceeds 25% over 2 weeks | Low |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
