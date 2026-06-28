# Priority Inflation Gaming

## Issue: Agent's Ticket Priority Classifier Is Exploited by Customers Who Learn Which Language Patterns Trigger High-Priority Routing, Degrading the Classifier's Usefulness Over Time

**Frequency**: Occasional

**Symptoms**
- Customers learn (through experience or shared advice) that specific phrases ("urgent," "escalate immediately," "legal action") reliably trigger high-priority routing and faster response, regardless of actual issue severity
- Priority classifier's accuracy degrades over time as the population of incoming tickets shifts toward gamed phrasing, without the underlying issue severity distribution actually changing
- High-priority queue becomes saturated with inflated-priority tickets, increasing response time for genuinely urgent tickets that did not happen to use trigger phrasing
- Classifier retraining on recent ticket data inadvertently reinforces the gamed patterns, since "tickets marked urgent" becomes a self-fulfilling training signal disconnected from actual severity

**Root Cause**
Priority classifiers trained on historical ticket text and outcome labels learn a mapping from observed language patterns to priority level, but this mapping is only valid as long as the underlying relationship between language and actual severity remains stable. Once customers discover and exploit which language reliably triggers high priority, the input distribution shifts adversarially in response to the classifier's own behavior, and a model that is not periodically re-validated against ground-truth severity (rather than just retrained on its own recent labeled outputs) will inherit and amplify the gaming pattern rather than correcting for it.

**Example**
```
Scenario: Online community shares advice that including "this is urgent, please escalate" reliably gets faster support response
Result: A growing share of low-severity tickets begin including this phrasing
Priority classifier: Trained on recent ticket/outcome data, where "urgent" phrasing correlates strongly with "marked high priority" (a label the classifier itself influenced)
Retraining: Reinforces the language-to-priority mapping rather than correcting it, since severity ground truth was never independently checked
Impact: High-priority queue fills with phrasing-driven tickets; genuinely severe tickets without the trigger phrase wait longer
```

**Key Statistics**
- Adversarial distribution shift, where a deployed model's own behavior changes the population of future inputs it receives, is a well-documented failure mode for any classifier whose output has a known, learnable effect on user behavior
- Self-reinforcing label loops (training on a model's own prior outputs as if they were ground truth) are identified in ML systems literature as a mechanism by which gaming patterns get amplified rather than corrected during retraining
- Independent severity validation (using outcome-based ground truth such as actual resolution complexity or business impact, rather than the priority label itself) is the standard recommended mitigation for this class of gaming

---

## Mitigation Strategies

1. **Ground-Truth Severity Validation**: Periodically validate priority classifications against an independent severity signal (actual resolution complexity, business impact, technical root cause severity) rather than retraining only on the classifier's own prior priority labels
2. **Anomaly Detection on Trigger-Phrase Frequency**: Monitor for sudden increases in the frequency of specific phrases correlating with priority escalation, as an early signal of emerging gaming patterns
3. **Multi-Signal Priority Scoring**: Combine language-based signals with objective signals less susceptible to gaming (account tier, number of affected users, system-detected error codes) so no single learnable phrase pattern can unilaterally drive priority
4. **Periodic Adversarial Re-Audit**: Treat the priority classifier as a system that will be gamed over time and schedule recurring adversarial audits specifically looking for emerging exploitation patterns

### Metrics
- Correlation drift between specific trigger phrases and independently-validated actual severity over time
- High-priority queue composition: % of high-priority tickets where independent severity validation agrees with the classifier's priority label
- Response time for genuinely high-severity tickets (by independent validation) relative to phrasing-triggered high-priority tickets

### Alerts
- Frequency of a specific trigger phrase in incoming tickets increases sharply without a corresponding increase in independently-validated severity → P2
- Agreement rate between classifier priority and independent severity validation drops below a defined threshold → P1

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Toward Super Agent System with Hybrid AI Routers](https://arxiv.org/pdf/2504.10519)
