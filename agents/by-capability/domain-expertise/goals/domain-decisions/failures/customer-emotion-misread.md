# Customer-Emotion Misread

## Issue: Agent mishandles empathy in debt collection, healthcare, support, or complaints.

**Frequency**: Common

**Symptoms**
- Sentiment/complaint escalation after response.
- [Add more specific symptoms]

**Root Cause**
Agent mishandles empathy in debt collection, healthcare, support, or complaints.

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
1. **Emotion and Risk Classifier**: Build classifier that analyzes customer input to detect: sentiment (positive, neutral, negative), emotional_intensity (low, medium, high), risk_level (escalation_risk, churn_risk). Classifier outputs: emotion_profile + risk_score. Route high-risk cases to human agent.
2. **Tone Evaluation Framework**: Define evaluation rubric for agent responses. Criteria: empathy_demonstrated, acknowledgment_of_concern, solution_clarity, respectful_language. Train evals to measure tone quality. Score responses; low scores trigger review.
3. **Context-Aware Response Generation**: Provide agent with emotion_context before responding. Example: 'Customer sentiment=angry + is_vip=true + churn_risk=high'. Specify response requirements ('acknowledge frustration', 'offer compensation'). Template responses tailored to emotion_context.

### Detection & Response
1. **Sentiment Deterioration Post-Response**: Monitor customer sentiment before-after agent response. Alert if sentiment worsens (negative becomes more negative) after agent interaction. Flag for review.
2. **Complaint Escalation Rate**: Track complaint escalation rate post-agent-response. Alert if escalation_rate > baseline (indicates emotional mishandling). Correlate escalations with tone scores.
3. **Emotion Audit Sampling**: Weekly sample 50 interactions with high_emotion_intensity. Domain experts rate: did agent handle empathy appropriately? Track accuracy by agent. Provide feedback.

### Architecture Patterns
1. **Emotion Detection Gate**: Pre-response, analyze customer message with emotion classifier. Output emotion_profile (sentiment, intensity, concern_type). Route high-risk cases to human. Low-risk cases proceed with tone-aware response generation.
2. **Tone Evaluation Feedback Loop**: After agent response, evaluate tone quality. Low-tone-quality responses flagged for human review before sending. Store feedback for agent retraining.
3. **Empathy Template Library**: Maintain library of empathetic response templates for different emotions/scenarios. Agent selects template matching emotion_context + concern_type. Templates pre-reviewed for tone quality.

### Metrics
1. **emotional_mishandling_rate_percent**: Target: < 2%; Alert threshold: > 5%; Track: negative_sentiment_post_response
2. **complaint_escalation_rate_post_agent_response_percent**: Target: < 5%; Alert if > 10%
3. **tone_score_average**: Target: > 0.80 (1.0=excellent empathy); Alert if < 0.70
4. **agent_empathy_consistency_percent**: Target: > 90%; Measure consistency across interactions
5. **customer_satisfaction_post_emotional_response**: Target: > 4.0/5.0; Measure satisfaction for high-emotion cases

### Alerts
1. **Emotional Mishandling Detected** (P2 - Warning): Condition - customer sentiment worsens post-agent-response OR escalation_risk increases. Action: Flag interaction for human review, provide corrective feedback to agent, resubmit with human approval.
2. **Low Empathy Score** (P2 - Warning): Condition - tone_score < 0.65 for response. Action: Agent review, response quality check, rewrite with empathy templates, human review before sending.
3. **High-Risk Emotional Mismatch** (P1 - Critical): Condition - VIP/churn_risk=high customer receives low-empathy response. Action: Immediate escalation to human agent, response rewrite, customer outreach/recovery.

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
