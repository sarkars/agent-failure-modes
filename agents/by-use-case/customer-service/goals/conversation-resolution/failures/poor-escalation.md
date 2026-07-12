# Poor Escalation

## Issue: Agent fails to hand off to a human at the right time.

**Frequency**: Common

**Symptoms**
- Repeated failure, angry user, compliance risk.
- [Add more specific symptoms]

**Root Cause**
Agent fails to hand off to a human at the right time.

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
1. **Explicit escalation trigger taxonomy**: define and continuously maintain a concrete list of hard triggers (N failed resolution attempts, detected anger/sentiment threshold, compliance-sensitive keywords like legal/medical/self-harm, explicit human request) that force escalation regardless of model judgment, since the failure is the agent relying on its own unreliable judgment of "the right time" instead of deterministic triggers. Trade-off: a fixed trigger list will always lag novel failure patterns and requires ongoing curation.
2. **Sentiment/frustration trend monitoring within conversation**: track sentiment trajectory turn-over-turn, not just current-turn sentiment, so escalation fires on a worsening trend even if no single message crosses an absolute anger threshold. Trade-off: trend-based triggers are noisier and can false-trigger on naturally emotional but resolvable conversations.
3. **Compliance-keyword hard-stop list**: maintain a hard-stop keyword/topic list (legal threats, safety/self-harm, regulatory complaints) that forces immediate human escalation independent of conversation flow, since compliance risk from a missed escalation is asymmetrically costly compared to an unnecessary one. Trade-off: an overly broad hard-stop list escalates too much routine language matching sensitive keywords, adding human workload.

### Detection & Response
1. **Failed-attempt counter with automatic escalation floor**: count consecutive unsuccessful resolution attempts within a conversation; once it crosses a floor (e.g., 3), force escalation even if the agent's own judgment says continue. Response: any conversation exceeding the floor without escalation is logged as a defect and reviewed.
2. **Post-hoc compliance-risk transcript audit**: sample conversations containing compliance-sensitive language (legal, safety, discrimination) that were not escalated, and have a human review whether escalation was warranted. Response: confirmed misses trigger immediate trigger-list updates and stakeholder notification.
3. **Angry-user-without-escalation detection**: run sentiment analysis over closed conversations and flag ones ending at high negative sentiment with no human handoff. Response: proactive outreach to the affected customer and a root-cause review of why the trigger didn't fire.

### Architecture Patterns
1. **Deterministic trigger layer independent of model judgment**: a rules/classifier layer that runs alongside the LLM and can force escalation regardless of what the LLM decides, so escalation-worthy situations aren't solely gated on the model choosing to invoke a handoff tool.
2. **Structured handoff-context packet**: architect escalation to always produce a structured summary (issue, attempts made, sentiment trend, relevant policy) handed to the human agent, since poor handoffs that lose context often cause repeated failure to compound.
3. **Escalation state machine with no-return-to-bot rule**: once escalated for a compliance-triggered reason, structurally prevent the conversation from routing back to the bot without human sign-off, avoiding oscillation between bot and human that itself causes user frustration.

### Metrics
1. **missed_escalation_rate**: Target: <2% of conversations meeting a hard trigger fail to escalate; Alert on >5%
2. **compliance_trigger_miss_rate**: Target: 0%; Alert on any confirmed occurrence
3. **conversation_ending_negative_sentiment_no_escalation**: Target: <3%; Alert on >6% weekly
4. **handoff_context_completeness_score**: Target: >90% of handoffs include the full structured context packet; Alert on <75%

### Alerts
1. **Compliance Trigger Miss** (P1): Condition - a conversation with confirmed legal/safety/regulatory content was not escalated to a human. Action: immediate escalation and customer outreach, notify compliance/legal within 1 hour, patch the trigger list same day.
2. **Escalation Floor Breach** (P2): Condition - a conversation exceeds the failed-attempt floor without escalating. Action: force escalation programmatically, log as a defect for the trigger-layer review.
3. **Rising Unescalated Anger** (P2): Condition - conversation_ending_negative_sentiment_no_escalation exceeds 6% weekly. Action: review sentiment-trend trigger thresholds and sample transcripts.

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
