# Feedback Ambiguity

## Issue: Feedback says 'bad' but not why.

**Frequency**: Occasional

**Symptoms**
- No failure label/root cause from review.
- Training updates in the "wrong" direction because a "bad" rating covering a tone issue is treated identically to one covering a factual error, and the agent overcorrects on the wrong dimension.
- Engineers cannot reproduce or cluster the failures a low score is meant to represent, since the same numeric/thumbs rating maps to many unrelated underlying problems.

**Root Cause**
Feedback says 'bad' but not why.

**Example**
```
A coding assistant's suggested patch gets a thumbs-down from a developer. The feedback widget only
captures a binary rating, no category or comment. The developer actually disliked the patch because
it used a deprecated API, but the same thumbs-down signal is indistinguishable from other rejected
patches that were disliked for being too verbose, too slow, or simply wrong. The learning pipeline
treats all thumbs-down events as one undifferentiated "avoid this kind of output" signal, so it cannot
tell the model whether to change API usage, verbosity, correctness, or something else entirely.
```

**Contributing Factors**
- Feedback UI only exposes a binary thumbs-up/down or single star rating with no required category or rationale field.
- Reviewers are under time pressure and default to the fastest possible input (a bare click) rather than writing a specific reason.
- No maintained failure-mode taxonomy exists, so even reviewers who want to be specific have no structured vocabulary to select from.
- Legacy or third-party feedback sources (e.g., app-store reviews, support chat ratings) provide only free text or a single scalar with no way to enforce structure retroactively.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Bare thumbs-down submission | Reviewer submits a thumbs-down with no category or rationale text | Feedback intake API rejects/quarantines the submission and prompts for a required category | Bare rating is accepted and stored as valid training signal |
| Vague rationale detection | Rationale text of "bad", "wrong", "not good" submitted with a rating | Rationale-quality scorer flags the entry as non-specific and routes it to re-review | Vague text passes through unflagged into the training pool |
| Category-to-behavior mapping | Set of 10 negative ratings spanning 3 distinct failure categories (tone, factual error, incompleteness) | Learning pipeline applies category-specific updates rather than one undifferentiated negative signal | All 10 items produce the same generic "avoid this output" update regardless of category |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| labeled_feedback_completeness_percent (eval set) | > 95% | Sample recent feedback records and measure the fraction containing a valid category and rationale |
| rationale_specificity_score | > 0.7 average | Score rationale text against a heuristic/classifier for concrete nouns/spans referencing the transcript |
| category_coverage_percent | 100% of taxonomy categories represented over a rolling window | Compare distribution of assigned categories against the maintained taxonomy list |

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
| ambiguous_feedback_rate_percent | > 20% |
| labeled_feedback_completeness_percent | < 80% |
| auto_tag_human_agreement_rate_percent | < 60% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Ambiguous Feedback Flooding Pipeline | ambiguous feedback rate exceeds 20% of items entering the learning pool | Critical |
| Completeness Gate Bypass Detected | feedback records without required fields found in the training data store | Medium |
| Auto-Tagging Accuracy Drift | human-agreement rate with auto-tagged categories drops below 60% | Low |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
