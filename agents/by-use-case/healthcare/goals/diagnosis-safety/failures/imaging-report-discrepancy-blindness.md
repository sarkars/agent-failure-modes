# Imaging Report Discrepancy Blindness

## Issue: Agent Summarizes the Radiology Impression Line Without Reconciling It Against the Ordering Clinician's Stated Question or Prior Comparison Imaging

**Frequency**: Common

**Symptoms**
- Agent extracts the final "Impression" line of a radiology report and presents it as the complete finding, dropping qualifying language in the body of the report ("cannot exclude," "correlate clinically," "recommend follow-up in 3 months")
- Comparison to prior imaging mentioned in the report ("increased in size compared to prior study") is not surfaced as a distinct, actionable change
- Discrepancy between the ordering clinician's specific question (e.g., "rule out PE") and what the report actually addresses is not flagged when the report is ambiguous or silent on the question
- Recommended follow-up imaging or specialist referral embedded in the report text is omitted from the agent's summary and therefore never scheduled

**Root Cause**
Radiology reports are structured as narrative prose with the most clinically decision-relevant content often appearing as qualifying phrases in the body rather than the headline impression. Summarization agents optimized for conciseness preferentially extract the shortest, most direct sentence (the impression line) and drop conditional or recommendation language that doesn't fit a terse summary format, even though that language frequently carries the actionable next step.

**Example**
```
Scenario: CT report ordered to rule out pulmonary embolism
Report body: "No central PE identified. Subsegmental opacity cannot be fully excluded given motion artifact. Recommend follow-up CT in 6 weeks if clinically indicated."
Agent summary: "CT: No PE."
Missed: Follow-up recommendation and motion-artifact caveat entirely dropped
Impact: Recommended follow-up imaging never ordered; residual diagnostic uncertainty not communicated to patient
```

**Key Statistics**
- Radiology report discrepancy and miscommunication between radiologists and referring clinicians is a well-documented and recurring source of diagnostic error in patient-safety literature
- A substantial share of "recommend follow-up" findings in radiology reports go unactioned without a closed-loop tracking mechanism
- Structured, closed-loop communication systems for actionable radiology findings have been shown to substantially improve follow-up completion rates compared to narrative-only reporting

---

## Mitigation Strategies

1. **Full-Report Extraction, Not Impression-Only**: Require the agent to extract and surface qualifying language, comparison-to-prior statements, and follow-up recommendations as distinct structured fields, not just the impression line
2. **Closed-Loop Follow-Up Tracking**: Any "recommend follow-up" or "correlate clinically" statement automatically generates a tracked task that must be explicitly resolved (ordered, deferred with reason, or declined)
3. **Question-Answer Alignment Check**: Compare the ordering clinician's stated clinical question against report content and flag when the report does not directly address it
4. **Change-from-Prior Highlighting**: Explicitly surface any "increased/decreased/new since prior study" language as a distinct, separately flagged finding

### Metrics
- % of agent summaries that include all qualifying/follow-up language present in the source report
- Closed-loop completion rate for "recommend follow-up" findings
- Rate of ordering-question/report-content mismatch flagged vs. missed

### Alerts
- Follow-up recommendation present in report but no tracked task generated → P1
- Report body contains exclusionary caveat ("cannot exclude," "correlate clinically") dropped from summary → P2

---

## References

- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
- [MedAgentAudit: Diagnosing and Quantifying Collaborative Failure Modes in Medical Multi-Agent Systems](https://arxiv.org/pdf/2510.10185)
