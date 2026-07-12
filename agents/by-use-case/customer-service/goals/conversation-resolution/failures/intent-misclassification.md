# Intent Misclassification

## Issue: Agent routes sales/support/billing/legal/technical issue incorrectly.

**Frequency**: Common

**Symptoms**
- Wrong workflow or team handoff.
- [Add more specific symptoms]

**Root Cause**
Agent routes sales/support/billing/legal/technical issue incorrectly.

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
1. **Routing-confidence threshold with fallback tier**: only auto-route to a specialized workflow when classifier confidence exceeds a calibrated threshold; below it, ask one disambiguating question or route to a generalist queue, since misrouting stems from forcing a top-1 classification even on genuinely ambiguous requests. Trade-off: the fallback tier adds an extra turn/queue hop for ambiguous requests, increasing time-to-resolution for legitimate edge cases.
2. **Multi-label intent detection for mixed requests**: detect when a message spans multiple categories (e.g., a billing question with a legal undertone) and route to the highest-priority/highest-risk category rather than forcing a single label, since real customer messages often blend intents and single-label classifiers pick the most textually salient one instead of the operationally correct one. Trade-off: multi-label routing logic is more complex to build and maintain than single-label classification.
3. **Category-specific eval sets from misroute post-mortems**: continuously mine confirmed misroutes from production and add them as regression tests for the intent classifier, since generic training data underrepresents the actual confusable phrasing seen in production. Trade-off: requires ongoing labeling effort and a feedback loop from downstream teams reporting misroutes.

### Detection & Response
1. **Receiving-team rejection tracking**: track how often a downstream team (billing, legal, technical) bounces a routed conversation back as "wrong queue," the most direct ground-truth signal of misclassification. Response: feed bounced cases into the classifier retraining/eval pipeline weekly.
2. **Legal/compliance-category recall audit**: specifically audit for false negatives on legal/compliance-sensitive intents (the costliest misroute direction) by sampling conversations routed to non-legal queues that contain legal-adjacent keywords. Response: any missed legal-intent case triggers immediate escalation and a classifier patch, given compliance exposure.
3. **First-contact-resolution-by-category drop detection**: monitor FCR broken out by routed category; an unexplained drop in one category's FCR combined with a rise in that category's rejection rate signals systematic misrouting. Response: root-cause via transcript sampling before the next classifier update.

### Architecture Patterns
1. **Confidence-threshold routing with human/generalist fallback**: a structural three-way router (high-confidence auto-route, medium-confidence disambiguate, low-confidence generalist queue) instead of a single always-commit classifier, so uncertainty is handled by design rather than masked by forced top-1 output.
2. **Hierarchical classification with risk-weighted tie-breaking**: classify coarse category first (sales/support/billing/legal/technical) then sub-intent, with tie-breaking rules that bias toward the higher-risk category when scores are close, since the cost of misrouting away from legal/compliance is asymmetric.
3. **Feedback-loop retraining pipeline**: a closed-loop architecture where downstream team rejections automatically become labeled training examples for the next classifier iteration, rather than misroutes being a dead end that never improves the model.

### Metrics
1. **misroute_rate**: Target: <5% of routed conversations bounced back; Alert on >8% weekly
2. **legal_intent_false_negative_rate**: Target: <1%; Alert on any confirmed case
3. **low_confidence_fallback_rate**: Target: 10-20% (healthy ambiguity handling); Alert on <5% (over-forcing) or >30% (classifier degraded)
4. **fcr_by_category_delta**: Target: within 10% of 90-day baseline per category; Alert on >20% drop

### Alerts
1. **Legal Intent Misroute** (P1): Condition - a conversation with legal/compliance content is confirmed routed away from the legal queue. Action: immediate escalation to compliance, patch classifier keyword/embedding rules same day.
2. **Misroute Rate Spike** (P2): Condition - misroute_rate exceeds 8% over 7 days. Action: pull the bounced-conversation sample, retrain/re-tune classifier thresholds.
3. **FCR Category Drop** (P3): Condition - any category's FCR drops >20% versus baseline. Action: sample transcripts routed to/from that category for misclassification patterns.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
