# No 'Should Not Decide' Detection

## Issue: Agent decides where human/domain expert should decide.

**Frequency**: Rare but Catastrophic

**Symptoms**
- High-risk decision made without escalation.
- [Add more specific symptoms]

**Root Cause**
Agent decides where human/domain expert should decide.

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
1. **Abstention Classifier**: Build classifier that identifies decision scenarios where agent SHOULD abstain (human/expert required). Criteria: ambiguous_case, high_financial_risk, legal_exposure, customer_anger, precedent_needed, policy_unclear. Classifier outputs: abstention_needed (yes/no), confidence_score, abstention_reason.
2. **Escalation Trigger Framework**: Define explicit escalation triggers (if condition_X then escalate_to_human_Y). Example: 'IF medical_diagnosis_needed THEN escalate_to_doctor', 'IF legal_interpretation_needed THEN escalate_to_legal_team'. Maintain trigger registry reviewed by domain experts.
3. **Know-Your-Limits Prompting**: During agent decision-making, embed reminders: 'Complex medical cases, legal interpretations, and policy exceptions require expert review. Consider escalation if uncertain.' Train agent to recognize cases it should abstain from.

### Detection & Response
1. **Abstention Failure Detection**: Monitor decisions where abstention_classifier indicated abstention needed BUT agent decided anyway. Alert on abstention failures. Log: decision, abstention_reason, actual_outcome.
2. **Escalation Rate Analysis**: Track escalation rates by decision type. Establish baselines. Alert if escalation_rate drops significantly (may indicate false confidence, under-escalation). Alert if escalation_rate spikes (may indicate over-escalation, model brittleness).
3. **Post-Decision Escalation**: Monitor if decisions agent made get escalated later by customers/supervisors. High post-decision-escalation-rate indicates agent should have abstained. Flag patterns of incorrectly-decided cases.

### Architecture Patterns
1. **Abstention Gate Pre-Decision**: Before agent commits to decision, run abstention classifier. If abstention_needed, route to human agent for decision. Agent only decides if abstention_classifier says OK. Log abstention gate decisions.
2. **Escalation Workflow**: Maintain escalation workflow with decision-tree routing to appropriate expert (legal, medical, financial, customer service manager, etc.). Agent initiates escalation with context. Expert decides or provides guidance.
3. **Human Handoff Protocol**: When escalating, ensure smooth handoff: provide context, summarize agent analysis, request expert decision, track outcome. Log all escalations with decision + outcome for feedback.

### Metrics
1. **abstention_failure_rate_percent**: Target: 0%; Alert threshold: > 0.1%; Track: decisions made despite abstention_needed=true
2. **escalation_rate_by_decision_type_percent**: Target: varies by type (baseline per decision type); Alert if drops > 20% or increases > 50%
3. **post_decision_escalation_rate_percent**: Target: < 5%; Decisions escalated later by customer/supervisor
4. **abstention_classifier_accuracy_percent**: Target: > 95%; Measure via expert audit sampling
5. **escalation_resolution_time_hours_p95**: Target: < 24hrs; Prompt expert decisions

### Alerts
1. **Abstention Failure - Agent Decided When Should Abstain** (P1 - Critical): Condition - abstention_classifier indicated abstention_needed BUT agent made decision anyway. Action: Immediate decision review, escalate to expert, potential decision reversal, customer outreach.
2. **Escalation Rate Collapse** (P1 - Critical): Condition - escalation_rate for decision_type drops > 20% month-over-month (under-escalation). Action: Investigate agent behavior, review recent decisions, potential retraining, escalation policy reminder.
3. **High Post-Decision Escalation** (P2 - Warning): Condition - post_decision_escalation_rate > 15% (decisions escalated by customers later). Action: Agent performance review, decision quality audit, potential skill/knowledge gap identification.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Critical |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
