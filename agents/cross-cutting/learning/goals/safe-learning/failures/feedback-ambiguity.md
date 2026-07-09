# Feedback Ambiguity

## Issue: Feedback says 'bad' but not why.

**Frequency**: Occasional

**Symptoms**
- No failure label/root cause from review.
- [Add more specific symptoms]

**Root Cause**
Feedback says 'bad' but not why.

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
1. **Structured Taxonomy-Based Feedback Forms**: Replace free-text-only "good/bad" widgets with a mandatory failure-category selector (drawn from a maintained taxonomy: factual error, tone, policy violation, incomplete, etc.) plus a required rationale field, so every negative rating carries an actionable reason at the point of capture.
2. **Minimum Annotation Completeness Gate**: Reject or quarantine feedback entries missing a category or rationale before they enter the learning pipeline, rather than allowing bare "bad" ratings to silently count as training signal with no interpretable direction.
3. **Reviewer Training & Calibration Sessions**: Run periodic calibration sessions where reviewers practice writing specific, actionable rationale against example transcripts, correcting the tendency to default to vague labels under time pressure.

### Detection & Response
1. **Ambiguous-Label Rate Monitoring**: Track the percentage of incoming feedback missing a category or containing only generic text ("bad", "wrong", "not good"); a rising rate signals the review UI or incentives are producing low-information labels.
2. **Free-Text Rationale Quality Scoring**: Use a lightweight classifier or heuristic to score rationale specificity (length, presence of concrete nouns/spans referencing the transcript) and flag entries that look templated or non-specific for re-review.
3. **Escalation to Structured Re-Review**: Route flagged ambiguous feedback back to the original or a secondary reviewer with a prompt requiring them to select a specific failure category before the item is accepted into the learning pool.

### Architecture Patterns
1. **Structured Feedback Schema Service**: A feedback intake API that enforces required fields (failure_category, severity, rationale_text, evidence_span) at the schema level, making it impossible to submit a bare thumbs-down without accompanying structure.
2. **Feedback Enrichment Pipeline**: For legacy or third-party feedback sources that only provide free text, run an LLM-assisted auto-tagging step that proposes a failure category and evidence span, with human verification before the enriched label is trusted.
3. **Feedback Quality Gate**: A pipeline stage between raw feedback capture and the learning/training system that blocks any record lacking the minimum structured fields, with a dashboard showing rejection reasons.

### Metrics
1. **labeled_feedback_completeness_percent**: Target: > 95%; Alert threshold: < 80%
2. **ambiguous_feedback_rate_percent**: Target: < 5%; Alert threshold: > 20%
3. **rationale_present_rate_percent**: Target: 100% (enforced at schema level); Alert threshold: < 90%
4. **auto_tag_human_agreement_rate_percent**: Target: > 85%; Alert threshold: < 60%

### Alerts
1. **Ambiguous Feedback Flooding Pipeline** (P1 - Critical): Condition - ambiguous feedback rate exceeds 20% of items entering the learning pool. Action: Pause ingestion of unstructured feedback into training, notify review team, tighten intake form validation.
2. **Completeness Gate Bypass Detected** (P2 - Warning): Condition - feedback records without required fields found in the training data store. Action: Audit ingestion pipeline for a bypassed validation step, purge non-compliant records.
3. **Auto-Tagging Accuracy Drift** (P3 - Info): Condition - human-agreement rate with auto-tagged categories drops below 60%. Action: Retrain/review the auto-tagging classifier, temporarily increase human verification sampling.

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
