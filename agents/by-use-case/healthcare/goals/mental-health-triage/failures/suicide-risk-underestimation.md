# Suicide & Self-Harm Risk Underestimation in Triage

## Issue: Agent Triages a Message Containing Indirect Self-Harm Indicators as Low Acuity Because No Explicit Keyword Was Present

**Frequency**: Occasional (Low frequency, catastrophic severity)

**Symptoms**
- Risk classifier relies heavily on explicit keywords ("suicide," "kill myself") and misses indirect expressions ("I don't think I'll need this prescription refill next month," "things will be easier for everyone soon")
- Agent correctly extracts sentiment as "negative" but does not escalate because no crisis keyword matched
- Repeated low-grade distress signals across multiple messages are scored independently rather than as an accumulating trend
- Triage routes the patient to standard scheduling queue instead of urgent behavioral health pathway

**Root Cause**
Many triage classifiers are tuned against explicit crisis-language datasets, which makes them effective at catching direct statements but brittle against the indirect, euphemistic, or future-oriented language that is common in genuine risk disclosures. Without longitudinal aggregation across a patient's messages and without training/prompting specifically calibrated to indirect risk language, the agent's acuity score reflects keyword presence rather than actual clinical risk.

**Example**
```
Scenario: Patient message to care team portal: "No need to refill my meds past this month, won't be needing them"
Keyword scan: No explicit self-harm terms detected
Sentiment: Negative, but not flagged as crisis
Triage: Routed to standard medication-refill queue, no urgent review
Reality: Statement is a classic indirect risk indicator requiring same-day clinical contact
Impact: Missed opportunity for timely risk assessment
```

**Key Statistics**
- Indirect or euphemistic expressions of suicidal ideation are documented as common in real clinical presentations and are systematically harder for keyword-based and even general-purpose LLM classifiers to detect than explicit statements
- Risk-assessment audits of AI triage tools report meaningfully lower sensitivity for indirect risk language compared to explicit crisis language
- Aggregating risk signal across multiple messages/visits, rather than scoring each message independently, has been shown to improve detection sensitivity for emerging risk

---

## Mitigation Strategies

1. **Indirect-Language Calibration**: Train/prompt the risk classifier on a labeled set that explicitly includes euphemistic and future-oriented risk language, not only explicit crisis terms
2. **Longitudinal Risk Aggregation**: Score risk across a rolling window of recent patient communications, not a single message in isolation, and escalate on accumulating trend even without a single high-scoring message
3. **Low-Confidence-High-Stakes Escalation Bias**: For mental health risk specifically, bias the system toward escalation on ambiguous signal rather than requiring high classifier confidence, given the asymmetric cost of false negatives
4. **Human-in-the-Loop for Borderline Scores**: Route any message scoring in an ambiguous middle band to a clinician for manual review rather than auto-resolving to low acuity

### Metrics
- Sensitivity/recall for indirect risk language on a held-out clinically-labeled test set
- Time-to-clinician-review for messages in the ambiguous middle risk band
- Rate of risk score escalation upon longitudinal aggregation vs. single-message scoring

### Alerts
- Negative-sentiment message in a patient with declining engagement trend not escalated → P1
- Any message scoring in ambiguous middle band auto-resolved without human review → P1

---

## References

- [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482)
- [Reinventing Clinical Dialogue: Agentic Paradigms for LLM Enabled Healthcare Communication](https://arxiv.org/pdf/2512.01453)
