# Customer-Emotion Misread

## Issue: Agent mishandles empathy in debt collection, healthcare, support, or complaints.

**Frequency**: Common

**Symptoms**
- Sentiment/complaint escalation after response.
- Agent responds with a procedurally correct but tone-deaf message to a customer expressing grief, anger, or financial distress.
- Customer explicitly complains about feeling unheard or dismissed rather than about the substance of the resolution offered.

**Root Cause**
The agent's generation path is optimized to resolve the literal content of a request, and without a dedicated emotion or sentiment classification step running before response generation, there is nothing to route an emotionally loaded message differently from a routine one. Response templates are validated for policy accuracy but never reviewed for tone, and high message volume creates pressure toward fast, templated replies — so a hardship disclosure receives the same procedurally correct, emotionally blind treatment as a routine status question, and the mismatch is only visible after the customer reacts to it.

**Example**
```
A customer messages a debt-collection agent explaining they just lost their
job and can't make the scheduled payment. The agent replies with a template
response listing late fees and the next payment due date, without
acknowledging the hardship or offering a hardship program. The customer
escalates to a regulator complaint citing "no compassion shown," triggering a
compliance review even though the payment terms cited were accurate.
```

**Contributing Factors**
- Agent optimizes for resolving the stated request rather than reading emotional signal in the message.
- No emotion/sentiment classification step before response generation.
- Response templates are policy-accurate but written without empathy review.
- High message volume pressures agent toward fast, templated replies over context-aware ones.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Hardship disclosure in collections | "I lost my job, can't pay this month" | Agent acknowledges hardship, offers hardship program/escalation | Agent replies with only fee/deadline template, no acknowledgment |
| Angry high-value customer | VIP customer expressing anger over repeated issue | Agent response scores high on empathy rubric | Agent response is procedurally correct but rated tone-deaf by reviewer |
| Neutral routine request | Standard order-status question, no emotional signal | Agent responds efficiently without unneeded empathy padding | Agent over-applies empathy template to a neutral request |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| empathy_rubric_score_eval_avg | > 0.80 | Average tone/empathy score across eval transcripts scored against rubric |
| emotion_classifier_precheck_coverage_percent | 100% | % of eval responses where emotion classifier ran before response generation |

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
| emotional_mishandling_rate_percent | > 5% |
| complaint_escalation_rate_post_agent_response_percent | > 10% |
| tone_score_average | < 0.70 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Emotional Mishandling Detected | Customer sentiment worsens post-response or escalation risk increases | Warning |
| Low Empathy Score | Tone score < 0.65 for a response | Warning |
| High-Risk Emotional Mismatch | VIP/churn-risk customer receives low-empathy response | Critical |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
