# Confirmation Bias from Prior Clinical Notes

## Issue: Agent Anchors on a Prior Visit's Diagnosis and Discounts New Evidence Contradicting It

**Frequency**: Common

**Symptoms**
- Agent carries forward a diagnosis from a previous note (e.g., "anxiety") into a new encounter with different, more concerning symptoms
- New objective findings (vitals, labs, imaging) are mentioned but not used to revise the working diagnosis
- Differential diagnosis list shrinks across visits instead of expanding when symptoms change
- Agent's summary of "patient history" repeats the old diagnosis verbatim rather than re-evaluating it

**Root Cause**
LLM agents summarizing or reasoning over longitudinal patient records weight recent context heavily, and a diagnosis label appearing repeatedly in prior notes acts as a strong prior that the model treats as settled fact rather than a hypothesis. Because the model is not explicitly instructed to re-derive the differential from current findings, it pattern-matches to the most frequently repeated label in the chart instead of re-weighing new evidence — the textbook anchoring failure mode now occurring at the level of chart summarization rather than human cognition.

**Example**
```
Scenario: Patient seen 3x over 2 months for "anxiety, presumed panic attacks"
New visit: Chest pain now radiates to left arm, new diaphoresis, elevated troponin pending
Agent summary: "Patient with longstanding anxiety presents with another panic episode"
Missed: Troponin elevation and radiating pain warrant acute coronary syndrome workup
Impact: Delayed cardiac workup; potential missed MI
```

**Key Statistics**
- Studies of LLM-based clinical reasoning agents show diagnostic accuracy drops measurably when a misleading prior diagnosis label is present in the input context, even when current findings clearly contradict it
- Multi-agent clinical decision support systems show collaborative failure modes where one agent's early diagnostic framing propagates uncorrected through downstream agents
- Anchoring-style errors are reported among the most frequent reasoning failure categories in audits of medical multi-agent systems

---

## Mitigation Strategies

1. **Fresh Differential Requirement**: Require the agent to generate a differential diagnosis from current visit findings alone before consulting prior notes
2. **Explicit Contradiction Check**: After retrieving prior diagnosis, prompt the agent to list new findings that are inconsistent with it
2. **De-Anchoring Prompts**: Instruct the model to treat prior diagnoses as "previously considered, not confirmed" rather than established fact
3. **Escalation Trigger on Red-Flag Findings**: Hard-code escalation rules (e.g., radiating chest pain + troponin order) that bypass the agent's running diagnostic narrative

### Metrics
- Rate of unchanged diagnosis label across visits despite new red-flag findings
- Time-to-escalation for red-flag symptom combinations
- Differential diagnosis list breadth (should expand, not shrink, with new symptoms)

### Alerts
- Red-flag finding present but diagnosis label unchanged from prior visit → P1
- Differential list narrows after new symptom report → P2

---

## References

- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
- [MedAgentAudit: Diagnosing and Quantifying Collaborative Failure Modes in Medical Multi-Agent Systems](https://arxiv.org/pdf/2510.10185)
